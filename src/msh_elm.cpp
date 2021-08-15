//
// Created by Nobuyuki Umetani on 2021-08-15.
//


#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/eigen.h>

#include "delfem2/mshelm.h"

namespace dfm2 = delfem2;
namespace py = pybind11;

void init_msh_elm(py::module &m) {
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
        &dfm2::nNodeElem,
        "number of cornder nodes in the elem");
}
