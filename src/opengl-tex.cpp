//
// Created by Nobuyuki Umetani on 2021-08-17.
//


#include <vector>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

#include "delfem2/opengl/tex.h"

namespace py = pybind11;
namespace dfm2 = delfem2;

dfm2::opengl::CTexRGB_Rect2D
GetTextureFromNumpy(
    const py::array_t<unsigned char>& a,
    const std::string& str_channels)
{
  assert(a.ndim()==3 && a.shape()[2] == 3);
  const size_t h = a.shape()[0];
  const size_t w = a.shape()[1];
  dfm2::opengl::CTexRGB_Rect2D tex;
  tex.Initialize(w,h,a.data(),str_channels);
  return tex;
}

void init_opengl_texture(py::module &m) {
  py::class_<dfm2::opengl::CTexRGB_Rect2D>(m, "Texture")
      .def(py::init<>())
      .def("draw",
           &dfm2::opengl::CTexRGB_Rect2D::Draw_oldGL)
      .def("init_gl",
           &dfm2::opengl::CTexRGB_Rect2D::InitGL)
      .def("minmax_xyz",
           &dfm2::opengl::CTexRGB_Rect2D::MinMaxAABB)
      .def("set_minmax_xy",
           &dfm2::opengl::CTexRGB_Rect2D::SetMinMaxXY)
      .def_readonly("width",
                    &dfm2::opengl::CTexRGB_Rect2D::width)
      .def_readonly("height",
                    &dfm2::opengl::CTexRGB_Rect2D::height);

  m.def("get_texture",
        &GetTextureFromNumpy);
}
