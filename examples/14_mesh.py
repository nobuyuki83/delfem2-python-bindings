import os, sys
import numpy

sys.path.append(os.path.join(
    os.path.dirname(__file__), '..'))
import delfem2.mesh

def abc(V,F):
    from delfem2.alembic.delfem2 import AlembicOPolyMesh
    abc_opolymesh = AlembicOPolyMesh("bunny.abc", 0.03)
    abc_opolymesh.set_mesh(V, F)

if __name__ == "__main__":
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

    V, F = delfem2.mesh.read_uniform_mesh(
        os.path.join(os.path.dirname(__file__), "asset", "bunny_1k.obj"))

    delfem2.mesh.write_uniform_mesh("hoge.obj", V, F)

    abc(V,F)

