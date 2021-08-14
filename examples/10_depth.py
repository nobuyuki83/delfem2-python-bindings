####################################################################
# Copyright (c) 2019 Nobuyuki Umetani                              #
#                                                                  #
# This source code is licensed under the MIT license found in the  #
# LICENSE file in the root directory of this source tree.          #
####################################################################

import os
import numpy
import OpenGL.GL as gl
from PIL import Image

import delfem2 as dfm2
import delfem2.framebuffer_glfw

def main():
  V, F = dfm2.read_triangle_mesh(os.path.join(os.getcwd(), "asset", "bunny_1k.obj"))
  V *= 0.02

  sampler = dfm2.Render2Tex()
  sampler.set_texture_property(size_res_width=256,size_res_height=256, is_rgba_8ui=True)

  with dfm2.framebuffer_glfw.FrameBufferGLFW([512, 512], format_color="4byte", is_depth=True):
    dfm2.gladLoadGL()
    gl.glEnable(gl.GL_TEXTURE_2D)
    gl.glActiveTexture(gl.GL_TEXTURE0)
    sampler.init_gl()
    sampler.start()
    gl.glClearColor(1,1,1,1)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    gl.glDisable(gl.GL_LIGHTING)
    gl.glDisable(gl.GL_BLEND)
    gl.glColor3d(0,0,0)
    dfm2.draw_meshtri3_edge(V, F)
    sampler.end()
    numpy_depth = dfm2.render2tex_depth_buffer_numpy(sampler)
    numpy_color = dfm2.render2tex_color_buffer_4byte(sampler)
    print(numpy.min(numpy_depth), numpy.max(numpy_depth))
    pil_image = Image.fromarray(numpy_depth*255)
    pil_image.show()
    pil_image = Image.fromarray(numpy_color)
    pil_image.show()

#  np_depth = numpy.array(dfm2.depth_buffer(sampler),copy=True)
#  print(np_depth.shape)
#  numpy.savetxt("hoge.txt",np_depth)

  #dfm2.gl.glfw.winDraw3d([msh,aabb,axis,sampler])
#  dfm2.gl.glfw.winDraw3d([msh,aabb,axis])

if __name__ == "__main__":
  main()