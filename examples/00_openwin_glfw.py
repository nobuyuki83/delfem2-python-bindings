####################################################################
# Copyright (c) 2019 Nobuyuki Umetani                              #
#                                                                  #
# This source code is licensed under the MIT license found in the  #
# LICENSE file in the root directory of this source tree.          #
####################################################################

import OpenGL.GL as gl
import glfw
import numpy as np

import delfem2 as dfm2
import delfem2.navigation_glfw
import os

nav = dfm2.navigation_glfw.NavigationGLFW(1.0)


def mouseButtonCB(win_glfw, btn, action, mods):
    nav.mouse(win_glfw, btn, action, mods)


def mouseMoveCB(win_glfw, x, y):
    nav.motion(win_glfw, x, y)


def keyFunCB(win_glfw, key, scancode, action, mods):
    nav.keyinput(win_glfw, key, scancode, action, mods)


def main():
    global nav

    V, F = dfm2.read_triangle_mesh(os.path.join(os.getcwd(), "asset", "bunny_1k.obj"))
    V *= 0.02
    print(V.shape, F.shape)

    glfw.init()
    win_glfw = glfw.create_window(640, 480, 'Hello World', None, None)
    glfw.make_context_current(win_glfw)

    #  dfm2.gl.setSomeLighting()
    gl.glEnable(gl.GL_DEPTH_TEST)

    glfw.set_mouse_button_callback(win_glfw, mouseButtonCB)
    glfw.set_cursor_pos_callback(win_glfw, mouseMoveCB)
    glfw.set_key_callback(win_glfw, keyFunCB)

    while not glfw.window_should_close(win_glfw):
        gl.glClearColor(1, 1, 1, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glEnable(gl.GL_POLYGON_OFFSET_FILL)
        gl.glPolygonOffset(1.1, 4.0)
        nav.camera.set_gl_camera()
        gl.glColor3d(0, 0, 0)
        gl.glDisable(gl.GL_LIGHTING)
        dfm2.draw_meshtri3_edge(V, F)
        glfw.swap_buffers(win_glfw)
        glfw.poll_events()
        if nav.isClose:
            break
    glfw.destroy_window(win_glfw)
    glfw.terminate()
    print("closed")


if __name__ == "__main__":
    main()
