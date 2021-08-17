from .delfem2 import *


class DrawerRender2Tex:
    def __init__(self, r2t):
        self.r2t = r2t
        self.drawer = delfem2._DrawerRender2Tex()

    def draw(self):
        self.drawer.draw(self.r2t)

    def init_gl(self):
        self.r2t.init_gl()
