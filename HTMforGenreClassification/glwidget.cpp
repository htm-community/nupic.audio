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

#include <QtOpenGL>
#include <QTimer>
#include <QTextStream>

#include <math.h>
#include <vector>
#include <algorithm>    // std::generate
#include <ctime>        // std::time
#include <cstdlib>      // std::rand, std::srand

#include <iostream>
#include <fstream>
#include <sstream>

using namespace std;

#include <marsyas/system/MarSystemManager.h>

#ifdef MARSYAS_MACOSX
#  include <OpenGL/glu.h>
#else
#  include <GL/glu.h>
#endif

#include "nupic/os/Timer.hpp"
#include <boost/circular_buffer.hpp>

#include "nupic/algorithms/SpatialPooler.hpp"
using nupic::algorithms::spatial_pooler::SpatialPooler; // aka SP

#define USE_TEMPORAL_POOLER
#if defined(USE_TEMPORAL_POOLER)
#include "nupic/algorithms/Cells4.hpp"
using nupic::algorithms::Cells4::Cells4; // aka Temporal Pooler (TP)
#endif

#include "nupic/algorithms/TemporalMemory.hpp"
using nupic::algorithms::temporal_memory::TemporalMemory; // aka TM

static SpatialPooler  gs_SP;
static Cells4         gs_TP;
static TemporalMemory gs_TM;

// Spatial Pooler, Temporal Pooler, and Temporal Memory settings
const UInt DIM_SDR = POWERSPECTRUM_BUFFER_SIZE; // SDR vector size
const UInt NUM_COLUMNS = 2048; // Number of columns
const UInt CELLS_PER_COLUMN = 32;

#define TM_RING_BUFFER_SIZE 10
static boost::circular_buffer<vector<UInt>> gs_TM_output(TM_RING_BUFFER_SIZE);

// Function generator: returns random (binary) numbers from {0,1}
static int RandomBinaryNumber () { return (rand()%2); }


GLWidget::GLWidget(const QString & inAudioFileName, QWidget *parent)
  : QGLWidget(parent)
{
  max_data.create(POWERSPECTRUM_BUFFER_SIZE);

  for (int i = 0; i < POWERSPECTRUM_BUFFER_SIZE; i++) {
    max_data(i) = -999.9;
  }

  //
  // Create the MarSystem to play and analyze the data
  //
  MarSystemManager mng;

  // A series to contain everything
  MarSystem* net = mng.create("Series", "net");

  MarSystem *accum = mng.create("Accumulator", "accum");
  net->addMarSystem(accum);

  MarSystem *accum_series = mng.create("Series", "accum_series");
  accum->addMarSystem(accum_series);

  accum_series->addMarSystem(mng.create("SoundFileSource/src"));
  accum_series->addMarSystem(mng.create("Stereo2Mono", "stereo2mono"));
  accum_series->addMarSystem(mng.create("AudioSink", "dest"));
  accum_series->addMarSystem(mng.create("Windowing", "ham"));
  accum_series->addMarSystem(mng.create("Spectrum", "spk"));
  accum_series->addMarSystem(mng.create("PowerSpectrum", "pspk"));

  net->addMarSystem(mng.create("ShiftInput", "si"));
  net->addMarSystem(mng.create("AutoCorrelation", "auto"));

  net->updControl("Accumulator/accum/mrs_natural/nTimes", 10);

  net->updControl("ShiftInput/si/mrs_natural/winSize", MEMORY_SIZE);

  net->updControl("mrs_real/israte", 22050.0);

  // Create a Qt wrapper that provides thread-safe control of the MarSystem:
  m_marsystem = net;
  m_system = new MarsyasQt::System(net);

  // Get controls:
  m_fileNameControl = m_system->control("Accumulator/accum/Series/accum_series/SoundFileSource/src/mrs_string/filename");
  m_initAudioControl = m_system->control("Accumulator/accum/Series/accum_series/AudioSink/dest/mrs_bool/initAudio");
  m_spectrumSource = m_system->control("mrs_realvec/processedData");

  // Initialize SP, TP, and TM
  vector<UInt> inputDimensions = {DIM_SDR};
  vector<UInt> columnDimension = {NUM_COLUMNS};

  gs_SP.initialize(inputDimensions, columnDimension, DIM_SDR, 0.5, true, -1.0, int(0.02*NUM_COLUMNS));
  gs_SP.setSynPermActiveInc(0.01);

  gs_TM.initialize(columnDimension, CELLS_PER_COLUMN);

#if defined(USE_TEMPORAL_POOLER)
  gs_TP.initialize(NUM_COLUMNS, CELLS_PER_COLUMN,
                   12, 8, 15, 5,
                   .5, .8, 1.0, .1, .1, 0.0,
                   false, true, false);
#endif

  // Connect the animation timer that periodically redraws the screen.
  // It is activated in the 'play()' function.
  connect( &m_updateTimer, SIGNAL(timeout()), this, SLOT(animate()) );

  play(inAudioFileName);
}

GLWidget::~GLWidget()
{
  makeCurrent();
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

  static const bool NO_UPDATE = false;
  m_fileNameControl->setValue(fileName, NO_UPDATE);
  m_initAudioControl->setValue(true, NO_UPDATE);
  m_system->update();

  // In ms
  m_updateDelta = 1000.0 / TIMER_COUNT_STEPS;

  m_system->start();
  m_updateTimer.start((int)m_updateDelta);

  m_audioFileName = fileName;
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
  gluPerspective(20,1,0.1,1000);

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
  glTranslated(-0.5, -0.5, -3);

  // Generate a random SDR
  m_inputSDR.reserve(DIM_SDR);
  generate(m_inputSDR.begin(), m_inputSDR.end(), RandomBinaryNumber);

  // Step NuPIC network
  stepNuPIC(m_inputSDR);

  // Draw the object
  redrawScene();

}

int GLWidget::stepNuPIC(vector<UInt>& inputSDR, bool learn)
{
  // clear the active columns indicies array
  m_activeColumnIndicies.assign(NUM_COLUMNS, 0);

  gs_SP.compute(inputSDR.data(), learn, m_activeColumnIndicies.data());
  gs_SP.stripUnlearnedColumns(m_activeColumnIndicies.data());

  gs_TM.compute(m_activeColumnIndicies.size(), m_activeColumnIndicies.data(), learn);

#if defined(USE_TEMPORAL_POOLER)
  const int _CELLS = NUM_COLUMNS * CELLS_PER_COLUMN;
  Real rIn[NUM_COLUMNS] = {}; // input for TP (must be Reals)
  Real rOut[_CELLS] = {};

  for (UInt i = 0; i < NUM_COLUMNS; i++) {
    rIn[i] = (Real)(m_activeColumnIndicies[i]);
  }

  gs_TP.compute(rIn, rOut, true, learn);
#endif

  return 0;
}

void GLWidget::redrawScene()
{
  mrs_realvec correlogram_data( m_spectrumSource->value().value<mrs_realvec>() );

  for (int x = 0; x < MEMORY_SIZE; x++) {
    for (int y = 0; y < POWERSPECTRUM_BUFFER_SIZE; y++) {
      if (correlogram_data(y,x) > max_data(y)) {
        max_data(y) = correlogram_data(y,x);
        // cout << "max_data(" << y << ")=" << max_data(y) << endl;
      }
    }
  }

  float x1,x2,y1,y2;

  float dx = 1.0/MEMORY_SIZE;
  float dy = 1.0/POWERSPECTRUM_BUFFER_SIZE;

  // Draw a rectangle for each element in the array
  for (int x = 0; x < MEMORY_SIZE; x++) {
    for (int y = 0; y < POWERSPECTRUM_BUFFER_SIZE; y++) {
      float color = (correlogram_data(y,x) * (1.0 / max_data(y)));

      glColor3f(color,color,color);
      // cout << "color=" << color << endl;

      x1 = (float)x*dx;
      x2 = x1+0.005;

      y1 = float(y)*dy;
      y2 = y1+0.005;

      glBegin(GL_QUADS);
      glVertex2f(x1, y1);
      glVertex2f(x2, y1);
      glVertex2f(x2, y2);
      glVertex2f(x1, y2);
      glEnd();

    }
  }
}

void GLWidget::animate()
{
  updateGL();
}
