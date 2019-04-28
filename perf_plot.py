from tree import tree_of_life
from tree_np import tree_of_life_np
from timeit import default_timer as timer
import numpy as np
from matplotlib import pyplot as plt
import statsmodels.api as sm


max_iters = 20
time_algo = np.zeros((max_iters, 2))
algos = [tree_of_life, tree_of_life_np]

for i in range(1, max_iters + 1):

    for j, algo in enumerate(algos):

        start = timer()
        algo(no_descendants=i, show_tree=False, save_tree=False).view_tree()
        end = timer()

        time_algo[i - 1, j] = end - start

# Linear Regression fitting log(Execution time) = a + b * Iterations
x = list(range(max_iters))
y_tree = np.log2(time_algo[:, 0])
y_tree_np = np.log2(time_algo[:, 1])
results_tree = sm.OLS(y_tree, sm.add_constant(x)).fit()
results_tree_np = sm.OLS(y_tree_np, sm.add_constant(x)).fit()

# Plotting
fig, ax = plt.subplots(2, sharex=True)
# Scatter plots
ax[0].scatter(x, time_algo[:, 0], c="g")
ax[0].scatter(x, time_algo[:, 1], c="r")
# Log-space scatter plots
ax[1].scatter(x, np.log2(time_algo[:, 0]), c="g")
ax[1].scatter(x, np.log2(time_algo[:, 1]), c="r")
# Display regression line overlaying above
ax[1].plot(x, results_tree.fittedvalues, c="g")
ax[1].plot(x, results_tree_np.fittedvalues, c="r")
# Legend formatting
ax[0].legend(("tree original", "tree numpy"))
params_orig = [str(results_tree.params[0])[0:6], str(results_tree.params[1])[0:6]]
label1 = "Orig: log2(time) = " + params_orig[0] + " + " + params_orig[1] + " * N"
params_np = [str(results_tree_np.params[0])[0:6], str(results_tree_np.params[1])[0:6]]
label2 = "Nmp: log2(time) = " + params_np[0] + " + " + params_np[1] + " * N"
ax[1].legend((label1, label2), fontsize=8)
# Axes formatting
ax[0].set_ylabel("Execution time (s)")
ax[0].set_title("Performance plots")
ax[1].set_ylabel("Log execution time (s)")
ax[1].set_xlabel("Iterations (no descendants)")
ax[1].set_xticks(np.arange(0, max_iters + 1, 5))
# save figure
fig.savefig("perf_plot.png")
