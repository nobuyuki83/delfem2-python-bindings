/*
 * Copyright (c) 2019 Nobuyuki Umetani
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <iostream>
#include <vector>
#include <deque>

namespace py = pybind11;

// ----------------------------------------------------------

void CppSayHelloWorld(){
  std::cout << "hello world!" << std::endl;
}

PYBIND11_MODULE(delfem2, m) {
  m.doc() = "my_cpp_module";
  m.def("say_hello_world", &CppSayHelloWorld);
}


