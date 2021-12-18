//
// Created by Nobuyuki Umetani on 2021/12/18.
//

#include <pybind11/pybind11.h>
#include <Alembic/AbcGeom/All.h>
#include <Alembic/AbcCoreOgawa/All.h>

namespace py = pybind11;

class AlembicOPolyMesh{
public:
  AlembicOPolyMesh(double dt) :
    archive(Alembic::AbcCoreOgawa::WriteArchive(), "simple.abc"),
    mesh_obj(Alembic::Abc::OObject(archive, Alembic::Abc::kTop), "mesh")
  {
    { // set time sampling
      const Alembic::Abc::TimeSampling time_sampling(dt, 0);
      const uint32_t time_sampling_index = archive.addTimeSampling(time_sampling);
      mesh_obj.getSchema().setTimeSampling(time_sampling_index);
    }
  }
  /*
  void Hoge(){
    const Alembic::AbcGeom::OPolyMeshSchema::Sample mesh_samp(
    Alembic::AbcGeom::V3fArraySample((const Alembic::Abc::V3f *) aXYZ.data(), aXYZ.size() / 3),
      Alembic::AbcGeom::Int32ArraySample(aTri.data(), aTri.size()),
      Alembic::AbcGeom::Int32ArraySample(aElmSize.data(), aElmSize.size()));
    mesh_obj.getSchema().set(mesh_samp);
  }
   */
 public:
  Alembic::Abc::OArchive archive;
  Alembic::AbcGeom::OPolyMesh mesh_obj;
};


void init_alembic_opolymesh(py::module &m) {
  // namespace dfm2 = delfem2;
  py::class_<AlembicOPolyMesh>(m, "AlembicOPolyMesh")
    .def(py::init<double>());

}
