# The Knapsack Problem

This tiny Python module provides two functions to solve the 0-1 knapsack problem, with a slight modification to find the closest solution, either above or below the target (depending on the function):

> Finds a subset of `values` whose sum is less/greater than or equal to `target` and the closest possible to it. Values are taken only once.

The algorithm uses dynamic programming and avoids the usual `N*W` table (where `N` is the number of values and `W` is the target value). Instead, it uses subset tuples built in a dynamic list of size `W`. A separate subset is built for the closest result (above or below the target) if no solution is found.

The general idea is to start from the target value and gather subsets of values whose sum equals the target.

## Examples

```python
from knapsack import solve_ge, solve_le
values = [2, 6, 3, 5]

# Sorting the values takes the smallest / greatest values first.
# Here, we take the greatest values first to reduce the risk of ending up
# with coarse values if the algorithm is used iteratively to extract
# multiple subsets.
values.sort(reverse=True)

# Both solve_ge and solve_le find the values that sum up to the exact target
# when it's possible:
solve_ge(values, 10)
# result: (5, 3, 2)
solve_le(values, 10)
# result: (5, 3, 2)

# When it's not possible to reach the target, solve_ge will try to find the
# minimum sum above it:
solve_ge(values, 12)
# result: (6, 5, 2)

# Similarly, solve_le will try to find the maximum sum below it:
solve_le(values, 12)
# result: (6, 5)

# When it's not possible to find a solution even below or above the target,
# an empty subset is returned:
solve_ge(values, 100)
# result: ()
```

A helper function extracts the values from a dictionary in which values are specified as `value`: `quantity` items:

```python
from knapsack import values_from_dict
data = { 10: 4, 20: 2, 5: 1 }
values_from_dict(data)
# result: [10, 10, 10, 10, 20, 20, 5]
```

You'll find one unit test, `test_iterations`, using this function and iterating through a chest of supplies to get as many subsets of 40 (or more) as possible.

## How It Works

The simplest form of the algorithm proceeds by testing all the possibilities. For each item, it tests the outcome by taking it or by not taking it. In pseudocode:

```python
values = [1, 2, 3, 5, 11]
n = len(values)
target = 10

def explore(index, total):
    if total > target:
        return 0
    if index == n:
        return total
    pick = explore(index + 1, total + values[index])
    leave = explore(index + 1, total)
    return max(pick, leave)

solution = explore(index=0, total=0)
```

The function is recursive, so it calls itself to compute the two outcomes and increments the index to consider the remaining values `index + 1` ... `n`.

Totals that exceed the target are not interesting, so the function directly returns 0 when that happens. In that case, the function that called it will favour the other solution; e.g. if `pick == 0`, it will prefer the value reached by `leave`. If both are null, the function returns 0 and will be discarded by the function above it, and so on.

When the function reaches the last value (`index == n`), there's nothing more to explore, so it returns the total. If the total is the target value, we have found a solution. If not, the total will be the sum that is the closest to the target.

Note that this pseudocode doesn't return the selected values but only their sum, for the sake of clarity.

## Dynamic Programming

The complexity of the approach above is O(2^n), so it's not very good. The major problem is that it repeats the same calculations by exploring the remaining values two times at each level.

Using dynamic programming, we can use a table to memorize the backtracking information more efficiently, avoiding exploring the same solutions multiple times.

```python
def solve(values: list[int], target: int) -> list[int]:
    n = len(values)

    # initializes a backtracking memoization array
    trace = array(lines=n + 1, columns=target, init=(0, 0))
    for total in range(target):
        trace[n][total] = (total, 0)

    # fills the table with backtracking data to get to the result
    for i in range(n - 1, -1, -1):
        value = values[i]
        for total in range(0, target + 1):
            pick = 0
            if total + value <= target:
                pick = trace[i + 1][total + value][0]
            leave = trace[i + 1][total][0]
            trace[i][total] = (max(pick, leave), 1 if pick > leave else 0)

    # backtracking of picked values
    subset = []
    total = 0
    for (i, value) in enumerate(values):
        if trace[i][total][1] == 1:
            subset.append(value)
            total += value
    return subset
```

The `trace` array is first initialized with zeroes except the last line, which is filled with incrementing values. The algorithm then proceeds line by line, starting with line `n - 1` and ending with line 0.

Next to the values, we also store a tag that will be used to retrieve the picked values. So, instead of filling the table with 0, we actually fill it with `(0, 0)` — the first being the value, the second being the tag.

Each line corresponds to the value at this index: `value[i]`, and the last line corresponds to target values from 0 to `target`. Here is an example of table for the same values as above without showing the tags on the last line:

    0 (  1): 0:0,  0:0,  0:0,  0:0,  0:0,  0:0,  0:0,  0:0,  0:0,  0:0,  0:0
    1 (  2): 0:0,  0:0,  0:0,  0:0,  0:0,  0:0,  0:0,  0:0,  0:0,  0:0,  0:0
    2 (  3): 0:0,  0:0,  0:0,  0:0,  0:0,  0:0,  0:0,  0:0,  0:0,  0:0,  0:0
    3 (  5): 0:0,  0:0,  0:0,  0:0,  0:0,  0:0,  0:0,  0:0,  0:0,  0:0,  0:0
    4 ( 11): 0:0,  0:0,  0:0,  0:0,  0:0,  0:0,  0:0,  0:0,  0:0,  0:0,  0:0
    5      : 0     1     2     3     4     5     6     7     8     9    10

On each line `i`, the algorithm inspects each column corresponding to a total to reach and checks in `i + 1` to see the outcome of picking the current value or not.
- Picking the value means adding it to the total (the column index), so it looks at `trace[i+1][total + value]` if `total + value` doesn't exceed the target (to remain in the table and because we want to reach the target, not exceed it)
- Leaving the value means not adding it, so it looks at `trace[i+1][total]`.

Here is the result after looping through the table:

    0 (  1): 10:0, 10:1, 10:0, 10:0, 10:1, 10:0, 10:1, 10:0, 10:0, 10:1, 10:0
    1 (  2): 10:1,  9:0, 10:0, 10:1,  9:0, 10:0,  9:0, 10:0, 10:1,  9:0, 10:0
    2 (  3):  8:1,  9:1, 10:1,  8:0,  9:0, 10:0,  9:1, 10:1,  8:0,  9:0, 10:0
    3 (  5):  5:1,  6:1,  7:1,  8:1,  9:1, 10:1,  6:0,  7:0,  8:0,  9:0, 10:0
    4 ( 11):  0:0,  1:0,  2:0,  3:0,  4:0,  5:0,  6:0,  7:0,  8:0,  9:0, 10:0
    5      :  0     1     2     3     4     5     6     7     8     9    10

The tags at `1` mean that the corresponding values were taken. The `10` in the upper left cell is the best solution; in this case, it's the target value.

To backtrack and find the corresponding subset of values, we start at the top with `total = 0` (the left column), and we go down until we see the first taken value. In this case, it's `[1][0] == 10:1`: by adding `2` to the previous total, we can reach `10`. To find the next value, we look at column `total = 2`, starting on the following line. Then we go down until we see another taken value. In this case, it's `[2][2] == 10:1`: by adding `3` to the previous total, we can reach `10`. And so on.

Here is the table with only the interesting values:

    0 (  1):   | 
    1 (  2): 10:1
    2 (  3):   +-------- 10:1
    3 (  5):               +-------------- 10:1
    4 ( 11):                                 |
    5      :  0     1     2     3     4     5     6     7     8     9    10

And so the result is: `2, 3, 5`.

The complexity is down to O(n * target), but the space is O(n * target) too.

This version of the algorithm was pushed earlier, and you can retrieve it from git with the `table` tag.

## Simplifying

When we decide to pick a value, we could directly store the resulting subset in a single vector instead of storing tags in a table and backtracking. After iterating through all the values, bottom to top (figuratively), we'll find the final subset in `subset[target]` if the solution exists. If it doesn't, `subset[target] == None` and we'll have to check the lower indices until the best result is found.

This is the simplified algorithm:

```python
def solve(values, target):
    subset = [(), *[None] * target]
    for value in values:
        for i in range(target - 1, -1, -1):
            if subset[i] is not None:
                if i + value <= target and subset[i + value] is None:
                    subset[i + value] = (*subset[i], value)
    return subset[target] or (), subset
```

`subset` is first initialized with `[(), None, ..., None]`. First, only `total = 0` is considered since all the other cells are `None`. 
- The first value, `1`, can be added or not, forming a new subset in `[0+1] = (1)`.
- The next value, `2`, can be added or not to any existing subset, forming two subsets in `[0+2] = (2)`, `[1+2] = (1, 2)`. And so on.

The final vector contains the following subsets:

      0: 
      1: 1
      2: 2
      3: 1, 2
      4: 1, 3
      5: 2, 3
      6: 1, 2, 3
      7: 2, 5
      8: 1, 2, 5
      9: 1, 3, 5
     10: 2, 3, 5

Here, the exact solution exists: `[10] == 2, 3, 5`.

From the loops, the complexity remains O(n * target), but the space is reduced in practical situations since all the hopeless subsets are discarded, making it unlikely to have `target` lists of `n` items. The worst case remains O(n * target), however.

## Best Sum >= Target

Storing all the values beyond the target would be inefficient and incompatible with the algorithm. In case there is no exact solution, we keep track of the best next thing, which is the minimum total greater than the target. It's a simple modification to the previous algorithm:

```python
def solve_ge(values: list[int], target: int) -> tuple | tuple[int]:
    subset = [(), *[None] * target] # initialized to [(), None, ..., None]
    above_min = sys.maxsize         # MAXINT
    above_subset = ()
    for value in values:
        for i in range(target - 1, -1, -1): # target-1 down to 0
            if subset[i] is not None:
                # builds the subset to get to i+value
                if i + value <= target and subset[i + value] is None:
                    subset[i + value] = (*subset[i], value)
                # keeps a potential best candidate in case the target cannot be reached
                if target < i + value < above_min:
                    above_min = i + value
                    above_subset = (*subset[i], value)
    if subset[target] is not None:
        return subset[target]
    else:
        return above_subset
```

`above_subset` contains the 'next best thing', and `above_min` contains the corresponding total. We initialize it with `MAXINT` to avoid a condition later — the first comparison will always find a lower value than `MAXINT`, so it will store the corresponding subset.

If no solution is found, we return the 'next best thing'. If it isn't possible to exceed the total, even by summing all the values, the function returns an empty subset.

A similar modification handles the case where we want the best sum that is less than or equal to the target.