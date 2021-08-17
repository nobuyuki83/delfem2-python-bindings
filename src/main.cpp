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

void init_msh_io(py::module &);
void init_msh_elm(py::module &);
void init_opengl_r2t(py::module &);
void init_opengl_old_mshuni(py::module &);
void init_opengleigen_funcs(py::module &);
void init_glad_glfw(py::module &);
void init_opengl_old_drawer_r2t(py::module &m);
void init_opengl_texture(py::module &m);

PYBIND11_MODULE(delfem2, m) {
  m.doc() = "my_cpp_module";

  init_msh_io(m);
  init_msh_elm(m);
  init_opengleigen_funcs(m);
  init_opengl_r2t(m);
  init_opengl_texture(m);
  init_opengl_old_mshuni(m);
  init_opengl_old_drawer_r2t(m);
  init_glad_glfw(m);
}


