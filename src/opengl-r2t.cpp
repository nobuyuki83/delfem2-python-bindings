#include <vector>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

#include "delfem2/opengl/r2t.h"

namespace py = pybind11;
namespace dfm2 = delfem2;

// -----------------

py::array_t<float> render2tex_depth_buffer(
    dfm2::opengl::CRender2Tex& sampler)
{
  assert(sampler.aZ.size()==sampler.height*sampler.width);
  std::vector<size_t> strides = {sizeof(float)*sampler.width, sizeof(float)};
  std::vector<size_t> shape = {(size_t)sampler.height, (size_t)sampler.width};
  unsigned int ndim = 2;
  return py::array(py::buffer_info(
      sampler.aZ.data(), sizeof(float),
      py::format_descriptor<float>::format(),
      ndim, shape, strides));
}

py::array_t<unsigned char> render2tex_color_buffer_4byte(
    dfm2::opengl::CRender2Tex& sampler)
{
  assert(sampler.aRGBA_8ui.size()==sampler.height*sampler.width*4);
  std::vector<size_t> strides = {
      sizeof(unsigned char)*sampler.width*4,
      sizeof(unsigned char)*4,sizeof(unsigned char)};
  std::vector<size_t> shape = {
      static_cast<size_t>(sampler.height),
      static_cast<size_t>(sampler.width), 4};
  unsigned int ndim = 3;
  return py::array(py::buffer_info(
      sampler.aRGBA_8ui.data(), sizeof(unsigned char),
      py::format_descriptor<unsigned char>::format(),
      ndim, shape, strides));
}

/*
py::array_t<float> color_buffer_4float(dfm2::opengl::CRender2Tex_DrawOldGL& sampler)
{
  std::vector<float> aRGBA;
  sampler.ExtractFromTexture_RGBA32F(aRGBA);
  assert(aRGBA.size()==sampler.nResY*sampler.nResX*4);
  std::vector<size_t> strides = {sizeof(float)*sampler.nResX*4,sizeof(float)*4,sizeof(float)};
  std::vector<size_t> shape = {(size_t)sampler.nResY,(size_t)sampler.nResX,4};
  size_t ndim = 3;
  return py::array(py::buffer_info(aRGBA.data(), sizeof(float),
                                   py::format_descriptor<float>::format(),
                                   ndim, shape, strides));
}

py::array_t<unsigned char> color_buffer_4byte(dfm2::opengl::CRender2Tex_DrawOldGL& sampler)
{
  std::vector<unsigned char> aRGBA;
  sampler.ExtractFromTexture_RGBA8UI(aRGBA);
  assert(aRGBA.size()==sampler.nResY*sampler.nResX*4);
  std::vector<size_t> strides = {sizeof(unsigned char)*sampler.nResX*4,sizeof(unsigned char)*4,sizeof(unsigned char)};
  std::vector<size_t> shape = {(size_t)sampler.nResY,(size_t)sampler.nResX,4};
  size_t ndim = 3;
  return py::array(py::buffer_info(aRGBA.data(), sizeof(unsigned char),
                                   py::format_descriptor<unsigned char>::format(),
                                   ndim, shape, strides));
}
*/

void init_opengl_r2t(py::module &m)
{
  // ---------------------------------------
  // Depth&Color Sampler
  py::class_<dfm2::opengl::CRender2Tex>(
      m,
      "_Render2Tex",
      "sample color and depth in the frame buffer")
  .def(py::init<>())
  .def("init_gl",
       &dfm2::opengl::CRender2Tex::InitGL)
  .def("set_texture_property",
       &dfm2::opengl::CRender2Tex::SetTextureProperty,
       py::arg("size_res_width"),
       py::arg("size_res_height"),
       py::arg("is_rgba_8ui") )
  .def("start",
       &dfm2::opengl::CRender2Tex::Start)
  .def("end",
       &dfm2::opengl::CRender2Tex::End)
  .def("set_zero_to_depth",
       &dfm2::opengl::CRender2Tex::SetZeroToDepth)
  .def("get_affinematrix_modelview_colmajor",
       &dfm2::opengl::CRender2Tex::GetAffineMatrixModelViewAsColMajorStlVector<double>)
  .def("get_affinematrix_projection_colmajor",
      &dfm2::opengl::CRender2Tex::GetAffineMatrixProjectionAsColMajorStlVector<double>)
  .def("set_affinematrix_modelview_colmajor",
       &dfm2::opengl::CRender2Tex::SetAffineMatrixModelViewAsColMajorStlVector<double>)
  .def("set_affinematrix_projection_colmajor",
       &dfm2::opengl::CRender2Tex::SetAffineMatrixProjectionAsColMajorStlVector<double>);

  m.def("_render2tex_depth_buffer",
        &render2tex_depth_buffer, "");
  m.def("_render2tex_color_buffer_4byte",
        &render2tex_color_buffer_4byte, "");

//  m.def("color_buffer_4float", &color_buffer_4float);
}
