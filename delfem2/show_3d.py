import numpy
import OpenGL.GL as gl
from delfem2.window_glfw import WindowGLFW
from .delfem2 import glad_load_gl, setup_glsl


def add_aabb3(lhs: numpy.ndarray, rhs: numpy.ndarray):
    assert lhs.shape == rhs.shape == (2, 3)
    if lhs[0, 0] > lhs[1, 0]:
        return rhs
    if rhs[0, 0] > rhs[1, 0]:
        return lhs
    np_cat = numpy.dstack([lhs, rhs])
    return numpy.array([np_cat.min(axis=2)[0], np_cat.max(axis=2)[1]])


def show_3d(list_obj: list,
            winsize=(400, 300),
            bgcolor=(1, 1, 1),
            glsl_vrt="",
            glsl_frg="",
            camera_rotation=(0.0, 0.0, 0.0),
            camera_scale=1.0,
            nframe=-1):
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
    #### glsl compile
    id_shader_program = 0
    if glsl_vrt != "" and glsl_frg != "":
        glad_load_gl()
        id_shader_program = setup_glsl(glsl_vrt, glsl_frg)
    #### adjust scale
    aabb3 = numpy.array([[+1., +1., +1.], [-1., -1, -1.]])
    for obj in list_obj:
        if hasattr(obj, 'minmax_xyz'):
            aabb3 = add_aabb3(aabb3, obj.minmax_xyz())
    if aabb3[0, 0] > aabb3[1, 0]:
        aabb3 = numpy.array([[-1., -1., -1.], [+1., +1., +1.]])
    window.wm.camera.adjust_scale_trans(aabb3)
    window.wm.camera.scale = camera_scale
    ## set camera rotation
    if len(camera_rotation) == 3:
        window.wm.camera.set_rotation(camera_rotation)
    ## initalizing opengl
    gl.glEnable(gl.GL_POLYGON_OFFSET_FILL)
    gl.glPolygonOffset(1.1, 4.0)
    gl.glUseProgram(id_shader_program)
    ## enter loop
    window.draw_loop(nframe=nframe)
