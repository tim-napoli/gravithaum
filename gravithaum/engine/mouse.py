import glfw

import gravithaum.engine.video as video

x = 0
y = 0
bleft = False
bright = False
bmiddle = False

def on_mouse_action(window, button, action, mods):
    global bleft
    global bright
    global bmiddle

    if button == glfw.MOUSE_BUTTON_LEFT:
        bleft = True if action == glfw.PRESS else False
    elif button == glfw.MOUSE_BUTTON_RIGHT:
        bright = True if action == glfw.PRESS else False
    elif button == glfw.MOUSE_BUTTON_MIDDLE:
        bmiddle = True if action == glfw.PRESS else False

def on_mouse_move(window, _x, _y):
    global x
    global y

    (x, y) = video.get_virtual_coord(_x, _y)

def start():
    glfw.set_mouse_button_callback(video._window, on_mouse_action)
    glfw.set_cursor_pos_callback(video._window, on_mouse_move)
