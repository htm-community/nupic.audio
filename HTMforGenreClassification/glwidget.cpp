/* ---------------------------------------------------------------------
 * Numenta Platform for Intelligent Computing (NuPIC)
 * Copyright (C) 2013-2015, Numenta, Inc.  Unless you have an agreement
 * with Numenta, Inc., for a separate license for this software code, the
 * following terms and conditions apply:
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 3 as
 * published by the Free Software Foundation.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 * See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see http://www.gnu.org/licenses.
 *
 * http://numenta.org/licenses/
 * ---------------------------------------------------------------------
 */

#include "glwidget.h"

using namespace std;

#include <marsyas/system/MarSystemManager.h>

static const bool NO_UPDATE = false;

#ifdef MARSYAS_MACOSX
#include <OpenGL/glu.h>
#else
#include <GL/glu.h>
#endif

#include "nupic/algorithms/SpatialPooler.hpp"
using nupic::algorithms::spatial_pooler::SpatialPooler; // aka SP
static SpatialPooler  gs_SP;

#include "nupic/algorithms/TemporalMemory.hpp"
using nupic::algorithms::temporal_memory::TemporalMemory; // aka TM
static TemporalMemory gs_TM;


#define NUM_TEXTURE_WINDOWS   10
#define TEXTURE_WINDOW_SIZE   20.0  //ms

#define SAMPLE_RATE           22050.0 // Samples per second
#define SAMPLES_PER_MS        (SAMPLE_RATE / 1000)

#define TIMER_DELTA           (1000.0 / TEXTURE_WINDOW_SIZE)

#define MEMORY_SIZE           (SAMPLES_PER_MS * TEXTURE_WINDOW_SIZE)
#define SPECTRUM_BUFFER_SIZE  (MEMORY_SIZE + 6)

// Spatial Pooler (SP) and Temporal Memory (TM) settings
const UInt DIM_SDR = SPECTRUM_BUFFER_SIZE;  // SDR vector size
const UInt NUM_COLUMNS = 2048;              // Number of columns
const UInt CELLS_PER_COLUMN = 32;

#include <boost/circular_buffer.hpp>
#define TM_RING_BUFFER_SIZE 10
static boost::circular_buffer<vector<UInt>> gs_TM_output(TM_RING_BUFFER_SIZE);

// Function generator: returns random (binary) numbers from {0,1}
static int RandomBinaryNumber () { return (rand()%2); }


GLWidget::GLWidget(const QString & inAudioFileName, QWidget *parent)
  : QGLWidget(parent)//, staticBuffer(0), dynamicBuffer(0), indexBuffer(0)
{
  cout << "Num texture windows: " << NUM_TEXTURE_WINDOWS << endl;
  cout << "Texture window size: " << TEXTURE_WINDOW_SIZE << " ms" << endl;
  cout << "Samples per ms:      " << SAMPLES_PER_MS << endl;
  cout << "Timer delta:         " << TIMER_DELTA << " ms" << endl;
  cout << "Memory size:         " << MEMORY_SIZE << endl;

  max_data.create(SPECTRUM_BUFFER_SIZE);

  for (int i = 0; i < SPECTRUM_BUFFER_SIZE; i++) {
    max_data(i) = -999999.9;
  }

  //
  // Create the MarSystem to play and analyze the data
  //
  MarSystemManager mng;

  // A series to contain everything
  MarSystem* net = mng.create("Series", "net");
  m_marSystem = net;

  // Note that you can only add one Marsystem to an Accumulator
  // any additional Systems added are simply ignored outputwise !!
  // e.g. if you want to use multiple Marsystems in a row and accumulate
  // their combined output, you need to put them in a series which you add
  // to the accumulator
  MarSystem *accum = mng.create("Accumulator", "accum");
  net->addMarSystem(accum);

  MarSystem *accum_series = mng.create("Series", "accum_series");
  accum->addMarSystem(accum_series);

  accum_series->addMarSystem(mng.create("SoundFileSource/src"));
  accum_series->addMarSystem(mng.create("Stereo2Mono", "stereo2mono"));
  accum_series->addMarSystem(mng.create("AudioSink", "dest"));

  MarSystem* fanout = mng.create("Fanout", "fanout");
  accum_series->addMarSystem(fanout);

  // Power spectrum
  MarSystem* spectrumMemory = mng.create("Series", "spectrumMemory");
  fanout->addMarSystem(spectrumMemory);
  {
    MarSystem* net = spectrumMemory;

    net->addMarSystem(mng.create("Windowing", "ham"));
    net->addMarSystem(mng.create("Spectrum", "spk"));
    net->addMarSystem(mng.create("PowerSpectrum", "pspk"));
  }

  // Cochlear based/inspired
  MarSystem* cochlearFeatures = mng.create("Series", "cochlearFeatures");
  //fanout->addMarSystem(cochlearFeatures);
  {
    MarSystem* net = cochlearFeatures;

    // Stabilised auditory image, from CARFAC
    net->addMarSystem(mng.create("CARFAC", "carfac"));
  }

  MarSystem* spatialFeatures = mng.create("Series", "spatialFeatures");
  fanout->addMarSystem(spatialFeatures);
  {
    MarSystem* net = spatialFeatures;

    // Into time-domain
    net->addMarSystem(mng.create("Windowing", "ham"));
    net->addMarSystem(mng.create("Spectrum", "spk"));
    net->addMarSystem(mng.create("PowerSpectrum", "pspk"));
    net->addMarSystem(mng.create("ShiftInput", "si")); // DC offset?

    // Energy measures
    net->addMarSystem(mng.create("Centroid", "centroid"));
    net->addMarSystem(mng.create("Rolloff", "rolloff"));
    net->addMarSystem(mng.create("Flux", "flux"));
    net->addMarSystem(mng.create("ZeroCrossings", "zc"));

    // Mel-Frequency Cepstral Coefficients
    net->addMarSystem(mng.create("MFCC", "mfcc"));

    // Five MFCC coefficients required
    net->updControl("MFCC/mfcc/mrs_natural/coefficients", 5);

    // A resulting feature vector for describing timbral texture consists of the
    // following features: means and variances of spectral centroid, rolloff, flux,
    // zero crossings over the texture window (8), low energy (1), and means and
    // variances of the first five MFCC coefficients over the texture window
    // (excluding the coefficient corresponding to the DC component) resulting
    // in a 19-dimensional feature vector, __as a starting point__.
  }

  net->addMarSystem(mng.create("AutoCorrelation", "auto"));

  // Setup texture windows, and window memory size
  net->updControl(
        "Accumulator/accum/mrs_natural/nTimes", NUM_TEXTURE_WINDOWS);
  net->updControl(
        "Accumulator/accum/Series/accum_series/Fanout/fanout/" \
        "Series/spatialFeatures/ShiftInput/si/mrs_natural/winSize", int(MEMORY_SIZE));

  net->updControl("mrs_real/israte", SAMPLE_RATE);

  //m_marSystem->put_html(cout);
  //cout << *m_marSystem;

  ofstream oss;
  oss.open("audioAnalysis.mpl");
  oss << *m_marSystem;

  // Create a Qt wrapper that provides thread-safe control of the MarSystem:
  m_system = new MarsyasQt::System(m_marSystem);

  // Get controls
  m_fileNameControl = m_system->control(
        "Accumulator/accum/Series/accum_series/" \
        "SoundFileSource/src/mrs_string/filename");
  m_initAudioControl = m_system->control(
        "Accumulator/accum/Series/accum_series/" \
        "AudioSink/dest/mrs_bool/initAudio");

  m_spectrumSource = m_system->control("mrs_realvec/processedData");

  m_SAIbinauralSAI = m_system->control(
        "Accumulator/accum/Series/accum_series/Fanout/fanout/" \
        "Series/cochlearFeatures/CARFAC/carfac/mrs_realvec/sai_output_binaural_sai");
  m_SAIthreshold = m_system->control(
        "Accumulator/accum/Series/accum_series/Fanout/fanout/" \
        "Series/cochlearFeatures/CARFAC/carfac/mrs_realvec/sai_output_threshold");
  m_SAIstrobes = m_system->control(
        "Accumulator/accum/Series/accum_series/Fanout/fanout/" \
        "Series/cochlearFeatures/CARFAC/carfac/mrs_realvec/sai_output_strobes");

  // Initialize SP and TM
  vector<UInt> inputDimensions = {DIM_SDR};
  vector<UInt> columnDimension = {NUM_COLUMNS};

  m_inputSDR.reserve(DIM_SDR);

  gs_SP.initialize(inputDimensions, columnDimension, DIM_SDR, 0.5, true, -1.0, int(0.02*NUM_COLUMNS));
  gs_SP.setSynPermActiveInc(0.01);

  gs_TM.initialize(columnDimension, CELLS_PER_COLUMN);

  // Connect the animation timer that periodically redraws the screen.
  // It is activated in the 'play()' function.
  connect( &m_updateTimer, SIGNAL(timeout()), this, SLOT(animate()) );

  // Queue given audio file
  //play(inAudioFileName);
  m_audioFileName = inAudioFileName;

  m_fileNameControl->setValue(m_audioFileName, NO_UPDATE);
  m_system->update();
}

GLWidget::~GLWidget()
{
  makeCurrent();

//  if (staticBuffer) glDeleteBuffers(1, &staticBuffer);
//  if (dynamicBuffer) glDeleteBuffers(1, &dynamicBuffer);
//  if (indexBuffer) glDeleteBuffers(1, &indexBuffer);
}

void GLWidget::open()
{
  QString fileName = QFileDialog::getOpenFileName(this);
  play(fileName);
}

void GLWidget::play( const QString & fileName )
{
  if (fileName.isEmpty())
    return;

  m_audioFileName = fileName;

  m_fileNameControl->setValue(fileName, NO_UPDATE);
  m_initAudioControl->setValue(true, NO_UPDATE);
  m_system->update();
  m_system->start();

  m_updateDelta = TIMER_DELTA; //milliseconds
  m_updateTimer.start((int)m_updateDelta);
}

void GLWidget::playPause()
{
  if (m_system->isRunning())
  {
    m_system->stop();
    m_updateTimer.stop();
  }
  else if (!m_audioFileName.isEmpty())
  {
    m_system->start();
    m_updateTimer.start((int)m_updateDelta);
  }
}

// The minimum size of the widget
QSize GLWidget::minimumSizeHint() const
{
  return QSize(400, 400);
}

// The maximum size of the widget
QSize GLWidget::sizeHint() const
{
  return QSize(600, 600);
}

// Initialize the GL widget
void GLWidget::initializeGL()
{
  initializeGLFunctions();

  createVertexBufferObjects();

  // Set the background color to white
  qglClearColor(Qt::black);

  // Set the shading model
  glShadeModel(GL_SMOOTH);

  // Enable depth testing
  glDisable(GL_DEPTH_TEST);
}

// Resize the window
void GLWidget::resizeGL(int width, int height)
{
  // The smallest side of the window
  int side = qMin(width, height);

  // Setup the glViewport
  glViewport((width - side) / 2, (height - side) / 2, side, side);

  // Switch to GL_PROJECTION matrix mode
  glMatrixMode(GL_PROJECTION);

  // Load the identity matrix
  glLoadIdentity();

  // Setup a perspective viewing system
  gluPerspective(45,1,0.1,1000);

  // Switch back to GL_MODELVIEW mode
  glMatrixMode(GL_MODELVIEW);
}

// Paint the GL widget
void GLWidget::paintGL()
{
  // Clear the color and depth buffer
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

  // Load the identity matrix
  glLoadIdentity();

  // // Translate the model
  glTranslated(-0.5, -0.5, -1.5);

  // Generate a random SDR
  generate(m_inputSDR.begin(), m_inputSDR.end(), RandomBinaryNumber);

  // Step NuPIC network
  stepNuPIC(m_inputSDR);

  // Determine what answers the presented SDR evokes
  queryNuPIC();

  // Draw the object
  redrawScene();

}

void GLWidget::animate()
{
  updateGL();
}

vector<UInt> GLWidget::encodeDataIntoSDR()
{
  vector<UInt> outputSDR;
  outputSDR.assign(DIM_SDR, 0);

  // Interrogate accumulator fanout series history

  return outputSDR;
}

int GLWidget::stepNuPIC(vector<UInt>& inputSDR, bool learn)
{
  // clear the active columns indicies array
  m_activeColumnIndicies.assign(NUM_COLUMNS, 0);

  gs_SP.compute(inputSDR.data(), learn, m_activeColumnIndicies.data());
  gs_SP.stripUnlearnedColumns(m_activeColumnIndicies.data());

  gs_TM.compute(m_activeColumnIndicies.size(), m_activeColumnIndicies.data(), learn);

  return 0;
}

void GLWidget::queryNuPIC()
{
  // Send activeColumns into classifier(s)

}

void GLWidget::createVertexBufferObjects()
{
/*
  // Create a grid of quads
  int iRows = MEMORY_SIZE;
  int iCols = POWERSPECTRUM_BUFFER_SIZE;

  staticVertexData.reserve(4*iRows*iCols);
  dynamicVertexData.reserve(4*iRows*iCols);
  indicies.reserve(4*iRows*iCols);

  // Create Vertices
  float dx = 1.0 / MEMORY_SIZE;
  float dy = 1.0 / POWERSPECTRUM_BUFFER_SIZE;

  vertexStruct::_vertexStatic vertex;
  vertexStruct::_vertexDynamic color;

  color.color[0] = 0;
  color.color[1] = 0;
  color.color[2] = 0;
  color.color[3] = 0;

  for (int y = 0, offset = 0; y < iRows; y++)
  {
    for(int x = 0; x < iCols; x++, offset += 4)
    {
      float x1, x2, y1, y2;

      x1 = (float)x * dx;
      x2 = x1 + 1.5;

      y1 = (float)y * dy;
      y2 = y1 + 1.5;

      vertex.position[0] = x1; vertex.position[1] = y1;
      staticVertexData.push_back(vertex);
      dynamicVertexData.push_back(color);

      vertex.position[0] = x2; vertex.position[1] = y1;
      staticVertexData.push_back(vertex);
      dynamicVertexData.push_back(color);

      vertex.position[0] = x2; vertex.position[1] = y2;
      staticVertexData.push_back(vertex);
      dynamicVertexData.push_back(color);

      vertex.position[0] = x1; vertex.position[1] = y2;
      staticVertexData.push_back(vertex);
      dynamicVertexData.push_back(color);

      indicies.push_back(offset+0);
      indicies.push_back(offset+1);
      indicies.push_back(offset+3);
      indicies.push_back(offset+2);
    }
  }

  // Allocate and assign a Vertex Buffer Objects
  glGenBuffers(1, &staticBuffer);

  // Bind our first VBO as being the active buffer and storing vertex attributes (coordinates)
  glBindBuffer(GL_ARRAY_BUFFER, staticBuffer);

  // Copy the vertex data from static vertex data to our buffer
  glBufferData(GL_ARRAY_BUFFER,
        staticVertexData.size() * sizeof(vertexStruct::vertexStatic),
        staticVertexData.data(), GL_STATIC_DRAW);

  // Allocate and assign a Vertex Buffer Objects
  glGenBuffers(1, &dynamicBuffer);

  // Bind our second VBO as being the active buffer and storing vertex attributes (colors)
  glBindBuffer(GL_ARRAY_BUFFER, dynamicBuffer);

  // Copy the color data from colors to our buffer
  glBufferData(GL_ARRAY_BUFFER,
        dynamicVertexData.size() * sizeof(vertexStruct::vertexDynamic),
        dynamicVertexData.data(), GL_DYNAMIC_DRAW);

  // Allocate and assign a Vertex Buffer Objects
  glGenBuffers(1, &indexBuffer);

  // Bind our third VBO as being the active buffer and storing vertex indicies
  glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indexBuffer);

  // Copy the index data from indicies to our buffer
  glBufferData(GL_ELEMENT_ARRAY_BUFFER,
        indicies.size()*sizeof(GLushort),
        indicies.data(), GL_STATIC_DRAW);
*/
}

void GLWidget::redrawScene()
{
  if (!m_system->isRunning())
    return;

  mrs_realvec data( m_spectrumSource->value().value<mrs_realvec>() );

  // Create a grid of quads
  int iRows = data.getCols();
  int iCols = data.getRows();

  for (int x = 0; x < iRows; x++) {
    for (int y = 0; y < iCols; y++) {
      if (data(y,x) > max_data(y)) {
        max_data(y) = data(y,x);
      }
    }
  }

  float x1, x2, y1, y2;
  float dx = 1.0f / iRows;
  float dy = 1.0f / iCols;

  // Draw a rectangle for each element in the array
  for (int x = 0; x < iRows; x++) {
    for (int y = 0; y < iCols; y++) {
      float color = data(y,x) / max_data(y);

      glColor3f(color, 0.0f, 1.0-color);
      //cout << "color=" << color << endl;

      x1 = float(x) * dx;
      x2 = x1 + dx;//0.05;

      y1 = float(y) * dy;
      y2 = y1 + dy;//0.05;

      glBegin(GL_QUADS);
      glVertex2f(x1, y1);
      glVertex2f(x2, y1);
      glVertex2f(x2, y2);
      glVertex2f(x1, y2);
      glEnd();

    }
  }

/*
  // Update each rectangle's color for each element in the array
  for (int x = 0, offset = 0; x < MEMORY_SIZE; x++)
  {
    for (int y = 0; y < POWERSPECTRUM_BUFFER_SIZE; y++)
    {
      float color = (correlogram_data(y,x) * (1.0 / max_data(y)));

      dynamicVertexData[offset].color[0] = 255*color;
      dynamicVertexData[offset].color[1] = 255*color;
      dynamicVertexData[offset].color[2] = 255*color;
      offset++;
      dynamicVertexData[offset].color[0] = 255*color;
      dynamicVertexData[offset].color[1] = 255*color;
      dynamicVertexData[offset].color[2] = 255*color;
      offset++;
      dynamicVertexData[offset].color[0] = 255*color;
      dynamicVertexData[offset].color[1] = 255*color;
      dynamicVertexData[offset].color[2] = 255*color;
      offset++;
      dynamicVertexData[offset].color[0] = 255*color;
      dynamicVertexData[offset].color[1] = 255*color;
      dynamicVertexData[offset].color[2] = 255*color;
      offset++;
    }
  }

  glBindBuffer(GL_ARRAY_BUFFER, staticBuffer);
  glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, sizeof(vertexStruct::vertexStatic), 0);
  glEnableVertexAttribArray(0);

  glBindBuffer(GL_ARRAY_BUFFER, dynamicBuffer);
  glVertexAttribPointer(1, 4, GL_UNSIGNED_BYTE, GL_FALSE, sizeof(vertexStruct::vertexDynamic), 0);
  glEnableVertexAttribArray(1);

  glBufferData(GL_ARRAY_BUFFER,
        dynamicVertexData.size() * sizeof(vertexStruct::vertexDynamic),
        NULL, GL_DYNAMIC_DRAW);

  glBufferSubData(GL_ARRAY_BUFFER, 0,
        dynamicVertexData.size() * sizeof(vertexStruct::vertexDynamic),
        dynamicVertexData.data());

  glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indexBuffer);
  glDrawElements(GL_TRIANGLE_STRIP, indicies.size(), GL_UNSIGNED_SHORT, 0);//(void*)sizeof(GLushort));

  glDisableVertexAttribArray(1);
  glDisableVertexAttribArray(0);

  glBindBuffer(GL_ARRAY_BUFFER, 0);
  glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0);
*/
}
