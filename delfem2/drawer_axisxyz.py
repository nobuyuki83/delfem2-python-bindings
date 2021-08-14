import numpy
import OpenGL.GL as gl

class AxisXYZ():
    def __init__(self, size=1.0, pos=(0.0,0.0,0.0), line_width=1):
        self.size = size
        self.pos = pos
        self.line_width=line_width

    def draw(self):
        gl.glDisable(gl.GL_LIGHTING)
        gl.glLineWidth(self.line_width)
        gl.glTranslated(+self.pos[0],+self.pos[1],+self.pos[2])
        ####
        gl.glBegin(gl.GL_LINES)
        gl.glColor3d(1,0,0)
        gl.glVertex3d(0,0,0)
        gl.glVertex3d(self.size,0,0)
        ####
        gl.glColor3d(0,1,0)
        gl.glVertex3d(0,0,0)
        gl.glVertex3d(0,self.size,0)
        ####
        gl.glColor3d(0,0,1)
        gl.glVertex3d(0,0,0)
        gl.glVertex3d(0,0,self.size)
        gl.glEnd()
        ####
        gl.glTranslated(-self.pos[0],-self.pos[1],-self.pos[2])

    def minmax_xyz(self):
        return numpy.array(
            [[0,0,0],
             [self.size,self.size,self.size]])