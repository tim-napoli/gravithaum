import OpenGL.GL as gl
import glfw

_window = None
_mode = None
_flags = None

_top_left = (0, 0)
_ratio = 1.0

def compute_viewport():
    global _mode
    global _window
    global _top_left
    global _ratio

    (ww, wh) = glfw.get_framebuffer_size(_window)

    # size = vsize * ratio
    xratio = ww / float(_mode["virtual_width"])
    yratio = wh / float(_mode["virtual_height"])

    if xratio * _mode["virtual_height"] > wh:
        # use yratio
        ratio = yratio
    else:
        # use xratio
        ratio = xratio

    tw = ratio * _mode["virtual_width"]
    th = ratio * _mode["virtual_height"]
    t = (wh - th) / 2
    l = (ww - tw) / 2

    gl.glViewport(int(l), int(t), int(tw), int(th))

    _top_left = (t, l)
    _ratio = ratio

def resize(window, w, h):
    global _mode

    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    compute_viewport()
    gl.glOrtho(0,
            _mode["virtual_width"], 0,
            _mode["virtual_height"], 0,
            1)
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadIdentity()

def start(mode, flags):
    global _window
    global _mode
    global _flags

    monitor = None
    if (flags["fullscreen"]):
        monitor = glfw.get_primary_monitor()

    _mode = mode
    _flags = flags

    _window = glfw.create_window(mode["width"], mode["height"],
                                 "Gravithaum", monitor, None)
    if not _window:
        glfw.terminate()
        raise "couldn't create window"

    glfw.make_context_current(_window)
    glfw.swap_interval(1)

    resize(_window, mode["width"], mode["height"])
    glfw.set_framebuffer_size_callback(_window, resize)

    gl.glEnable(gl.GL_POINT_SMOOTH)
  
def flip():
    global _window

    glfw.swap_buffers(_window)

def close():
    global _window

    if _window:
        glfw.destroy_window(_window)

def get_virtual_coord(x, y):
    """ Return the virtual coordinates of a point given in system coordinates.
    """
    global _top_left
    global _ratio

    (t, l) = _top_left
    gx = (x - l) * (1.0 / _ratio)
    gy = 720 - (y - t) * (1.0 / _ratio)

    return (gx, gy)
