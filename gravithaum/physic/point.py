from gravithaum.math.vector import vector as vector

G = 0.001

class point(object):

    def __init__(self, pos, speed, weight):
        assert weight > 0
        self.pos = pos
        self.speed = speed
        self.weight = weight

    def translate(self, v):
        self.pos = self.pos + v

    def add_force(self, f):
        self.speed = self.speed + f

    def update(self):
        self.pos = self.pos + self.speed

    def attracts(self, other):
        pdist = (self.pos - other.pos).square_length()
        other.add_force((self.pos - other.pos) \
                        * (G * (self.weight * other.weight) / pdist))

