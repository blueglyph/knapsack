import sys


def solve_le(values: list[int], target: int) -> tuple | tuple[int]:
    """
    Finds a subset of `values` whose sum is less than or equal to `target` and the closest possible to it.
    Values are taken only once.

    Returns the subset, or an empty tuple if no solution is found.

    The data in `values` can be sorted in reverse order so that greater values are taken in priority.
    This may give better results when removing the subset and iterating; for example, when several
    subsets are required.
    """
    subset = [(), *[None] * target]         # initialized to [(), None, ..., None]
    below_max = 0
    below_subset = ()
    for value in values:
        for i in range(target - 1, -1, -1): # target-1 down to 0
            if subset[i] is not None:
                # builds the subset to get to i+value
                if i + value <= target and subset[i + value] is None:
                    subset[i + value] = (*subset[i], value)
                # keeps a potential best candidate in case the target cannot be reached
                if below_max < i + value < target:
                    below_max = i + value
                    below_subset = (*subset[i], value)
    if subset[target] is not None:
        return subset[target]
    else:
        return below_subset


def solve_ge(values: list[int], target: int) -> tuple | tuple[int]:
    """
    Finds a subset of `values` whose sum is greater than or equal to `target` and the closest possible to it.
    Values are taken only once.

    Returns the subset, or an empty tuple if no solution is found.

    The data in `values` can be sorted in reverse order so that greater values are taken in priority.
    This may give better results when removing the subset and iterating; for example, when several
    subsets are required.
    """
    subset = [(), *[None] * target]         # initialized to [(), None, ..., None]
    above_min = sys.maxsize                 # initialized to INFINITY / MAXINT
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


def values_from_dict(data: dict) -> list[int]:
    """Extracts values for a `value: quantity` dictionary"""
    return [v for (v, nbr) in data.items() for _ in range(nbr)]
