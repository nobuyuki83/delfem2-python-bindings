//
// Created by Nobuyuki Umetani on 2021/12/18.
//

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

#include <Alembic/AbcGeom/All.h>
#include <Alembic/AbcCoreOgawa/All.h>

namespace py = pybind11;

class AlembicOPolyMesh{
public:
  AlembicOPolyMesh(const std::string& path, double dt) :
    archive(Alembic::AbcCoreOgawa::WriteArchive(), path),
    mesh_obj(Alembic::Abc::OObject(archive, Alembic::Abc::kTop), "mesh")
  {
    { // set time sampling
      const Alembic::Abc::TimeSampling time_sampling(dt, 0);
      const uint32_t time_sampling_index = archive.addTimeSampling(time_sampling);
      mesh_obj.getSchema().setTimeSampling(time_sampling_index);
    }
  }
  void SetMesh(
    const py::array_t<float>& vtx_xyz,
    const py::array_t<int>& elem_vtx){
    const auto vtx_xyz_shape = vtx_xyz.request().shape;
    if (vtx_xyz_shape.size() != 2) { return; }
    const auto elem_vtx_shape = elem_vtx.request().shape;
    if (elem_vtx_shape.size() != 2) { return; }
    std::vector<int> elem_nnode( elem_vtx_shape[0], static_cast<int>(elem_vtx_shape[1]) );
    const Alembic::AbcGeom::OPolyMeshSchema::Sample mesh_samp(
      Alembic::AbcGeom::V3fArraySample((const Alembic::Abc::V3f *)vtx_xyz.data(), vtx_xyz_shape[0]),
      Alembic::AbcGeom::Int32ArraySample(elem_vtx.data(), elem_vtx.size()),
      Alembic::AbcGeom::Int32ArraySample(elem_nnode.data(), elem_nnode.size()));
    mesh_obj.getSchema().set(mesh_samp);
  }

  void SetVertices(
    const py::array_t<float>& vtx_xyz)
  {
    const auto vtx_xyz_shape = vtx_xyz.request().shape;
    if (vtx_xyz_shape.size() != 2) { return; }
    const Alembic::AbcGeom::OPolyMeshSchema::Sample mesh_samp(
    Alembic::AbcGeom::V3fArraySample((const Alembic::Abc::V3f *)vtx_xyz.data(), vtx_xyz_shape[0]));
    mesh_obj.getSchema().set(mesh_samp);
  }

 public:
  Alembic::Abc::OArchive archive;
  Alembic::AbcGeom::OPolyMesh mesh_obj;
};


void init_alembic_opolymesh(py::module &m) {
  // namespace dfm2 = delfem2;
  py::class_<AlembicOPolyMesh>(m, "AlembicOPolyMesh")
    .def(py::init<const std::string&, double>())
    .def("set_mesh", &AlembicOPolyMesh::SetMesh)
    .def("set_vertices", &AlembicOPolyMesh::SetVertices);
}
