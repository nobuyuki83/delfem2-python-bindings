/*
 * Copyright (c) 2021 Nobuyuki Umetani
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

#include <deque>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/eigen.h>

#include "delfem2/opengleigen/funcs.h"

namespace py = pybind11;

// ----------------------------------------------------------

void init_opengleigen_funcs(py::module &m) {
  m.def("draw_meshtri3_edge",
        &delfem2::opengleigen::DrawMeshTri3_Edge_EigenMats, "");
}