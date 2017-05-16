import OpenGL.GL as gl

from gravithaum.math.vector import vector as vector
from gravithaum.game.atom import atom as atom
from gravithaum.game.forcefield import forcefield as forcefield
from gravithaum.game.molecule import molecule as molecule
from gravithaum.game.universe import universe as universe

atom_colors = [
    (0, 0, 0),
    (192,   0,   0),
    (  0, 192,   0),
    (  0,   0, 192),
    (192, 192,   0),
    (  0, 192, 192),
    (192,   0, 192),
    (192,  86,   0),
    (  0, 192,  86),
    (192,   0,  86),
    ( 86, 192,   0)
]

def render_molecule(molecule):
    gl.glColor3ub(64, 32, 196)
    gl.glBegin(gl.GL_LINES)
    for child in molecule.links:
        other = child.node
        gl.glVertex2f(float(molecule.atom.pos.x), float(molecule.atom.pos.y))
        gl.glVertex2f(float(other.atom.pos.x),    float(other.atom.pos.y))
    gl.glEnd()

    (r, g, b) = atom_colors[molecule.atom.weight]
    gl.glColor3ub(r, g, b)
    gl.glPointSize(float(molecule.atom.radius))
    gl.glBegin(gl.GL_POINTS)
    gl.glVertex2f(float(molecule.atom.pos.x), float(molecule.atom.pos.y))
    gl.glEnd()
    for child in molecule.links:
        render_molecule(child.node)

    #if not molecule.parent:
    #    # Bounding box
    #    gl.glColor3ub(255, 0, 0)
    #    gl.glBegin(gl.GL_LINES)
    #    gl.glVertex2f(molecule.bounding_box.tl.x, molecule.bounding_box.tl.y)
    #    gl.glVertex2f(molecule.bounding_box.br.x, molecule.bounding_box.tl.y)

    #    gl.glVertex2f(molecule.bounding_box.br.x, molecule.bounding_box.tl.y)
    #    gl.glVertex2f(molecule.bounding_box.br.x, molecule.bounding_box.br.y)

    #    gl.glVertex2f(molecule.bounding_box.br.x, molecule.bounding_box.br.y)
    #    gl.glVertex2f(molecule.bounding_box.tl.x, molecule.bounding_box.br.y)

    #    gl.glVertex2f(molecule.bounding_box.tl.x, molecule.bounding_box.br.y)
    #    gl.glVertex2f(molecule.bounding_box.tl.x, molecule.bounding_box.tl.y)
    #    gl.glEnd()

    #    # Gravity centre
    #    gl.glColor3ub(255, 0, 0)
    #    gl.glPointSize(4.0)
    #    gl.glBegin(gl.GL_POINTS)
    #    gl.glVertex2f(molecule.pos.x, molecule.pos.y)
    #    gl.glEnd()

def render_grid(ff):
    gl.glColor3ub(70, 100, 130)
    gl.glPointSize(1)

    gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
    gl.glVertexPointer(2, gl.GL_INT, 0, ff.array.tostring())

    gl.glDrawArrays(gl.GL_POINTS, 0, ff.point_count)
    gl.glDisableClientState(gl.GL_VERTEX_ARRAY)

def render_goal(goal):
    # Compute bounds
    size = vector(goal.bounding_box.br.x - goal.bounding_box.tl.x,
                  goal.bounding_box.tl.y - goal.bounding_box.br.y) * 1.2

    gl.glLoadIdentity()

    gl.glColor3ub(20, 20, 20)
    gl.glBegin(gl.GL_QUADS)
    gl.glVertex2f(1280 - size.x, 720)
    gl.glVertex2f(1280, 720)
    gl.glVertex2f(1280, 720 - size.y)
    gl.glVertex2f(1280 - size.x, 720 - size.y)
    gl.glEnd()

    target = vector(1280, 720) - (size * 0.9)
    diff = target - goal.bounding_box.tl
    goal.translate(diff + vector(0, goal.bounding_box.tl.y - goal.bounding_box.br.y))
    render_molecule(goal)
    goal.translate((diff * -1) + (vector(0, goal.bounding_box.tl.y - goal.bounding_box.br.y) * -1))


def render(cam, universe):
    # Attraction points
    attrs = universe.get_attractors_in(cam.get_viewfield())
    gl.glColor3ub(32, 32, 32)
    for attr in attrs:
        gl.glPointSize(float(attr.weight))
        gl.glBegin(gl.GL_POINTS)
        gl.glVertex2f(float(attr.pos.x), float(attr.pos.y))
        gl.glEnd()

    # Grid
    render_grid(universe.grid)

    # Molecules
    molecules = universe.get_molecules_in(cam.get_viewfield())
    for m in molecules:
        render_molecule(m)

    # Goal
    if universe.goal != None:
        render_goal(universe.goal)

    # fov = cam.get_viewfield()
    # gl.glBegin(gl.GL_QUADS)
    # gl.glTexCoord2f(0.0, 0.0)
    # gl.glVertex2f(fov.tl.x, fov.tl.y)
    # gl.glTexCoord2f(1.0, 0.0)
    # gl.glVertex2f(fov.br.x, fov.tl.y)
    #
    # gl.glTexCoord2f(1.0, 0.0)
    # gl.glVertex2f(fov.br.x, fov.tl.y)
    # gl.glTexCoord2f(1.0, 1.0)
    # gl.glVertex2f(fov.br.x, fov.br.y)
    #
    # gl.glTexCoord2f(1.0, 1.0)
    # gl.glVertex2f(fov.br.x, fov.br.y)
    # gl.glTexCoord2f(0.0, 1.0)
    # gl.glVertex2f(fov.tl.x, fov.br.y)
    #
    # gl.glTexCoord2f(0.0, 1.0)
    # gl.glVertex2f(fov.tl.x, fov.br.y)
    # gl.glTexCoord2f(0.0, 0.0)
    # gl.glVertex2f(fov.tl.x, fov.tl.y)
    # gl.glEnd()
