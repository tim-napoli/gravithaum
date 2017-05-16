import OpenGL.GL as gl
import glfw
import pickle
import sys
import getopt
import os.path
import copy

import gravithaum.engine.video as video
import gravithaum.engine.keyboard as keyb
import gravithaum.engine.mouse as mouse
from gravithaum.math.vector import vector as vector
from gravithaum.physic.point import point as point
from gravithaum.game.atom import atom as atom
from gravithaum.game.molecule import molecule
from gravithaum.game.universe import universe as universe
from gravithaum.game.universe import generate_random_universe
from gravithaum.game.universe import load_universe_from_file
from gravithaum.renderer.camera import camera as camera
import gravithaum.renderer.renderer as renderer

class attractor_putter:

    NOTHING = 0
    CREATION = 1

    def __init__(self, universe, cam):
        self.universe = universe
        self.cam = cam
        self.state = attractor_putter.NOTHING

    def update(self):
        if (self.state == attractor_putter.NOTHING):
            if (mouse.bleft):
                self.attr = point(vector(mouse.x + self.cam.pos.x,
                                         mouse.y + self.cam.pos.y),
                                  vector(0, 0),
                                  1.0)
                self.state = attractor_putter.CREATION
                self.universe.attractors.append(self.attr)
            elif (mouse.bright):
                self.universe.remove_attractor_at(vector(mouse.x + self.cam.pos.x,
                                                         mouse.y + self.cam.pos.y))
                self.universe.grid.refresh()

        elif self.state == attractor_putter.CREATION:
            if (not mouse.bleft):
                self.state = attractor_putter.NOTHING
                self.universe.grid.refresh()
            else:
                dist = ((vector(mouse.x, mouse.y) + self.cam.pos) - self.attr.pos).length()
                if dist > 64:
                    dist = 64
                if (dist > 0):
                    self.attr.weight = dist

class molecule_putter:

    NOTHING = 0
    CREATION = 1
    LINKING = 2

    def __init__(self, universe, cam):
        self.universe = universe
        self.cam = cam
        self.state = molecule_putter.NOTHING
        self.to_link = None


    def update(self):
        if (self.state == molecule_putter.NOTHING):
            if (mouse.bleft):
                mol = self.universe.get_molecules_at(
                        vector(mouse.x + self.cam.pos.x,mouse.y + self.cam.pos.y)
                       )
                if mol != None:
                    self.state = self.LINKING
                    self.to_link = mol

                else:
                    self.attr = molecule(
                        atom(
                            vector(mouse.x + self.cam.pos.x,
                                   mouse.y + self.cam.pos.y),
                            vector(0, 0),
                            1,
                            1)
                        )
                    self.state = self.CREATION
                    self.universe.molecules.append(self.attr)
            elif (mouse.bright):
                self.universe.remove_molecule_at(
                    vector(mouse.x + self.cam.pos.x,mouse.y + self.cam.pos.y))

        elif self.state == self.CREATION:
            if (not mouse.bleft):
                self.state = self.NOTHING
            else:
                dist = ((vector(mouse.x, mouse.y) + self.cam.pos) - self.attr.pos).length()
                if dist > 50:
                    dist = 50
                if (dist >= 5):
                    self.attr.change_weight(int(dist / 5))

        elif self.state == self.LINKING:
            if (not mouse.bleft):
                mol = self.universe.get_molecules_at(
                        vector(mouse.x + self.cam.pos.x,mouse.y + self.cam.pos.y)
                       )
                if mol != None and mol != self.to_link and not mol.contains(self.to_link):
                    self.to_link.fusion(mol)


                self.state = self.NOTHING
                self.to_link = None

            else:
                gl.glColor3ub(64, 32, 196)
                gl.glBegin(gl.GL_LINES)
                gl.glVertex2f(float(self.to_link.atom.pos.x), float(self.to_link.atom.pos.y))
                gl.glVertex2f(float(mouse.x), float(mouse.y))
                gl.glEnd()

class backup:

    def __init__(self, save, putter):
        self.backup = copy.deepcopy(save)
        self.live = save
        self.putter = putter

    def restaure(self):
        self.live = copy.deepcopy(self.backup)
        self.putter.universe = self.live

_paused = False
_target_molecule = False

def switch_pause():
    global _paused
    _paused = not _paused

def switch_target(putter, univ_mol, univ_tar):
    global _target_molecule
    _target_molecule = not _target_molecule
    if _target_molecule:
        putter.universe = univ_tar
        print "Target"
    else:
        putter.universe = univ_mol
        print "Molecules"

current_univ = 1

def main(editor, filePath):
    global current_univ
    global univ_instance

    # Initialize the library
    if not glfw.init():
        return

    # Engine initialisation
    mode = {
        "width": 1024,
        "height": 768,
        "virtual_width": 1280,
        "virtual_height": 720
    }
    flags = {
        "fullscreen": False
    }
    video.start(mode, flags)
    keyb.start(video)
    mouse.start()

    # Camera
    cam = camera(vector(-640, -360), 1.0)

    # Universe
    if filePath != None and os.path.isfile(filePath):
        univ = backup(load_universe_from_file(filePath), None)
    elif editor == True:
        univ = backup(universe(), None)
    else:
        univ = backup(load_universe_from_file("levels/" + str(current_univ)), None)

    # Assets
    # load_assets()

    # Keyboard binds
    keyb.add_bind_on_release(glfw.KEY_ESCAPE,
                  lambda win : glfw.set_window_should_close(win, 1),
                  [video._window])
    keyb.add_bind(glfw.KEY_UP,
                  lambda cam : cam.add_force(vector(0, 2)),
                  [cam])
    keyb.add_bind(glfw.KEY_DOWN,
                  lambda cam : cam.add_force(vector(0, -2)),
                  [cam])
    keyb.add_bind(glfw.KEY_LEFT,
                  lambda cam : cam.add_force(vector(-2, 0)),
                  [cam])
    keyb.add_bind(glfw.KEY_RIGHT,
                  lambda cam : cam.add_force(vector(2, 0)),
                  [cam])
    keyb.add_bind_on_press(glfw.KEY_SPACE,
                  lambda: switch_pause(),
                  [])
    keyb.add_bind_on_release(glfw.KEY_R,
                  lambda b: b.restaure(),
                  [univ])

    # Loop until the user closes the window
    if not editor:
        game_loop(keyb, univ, cam, renderer, video)
    else:
        editor_loop(keyb, univ, cam, renderer, video)




def game_loop(keyb, univ, cam, renderer, video):
    global current_univ

    putter = attractor_putter(univ.live, cam)
    univ.putter = putter

    while not glfw.window_should_close(video._window):
        keyb.update()

        putter.update()

        if not _paused:
            univ.live.update()
            if univ.live.is_win() or keyb._keys[glfw.KEY_X]:
                print "Won !"
                current_univ += 1
                univ = backup(load_universe_from_file("levels/" + str(current_univ)), putter)
                putter.universe = univ.live
                keyb.add_bind_on_release(glfw.KEY_R,
                                         lambda b: b.restaure(),
                                         [univ])

        gl.glLoadIdentity()
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        cam.update()
        cam.use()

        renderer.render(cam, univ.live)

        # Swap front and back buffers
        video.flip()

        # Poll for and process events
        glfw.poll_events()

    glfw.terminate()

def editor_loop(keyb, univ, cam, renderer, video):

    putter = molecule_putter(univ.live, cam)
    univ.putter = putter

    univ_target = universe()

    if univ.live.goal != None:
        univ_target.molecules.append(univ.live.goal)

    # Editor keyboard binds
    keyb.add_bind(glfw.KEY_C,
              lambda univ: univ.clear(),
              [univ.live])
    keyb.add_bind(glfw.KEY_C,
              lambda univ: univ.clear(),
              [univ_target])

    keyb.add_bind_on_release(glfw.KEY_TAB,
              lambda put, uni_mol, uni_tar: switch_target(put, uni_mol, uni_tar),
              [putter, univ.live, univ_target])


    while not glfw.window_should_close(video._window):
        gl.glLoadIdentity()
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        keyb.update()

        putter.update()


        cam.update()
        cam.use()

        if not _target_molecule:
            renderer.render(cam, univ.live)
        else:
            renderer.render(cam, univ_target)

        # Swap front and back buffers
        video.flip()

        # Poll for and process events
        glfw.poll_events()

    glfw.terminate()

    univ.live.goal = univ_target.molecules[0].get_root()

    try:
        univ.live.save_to_file(filePath)
    except Exception as e:
        print "Impossible de sauvegarder le fichier {}".format(filePath)



if __name__ == "__main__":
    filePath = None
    editor = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hf:e", ["help","file=","editor"])
    except getopt.GetoptError:
        print "gravithaum.py [-f saveFile] [-e]"
        sys.exit(0)

    for opt, arg in opts:
        if opt == "--editor" or opt == "-e":
            editor = True

        elif opt == "--file" or opt == "-f":
            filePath = arg

        else:
            print "gravithaum.py [-f saveFile] [-e]"
            sys.exit(0)

    if editor == True and filePath == None:
        print "Aucun nom de fichier fourni."
        sys.exit(0)

    main(editor, filePath)
