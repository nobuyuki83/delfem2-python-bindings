####################################################################
# Copyright (c) 2019 Nobuyuki Umetani                              #
#                                                                  #
# This source code is licensed under the MIT license found in the  #
# LICENSE file in the root directory of this source tree.          #
####################################################################

import sys, math
import delfem2 as dfm2
import numpy as np
from PIL import Image
from delfem2.drawer_axisxyz import AxisXYZ
from delfem2.plot3 import plot3

def main():
  pil_image_lenna = Image.open("asset/lenna.png")
  np_img = np.array(pil_image_lenna)
  axis = AxisXYZ(100)
  tex = dfm2.get_texture(np_img,"rgb")
  plot3([axis,tex],winsize=(400,300),
          camera_rotation=[math.pi, 0, 0])

if __name__ == "__main__":
  main()