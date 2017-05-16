# vector class

import math

class vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "({0}, {1})".format(self.x, self.y)

    # Operations
    def add(self, v):
        """ Vector addition
        >>> a = vector(1, 2)
        >>> b = vector(2, 1)
        >>> print a.add(b)
        (3, 3)
        """
        return vector(self.x + v.x, self.y + v.y)

    def sub(self, v):
        """ Vector substraction
        >>> a = vector(1, 1)
        >>> b = vector(1, 5)
        >>> print a.sub(b)
        (0, -4)
        """
        return vector(self.x - v.x, self.y - v.y)

    def mul(self, k):
        """ Vector multiplcation
        >>> a = vector(1, 1)
        >>> print a.mul(5)
        (5, 5)
        """
        return vector(self.x * k, self.y * k)

    def div(self, k):
        """ Vector division
        >>> a = vector(5, 5)
        >>> print a.div(5)
        (1.0, 1.0)
        """
        return vector(self.x / float(k), self.y / float(k))

    def dot(self, v):
        """ Vector dotproduct
        >>> a = vector(5, 5)
        >>> b = vector(2, -1)
        >>> print a.dot(b)
        5
        """
        return self.x * v.x + self.y * v.y

    def crossp(self, v):
        """
        >>> a = vector(2, 3)
        >>> b = vector(5, 7)
        >>> a.crossp(b)
        -1
        """
        return self.x * v.y - self.y * v.x

    def square_length(self):
        """ vector length
        >>> a = vector(1, 1)
        >>> print a.square_length()
        2
        """
        return self.x * self.x + self.y * self.y

    def length(self):
        """ vector length
        >>> a = vector(1, 1)
        >>> print a.length()
        1.41421356237
        """
        return math.sqrt(self.x * self.x + self.y * self.y)

    def normalized(self):
        """ Vector normalization
        >>> a = vector(1, 1)
        >>> b = a.normalized()
        >>> b.length() == 0.9999999999999999
        True
        """
        return vector(self.x / self.length(), self.y / self.length())

    def angle(self, c = None):
        """ angle (radiant) with (1, 0)
        >>> a = vector(0, 1)
        >>> a.angle() == math.pi / 2
        True
        >>> a = vector(5, 6)
        >>> a.angle(vector(5, 5)) == math.pi / 2
        True
        """
        if (c == None):
            c = vector(0, 0)
        return math.atan2(self.y - c.y, self.x - c.x) - math.atan2(0, 1)

    def angle_with(self, v, c = None):
        """ directed angle (radiant) with another vector
        >>> a = vector(0, 1)
        >>> a.angle_with(vector(1, 0)) == 3 * (math.pi / 2)
        True
        >>> a.angle_with(vector(-1, 0)) == math.pi / 2
        True
        """
        angle = v.angle(c) - self.angle(c)
        if (angle < 0):
            angle = angle + 2 * math.pi
        return angle


    # Operators overloading
    def __eq__(self, other):
        """
        >>> vector(0, 0) == vector(0, 0)
        True
        """
        if (other == None):
            return False
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        """
        >>> a = vector(0, 0) + vector(1, 1)
        >>> a == vector(1, 1)
        True
        """
        return self.add(other)

    def __sub__(self, other):
        """
        >>> a = vector(1, 1) - vector(0, 0)
        >>> a == vector(1, 1)
        True
        """
        return self.sub(other)

    def __mul__(self, other):
        """
        >>> a = vector(1, 1) * 3
        >>> a == vector(3, 3)
        True
        """
        return self.mul(other)

    def __truediv__(self, other):
        """
        >>> a = vector(3, 3) / 3
        >>> a == vector(1, 1)
        True
        """
        return self.div(other)

    def __pow__(self, other):
        """
        >>> a = vector(2, 2) ** vector(3, 3)
        >>> a == 12
        True
        """
        return self.dot(other)

    def __xor__(self, other):
        """
        >>> a = vector(2, 3) ^ vector(5, 7)
        >>> a == -1
        True
        """
        return self.crossp(other)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
