//
// Created by Nobuyuki Umetani on 2021-10-29.
//

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "delfem2/rig_bvh.h"

namespace py = pybind11;
namespace dfm2 = delfem2;

// ----------------------------------------------------------


void init_bvh(py::module &m) {
  namespace dfm2 = delfem2;
  py::class_<delfem2::CRigBone>(m, "RigBone")
      .def(py::init<>())
      .def("position", &delfem2::CRigBone::RootPosition)
      .def_readonly("name", &delfem2::CRigBone::name)
      .def_readonly("parent_bone_idx", &delfem2::CRigBone::ibone_parent);

  py::class_<delfem2::CChannel_BioVisionHierarchy>(m, "Channel_BioVisionHierarchy")
      .def(py::init<unsigned int, int, bool>())
      .def_readonly("ibone", &delfem2::CChannel_BioVisionHierarchy::ibone)
      .def_readonly("iaxis", &delfem2::CChannel_BioVisionHierarchy::iaxis)
      .def_readonly("is_rot", &delfem2::CChannel_BioVisionHierarchy::isrot);

  py::class_<dfm2::BioVisionHierarchy>(m, "BVH")
      .def(py::init<>())
      .def("open",&dfm2::BioVisionHierarchy::Open)
      .def("set_frame",&dfm2::BioVisionHierarchy::SetFrame)
      .def("clear_pose", &dfm2::BioVisionHierarchy::ClearPose)
      .def("minmax_xyz", &dfm2::BioVisionHierarchy::MinMaxXYZ)
      .def("get_bone", &dfm2::BioVisionHierarchy::GetBone)
      .def_readonly("nframe", &dfm2::BioVisionHierarchy::nframe)
      .def_readonly("bones", &dfm2::BioVisionHierarchy::bones)
      .def_readonly("channels", &dfm2::BioVisionHierarchy::channels);
}