import glfw

import gravithaum.engine.video as video

_keys = [False] * glfw.KEY_LAST
_binds = []
_binds_press = {}
_binds_release = {}

class bind:

    def __init__(self, key, func, data_list):
        self.key = key
        self.func = func
        self.data_list = data_list

    def execute(self):
        self.func(*self.data_list)


def on_key(window, key, scancode, action, mods):
    global _keys
    global _binds_press
    global _binds_release

    if action == glfw.PRESS:
        _keys[key] = True
        if key in _binds_press:
            for b in _binds_press[key]:
                b.execute()
    elif action == glfw.RELEASE:
        _keys[key] = False
        if key in _binds_release:
            for b in _binds_release[key]:
                b.execute()

def add_bind(key, func, data_list):
    global _binds

    _binds.append(bind(key, func, data_list))

def add_bind_on_press(key, func, data_list):
    global _binds_press

    if key in _binds_press:
        _binds_press[key].append(bind(key, func, data_list))
    else:
        _binds_press[key] = [bind(key, func, data_list)]

def add_bind_on_release(key, func, data_list):
    global _binds_release
    _binds_release[key] = [bind(key, func, data_list)]
        
def start(video):
    global _keys
    global _binds

    _keys = [False] * glfw.KEY_LAST
    _binds = []
    glfw.set_key_callback(video._window, on_key)

def update():
    global _keys
    global _binds

    for b in _binds:
        if _keys[b.key]:
            b.execute()
