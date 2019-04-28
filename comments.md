Empirical performance: tree.py vs tree_np.py

The first subplot suggests that the original tree.py script runs in exponential time as iterations N grow (in 2^N). 
Also, it suggets that the numpy tree seems to run in linear time as iterations N grow (in N). So, for 20 iterations,
numpy seems to be a much better option than using lists to grow the tree.

Investigating further and taking logs in base 2 of both execution times across iterations, subplot 2 was created.
Firstly, it shows the scattered plot of log2(execution time) versus iterations (N) for both algorithms. The scatter plots
suggest that both algorithms are O(2^N). That is, execution time is exponential in both cases. So, in the limit
when N goes to infinity, both algorithms are identical. I assumed that the constants in both regressions are the baseline
time to run each algorithm with N=0; both constants are very close and thus I ignored them for the performance comparison
in the last paragraph. The baseline accounts for growing a tree (2^N) and the different functions used to build the 2 classes.

Log 2 was applied to the exec time as for a binary tree of height h there will be 2^h nodes. Thus, from a level of the tree 
to the next, 2^h nodes are added. So, when both algorithms start at h=0 and run until h=N, for each h there will be 2^h 
additional nodes 'grown'. So, I expect the time to grow the tree to be exponential in base 2 (2^N) given each node would 
take the same amount of time to be created. Letting f(N) be the fitted regression of the original tree and g(N) of the numpy tree,
then limit when N -> inf of f(N)/g(N) -> inf. This means that f(N) is not in O(g(N)) while g(N) is in O(f(N)). This shows that
both algos are O(2^N).

Still, for discrete values of N the following cases are distinguishable:
1. for N<=3, the original tree algo (with lists) is faster (lower exec time)
2. for N>3 but finite, the numpy solution is faster. This is shown by the slope of execution time (2nd plot) which is almost twice as
small for the numpy solution than the original one (0.5736 vs 0.9979).
Then, as N -> inf, both solutions are O(exp(N))
To check if there is an added performance of numpy, I disregarded the 2^N complexity of building a tree and took the slopes as indicators.

Why is the numpy algo faster? It is because of the following:
The inner loop from the original algorithm (w/ element-wise operations) was replaced by vector operations.
The math sin and cos functions with a single numpy.sin function. 
The array of new branches is now grown with vstack rather than append within the inner loop. So, we're no longer reallocating and copying lists 
within the inner loop.
Usage of a single array rather than one for the cos and one for the sin outputs.
Numpy partly written in C which makes it faster.

Possible improvements;
Better use of maths to work out the formulas to simplify them.
Using fewer numpy arrays and speed up the algo (but at the cost of code readability).

Note: for both algos, I tried to focus on code readability (although I not a mathematician/computer scientist and thus treated the math formulas 
as 'given'). Both algos could be sped up but I believe code readability would decrease.




