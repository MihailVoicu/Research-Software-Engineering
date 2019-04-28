import random


class Laboratory(object):
    def __init__(self, inputfile):

        self.input = inputfile

        if type(self.input) != dict:
            raise TypeError("Input yaml file must define a proper python dict")
        if list(self.input.keys()) != ["lower", "upper"]:
            if list(self.input.keys()) != ["upper", "lower"]:
                raise TypeError("Input yaml file must have a lower and an upper shelf")

        self.shelf1 = inputfile["lower"]
        self.shelf2 = inputfile["upper"]

        if not (isinstance(self.shelf1, list) and isinstance(self.shelf2, list)):
            raise TypeError("lower and upper shelves must be defined as lists")
        else:
            if not (
                all(list(isinstance(i, str) for i in self.shelf1))
                or all(list(isinstance(i, str) for i in self.shelf2))
            ):
                raise TypeError(
                    "lower and upper shelves must be defined as lists of str"
                )

    def update_shelves(self, substance1, substance2_index):

        if substance2_index > len(self.shelf2):
            raise ValueError(
                "Cannot updt upper shelf with subst out of range at index: ",
                substance2_index,
            )
        if substance1 not in self.shelf1:
            raise ValueError("Cannot updt lower shelf with", substance1, "not on shelf")

        index1 = self.shelf1.index(substance1)
        self.shelf1 = self.shelf1[:index1] + self.shelf1[index1 + 1:]
        self.shelf2 = (
            self.shelf2[:substance2_index] + self.shelf2[substance2_index + 1:]
        )

    def do_a_reaction(self):

        """ check can_react() method in Substance class returns a boolean """
        i, j = "antiA", "A"
        if type(Substance(i, j).can_react()) != bool:
            raise TypeError("can_react() method must return a boolean")

        for substance1 in self.shelf1:
            possible_targets = [
                i
                for i, target in enumerate(self.shelf2)
                if Substance(substance1, target).can_react()
            ]
            if not possible_targets:
                continue
            else:
                substance2_index = random.choice(possible_targets)
                self.update_shelves(substance1, substance2_index)
                break

    def run_full_experiment(self):

        count = 0
        ended = False
        while not ended:
            shelf1_old, shelf2_old = self.shelf1, self.shelf2
            self.do_a_reaction()
            if shelf1_old != self.shelf1:
                count += 1
            ended = (shelf1_old == self.shelf1) and (shelf2_old == self.shelf2)

        return self.shelf1, self.shelf2, count


""" This is exogenous to this module. Can be redefined by other helpers """


class Substance(object):
    def __init__(self, substance1=None, substance2=None, reaction_type="anti"):

        """ This class must have some checks in place. Suggestion to other
        users/lab helpers: leave the 3 checks below into place """
        if (substance1 is None) or (substance1 is None):
            raise TypeError("2 substances must be passed as arguments")
        if not (isinstance(substance1, str) and isinstance(substance2, str)):
            raise TypeError("Substances must be strings")
        if not (isinstance(reaction_type, str)):
            raise TypeError("Type of reaction must be a string e.g. 'anti'")

        self.substance1 = substance1
        self.substance2 = substance2
        self.reaction = reaction_type

        """ reduce even occurances of 'anti' to 0 and odd occurences to 1
        that are present in either substances """
        skips = len(self.reaction)

        anti_occ = self.substance1.count(reaction_type)
        if anti_occ % 2 == 0:
            self.substance1 = self.substance1[skips * anti_occ:]
        else:
            self.substance1 = self.substance1[skips * (anti_occ - 1):]

        anti_occ = self.substance2.count(reaction_type)
        if anti_occ % 2 == 0:
            self.substance2 = self.substance2[skips * anti_occ:]
        else:
            self.substance2 = self.substance2[skips * (anti_occ - 1):]

    def can_react(self):
        return (self.substance1 == self.reaction + self.substance2) or (
            self.substance2 == self.reaction + self.substance1
        )
