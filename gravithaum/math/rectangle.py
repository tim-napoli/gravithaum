import math
from vector import vector

class rectangle:

    def __init__(self, tl, br):
        self.tl = tl
        self.br = br
        assert tl.x <= br.x, self.__str__()
        assert tl.y >= br.y, self.__str__()

    def __str__(self):
        return "({0}, {1})".format(self.tl, self.br)

    def translate(self, v):
        """
        >>> b = rectangle(vector(0, 1), vector(1, 0))
        >>> b.translate(vector(1,2))
        >>> print b
        ((1, 3), (2, 2))
        """
        self.tl = self.tl + v
        self.br = self.br + v

    def point_in(self, p):
        """
        >>> b = rectangle(vector(0, 1), vector(1, 0))
        >>> b.point_in(vector(0.5, 0.5))
        True
        """
        return (    p.x >= self.tl.x
                and p.x <= self.br.x
                and p.y <= self.tl.y
                and p.y >= self.br.y)

    def intersects(self, rectangle):
        """
        >>> b1 = rectangle(vector(0, 2), vector(2, 0))
        >>> b2 = rectangle(vector(1, 3), vector(3, 1))
        >>> b1.intersects(b2)
        True
        """
        return not (    rectangle.tl.x > self.br.x
                    or  rectangle.br.x < self.tl.x
                    or  rectangle.tl.y < self.br.y
                    or  rectangle.br.y > self.tl.y)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
