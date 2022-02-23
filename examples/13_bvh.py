import os, sys, math
import numpy

sys.path.append(os.path.join(
    os.path.dirname(__file__), '..'))
import delfem2.mesh
from delfem2.delfem2 import \
    BVH, \
    get_meshtri3_rigbones_octahedron, \
    get_joint_position_history_bvh
from delfem2.alembic.delfem2 import AlembicOPolyMesh


def norm_l2(a, b):
    assert len(a) == len(b)
    sum = 0.
    for i in range(len(a)):
        sum += (a[i] - b[i]) * (a[i] - b[i])
    return math.sqrt(sum)


def main():
    path = os.path.join(os.path.dirname(__file__), "asset", "walk.bvh")
    bvh = BVH()
    bvh.open(path)
    print("nframe", bvh.nframe)
    bvh.set_frame(0)
    bvh.clear_pose()

    for bone in bvh.bones:
        print(bone.name, bone.position(), bone.parent_bone_idx)

    for ch in bvh.channels:
        print(ch.ibone, ch.iaxis, ch.is_rot)

    bb = bvh.minmax_xyz()
    print("skeleton_size", bb)

    abc_opolymesh = AlembicOPolyMesh("hoge.abc", 0.03)
    for iframe in range(bvh.nframe):
        bvh.set_frame(iframe)
        V, F = get_meshtri3_rigbones_octahedron(bvh)
        if iframe == 0:
            abc_opolymesh.set_mesh(V, F)
        else:
            abc_opolymesh.set_vertices(V)

    joint_positions = get_joint_position_history_bvh(bvh)

    V = joint_positions[:, 0, :].copy()
    E = numpy.array([[i, i + 1] for i in range(V.shape[0] - 1)])
    delfem2.mesh.write_uniform_mesh("trajectory_root.obj", V, E)

    list_VE = []
    for ind_j in {0, 5, 11, 18, 23, 32}:
        V = joint_positions[:, ind_j, :].copy()
        E = numpy.array([[i, i + 1] for i in range(joint_positions.shape[0] - 1)])
        list_VE.append( [V,E] )
    V, E = delfem2.mesh.concat(list_VE)
    delfem2.mesh.write_uniform_mesh("trajectories.obj", V, E)




if __name__ == "__main__":
    main()
