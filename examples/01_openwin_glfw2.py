####################################################################
# Copyright (c) 2019 Nobuyuki Umetani                              #
#                                                                  #
# This source code is licensed under the MIT license found in the  #
# LICENSE file in the root directory of this source tree.          #
####################################################################

import OpenGL.GL as gl
import numpy
import delfem2 as dfm2
import delfem2.mesh
import delfem2.window_glfw
import os


def draw_func():
    gl.glDisable(gl.GL_LIGHTING)
    gl.glColor3d(0, 0, 0)
    dfm2.mesh.draw_meshtri3_edge(V, F)


V, F = dfm2.mesh.read_triangle_mesh(os.path.join(os.getcwd(), "asset", "bunny_1k.obj"))
V -= numpy.average(V,axis=0)
V /= V.max() - V.min()

win = dfm2.window_glfw.WindowGLFW(1.0, winsize=(400, 300))
win.list_func_draw.append(draw_func)
win.draw_loop()
