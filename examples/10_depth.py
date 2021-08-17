####################################################################
# Copyright (c) 2019 Nobuyuki Umetani                              #
#                                                                  #
# This source code is licensed under the MIT license found in the  #
# LICENSE file in the root directory of this source tree.          #
####################################################################

import os
import numpy
import OpenGL.GL as gl
from PIL import Image

import delfem2 as dfm2
import delfem2.drawer_mesh
import delfem2.show_3d
from delfem2.framebuffer_glfw import FrameBufferGLFW


def main():
    V, F = dfm2.read_triangle_mesh(os.path.join(os.getcwd(), "asset", "bunny_1k.obj"))
    V *= 0.02

    sampler = dfm2.Render2Tex()
    sampler.set_texture_property(
        size_res_width=256, size_res_height=256, is_rgba_8ui=True)

    drawer_mesh = delfem2.drawer_mesh.DrawerMesh(
        V, F, dfm2.TRI,
        is_draw_edge=True, is_draw_face=True)

    with FrameBufferGLFW([512, 512], format_color="4byte", is_depth=True):
        dfm2.glad_load_gl()
        sampler.init_gl()
        sampler.start()
        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glClearColor(1, 1, 1, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glDisable(gl.GL_LIGHTING)
        gl.glDisable(gl.GL_BLEND)
        gl.glColor3d(0, 0, 0)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glMultMatrixd(sampler.get_matrix_projection())
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.glMultMatrixd(sampler.get_matrix_model_view())
        drawer_mesh.draw()
        sampler.end()

    drawer_r2t = delfem2.DrawerRender2Tex(sampler)
    drawer_r2t.drawer.color_point = [1, 0, 0, 1]
    dfm2.show_3d.show_3d([drawer_mesh, drawer_r2t])


if __name__ == "__main__":
    main()
