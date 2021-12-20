//
// Created by Nobuyuki Umetani on 2021/12/11.
//

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include <pybind11/eigen.h>

#include "delfem2/quat.h"
#include "delfem2/mat3.h"

namespace dfm2 = delfem2;
namespace py = pybind11;

auto PyMat3_EulerAngle(
  const std::array<double, 3> &rads,
  const std::array<int, 3> &axis_idxs) {
  double q[4] = {0., 0., 0., 1.};
  delfem2::Quaternion_EulerAngle(q, rads, axis_idxs);
  py::array_t<double> y{{3, 3}};
  delfem2::Mat3_Quat(y.mutable_data(), q);
  return y;
}

auto pyAxisAngleVector_Cartesian_Mat3(const Eigen::Matrix<double, 3, 3, Eigen::RowMajor> &m) {
  py::array_t<double> y{3};
  dfm2::AxisAngleVectorCartesian_Mat3(y.mutable_data(), m.data());
  return y;
}

auto pyQuaternion_Mat3(
  const Eigen::Matrix<double, 3, 3, Eigen::RowMajor> &m) {
  py::array_t<double> y{4};
  dfm2::Quat_Mat3(y.mutable_data(), m.data());
  return y;
}

auto pyMat3_Quaternion(
  const std::array<double, 4> &quat)
{
  py::array_t<double> y{{3, 3}};
  delfem2::Mat3_Quat(y.mutable_data(), quat.data());
  return y;
}

auto pyEulerAngle_Mat3(
  const Eigen::Matrix<double, 3, 3, Eigen::RowMajor> &m,
  const std::array<int, 3> &axis_idxs)
{
  py::array_t<double> y{3};
  delfem2::EulerAngle_Mat3(
    y.mutable_data(),
    m.data(), axis_idxs);
  return y;
}

auto pyMat3_AxisAngleVectorCartesian(
  const std::array<double, 3> &aa)
{
  py::array_t<double> y{{3, 3}};
  delfem2::Mat3_Rotation_Cartesian(y.mutable_data(), aa.data());
  return y;
}

auto pyMultiply_Quaternion_Quaternion(
  const std::array<double, 4> &q0,
  const std::array<double, 4> &q1)
{
  py::array_t<double> y{4};
  delfem2::QuatQuat(y.mutable_data(), q0.data(), q1.data());
  return y;
}

void init_mat3(py::module &m) {
  m.def(
    "mat3_from_euler_angle",
    PyMat3_EulerAngle);
  m.def(
    "cartesian_axis_angle_vector_from_mat3",
    pyAxisAngleVector_Cartesian_Mat3);
  m.def(
    "quaternion_from_mat3",
    pyQuaternion_Mat3);
  m.def(
    "mat3_from_quaternion",
    pyMat3_Quaternion);
  m.def(
    "euler_angle_from_mat3",
    pyEulerAngle_Mat3);
  m.def(
    "mat3_from_cartesian_axis_angle_vector",
    pyMat3_AxisAngleVectorCartesian);
  m.def(
    "multiply_quaternion_quaternion",
    pyMultiply_Quaternion_Quaternion);
}
