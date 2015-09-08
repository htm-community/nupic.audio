TARGET = HTMforGenreClassification
TEMPLATE = app

QT += opengl

CONFIG += c++11 debug_and_release

QMAKE_CXXFLAGS += -DNTA_ARCH_64 -DHAVE_CONFIG_H -DNTA_INTERNAL -DBOOST_NO_WREGEX -DNUPIC2 -DNTA_ASSERTIONS_ON -DNTA_ASM -Wno-unused-local-typedefs

win32:QMAKE_CXXFLAGS += -DNTA_OS_WINDOWS -DNTA_COMPILER_MSVC -DPSAPI_VERSION=1 -DAPR_DECLARE_STATIC -DAPU_DECLARE_STATIC -DZLIB_WINAPI -DWIN32 -D_WINDOWS -D_MBCS -D_CRT_SECURE_NO_WARNINGS -DNDEBUG -DCAPNP_LITE=1 -D_VARIADIC_MAX=10 -DNOMINMAX
else: QMAKE_CXXFLAGS += -DNTA_OS_LINUX -DNTA_COMPILER_GNU -DHAVE_UNISTD_H -fvisibility=hidden

build_pass:CONFIG(debug, debug|release) {
  unix: TARGET = $$join(TARGET,,,_debug)
  else: TARGET = $$join(TARGET,,,d)
}

# Add in NuPIC and Marsyas common directories
INCLUDEPATH += . common nupic.core/include

# Add Open Gl utility library
# ("QT += opengl" above takes care of Open Gl library)
LIBS += -lGLU

# Add the Marsyas library
win32:LIBS += "marsyas/lib/marsyas.lib"
else: LIBS += -lmarsyas

# Add the NuPIC library
win32:LIBS += "nupic.core/lib/libnupic_core.lib"
else: LIBS += "-Lnupic.core/lib" -lnupic_core

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

