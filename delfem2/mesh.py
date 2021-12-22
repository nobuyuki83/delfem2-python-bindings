import numpy

# no dependency
from .delfem2 import \
    read_uniform_mesh, \
    write_uniform_mesh
from .delfem2 import TRI

# opengl
from .delfem2 import draw_meshtri3_edge


def concat(list_VE: list):
    if len(list_VE) == 0:
        return
    assert len(list_VE[0]) == 2
    V = list_VE[0][0]
    E = list_VE[0][1]
    for il in range(1, len(list_VE)):
        i0 = V.shape[0]
        V = numpy.concatenate([V, list_VE[il][0]], axis=0)
        E = numpy.concatenate([E, list_VE[il][1]+i0], axis=0)
    return V, E
