#include <vector>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

#include "delfem2/opengl/old/r2tglo.h"

namespace py = pybind11;
namespace dfm2 = delfem2;

void init_opengl_old_drawer_r2t(py::module &m) {
  py::class_<dfm2::opengl::CDrawerOldGL_Render2Tex>(
      m,
      "_DrawerRender2Tex",
      "sample color and depth in the frame buffer")
      .def(py::init<>())
      .def(
          "draw",
          &dfm2::opengl::CDrawerOldGL_Render2Tex::Draw)
      .def_readwrite(
          "color_point",
          &dfm2::opengl::CDrawerOldGL_Render2Tex::colorPoint);
}