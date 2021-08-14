
from typing import List
import delfem2.window_glfw

class FrameBufferGLFW:
    def __init__(self,
                 win_size: List[int],
                 format_color: str,
                 is_depth: bool):
        self.win = delfem2.window_glfw.WindowGLFW(isVisible=False)
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