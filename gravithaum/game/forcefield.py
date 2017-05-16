import array

from gravithaum.physic.point    import point as point
from gravithaum.math.vector     import vector as vector
from gravithaum.math.rectangle  import rectangle as rectangle

class forcefield:
    MAX_X = 2000
    MIN_X = -2000
    MAX_Y = 700
    MIN_Y = -700
    STEP_BIG = 100
    STEP_SMALL = 10

    def __init__(self, universe):
        self.universe = universe
        self.array = None
        self.point_count = 0

        self.refresh()

    def refresh(self):
        self.array = array.array('i')
        self.point_count = 0

        for x in xrange(self.MIN_X, self.MAX_X, self.STEP_BIG):
            for y in xrange(self.MIN_Y, self.MAX_Y, self.STEP_SMALL):
                self.update_force(x, y)

        for y in xrange(self.MIN_Y, self.MAX_Y, self.STEP_BIG):
            for x in xrange(self.MIN_X, self.MAX_X, self.STEP_SMALL):
                self.update_force(x, y)

    def update_force(self, x, y):
        p = point(vector(x, y), vector(0,0), 1)

        for a in self.universe.attractors:
            a.attracts(p)

        self.point_count += 1
        self.array.append(int(p.pos.x + 50000 * p.speed.x))
        self.array.append(int(p.pos.y + 50000 * p.speed.y))
