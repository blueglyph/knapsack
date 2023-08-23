import os, unittest, timeit
from knapsack import solve_le, solve_ge, values_from_dict


def print_array(subset = None, msg ='result:'):
    if subset is not None:
        print(f'  {msg}', ', '.join(str(x) for x in subset))
    elif msg:
        print(msg)


class TestKnapsack(unittest.TestCase):
    def run_test(self, algorithms, t_values, title='Test'):
        print(f'\n{title}')
        n_err = 0
        for (j, solve) in enumerate(algorithms):
            if len(algorithms) > 1:
                print(f'algorithm #{j}')
            for (i, (values, target, sort, expected)) in enumerate(t_values):
                print(f'- test #{i}: ', end='')
                if sort:
                    values = sorted(values, reverse=True)
                subset = solve(values, target)
                if sorted(subset) == sorted(expected):
                    print_array(subset)
                else:
                    n_err += 1
                    print('  ERROR, expected:', ", ".join(str(x) for x in expected))
                    print_array(subset)
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

        self.run_test([solve_le, solve_ge], t_values, 'Tests exact targets')

    def test_lt_target(self):
        t_values = [
            # values                    target	sort	expected
            # ----------------------------------------------------------------
            ([2, 6, 3, 5],              15,     True,   [6, 5, 3]),
            ([10, 10, 10, 20, 20],      45,     True,   [20, 20]),
            ([10, 10, 10, 10, 20, 20],  55,     True,   [20, 20, 10]),
            ([20, 30],                  10,     True,   []),
            ([1, 2],                    10,     True,   [2, 1])
        ]
        self.run_test([solve_le], t_values, 'Tests results < targets')

    # expected to fail for now
    def test_gt_target(self):
        t_values = [
            # values                    target	sort	expected
            # ----------------------------------------------------------------
            ([2, 5, 6, 7],              10, 	True,   [6, 5]),
            ([10, 10, 10, 20, 20],      45,     True,   [20, 20, 10]),
            ([10, 10, 10, 10, 20, 20],  55,     True,   [20, 20, 10, 10]),
            ([20, 30],                  10,     True,   [20]),
            ([1, 2],                    10,     True,   [])
        ]
        self.run_test([solve_ge], t_values, 'Tests results > targets')

    def test_exact_long(self):
        # sorted: {1: 3, 2: 1, 3: 144, 4: 78, 5: 53, 6: 24, 7: 10, 8: 14, 10: 14, 12: 5, 15: 2, 20: 1, 21: 1}
        data = {4: 78, 10: 14, 5: 53, 1: 3, 6: 24, 12: 5, 8: 14, 15: 2, 3: 144, 2: 1, 21: 1, 20: 1, 7: 10}
        values = values_from_dict(data)
        t_values = [
            # values                    target	sort	expected
            # ----------------------------------------------------------------
            (values,                    40,     True,   [10, 15, 15]),
            (values,                    40,     False,  [4, 4, 4, 4, 4, 4, 4, 4, 4, 4])
        ]
        self.run_test([solve_le, solve_ge], t_values, 'Tests real case')

    def test_iterations(self):
        def remove_from_chest(chest: dict[int], subset: tuple[int]):
            for value in subset:
                chest[value] -= 1
        data = {40: 16, 21: 1, 20: 2, 15: 2, 12: 5, 10: 18, 8: 15, 7: 11, 6: 36, 5: 57, 4: 112, 3: 102, 2: 2, 1: 1}
        expected = [*[40]*55, *[42]*5]
        result = []
        it = 1
        while True:
            print(f'Iteration #{it}: {data}')
            values = sorted(values_from_dict(data), reverse=True)
            subset = solve_ge(values, 40)
            total = sum(subset)
            print(f'-> {total} in {subset}')
            if len(subset) == 0:
                break
            result.append(total)
            remove_from_chest(data, subset)
            it += 1
        self.assertEqual(result, expected)

    def test_timer(self):
        if os.environ.get('TIMEIT', None) is not None:
            timeit.timeit('values = [215, 275, 335, 355, 420, 580]*3\nsolve_le(values, 1505)',
                          number=1000,
                          setup="from knapsack import solve_le")

    def test_inspect(self):
        # values = [2, 3, 4, 5, 9]
        values = [1, 2, 3, 5, 11]
        subset = solve_le(values, 10)
        print_array(subset)


if __name__ == '__main__':
    unittest.main()
