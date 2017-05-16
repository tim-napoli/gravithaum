import OpenGL.GL as gl

from gravithaum.physic.point import point as point
from gravithaum.math.rectangle import rectangle as rectangle
from gravithaum.math.vector import vector as vector
from gravithaum.physic.point import point as point

class camera(point):

    def __init__(self, pos = vector(0, 0), zoom = 1.0):
        point.__init__(self, pos, vector(0, 0), 1)
        self.zoom = zoom

    def zoom(self, z):
        self.zoom = 1.0 # self.zoom + z 

    def get_viewfield(self):
        """ Get real coordinates of the view field
        """
        return rectangle(self.pos + vector(0, 720), self.pos + vector(1280, 0))

    def decelerate(self):
        self.speed = self.speed * 0.9

    def update(self):
        point.update(self)
        self.decelerate()

    def use(self):
        """ OpenGL transformation handling.
        """
        gl.glTranslatef(float(-self.pos.x), float(-self.pos.y), 0.0)
        # TODO zoom
