import random as r
import math

from gravithaum.physic.point    import point as pt
from gravithaum.math.vector     import vector as vect
from gravithaum.math.rectangle  import rectangle as rect

DIAGONALE = 0.66

class atom(pt):

    def __init__(self, position, velocity, weight, load):
        pt.__init__(self, position, velocity, weight)
        self.radius = weight * 5
        self.load = load


    def __str__(self):
        return "({0}, {1}, {2})".format(self.position, self.velocity, self.weight)


    def get_bounding_box(self):
        """ Atom bounding box
        >>> a = atom(vect(0,0), vect(0,0), 2, 0)
        >>> print a.get_bounding_box()
        ((-1.0, 1.0), (1.0, -1.0))
        """
        return rect(self.pos - vect(self.radius, -self.radius) * DIAGONALE,
                    self.pos + vect(self.radius, -self.radius) * DIAGONALE)


def random_atom():
    return atom(vect(r.randrange(-1280, 1280),
                     r.randrange(-720,  720)),
                     vect(0,0),
                     r.randrange(1,10),
                     1)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
