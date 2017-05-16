import copy

from gravithaum.math.vector import vector as vector
from gravithaum.math.rectangle import rectangle as rectangle
from gravithaum.physic.point import point as point
from gravithaum.game.atom import DIAGONALE
from gravithaum.game.atom import atom as atom


def box_merge(x, y):
    t = max(x.tl.y, y.tl.y)
    l = min(x.tl.x, y.tl.x)
    b = min(x.br.y, y.br.y)
    r = max(x.br.x, y.br.x)
    return rectangle(vector(l, t), vector(r, b))

def compute_barycentre(centres, weights):
    assert len(centres) == len(weights)
    centre = vector(0, 0)
    weight = 0
    for i in range(0, len(centres)):
        centre = centre + (centres[i] * weights[i])
        weight += weights[i]
    return centre.div(weight)

class link:

    def __init__(self, angle, node):
        self.angle = angle
        self.node = node


class molecule(point):

    def __init__(self, atom):
        point.__init__(self, copy.copy(atom.pos), copy.copy(atom.speed),
                       atom.weight)
        self.atom = atom
        self.links = []
        self.empty_load = self.atom.load
        self.bounding_box = self.atom.get_bounding_box()
        self.parent = None

    def get_root(self):
        if (self.parent == None):
            return self
        else:
            return self.parent.get_root()

    def collide_atom(self, atom):
        """ @return the node of this tree that is in collision with `atom`
                    or `None` if there is no collision.
        """
        if (atom.get_bounding_box().intersects(self.bounding_box)):
            dist = (atom.pos - self.atom.pos).length()
            if (dist < (atom.radius + self.atom.radius) * DIAGONALE):
                return self
            for child in self.links:
                n = child.node.collide_atom(atom)
                if (n != None):
                    return n
        return None


    def collide_molecule(self, node):
        """ @return a couple of molecule nodes from (self, node)
        """
        if not node.bounding_box.intersects(self.bounding_box):
            return None
        res = self.collide_atom(node.atom)
        if (res != None):
            return (node, res)
        for child in node.links:
            res = self.collide_molecule(child.node)
            if (res != None):
                return res
        return None

    def translate(self, t):
        self.bounding_box.tl = self.bounding_box.tl + t
        self.bounding_box.br = self.bounding_box.br + t
        self.atom.pos = self.atom.pos + t
        self.pos = self.pos + t
        for child in self.links:
            child.node.translate(t)

    def remove_child(self, node):
        for child in self.links:
            if child.node == node:
                self.links.remove(child)
                return

    def reverse_hierarchy(self, new_parent):
        # Self (parent of new_parent) become a child
        if (self.parent != None):
            self.parent.reverse_hierarchy(self)
        self.remove_child(new_parent)
        new_parent.links.append(link(0, self))
        self.parent = new_parent

    def update_bbox(self):
        if (len(self.links) > 0):
            child_bbox = None
            for child in self.links:
                child.node.update_bbox()
                if (child_bbox == None):
                    child_bbox = copy.copy(child.node.bounding_box)
                else:
                    child_bbox = box_merge(child_bbox, child.node.bounding_box)
            self.bounding_box = box_merge(self.atom.get_bounding_box(),
                                          child_bbox)
        else:
            self.bounding_box = self.atom.get_bounding_box()


    def update_physic(self):
        if (len(self.links) > 0):
            centres = []
            weights = []
            for child in self.links:
                child.node.update_physic()
                centres.append(child.node.pos)
                weights.append(child.node.weight)

            centres.append(self.atom.pos)
            weights.append(self.atom.weight)

            self.pos = compute_barycentre(centres, weights)
            self.weight = reduce(lambda x, y: x + y, weights)

        else:
            self.pos = self.atom.pos
            self.weight = self.atom.weight

    def fusion(self, other):
        # Move self and other in order to have a distance between them of
        # link length + self.weight + other.weight

        assert other.atom != self.atom
        diff = (other.atom.pos - self.atom.pos)
        norm_diff = diff.normalized()

        # Translate other
        other_pos = self.atom.pos \
                  + norm_diff * (self.atom.radius + other.atom.radius) * 1.25
        trans_pos = other_pos - other.atom.pos
        other.get_root().translate(trans_pos)

        self_speed = self.get_root().speed
        other_speed = other.get_root().speed
        self_weight = self.get_root().weight
        other_weight = self.get_root().weight
        sum_weight = float(self_weight + other_weight)

        self.get_root().speed = (self_speed * (self_weight / sum_weight)) \
                              + (other_speed * (other_weight / sum_weight))

        root = other.get_root()
        other.reverse_hierarchy(self)
        self.get_root().update_bbox()
        self.get_root().update_physic()
        return root

    def update(self):
        self.translate(self.speed)

    def change_weight(self, new_weight):
        self.atom.weight = new_weight
        self.atom.radius = new_weight * 5
        self.atom.load = new_weight
        self.empty_load = new_weight
        self.bounding_box = self.atom.get_bounding_box()

    def count(self):
        sum_count = 0
        for child in self.links:
            sum_count += child.node.count()
        return 1 + sum_count

    def _to_assoc_list(self, l):
        for child in self.links:
            a = max(self.atom.weight, child.node.atom.weight)
            b = min(self.atom.weight, child.node.atom.weight)
            l.append([a, b])
            child.node._to_assoc_list(l)

    def to_assoc_list(self):
        l = []
        self.get_root()._to_assoc_list(l)
        return l

    def contains(self, other):
        if other == self:
            return True

        for child in self.links:
            if child.node.contains(other):
                return True

        return False


def compare_assoc_list(m, n):
    if len(m) != len(n):
        return False
    n = copy.copy(n)
    for a in m:
        found = False
        for b in n:
            if a[0] == b[0] and a[1] == b[1]:
                n.remove(b)
                found = True
                break
        if not found:
            return False
    return True
