from matplotlib import pyplot as plt
import numpy as np


def sine(x, a):
    return np.sin(x - a)


def cosine(x, a):
    return np.sin(np.pi / 2 - (x - a))


def sort_branches(branches):
    return branches[branches[:, 0].argsort()]


"""
Tree_of_life class with numpy
"""


class tree_of_life_np:
    def __init__(
        self,
        no_descendants=5,
        tree_size=1,
        branch_overlap=0.6,
        offset=0.1,
        fig_name="tree_np.png",
        show_tree=True,
        save_tree=True,
    ):

        self.size = tree_size
        self.overlap = branch_overlap
        self.no_descendants = range(no_descendants)
        self.offset = offset
        self.current_branches = np.array([0, 1, 0]).reshape(1, 3)
        self.fig_name = fig_name
        self.show_tree = show_tree
        self.save_tree = save_tree
        if self.show_tree or self.save_tree:
            plt.plot([0, 0], [0, 1])

    def update_branches_size(self):
        self.size = self.size * self.overlap

    def displacement_vect(self):
        offset_vector = self.offset * np.ones(len(self.current_branches))
        self.displacement_vector = np.hstack((offset_vector, -offset_vector))

    def stack_current_branches(self):
        self.stk_brnchs = np.vstack((self.current_branches, self.current_branches))

    def update_branches(self):
        sine_calc = sine(self.stk_brnchs[:, 2], self.displacement_vector)
        cosine_calc = cosine(self.stk_brnchs[:, 2], self.displacement_vector)

        x_updt = self.stk_brnchs[:, 0] + self.size * sine_calc
        y_updt = self.stk_brnchs[:, 1] + self.size * cosine_calc
        z_updt = self.stk_brnchs[:, 2] - self.displacement_vector

        """ 
        Comment added for assessment, not Refactoring!       
        Performance trials      
        vstack:        0.5729 slope in perf plot
            np.vstack((x_updt, y_updt, z_updt), axis=0).T
            
        concatenate:   0.5790 slope in perf plot
            np.concatenate((x_updt[:, np.newaxis], 
                            y_updt[:, np.newaxis], 
                            z_updt[:, np.newaxis]), axis=1)
            
        column_stack: 0.5778 slope in perf plot
            np.colum_stack((x_updt, y_updt, z_updt)).T
        
        So, I used the vstack option as it's marginally faster
        """
        self.updated_branches = np.vstack((x_updt, y_updt, z_updt)).T

    def plot_tree(self):
        if self.show_tree or self.save_tree:
            sorted_branches = sort_branches(self.updated_branches)
            sort_stk_brnchs = sort_branches(self.stk_brnchs)

            left_brnch_plot = [sort_stk_brnchs[:, 0], sorted_branches[:, 0]]
            right_brnch_plot = [sort_stk_brnchs[:, 1], sorted_branches[:, 1]]

            plt.plot(left_brnch_plot, right_brnch_plot)

    def grow_tree(self):
        for descendant in self.no_descendants:
            self.displacement_vect()
            self.stack_current_branches()
            self.update_branches()
            self.plot_tree()

            self.current_branches = self.updated_branches
            self.update_branches_size()

    def view_tree(self):

        self.grow_tree()

        if self.save_tree or self.show_tree:
            plt.title("Tree of life (numpy)")
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

    parser = argparse.ArgumentParser(description="Create tree of life plot w/ numpy")

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

    tree_of_life_np(
        args.no_descendants,
        args.tree_size,
        args.branch_overlap,
        offset=args.offset,
        show_tree=display,
        save_tree=save,
    ).view_tree()
