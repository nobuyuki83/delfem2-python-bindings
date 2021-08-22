####################################################################
# Copyright (c) 2019 Nobuyuki Umetani                              #
#                                                                  #
# This source code is licensed under the MIT license found in the  #
# LICENSE file in the root directory of this source tree.          #
####################################################################

import os
import numpy
import delfem2 as dfm2
import delfem2.mesh
import delfem2.plot3
import delfem2.drawer_axisxyz
import delfem2.drawer_mesh

V, F = dfm2.mesh.read_triangle_mesh(os.path.join(os.getcwd(), "asset", "bunny_1k.obj"))
V -= numpy.average(V,axis=0)
V /= V.max() - V.min()

axis_xyz = delfem2.drawer_axisxyz.AxisXYZ()
drawer = delfem2.drawer_mesh.DrawerMesh(V,F)

dfm2.plot3.plot3([axis_xyz,drawer], winsize=(400, 300))
