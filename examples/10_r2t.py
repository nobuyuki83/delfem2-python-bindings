####################################################################
# Copyright (c) 2019 Nobuyuki Umetani                              #
#                                                                  #
# This source code is licensed under the MIT license found in the  #
# LICENSE file in the root directory of this source tree.          #
####################################################################

import os
import OpenGL.GL as gl
import numpy as np
import math

import delfem2 as dfm2
import delfem2.mesh
import delfem2.drawer_mesh
import delfem2.plot3
import delfem2.render_to_texture
import delfem2.drawer_axisxyz
from delfem2.invisible_window_glfw import InVisibleWindowGLFW


def show_default(drawer, r2t):
    with InVisibleWindowGLFW([512, 512]):
        dfm2.glad_load_gl()
        if hasattr(drawer, "init_gl"):
            drawer.init_gl()
        r2t.init_gl()
        r2t.start()
        gl.glClearColor(1, 1, 1, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        r2t.set_modelviewprojection_matrix_legacy_opengl()
        drawer.draw()
        r2t.end()

    drawer_r2t = delfem2.render_to_texture.DrawerRender2Tex(r2t)
    drawer_r2t.drawer.color_point = [1, 0, 0, 1]
    dfm2.plot3.plot3(
        [drawer, drawer_r2t], duration=3,
        camera_rotation=(math.pi * 0.1, math.pi * 0.4, math.pi * 0.0))


def affinematrix_modelview_localcoordinate(
        org: np.ndarray, az: np.ndarray, ax: np.ndarray):
    ay = np.cross(az, ax)
    o = np.array([ax.dot(org), ay.dot(org), az.dot(org)])
    return np.array([
        [ax[0], ax[1], ax[2], -o[0]],
        [ay[0], ay[1], ay[2], -o[1]],
        [az[0], az[1], az[2], -o[2]],
        [0, 0, 0, 1]])


def affinematrix_projection_orthogonal(num_res_x, num_res_y, len_pix, z_range):
    l = -len_pix * num_res_x * 0.5
    r = +len_pix * num_res_x * 0.5
    b = -len_pix * num_res_y * 0.5
    t = +len_pix * num_res_y * 0.5
    n = -z_range * 0.5
    f = +z_range * 0.5
    return np.array([
        [2.0 / (r - l), 0, 0, -(l + r) / (r - l)],
        [0, 2.0 / (t - b), 0, -(t + b) / (t - b)],
        [0, 0, 2.0 / (n - f), -(n + f) / (n - f)],
        [0, 0, 0, 1]])


def main():
    V, F = dfm2.mesh.read_triangle_mesh(os.path.join(os.getcwd(), "asset", "bunny_1k.obj"))
    V -= np.average(V, axis=0)
    V /= np.max(V) - np.min(V)

    drawer_mesh = delfem2.drawer_mesh.DrawerMesh(
        V, F, dfm2.mesh.TRI,
        is_draw_edge=True, is_draw_face=True)

    r2t = dfm2.render_to_texture.Render2Tex(
        width=256, height=256, is_rgba_8ui=True)

    show_default(drawer_mesh, r2t)

    str_glsl_vrt = "\
    varying vec3 vNormal; \n\
    varying vec4 vPosition; \n\
    void main() \n\
    { \n\
      vNormal = normalize(vec3(gl_ModelViewMatrix * vec4(gl_Normal.xyz,0.0))); \n\
      gl_Position = ftransform(); \n\
      vPosition = gl_ModelViewMatrix * gl_Vertex; \n\
    }"

    str_glsl_frg = "\
    varying vec3 vNormal; \n\
    varying vec4 vPosition; \n\
    void main() \n\
    { \n\
    gl_FragColor = vec4(0.5+0.5*vNormal.x, 0.5-0.5*vNormal.y, 0.5*vNormal.z+0.5, 1.0); \n\
    }"

    drawer_mesh = delfem2.drawer_mesh.DrawerMesh(
        V, F, dfm2.mesh.TRI,
        is_draw_edge=False, is_draw_face=True,
        glsl_vtx=str_glsl_vrt, glsl_frag=str_glsl_frg)

    show_default(drawer_mesh, r2t)

    r2t = dfm2.render_to_texture.Render2Tex(
        width=512, height=256, is_rgba_8ui=True,
        affinematrix_modelview=affinematrix_modelview_localcoordinate(
            np.array([0, 0, 0]), np.array([0, 1, 0]), np.array([1, 0, 0])),
        affinematrix_projection=affinematrix_projection_orthogonal(512, 256, 2. / 256., 2.0)
    )

    show_default(drawer_mesh, r2t)


if __name__ == "__main__":
    main()
