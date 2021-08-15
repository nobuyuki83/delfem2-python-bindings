####################################################################
# Copyright (c) 2019 Nobuyuki Umetani                              #
#                                                                  #
# This source code is licensed under the MIT license found in the  #
# LICENSE file in the root directory of this source tree.          #
####################################################################

import math, numpy
import quaternion
import OpenGL.GL as gl

from enum import Enum


def motion_rot(
        scrnx1, scrny1,
        scrnx0, scrny0,
        quat, trans):
    assert len(trans) == 2
    assert isinstance(quat, numpy.quaternion)
    dx = scrnx1 - scrnx0
    dy = scrny1 - scrny0
    a = math.sqrt(dx * dx + dy * dy)
    if a > 1.0e-3:
        dq = numpy.quaternion(
            math.cos(a * 0.5),
            +dy * math.sin(a * 0.5) / a,
            -dx * math.sin(a * 0.5) / a,
            0.0)
    else:
        dq = numpy.quaternion(1, -dy, dx, 0.0)
    if a != 0.0:
        quat = quat * dq
    return quat, trans


def motion_trans(scrnx1, scrny1,
                 scrnx0, scrny0,
                 quat, trans, view_height,
                 scale: float):
    assert len(trans) == 2
    assert isinstance(quat, numpy.quaternion)
    dx = scrnx1 - scrnx0
    dy = scrny1 - scrny0
    trans[0] += dx * view_height * 0.5 / scale
    trans[1] += dy * view_height * 0.5 / scale
    return quat, trans


class CAMERA_ROT_MODE(Enum):
    YTOP = 1
    ZTOP = 2
    TBALL = 3


class Camera:
    def __init__(self, view_height=1.0):
        self.view_height = view_height
        self.scale = 1.0
        self.scr_trans = [0., 0.]  # position of the pivot in the screen
        self.pivot = [0., 0., 0.]  # pivot location
        self.quat = numpy.quaternion(1, 0, 0, 0)
        self.camera_rot_mode = CAMERA_ROT_MODE.TBALL
        self.fovy = 60  # degree
        self.theta = 0.0
        self.psi = 0.0

    def set_gl_camera(self):
        viewport = gl.glGetIntegerv(gl.GL_VIEWPORT)
        win_w = viewport[2]
        win_h = viewport[3]
        depth = self.view_height / (self.scale * math.tan(0.5 * self.fovy * 3.1415 / 180.0))
        asp = float(win_w) / win_h
        ####
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(-self.view_height / self.scale * asp,
                   +self.view_height / self.scale * asp,
                   -self.view_height / self.scale,
                   +self.view_height / self.scale,
                   -depth * 10,
                   +depth * 10)

        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.glTranslated(self.scr_trans[0], self.scr_trans[1], -depth)
        gl.glMultMatrixf(self.affine_matrix())
        gl.glTranslated(self.pivot[0], self.pivot[1], self.pivot[2])

    def affine_matrix(self) -> numpy.ndarray:
        if self.camera_rot_mode == CAMERA_ROT_MODE.TBALL:
            mR3 = quaternion.as_rotation_matrix(self.quat)
            mMV = numpy.zeros([4, 4], dtype=numpy.float64)
            mMV[:3, :3] = mR3[:, :]
            mMV[3, 3] = 1.
        elif self.camera_rot_mode == CAMERA_ROT_MODE.YTOP:
            x = math.sin(self.theta) * math.cos(self.psi)
            z = math.cos(self.theta) * math.cos(self.psi)
            y = math.sin(self.psi)
            ey = numpy.array([x, y, z])
            up = numpy.array([0, 1, 0])
            up = up - ey * numpy.dot(ey, up)
            up /= numpy.linalg.norm(up)
            vx = numpy.cross(up, ey).normalize()  # v3_normalize(v3_cross(up, ey))
            mMV = [vx[0], up[0], ey[0], 0,
                   vx[1], up[1], ey[1], 0,
                   vx[2], up[2], ey[2], 0,
                   0, 0, 0, 1]
            mMV = numpy.array(mMV)
        return mMV

    def rotation(self, sx1, sy1, sx0, sy0):
        if self.camera_rot_mode == CAMERA_ROT_MODE.TBALL:
            self.quat, self.trans = motion_rot(
                sx1, sy1, sx0, sy0,
                self.quat, self.scr_trans)
        elif self.camera_rot_mode == CAMERA_ROT_MODE.YTOP:
            self.theta -= sx1 - sx0
            self.psi -= sy1 - sy0
            self.psi = min(max(-math.pi * 0.499, self.psi), math.pi * 0.499)
        return

    def translation(self, sx1, sy1, sx0, sy0):
        self.quat, self.trans = motion_trans(
            sx1, sy1, sx0, sy0, self.quat,
            self.scr_trans, self.view_height,
            self.scale)
        return

    def adjust_scale_trans(self, aPos: numpy.ndarray):
        assert (aPos.shape == (2, 3))
        (win_w, win_h) = gl.glGetIntegerv(gl.GL_VIEWPORT)[2:]
        asp = float(win_w) / win_h
        vh1 = (aPos[1, 0] - aPos[0, 0]) / asp
        vh0 = (aPos[1, 1] - aPos[1, 0])
        self.pivot[0] = -0.5 * (aPos[0, 0] + aPos[1, 0])
        self.pivot[1] = -0.5 * (aPos[0, 1] + aPos[1, 1])
        self.pivot[2] = -0.5 * (aPos[0, 2] + aPos[1, 2])
        self.scr_trans[0] = 0.0
        self.scr_trans[1] = 0.0
        self.view_height = max(vh0, vh1)
        self.scale = 1.0

    def set_rotation(self, rot: numpy.ndarray):
        self.quat = quaternion.from_rotation_vector(rot)

    '''
    def adjust_scale_trans(self, aPos):
      minmax_x = minMaxLoc(aPos, [1., 0., 0.])
      minmax_y = minMaxLoc(aPos, [0., 1., 0.])
      minmax_z = minMaxLoc(aPos, [0., 0., 1.])
      (win_w,win_h) = gl.glGetIntegerv(gl.GL_VIEWPORT)[2:]
      asp = float(win_w) / win_h
      vh1 = (minmax_x[1]-minmax_x[0])/asp
      vh0 = (minmax_y[1]-minmax_y[0])
      self.pivot[0] = -0.5*(minmax_x[0]+minmax_x[1])
      self.pivot[1] = -0.5*(minmax_y[0]+minmax_y[1])
      self.pivot[2] = -0.5*(minmax_z[0]+minmax_z[1])
      self.scr_trans[0] = 0.0
      self.scr_trans[1] = 0.0
      self.view_height = max(vh0,vh1)
      self.scale = 1.0
    '''
