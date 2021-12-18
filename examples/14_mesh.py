import os, sys, math
import numpy

sys.path.append(os.path.join(
    os.path.dirname(__file__), '..'))
import delfem2.mesh
from delfem2.delfem2 import AlembicOPolyMesh

if __name__ == "__main__":
    V, F = delfem2.mesh.read_uniform_mesh(
        os.path.join(os.path.dirname(__file__), "asset", "bunny_1k.obj"))

    abc_opolymesh = AlembicOPolyMesh("bunny.abc", 0.03)
    abc_opolymesh.set_mesh(V, F)

    delfem2.mesh.write_uniform_mesh("hoge.obj", V, F)

    V = numpy.array([
        [0, 0, 0],
        [1, 1, 1],
        [1, 1, 2]])

    F = numpy.array([
        [0, 1],
        [1, 2]])

    print(V, type(V))
    print(F, type(F))
    delfem2.mesh.write_uniform_mesh("edge.obj", V, F)
