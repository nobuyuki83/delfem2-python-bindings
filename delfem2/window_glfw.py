####################################################################
# Copyright (c) 2019 Nobuyuki Umetani                              #
#                                                                  #
# This source code is licensed under the MIT license found in the  #
# LICENSE file in the root directory of this source tree.          #
####################################################################

import OpenGL.GL as gl
import glfw
from delfem2.navigation_glfw import NavigationGLFW
from delfem2.camera import Camera

class WindowGLFW:
    """
    class to manage a glfw window
    """

    def __init__(self, view_height=1.0, winsize=(400, 300), isVisible=True):
        self.is_valid = True
        try:
            glfw.init()
        except:
            self.is_valid = False
            return
        if not isVisible:
            glfw.window_hint(glfw.VISIBLE, False)
        self.win = glfw.create_window(
            winsize[0], winsize[1],
            '3D Window',
            None, None)
        glfw.make_context_current(self.win)
        ###
        self.nav = NavigationGLFW(view_height)
        self.camera = Camera()
        self.list_func_mouse = []
        self.list_func_motion = []
        self.list_func_step_time = []
        self.list_func_draw = []
        self.list_func_key = []
        self.color_bg = (1, 1, 1)
        gl.glEnable(gl.GL_DEPTH_TEST)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        #    self.close()
        pass

    def draw_loop(self, nframe=-1):
        """
        Enter the draw loop

        render -- a function to render
        """
        glfw.set_mouse_button_callback(self.win, self.mouse)
        glfw.set_cursor_pos_callback(self.win, self.motion)
        glfw.set_key_callback(self.win, self.keyinput)
        glfw.set_scroll_callback(self.win, self.scroll)
        #    glfw.set_window_size_callback(self.win, self.window_size)
        iframe = 0
        while not glfw.window_should_close(self.win):
            gl.glClearColor(self.color_bg[0], self.color_bg[1], self.color_bg[2], 1.0)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
            gl.glEnable(gl.GL_POLYGON_OFFSET_FILL)
            gl.glPolygonOffset(1.1, 4.0)
            self.camera.set_gl_camera()
            for func_step_time in self.list_func_step_time:
                func_step_time()
            for draw_func in self.list_func_draw:
                draw_func()
            glfw.swap_buffers(self.win)
            glfw.poll_events()
            iframe += 1
            if nframe > 0 and iframe > nframe:
                break
            if self.nav.isClose:
                break
        self.close()

    def close(self):
        glfw.destroy_window(self.win)
        glfw.terminate()

    def mouse(self, win0, btn, action, mods):
        self.nav.mouse(win0, btn, action, mods)
        mMV = gl.glGetFloatv(gl.GL_MODELVIEW_MATRIX)
        mPj = gl.glGetFloatv(gl.GL_PROJECTION_MATRIX)
        '''
        src = screenUnProjection(numpy.array([float(self.wm.mouse_x),float(self.wm.mouse_y),0.0]),
                                 mMV, mPj)
        dir = screenUnProjectionDirection(numpy.array([0,0,1]), mMV,mPj)
        for func_mouse in self.list_func_mouse:
          func_mouse(btn,action,mods, src, dir, self.wm.camera.view_height)
        '''

    def motion(self, win0, x, y):
        if self.nav.button == -1:
            return
        self.nav.motion(win0, x, y, self.camera)
        mMV = gl.glGetFloatv(gl.GL_MODELVIEW_MATRIX)
        mPj = gl.glGetFloatv(gl.GL_PROJECTION_MATRIX)
        '''
        src0 = screenUnProjection(numpy.array([float(self.wm.mouse_pre_x),float(self.wm.mouse_pre_y),0.0]),
                                 mMV, mPj)
        src1 = screenUnProjection(numpy.array([float(self.wm.mouse_x),float(self.wm.mouse_y),0.0]),
                                 mMV, mPj)
        dir = screenUnProjectionDirection(numpy.array([0,0,1]), mMV,mPj)
        for func_motion in self.list_func_motion:
          func_motion(src0,src1,dir)
        '''

    def keyinput(self, win0, key, scancode, action, mods):
        self.nav.keyinput(win0, key, scancode, action, mods, self.camera)
        if action != glfw.PRESS:
            return
        key_name = glfw.get_key_name(key, scancode)
        for func_key in self.list_func_key:
            func_key(key_name)

    def scroll(self, win0, xoffset: float, yoffset: float):
        self.camera.scale *= pow(1.01, yoffset)