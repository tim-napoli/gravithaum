import pickle
import random as r
import sys


from atom                       import atom
from atom                       import random_atom
from forcefield                 import forcefield
from molecule                   import molecule
from molecule                   import compare_assoc_list
from gravithaum.physic.point    import point as pt
from gravithaum.math.vector     import vector as vect
from gravithaum.math.rectangle  import rectangle as rect

class universe:

    def __init__(self):
        self.attractors = []
        self.molecules = []
        self.grid = forcefield(self)
        self.goal = None

    def __str__(self):
        return "({0},{1},{2})".format(self.molecules, self.attractors, self.goal)

    def attracts_molecule(self, molecule):
        for attr in self.attractors:
            attr.attracts(molecule)

    def collides_molecule(self, molecule):
        for other in self.molecules:
            if (other == molecule or other in self.blacklist):
                continue
            res = molecule.collide_molecule(other)
            if (res != None):
                (a, b) = res
                root = a.fusion(b)
                self.blacklist.append(root)
                break

    def update(self):
        map(self.attracts_molecule, self.molecules)

        self.blacklist = []
        for mol in self.molecules:
            if mol not in self.blacklist:
                mol.update()
                self.collides_molecule(mol)
        for mol in self.blacklist:
            self.molecules.remove(mol)

        # Check for molecules out of the screen
        for mol in self.molecules:
            if mol.bounding_box.tl.x <= -640:
                mol.speed.x = -mol.speed.x
            if mol.bounding_box.br.x >= 640:
                mol.speed.x = -mol.speed.x
            if mol.bounding_box.br.y <= -360:
                mol.speed.y = -mol.speed.y
            if mol.bounding_box.tl.y >= 360:
                mol.speed.y = -mol.speed.y

        # self.compare_molecules()

    def clear(self):
        self.attractors = []
        self.molecules = []
        self.goal = None

    def get_molecules_in(self, rect):
        return filter(lambda m: m.bounding_box.intersects(rect),
                      self.molecules)

    def get_molecules_at(self, v):
        for mol in self.molecules:
            if ((v -  mol.atom.pos).length() <= mol.atom.weight + 10):
                return mol
        return None

    def get_attractors_in(self, rect):
        return filter(lambda a: rect.point_in(a.pos),
                      self.attractors)

    def remove_attractor_at(self, v):
        for attr in self.attractors:
            if ((v - attr.pos).length() <= attr.weight + 10):
                self.attractors.remove(attr)
                return

    def remove_molecule(self, mol):
        for child in mol.links:
            self.remove_molecule(child.node)

        self.molecules.remove(mol)

    def remove_molecule_at(self, v):
        for mol in self.molecules:
            if ((v -  mol.atom.pos).length() <= mol.atom.weight + 10):
                self.remove_molecule(mol.get_root())
                return

    def compare_molecules(self):
        l = []
        for mol in self.molecules:
            if mol.get_root().count() > 1:
                l.append(mol.to_assoc_list())
        print "------"
        for i in range(0, len(l) - 1):
            for j in range(i + 1, len(l)):
                if compare_assoc_list(l[i], l[j]):
                    print "list {} = list {}".format(l[i], l[j])
                else:
                    print "list {} != list {}".format(l[i], l[j])

    def is_win(self):
        if (self.goal == None):
            return False
        goal_assoc = self.goal.to_assoc_list()
        assocs = []
        for mol in self.molecules:
            if mol.get_root().count() > 1:
                assocs.append(mol.to_assoc_list())
        for assoc in assocs:
            if compare_assoc_list(assoc, goal_assoc):
                return True
        return False

    def save_to_file(self, path):
        try:
            pickle.dump(self, file(path, "wb"))
        except Exception as e:
            print "Impossible de sauvegarder le fichier"

def load_universe_from_file(path):
    u = None
    try:
        u = pickle.load(open(path, 'rb'))
    except Exception as e:
        print "Erreur de chargement de {}".format(path)
        print "Message : {}".format(e)
        sys.exit(1)

    return u

def generate_random_universe():
    u = universe()
    mols = []
    attractors = []

    for i in range(0, 100): mols.append(molecule(random_atom()))

    u.molecules = mols
    u.attractors = attractors

    return u
