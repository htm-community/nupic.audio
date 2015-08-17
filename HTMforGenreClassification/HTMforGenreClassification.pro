TEMPLATE = app
TARGET = HTMforGenreClassification
QT += core gui opengl

INCLUDEPATH += . common

LIBS += -lGLU -lmarsyas

QMAKE_CFLAGS += -std=gnu++11
QMAKE_CXXFLAGS += -std=gnu++11

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
