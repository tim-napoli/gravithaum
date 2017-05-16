class interval:

    def __init__(self, lbound, rbound):
        assert lbound <= rbound, "lbound must be lower than rbound"
        self.lbound = lbound
        self.rbound = rbound

    def is_in(self, v):
        """
        >>> interval(0, 1).in(0.5)
        True
        >>> interval(0, 1).in(2)
        False
        """
        return v >= self.lbound and v <= self.rbound

    def is_out(self, v):
        """
        >>> interval(0, 1).out(0.5)
        False
        >>> interval(0, 1).out(2)
        True
        """
        return not self.is_in(v)

    def intersects(self, other):
        """
        >>> interval(0, 1).intersects(interval(0.5, 1.5))
        True
        >>> interval(0, 1).intersects(interval(-0.5, 0.5))
        True
        >>> interval(0, 1).intersects(interval(-1, 2))
        True
        >>> interval(0, 1).intersects(interval(2, 3))
        False
        """
        return (    (    other.lbound <= self.lbound
                     and other.rbound >= self.rbound)
                or self.is_in(other.lbound)
                or self.is_in(other.rbound)
               )

if __name__ == "__main__":
    import doctest
    doctest.testmod()
