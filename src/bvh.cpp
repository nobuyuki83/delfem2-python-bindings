//
// Created by Nobuyuki Umetani on 2021-10-29.
//

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

#include "delfem2/rig_bvh.h"

namespace py = pybind11;
namespace dfm2 = delfem2;

// ----------------------------------------------------------

py::array_t<double> get_parameter_history_bvh(
  dfm2::BioVisionHierarchy &bvh) {
  const size_t nf = bvh.nframe;
  const size_t nc = bvh.channels.size();
  std::vector<size_t> strides = {
    sizeof(double) * nc,
    sizeof(double)};
  std::vector<size_t> shape = {
    nf,
    nc};
  return py::array(
    py::buffer_info(bvh.frame_channel.data(), sizeof(double),
                    py::format_descriptor<double>::format(),
                    2, shape, strides));
}

py::array_t<double> get_joint_position_history_bvh(
  dfm2::BioVisionHierarchy &bvh) {
  const std::vector<std::size_t> shape = {
    static_cast<size_t>(bvh.nframe),
    bvh.bones.size(),
    3};
  py::array_t<double> arr{shape};
  for (unsigned int iframe = 0; iframe < bvh.nframe; ++iframe) {
    bvh.SetFrame(iframe);
    for (unsigned int ib = 0; ib < bvh.bones.size(); ++ib) {
      const auto p0 = bvh.bones[ib].RootPosition();
      arr.mutable_at(iframe, ib, 0) = p0[0];
      arr.mutable_at(iframe, ib, 1) = p0[1];
      arr.mutable_at(iframe, ib, 2) = p0[2];
    }
  }
  return arr;
}

template<typename T>
void set_parameter_history_bvh(
  dfm2::BioVisionHierarchy &bvh,
  const py::array_t<T> arr) {
  const auto &buff_info = arr.request();
  const auto &shape = buff_info.shape;
  if (shape.size() != 2) { return; }
  if (shape[1] != static_cast<long>(bvh.channels.size())) { return; }
  // std::cout << shape[0] << " " << shape[1] << std::endl;
  bvh.nframe = shape[0];
  const size_t nc = bvh.channels.size();
  bvh.frame_channel.resize(bvh.nframe * nc);
  for (size_t iframe = 0; iframe < bvh.nframe; ++iframe) {
    for (size_t ic = 0; ic < nc; ++ic) {
      bvh.frame_channel[iframe * nc + ic] = arr.at(iframe, ic);
    }
  }
  /*
  const size_t nf = bvh.nframe;
  const size_t nc = bvh.channels.size();
  std::vector<size_t> strides = {
      sizeof(double)*nc,
      sizeof(double)};
  std::vector<size_t> shape = {
      nf,
      nc};
  return py::array(
      py::buffer_info(bvh.frame_channel.data(), sizeof(double),
                      py::format_descriptor<double>::format(),
                      2, shape, strides));
                      */
}

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
    .def(py::init<const std::string &>())
    .def("open", &dfm2::BioVisionHierarchy::Open)
    .def("set_frame", &dfm2::BioVisionHierarchy::SetFrame)
    .def("clear_pose", &dfm2::BioVisionHierarchy::ClearPose)
    .def("minmax_xyz", &dfm2::BioVisionHierarchy::MinMaxXYZ)
    .def("get_bone", &dfm2::BioVisionHierarchy::GetBone)
    .def_readonly("nframe", &dfm2::BioVisionHierarchy::nframe)
    .def_readonly("bones", &dfm2::BioVisionHierarchy::bones)
    .def_readonly("channels", &dfm2::BioVisionHierarchy::channels);

  m.def("get_parameter_history_bvh", &get_parameter_history_bvh);
  m.def("get_joint_position_history_bvh", &get_joint_position_history_bvh);
  m.def("set_parameter_history_bvh_double", &set_parameter_history_bvh<double>);
}