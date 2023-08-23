# The Knapsack Problem

This tiny Python module provides two functions to solve the 0-1 knapsack problem, with a slight modification to find the closest solution, either above or below the target (depending on the function):

> Finds a subset of `values` whose sum is less/greater than or equal to `target` and the closest possible to it. Values are taken only once.

The algorithm uses dynamic programming and avoids the usual `N*W` table (where `N` is the number of values and `W` is the target value). Instead, it uses subset tuples that are built in a dynamic list of size `W`. A separate subset is built for the closest result (above or below the target) in case no solution is found.

The general idea is to start from the target value and gather subsets of values whose sum equals the target.

## Examples

```python
from knapsack import solve_gt, solve_lt
values = [2, 6, 3, 5]

# Sorting the values takes the smallest / greatest values first.
# Here we take the greatest values first to reduce the risk of ending up
# with coarse values if the algorithm is used iteratively to extract
# multiple subsets.
values.sort(reverse=True)

# Both solve_gt and solve_lt find the values that sum up to the exact target
# when it's possible:
solve_gt(values, 10)
# result: (5, 3, 2)
solve_lt(values, 10)
# result: (5, 3, 2)

# When it's not possible to reach the target, solve_gt will try to find the
# minimum sum above it:
solve_gt(values, 12)
# result: (6, 5, 2)

# Similarly, solve_lt will try to find the maximum sum below it:
solve_lt(values, 12)
# result: (6, 5)

# When it's not possible to find a solution even below or above the target,
# an empty subset is returned:
solve_gt(values, 100)
# result: ()
```
