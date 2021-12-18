import os, sys, math
import numpy

sys.path.append(os.path.join(
    os.path.dirname(__file__), '..'))
import delfem2.mesh
from delfem2.delfem2 import AlembicOPolyMesh

if __name__ == "__main__":
    V, F = delfem2.mesh.read_triangle_mesh(
        os.path.join(os.path.dirname(__file__), "asset", "bunny_1k.obj"))

    mesh = AlembicOPolyMesh(0.03)
