import numpy as np
import OpenGL.GL as gl
from .delfem2 import \
    _Render2Tex, \
    _DrawerRender2Tex, \
    _render2tex_depth_buffer, \
    _render2tex_color_buffer_4byte

class DrawerRender2Tex:
    def __init__(self, r2t):
        self.r2t = r2t
        self.drawer = _DrawerRender2Tex()

    def draw(self):
        self.drawer.draw(self.r2t._r2t)

    def init_gl(self):
        self.r2t.init_gl()

    def minmax_xyz(self):
        mvp = self.r2t.affinematrix_projection() @ self.r2t.affinematrix_modelview()
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


class Render2Tex:
    def __init__(self, width, height, is_rgba_8ui=True,
                 affinematrix_modelview=None,
                 affinematrix_projection=None):
        self._r2t = _Render2Tex()
        self._r2t.set_texture_property(size_res_width=width, size_res_height=height, is_rgba_8ui=is_rgba_8ui)
        if isinstance(affinematrix_modelview,np.ndarray):
            mvt = list(affinematrix_modelview.copy().reshape([16]))
            self._r2t.set_affinematrix_modelview(mvt)
        if isinstance(affinematrix_projection,np.ndarray):
            mp = list(affinematrix_projection.copy().reshape([16]))
            self._r2t.set_affinematrix_projection(mp)


    def init_gl(self):
        self._r2t.init_gl()

    def start(self):
        self._r2t.start()

    def end(self):
        self._r2t.end()

    def affinematrix_projection(self):
        return np.array(self._r2t.get_affinematrix_projection()).reshape(4,4)

    def affinematrix_modelview(self):
        return np.array(self._r2t.get_affinematrix_modelview()).reshape(4,4)

    def get_depth(self):
        return _render2tex_depth_buffer(self._r2t)

    def get_color_4byte(self):
        return _render2tex_color_buffer_4byte(self._r2t)

    def set_modelviewprojection_matrix_legacy_opengl(self):
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        mp = np.diag([1.,1.,-1.,1.]) @ self.affinematrix_projection()
        gl.glMultMatrixd( mp.transpose() )
        #
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.glMultMatrixd( self.affinematrix_modelview().transpose() )
