/*
 * Copyright (c) 2021 Nobuyuki Umetani
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/eigen.h>

#include "delfem2/eigen/msh_io.h"

namespace py = pybind11;
namespace dfm2 = delfem2;

// ----------------------------------------------------------

void init_msh_io(py::module &m) {
  m.def("read_uniform_mesh",
        &ReadTriangleMeshObj, "");

  m.def("write_uniform_mesh",
        &WriteUniformMesh);
}