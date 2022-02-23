
#include <pybind11/pybind11.h>
#ifdef _WIN32
#  define NOMINMAX   // to remove min,max macro
#  include <windows.h>  // should be put before opengl headers
#endif

#include "glad/glad.h"
#include "delfem2/opengl/funcs.h"

namespace py = pybind11;

bool MyGladLoadGLLoader(){
  if (!gladLoadGL() ) {
    return false;
  }
  return true;
}

void init_glad_glfw(py::module &m) {
  m.def("glad_load_gl",
        &MyGladLoadGLLoader, "");

  m.def("setup_glsl",
        &delfem2::opengl::setUpGLSL, "");
}