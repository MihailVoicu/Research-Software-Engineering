"""
Functions used for the tree_of_life class
"""

# fix sin & cos dependencies in updt_full()
def sine(x):
    from math import sin

    return sin(x)


def cosine(x):
    from math import cos

    return cos(x)


# this function updates the tree with the left and right branches as it grows
def updt_full(func, func_arg, func_off, size=None, data=None):

    # this is used to offset the sin/cos functions by +-0.1 offset
    def func_offset(f, arg, off):
        return f(arg + off)

    # this is used to update the coords of the left and right branches
    def updt_branch(start, scale, func_value):
        if start == None or scale == None:
            return func_value
        return start + scale * func_value

    return updt_branch(data, size, func_offset(func, func_arg, func_off))


# view left and right branches as tree grows
def view_tree(coord1=None, coord2=None, start_tree=False):
    from matplotlib import pyplot as plt

    #  if start_tree, plot initial branch from 0 to 1 on y-axis
    if start_tree:
        coord1 = [0, 0]
        coord2 = [0, 1]

        plt.plot(coord1, coord2)
    # if not at the start, form the coords per CW formulas
    else:
        coord_left1 = [coord1[0], coord2[-2][0]]
        coord_left2 = [coord1[1], coord2[-2][1]]

        coord_right1 = [coord1[0], coord2[-1][0]]
        coord_right2 = [coord1[1], coord2[-1][1]]

        plt.plot(coord_left1, coord_left2)
        plt.plot(coord_right1, coord_right2)


"""
Tree_of_life class
"""


class tree_of_life:
    def __init__(
        self,
        no_descendants=5,
        tree_size=1,
        branch_overlap=0.6,
        offset=0.1,
        fig_name="tree.png",
        show_tree=True,
        save_tree=True,
    ):

        self.size = tree_size
        self.overlap = branch_overlap
        self.no_descendants = range(no_descendants)
        self.offset = [-offset, offset]
        self.current_branches = [[0, 1, 0]]
        self.fig_name = fig_name
        self.show_tree = show_tree
        self.save_tree = save_tree
        if self.show_tree or self.save_tree:
            view_tree(start_tree=True)

    def update_branches_size(self):
        self.size = self.size * self.overlap

    # function to grow tree from parent to next descendants
    def grow_branches(self):
        self.updated_branches = []
        for angle in self.current_branches:
            for off in self.offset:

                x_update = updt_full(sine, angle[2], off, self.size, angle[0])
                y_update = updt_full(cosine, angle[2], off, self.size, angle[1])
                z_update = angle[2] + off
                self.updated_branches.append([x_update, y_update, z_update])

            if self.show_tree or self.save_tree:
                view_tree(angle, self.updated_branches)

    def grow_tree(self):
        for descendant in self.no_descendants:
            self.grow_branches()
            self.current_branches = self.updated_branches
            self.update_branches_size()

    def view_tree(self):
        self.grow_tree()

        from matplotlib import pyplot as plt

        if self.save_tree or self.show_tree:
            plt.title("Tree of life")
            plt.ylabel("Descendants")
            plt.xlabel("contemporary relatives")
            plt.xticks([])

        if self.save_tree:
            import os
            plt.savefig(os.path.join(os.path.dirname(__file__), self.fig_name))
        if self.show_tree:
            plt.show()


"""
Use argparse to manage inputs to tree_of_life
"""

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description="Create tree of life plot")

    # required arg: no of descendants
    parser.add_argument(
        "no_descendants", help="number of descendants/nodes in tree", type=int
    )
    # optional args: tree size, branch overlap, offset
    parser.add_argument("-t", "--tree_size", help="size of branches", type=float)
    parser.add_argument(
        "-o", "--branch_overlap", help="overlap of branch leaves", type=float
    )
    parser.add_argument("-f", "--offset", help="offset size", type=float)
    # optional arg: display plot to screen or not
    parser.add_argument(
        "-nd",
        "--not_display",
        help="disable display of tree to screen",
        action="store_true",
    )
    parser.add_argument(
        "-ns", "--not_save", help="disable save of tree", action="store_true"
    )

    args = parser.parse_args()

    # default values of optional args and displaying/saving args
    if args.tree_size is None:
        args.tree_size = 1
    if args.branch_overlap is None:
        args.branch_overlap = 0.6
    if args.offset is None:
        args.offset = 0.1
    display = not (args.not_display)
    save = not (args.not_save)

    tree_of_life(
        args.no_descendants,
        args.tree_size,
        args.branch_overlap,
        offset=args.offset,
        show_tree=display,
        save_tree=save,
    ).view_tree()
