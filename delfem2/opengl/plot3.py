import numpy
import OpenGL.GL as gl
from delfem2.opengl.window_glfw import WindowGLFW
from delfem2.opengl.delfem2 import glad_load_gl

def _add_aabb3(
        lhs: list,
        rhs: list) -> list:
    """
    internal function to compute the axis-aligned bounding box (AABB) of two AABBs
    :param lhs: AABB
    :param rhs: AABB
    :return: AABB that include lhs and rhs
    """
    assert len(lhs) == len(rhs) == 6
    if lhs[0] > lhs[1]:
        return rhs
    if rhs[0] > rhs[1]:
        return lhs
    np_cat = numpy.array([lhs, rhs]).transpose()
    return [np_cat[0].min(), np_cat[1].min(), np_cat[2].min(),
            np_cat[3].max(), np_cat[4].max(), np_cat[5].max()]


def plot3(list_obj: list,
          winsize=(400, 300),
          bgcolor=(1, 1, 1),
          glsl_vrt="",
          glsl_frg="",
          camera_rotation=(0.0, 0.0, 0.0),
          camera_scale=1.0,
          duration=-1):
    """
    draw the input object into openGL window

    obj -- the object to draw.
      this object need to have a method "draw()"

    winsize -- the size of the window (width,height)
    """

    #### initialize window
    window = WindowGLFW(winsize=winsize)
    if not window.is_valid:
        print("aborting opening window..")
        return
    glad_load_gl()
    window.color_bg = bgcolor
    for obj in list_obj:
        if hasattr(obj, 'init_gl'):
            obj.init_gl()
        if hasattr(obj, 'mouse'):
            window.list_func_mouse.append(obj.mouse)
        if hasattr(obj, 'motion'):
            window.list_func_motion.append(obj.motion)
        if hasattr(obj, "draw"):
            window.list_func_draw.append(obj.draw)
        if hasattr(obj, "step_time"):
            window.list_func_step_time.append(obj.step_time)
        if hasattr(obj, "key"):
            window.list_func_key.append(obj.key)
    #### adjust scale
    aabb3 = [+1., 0., 0., -1., 0., 0.]
    for obj in list_obj:
        if hasattr(obj, 'minmax_xyz'):
            aabb3 = _add_aabb3(aabb3, obj.minmax_xyz())
    if aabb3[0] > aabb3[3]:
        aabb3 = [-1., -1., -1., +1., +1., +1.]
    window.camera.adjust_scale_trans(aabb3)
    window.camera.scale = camera_scale
    ## set camera rotation
    if len(camera_rotation) == 3:
        window.camera.set_rotation(camera_rotation)
    ## initalizing opengl
    gl.glEnable(gl.GL_POLYGON_OFFSET_FILL)
    gl.glPolygonOffset(1.1, 4.0)
    ## enter loop
    window.draw_loop(duration=duration)
