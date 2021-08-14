/*
 * Copyright (c) 2019 Nobuyuki Umetani
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

#include <iostream>
#include <deque>
#include <pybind11/pybind11.h>

#include "delfem2/mshelm.h"

namespace dfm2 = delfem2;
namespace py = pybind11;

void init_mshio(py::module &);
void init_opengleigen_funcs(py::module &);
void init_opengl_r2t(py::module &m);
void init_glad_glfw(py::module &m);

PYBIND11_MODULE(delfem2, m) {
  m.doc() = "my_cpp_module";
  init_mshio(m);
  init_opengleigen_funcs(m);
  init_opengl_r2t(m);
  init_glad_glfw(m);

  py::enum_<dfm2::MESHELEM_TYPE>(m, "MESH_ELEM_TYPE")
      .value("TRI", dfm2::MESHELEM_TYPE::MESHELEM_TRI)
      .value("QUAD", dfm2::MESHELEM_TYPE::MESHELEM_QUAD)
      .value("TET", dfm2::MESHELEM_TYPE::MESHELEM_TET)
      .value("PYRAMID", dfm2::MESHELEM_TYPE::MESHELEM_PYRAMID)
      .value("WEDGE", dfm2::MESHELEM_TYPE::MESHELEM_WEDGE)
      .value("HEX", dfm2::MESHELEM_TYPE::MESHELEM_HEX)
      .value("LINE", dfm2::MESHELEM_TYPE::MESHELEM_LINE)
      .export_values();
  m.def("num_node_elem",
        &dfm2::nNodeElem);
}


