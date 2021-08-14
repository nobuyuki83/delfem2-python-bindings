import OpenGL.GL as gl
import numpy
from .delfem2 import *


class DrawerMesh():
    def __init__(self,
                 np_pos=numpy.ndarray((0, 3), dtype=numpy.float64),
                 np_elm=numpy.ndarray((0, 3), dtype=numpy.uint32),
                 elem_type=TRI):
        assert type(np_pos) == numpy.ndarray
        assert type(np_elm) == numpy.ndarray
        assert np_pos.dtype == numpy.float64
        assert np_elm.dtype == numpy.uint32
        assert np_elm.shape[1] == num_node_elem(elem_type)
        self.np_pos = np_pos
        self.np_elm = np_elm
        self.elem_type = elem_type
        self.is_draw_face = False
        self.is_draw_edge = True

    def minmax_xyz(self):
        if self.np_pos.shape[0] == 0:
            return [1, -1, 0, 0, 0, 0]
        x_min = numpy.min(self.np_pos[:, 0])
        x_max = numpy.max(self.np_pos[:, 0])
        y_min = numpy.min(self.np_pos[:, 1])
        y_max = numpy.max(self.np_pos[:, 1])
        if self.np_pos.shape[1] >= 3:
            z_min = numpy.min(self.np_pos[:, 2])
            z_max = numpy.max(self.np_pos[:, 2])
        else:
            z_min = 0.0
            z_max = 0.0
        return numpy.array([[x_min, y_min, z_min], [x_max, y_max, z_max]])

    def draw(self):
        if self.is_draw_face:
            gl.glColor4d(self.color_face[0], self.color_face[1], self.color_face[2], self.color_face[3])
            gl.glMaterialfv(gl.GL_FRONT_AND_BACK, gl.GL_DIFFUSE, self.color_face)
            draw_mesh_facenorm(self.np_pos, self.np_elm, self.elem_type)

        if self.is_draw_edge:
            gl.glDisable(gl.GL_LIGHTING)
            gl.glLineWidth(1)
            gl.glColor3d(0, 0, 0)
            draw_meshtri3_edge(self.np_pos, self.np_elm)
