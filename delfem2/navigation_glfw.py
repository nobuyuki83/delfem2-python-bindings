import glfw
from delfem2.camera import Camera


class NavigationGLFW:
    """
    class for GUI for camera control
    """

    def __init__(self, view_height):
        self.camera = Camera(view_height)
        self.modifier = 0
        self.mouse_x = 0.0
        self.mouse_y = 0.0
        self.mouse_pre_x = 0.0
        self.mouse_pre_y = 0.0
        self.button = -1
        self.isClose = False

    def keyinput(self, win_glfw, key, scancode, action, mods) -> None:
        if key == glfw.KEY_Q and action == glfw.PRESS:
            self.isClose = True
        if key == glfw.KEY_PAGE_UP:
            self.camera.scale *= 1.03
        if key == glfw.KEY_PAGE_DOWN:
            self.camera.scale /= 1.03

    def mouse(self, win_glfw, btn, action, mods) -> None:
        (win_w, win_h) = glfw.get_window_size(win_glfw)
        (x, y) = glfw.get_cursor_pos(win_glfw)
        self.mouse_x = (2.0 * x - win_w) / win_w
        self.mouse_y = (win_h - 2.0 * y) / win_h
        self.modifier = mods
        if action == glfw.PRESS:
            self.button = btn
        elif action == glfw.RELEASE:
            self.button = -1

    def motion(self, win_glfw, x, y) -> None:
        (win_w, win_h) = glfw.get_window_size(win_glfw)
        self.mouse_pre_x, self.mouse_pre_y = self.mouse_x, self.mouse_y
        (x, y) = glfw.get_cursor_pos(win_glfw)
        self.mouse_x = (2.0 * x - win_w) / win_w
        self.mouse_y = (win_h - 2.0 * y) / win_h
        if self.button == glfw.MOUSE_BUTTON_LEFT:
            if self.modifier == glfw.MOD_ALT:  # shift
                self.camera.rotation(self.mouse_x, self.mouse_y, self.mouse_pre_x, self.mouse_pre_y)
            if self.modifier == glfw.MOD_SHIFT:
                self.camera.translation(self.mouse_x, self.mouse_y, self.mouse_pre_x, self.mouse_pre_y)
