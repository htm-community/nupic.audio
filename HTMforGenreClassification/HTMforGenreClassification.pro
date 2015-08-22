TARGET = HTMforGenreClassification
TEMPLATE = app

QT += opengl

CONFIG += c++11 debug_and_release

build_pass:CONFIG(debug, debug|release) {
  unix: TARGET = $$join(TARGET,,,_debug)
  else: TARGET = $$join(TARGET,,,d)
}

# Add in NuPIC and Marsyas common directories
INCLUDEPATH += . common nupic.core/include

# Add Open Gl utility library
# ("QT += opengl" above takes care of Open Gl)
LIBS += -lGLU

# Add the Marsyas library
win32:LIBS += "marsyas/lib/marsyas.lib"
else:LIBS += -lmarsyas

# Add the NuPIC library
win32:LIBS += "nupic.core/lib/libnupic_core.lib"
else:LIBS += "-Lnupic.core/lib" -lnupic_core

# Headers for the main app and Marsyas wrapper
HEADERS += glwidget.h \
           window.h \
           common/control_model.h \
           common/marsyasqt_common.h \
           common/marsystem_wrapper.h \
           common/realvec_item_model.h \
           common/realvec_table_widget.h

# Source code for the main app and Marsyas wrapper
SOURCES += glwidget.cpp \
           main.cpp \
           window.cpp \
           common/control_model.cpp \
           common/marsystem_wrapper.cpp \
           common/realvec_item_model.cpp \
           common/realvec_table_widget.cpp

