
from typing import List
from delfem2.opengl.window_glfw import WindowGLFW

class InVisibleWindowGLFW:
    def __init__(self,
                 win_size: List[int]):
        self.win = WindowGLFW(
            winsize=win_size,
            isVisible=False)
        self.is_open = True

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_value, trace):
        self.close()

    def __del__(self):
        self.close()

    def close(self):
        if self.is_open:
            self.win.close()
        self.is_open = False