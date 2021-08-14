/*
 * Copyright (c) 2019 Nobuyuki Umetani
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

#include <iostream>
#include <deque>
#include <pybind11/pybind11.h>

namespace py = pybind11;

void init_mshio(py::module &);
void init_opengleigen_funcs(py::module &);

PYBIND11_MODULE(delfem2, m) {
  m.doc() = "my_cpp_module";
  init_mshio(m);
  init_opengleigen_funcs(m);
}


