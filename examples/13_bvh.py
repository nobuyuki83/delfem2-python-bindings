import os, sys, math
import numpy
sys.path.append(os.path.join(
    os.path.dirname(__file__), '..'))
import delfem2
from delfem2.delfem2 import BVH

def norm_l2(a,b):
    assert len(a) == len(b)
    sum = 0.
    for i in range(len(a)):
        sum += (a[i]-b[i])*(a[i]-b[i])
    return math.sqrt(sum)

def main():
    path = os.path.join( os.path.dirname(__file__), "asset", "walk.bvh")
    bvh = BVH()
    bvh.open(path)
    print("nframe",bvh.nframe)
    bvh.set_frame(0)
    bvh.clear_pose()

    for bone in bvh.bones:
        print(bone.name, bone.position(), bone.parent_bone_idx)

    for ch in bvh.channels:
        print(ch.ibone, ch.iaxis, ch.is_rot)

    bb = bvh.minmax_xyz()
    print("skeleton_size",bb)

if __name__ == "__main__":
    main()