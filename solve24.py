#!/usr/bin/env python

import sys
from argparse import ArgumentParser
from typing import List, Dict
from functools import lru_cache
import copy

TARGET = 24
SKIP = 'skip'


def main():
    args = init_param()

    nums = args.numbers
    solution = solve(nums)
    if not solution:
        print(f'No solution found for {nums}')
        return

    print(f'Input numbers: {nums}')
    pretty_print(solution, nums)


def backtrack(a: Dict[str, float], solution: List[List[str]], input_: List[int]) -> None:
    """ Runs DFS search and compute all possible results.
    Args:
        a: all possible values from last calculation.
        solution: solutions found
        input_: input numbers

    Returns:
        None
    """

    if not input_:
        # Check if we have got 24.
        process_result(a, solution)
        return

    for i in list(range(len(input_))):
        # make_move
        num = input_.pop(i)
        current_state = copy.deepcopy(a)
        a = construct_candidates(a, num)

        # backtrack
        backtrack(a, solution, input_)

        # unmake_move
        input_.insert(i, num)
        a = current_state


def pretty_print(solution: List[str], nums: List[int]) -> None:
    """Print the solutions nicely, lined up in the order of original input numbers.

    Args:
        solution: a list of operation history on the numbers
        nums: the original input of 4 numbers.

    Returns:

    """
    input_str = list(map(str, nums))
    input_str.append(SKIP)

    i = 0
    printed = []
    for prefix in input_str:
        if prefix in printed:
            continue

        for s in solution:
            steps = s.split(',')
            pretty_solution = ''
            if steps[0] != prefix:
                continue

            for j, val in enumerate(steps):
                if j == 0:
                    pretty_solution += '{:>4s},'.format(val)
                elif j in [1, 2]:
                    pretty_solution += '{:>18s},'.format(val)
                elif j == 3:
                    pretty_solution += '{:>18s}'.format(val)

            i += 1
            print('Solution {:2d}:  {}'.format(i, pretty_solution))

        printed.append(prefix)


def process_result(values: Dict[str, float], solution: List[str]) -> None:
    """Get operation histories if exist, and add to the solution list if they're new.

    Args:
        values:
        solution:

    Returns:

    """
    result = [history for history, val in values.items() if val == TARGET]

    if result:
        solution.extend([history for history in result if history not in solution])


def construct_candidates(a: Dict, num: float) -> Dict[str, float]:
    """This function performs all 4 possible operations for numbers in a with num, and returns newly
    calculated result.

    Args:
        a: partial result from last calculation, in pairs of (value, history).
        num: int or float, next number to calculate.

    Returns:

    """
    candidates = {}

    if not a:
        candidates = {f'{num}': num}

    else:
        for history, val in a.items():
            result = compute(val, num)

            for new_hist, new_val in result.items():
                new_key = f'{history}, {new_hist}'
                candidates[new_key] = new_val

    return candidates


@lru_cache(None)
def compute(a: float, b: float) -> Dict[str, float]:
    """Get all possible results from 2 input numbers (int or float)

    Args:
        a: first number
        b: second number

    Returns:
        A dict, where keys are strings of operation history, and its corresponding output value.

    """
    result = list()
    result.append((a + b, f'{a} + {b} = {a + b}'))
    result.append((a * b, f'{a} * {b} = {a * b}'))
    result.append((a - b, f'{a} - {b} = {a - b}'))
    result.append((b - a, f'{b} - {a} = {b - a}'))

    if b != 0:
        result.append((a / b, f'{a} / {b} = {a / b}'))
    if a != 0:
        result.append((b / a, f'{b} / {a} = {b / a}'))

    return {history: val for val, history in result}


@lru_cache(None)
def compute_groups(g1: List[int], g2: List[int]) -> List[str]:
    """Get all possible values from 2 groups of 2 numbers.

    Args:
        g1: first group
        g2: second group

    Returns:
        A list of solutions in strings.

    """
    a, b = g1
    c, d = g2
    output1 = compute(a, b)
    output2 = compute(c, d)

    solution = list()
    for hist1, val1 in output1.items():
        for hist2, val2 in output2.items():
            result = compute(val1, val2)
            solution.extend([f'skip, {hist1}, {hist2}, {hist}' for hist, val in result.items()
                             if val == TARGET])

    return solution


def solve(nums: List[int]) -> List[str]:
    """

    Args:
        nums: an array of 4 positive integers

    Returns:
        A list of solutions in 4 steps to make 24.

    """
    # Numbers used so far
    a = {}

    # Solutions for this game
    solution = []

    # Backtrack
    backtrack(a, solution, nums)

    # Find out other solutions by dividing numbers into two groups of two numbers.
    n1, n2, n3, n4 = nums
    groups = [[(n1, n2), (n3, n4)],
              [(n1, n3), (n2, n4)],
              [(n1, n4), (n2, n3)]
             ]

    for g1, g2 in groups:
        result = compute_groups(g1, g2)
        solution.extend([s for s in result if s not in solution])

    return solution


def init_param():
    sample_usage = f'Sample usage: {sys.argv[0]} -n 2, 3, 4, 8'
    parser = ArgumentParser(description='The 24 Game solver using backtrack algorithm',
                            epilog=sample_usage)

    parser.add_argument('-n', '--numbers', metavar='num', type=int, nargs='+',
                        help='4 positive numbers to play.')

    args = parser.parse_args()
    count = len(args.numbers)
    if count < 4:
        sys.stderr.write(f'You\'ve specified {count} numbers, please add {4 - count} more number(s).\n')
        sys.exit(1)

    return args


if __name__ == '__main__':
    main()
