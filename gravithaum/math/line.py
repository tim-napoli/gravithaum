import math
from vector import vector
from interval import interval as interval

class line:

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def intersection(self, l):
        """ Compute the intersection of two lines.
            This function could return `None` if two lines do not intersect,
            a vector if they are intersecting at a point, or a line if they
            are intersecting on a line.
            see http://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
            for more details.
        >>> l1 = line(vector(0, 0), vector(10, 10))
        >>> l2 = line(vector(0, 10), vector(10, 0))
        >>> l3 = line(vector(0, 20), vector(20, 20))
        >>> l4 = line(vector(5, 5), vector(15, 15))
        >>> l4 = line(vector(15, 15), vector(20, 20))
        >>> l1.intersection(l2) == vector(5.0, 5.0)
        True
        >>> l1.intersection(l3) == None
        True
        >>> l1.intersection(l4) == line(vector(5, 5), vector(10, 10))
        True
        >>> l4.intersection(l1) == line(vector(10, 10), vector(5, 5))
        True
        """
        p = self.a
        r = self.b - p
        q = l.a
        s = l.b - q

        if (r ^ s) == 0 and ((q - p) ^ r) == 0:
            # Two lines are colinears
            t0 = (q.sub(p)).dot(r.div(r.dot(r)))
            t1 = t0 + s.dot(r.div(r.dot(r)))

            if (s ** r < 0):
                if interval.interval(t1, t0).intersects(interval.interval(0, 1)):
                    return line(p + r * max(0, t1), p + r * min(t0, 1))
            else:
                if interval(t0, t1).intersects(interval(0, 1)):
                    return line(p + r * max(0, t0), p + r * min(t1, 1))
            return None
        elif (r ^ s) == 0 and ((q - p) ^ r) != 0:
            # Colinears and non-intersecting
            return None
        elif (r ^ s) != 0:
            # Maybe crossing
            t = (q - p) ^ (s.div(r ^ s))
            u = (q - p) ^ (r.div(r ^ s))
            if 0 <= t and t <= 1 and 0 <= u and u <= 1:
                return p + r * t
            else:
                return None
        return None


    def __eq__(self, other):
        return self.a == other.a and self.b == other.b

if __name__ == "__main__":
    import doctest
    doctest.testmod()
