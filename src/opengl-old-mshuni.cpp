//
// Created by Nobuyuki Umetani on 2021-08-15.
//

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

#include "delfem2/opengl/old/mshuni.h"
#include "delfem2/mshelm.h"

namespace py = pybind11;
namespace dfm2 = delfem2;

void PyDrawMesh_FaceNorm(
    const py::array_t<double>& pos,
    const py::array_t<unsigned int>& elm,
    const dfm2::MESHELEM_TYPE type)
{
  assert(pos.ndim()==2);
  assert(elm.ndim()==2);
  const auto shape_pos = pos.shape();
  const auto shape_elm = elm.shape();
  if( shape_pos[1] == 3 ){ // 3D Mesh
    if( type == dfm2::MESHELEM_TRI  ){  dfm2::opengl::DrawMeshTri3D_FaceNorm( pos.data(), elm.data(), shape_elm[0]); }
    if( type == dfm2::MESHELEM_QUAD ){  dfm2::opengl::DrawMeshQuad3D_FaceNorm(pos.data(), elm.data(), shape_elm[0]); }
    if( type == dfm2::MESHELEM_HEX  ){  dfm2::opengl::DrawMeshHex3D_FaceNorm( pos.data(), elm.data(), shape_elm[0]); }
    if( type == dfm2::MESHELEM_TET  ){  dfm2::opengl::DrawMeshTet3D_FaceNorm( pos.data(), elm.data(), shape_elm[0]); }
  }
}

void PyDrawMesh_Edge(
    const py::array_t<double>& pos,
    const py::array_t<unsigned int>& elm,
    const dfm2::MESHELEM_TYPE type)
{
  assert(pos.ndim()==2);
  assert(elm.ndim()==2);
  const auto shape_pos = pos.shape();
  const auto shape_elm = elm.shape();
  if( shape_pos[1] == 3 ){ // 3D Mesh
    if( type == dfm2::MESHELEM_TRI  ){  dfm2::opengl::DrawMeshTri3D_Edge( pos.data(), shape_pos[0], elm.data(), shape_elm[0]); }
    if( type == dfm2::MESHELEM_QUAD ){  dfm2::opengl::DrawMeshQuad3D_Edge(pos.data(), shape_pos[0], elm.data(), shape_elm[0]); }
    if( type == dfm2::MESHELEM_HEX  ){  dfm2::opengl::DrawMeshHex3D_Edge( pos.data(), shape_pos[0], elm.data(), shape_elm[0]); }
    if( type == dfm2::MESHELEM_TET  ){  dfm2::opengl::DrawMeshTet3D_Edge( pos.data(), shape_pos[0], elm.data(), shape_elm[0]); }
    if( type == dfm2::MESHELEM_LINE ){  dfm2::opengl::DrawMeshLine3D_Edge( pos.data(), shape_pos[0], elm.data(), shape_elm[0]); }
  }
  if( shape_pos[1] == 2 ){ // 2D Mesh
    if( type == dfm2::MESHELEM_TRI  ){  dfm2::opengl::DrawMeshTri2D_Edge( pos.data(), shape_pos[0], elm.data(), shape_elm[0]); }
    if( type == dfm2::MESHELEM_QUAD ){  dfm2::opengl::DrawMeshQuad2D_Edge(pos.data(), shape_pos[0], elm.data(), shape_elm[0]); }
  }
}

// ----------------------------------------------------------

void init_opengl_old_mshuni(py::module &m) {
  m.def("draw_mesh_facenorm",  &PyDrawMesh_FaceNorm);
  m.def("draw_mesh_edge",      &PyDrawMesh_Edge);
}