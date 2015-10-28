#ifndef GLWIDGET_H
#define GLWIDGET_H

#include <QGLFunctions>
#include <QGLWidget>
#include <QTimer>
#include <QMainWindow>
#include <QMenu>
#include <QMenuBar>
#include <QSlider>
#include <QLineEdit>
#include <QTimeEdit>
#include <QAction>
#include <QTimer>
#include <QTextStream>
#include <QLabel>
#include <QGridLayout>
#include <QFileDialog>
#include <QMessageBox>

#include <math.h>
#include <vector>
#include <algorithm>    // std::generate
#include <ctime>        // std::time
#include <cstdlib>      // std::rand, std::srand

#include <iostream>
#include <fstream>
#include <sstream>

using namespace std;

// NuPIC

#include "nupic/types/Types.hpp"

using namespace nupic;

// Marsyas

#include "./common/marsystem_wrapper.h"

using namespace Marsyas;
using namespace MarsyasQt;

class GLWidget : public QGLWidget, protected QGLFunctions
{
  Q_OBJECT

public:
  GLWidget(const QString & inAudioFileName, QWidget *parent = 0);
  ~GLWidget();

  QSize minimumSizeHint() const;
  QSize sizeHint() const;

public slots:
  void open(); // Open an audio file selected from dialog
  void play( const QString & fileName ); // Open a given audio file
  void playPause(); // Play or pause the playback of the song
  void animate();

protected:
  void initializeGL();                    // Initialize the GL window
  void paintGL();                         // Paint the objects in the GL window
  void resizeGL(int width, int height);   // Resize the GL window

private:
  void createVertexBufferObjects();
  void redrawScene();

  vector<UInt>  encodeDataIntoSDR();
  int           stepNuPIC(vector<nupic::UInt>& inputSDR, bool learn = true);
  void          queryNuPIC();

  vector<nupic::UInt> m_inputSDR;
  vector<nupic::UInt> m_activeColumnIndicies;

  QString m_audioFileName;

  // A timer to make the animation happen
  QTimer m_updateTimer;
  qreal m_updateDelta; //ms

  // Marsyas
  MarSystem* m_marSystem;

  MarsyasQt::System *m_system;

  MarsyasQt::Control *m_fileNameControl;
  MarsyasQt::Control *m_initAudioControl;

  MarsyasQt::Control *m_spectrumSource;

  MarsyasQt::Control *m_SAIbinauralSAI;
  MarsyasQt::Control *m_SAIthreshold;
  MarsyasQt::Control *m_SAIstrobes;

  // Maximum data for drawing when scaling
  Marsyas::mrs_realvec max_data;

/*
  typedef struct _vertexStruct
  {
    typedef struct _vertexStatic{
        GLfloat position[2];
    } vertexStatic;

    typedef struct _vertexDynamic {
        GLubyte color[4];
    } vertexDynamic;

    GLfloat position[2];
    GLubyte color[4];

  } vertexStruct;

  GLuint GLKVertexAttribPosition;
  GLuint GLKVertexAttribColor;

  // Separate buffers for static and dynamic data.
  GLuint staticBuffer;
  GLuint dynamicBuffer;
  GLuint indexBuffer;

  std::vector<vertexStruct::vertexStatic> staticVertexData;
  std::vector<vertexStruct::vertexDynamic> dynamicVertexData;
  std::vector<GLushort> indicies;
*/
};

#endif
