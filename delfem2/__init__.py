import OpenGL.GL as gl
import numpy as np

from .delfem2 import *



class DrawerRender2Tex:
    def __init__(self, r2t):
        self.r2t = r2t
        self.drawer = delfem2._DrawerRender2Tex()

    def draw(self):
        self.drawer.draw(self.r2t)

    def init_gl(self):
        self.r2t.init_gl()

    def minmax_xyz(self):
        mvp = np.array(self.r2t.get_matrix_projection()).reshape(4,4).transpose() * \
              np.array(self.r2t.get_matrix_model_view()).reshape(4,4).transpose()
        mvp_inverse = np.linalg.inv(mvp)

        # coorinates of the corner points in the global coordinate
        corner = mvp_inverse @ np.array([
            [-1,-1,-1,+1],
            [-1,-1,+1,+1],
            [-1,+1,-1,+1],
            [-1,+1,+1,+1],
            [+1,-1,-1,+1],
            [+1,-1,+1,+1],
            [+1,+1,-1,+1],
            [+1,+1,+1,+1]], dtype=np.float32).transpose()
        corner = corner[:-1,:]  # change homogenous coordinate to xyz coordinate

        return [corner[0].min(),corner[1].min(),corner[2].min(),
                corner[0].max(),corner[1].max(),corner[2].max()]


def _r2t_get_depth(self):
    return delfem2._render2tex_depth_buffer(self)

setattr(delfem2.Render2Tex,"get_depth",_r2t_get_depth)

def _r2t_get_color_4byte(self):
    return delfem2._render2tex_color_buffer_4byte(self)

setattr(delfem2.Render2Tex,"get_color_4byte",_r2t_get_color_4byte)