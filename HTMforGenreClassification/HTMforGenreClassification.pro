TARGET = HTMforGenreClassification
TEMPLATE = app

message(Using Qt $$[QT_VERSION] installed in $$[QT_INSTALL_PREFIX])

QT += opengl

CONFIG += c++11 debug_and_release

build_pass:CONFIG(debug, debug|release) {
  unix: TARGET = $$join(TARGET,,,_debug)
  else: TARGET = $$join(TARGET,,,d)
}
CONFIG(release, debug|release):
  message($$TARGET (release) will be built into $$DESTDIR)
CONFIG(debug, debug|release):
  message($$TARGET (debug) will be built into $$DESTDIR)

INCLUDEPATH += . common

LIBS += -lGLU -lmarsyas
#win32:LIBS += "C:/mylibs/extra libs/extra.lib"
#unix:LIBS += "-L/home/user/extra libs" -lextra

HEADERS += glwidget.h \
           window.h \
           common/control_model.h \
           common/marsyasqt_common.h \
           common/marsystem_wrapper.h \
           common/realvec_item_model.h \
           common/realvec_table_widget.h

SOURCES += glwidget.cpp \
           main.cpp \
           window.cpp \
           common/control_model.cpp \
           common/marsystem_wrapper.cpp \
           common/realvec_item_model.cpp \
           common/realvec_table_widget.cpp

