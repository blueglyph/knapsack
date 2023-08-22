import os
import unittest
import timeit

def solve(values, target):
    subset = [(), *[None] * target]
    for value in values:
        for i in range(target - 1, -1, -1):
            if subset[i] is not None:
                if i + value <= target and subset[i + value] is None:
                    subset[i + value] = (*subset[i], value)
    return subset[target] or (), subset

def print_array(values, subset = None, trace = None, msg ='result:'):
    if subset is not None:
        print(f'  {msg}', ', '.join(str(x) for x in subset))
    elif msg:
        print(msg)
    print(f'  values: {values}')
    if trace is not None:
        for (i, subset) in enumerate(trace):
            if subset is not None:
                print(f'  {i:3}: {", ".join(str(x) for x in subset)}')

class TestKnapsack(unittest.TestCase):
    def run_test(self, t_values, title='Test'):
        print(f'\n{title}')
        n_err = 0
        for (i, (values, target, sort, expected)) in enumerate(t_values):
            print(f'- test #{i}: ', end='')
            if sort:
                values = sorted(values, reverse=True)
            subset, trace = solve(values, target)
            if sorted(subset) == sorted(expected):
                print_array(values, subset, None)
            else:
                n_err += 1
                print('  ERROR, expected:', ", ".join(str(x) for x in expected))
                print_array(values, subset, trace)
        self.assertTrue(n_err == 0)

    def test_exact_target(self):
        t_values = [
            # values                    target	sort	expected
            # ----------------------------------------------------------------
            ([2, 6, 3, 5],              10,     False,  [2, 3, 5]),
            ([2, 5, 9, 3, 4],           10,     False,  [2, 3, 5]),
            ([10, 10, 10, 20, 20],      40,     True,   [20, 20]),
            ([10, 10, 10, 20, 20],      40,     False,  [10, 10, 20]),
            ([10, 10, 10, 10, 20, 20],  40,     True,   [20, 20]),
            ([10, 10, 10, 10, 20, 20],  40,     False,  [10, 10, 10, 10])
        ]
        self.run_test(t_values, 'Tests exact targets')

    def test_exact_long(self):
        # sorted: {1: 3, 2: 1, 3: 144, 4: 78, 5: 53, 6: 24, 7: 10, 8: 14, 10: 14, 12: 5, 15: 2, 20: 1, 21: 1}
        data = {4: 78, 10: 14, 5: 53, 1: 3, 6: 24, 12: 5, 8: 14, 15: 2, 3: 144, 2: 1, 21: 1, 20: 1, 7: 10}
        values = []
        for (value, num) in data.items():
            values.extend([value]*num)
        t_values = [
            # values                    target	sort	expected
            # ----------------------------------------------------------------
            (values,                    40,     True,   [10, 15, 15]),
            (values,                    40,     False,  [4, 4, 4, 4, 4, 4, 4, 4, 4, 4])
        ]
        self.run_test(t_values, 'Tests real case')

    # expected to fail for now
    def test_gt_target(self):
        t_values = [
            # values                    target	sort	expected
            # ----------------------------------------------------------------
            ([2, 5, 6, 7],              10, 	False, 	[5, 6]),
        ]
        self.run_test(t_values, 'Tests results > targets')

    def test_timer(self):
        if os.environ.get('TIMEIT', None) is not None:
            timeit.timeit('values = [215, 275, 335, 355, 420, 580]*3\nsolve(values, 1505)',
                          number=1000,
                          setup="from knapsack import solve")

    def test_inspect(self):
        # values = [2, 3, 4, 5, 9]
        values = [1, 2, 3, 5, 11]
        subset, trace = solve(values, 10)
        print_array(values, subset, trace)

if __name__ == '__main__':
    unittest.main()
