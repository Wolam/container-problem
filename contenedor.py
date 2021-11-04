#!/usr/bin/python3

import sys
import textwrap
import numpy as np

# Algorithm constants
BRUTE_FORCE = 1
BOTTOM_UP = 2
TOP_DOWN = 3
ALL = 4


# Argument usage helper
def show_usage():
    help = textwrap.dedent('''
    NAME
        Python 3 Knapsack Problem Analysis
    SYNOPSIS
        contenedor.py [-h] algorithm -a file.txt iterations
        contenedor.py [-h] algorithm -p capacity N weights benefits iterations
    DESCRIPTION
    
    ALGORITHM
        Desired algorithm to solve the problem.
        1 = 
        2 = 
        3 = 
        4 =
    FILE 
        Text file with the knapsack problem in the correct format
    CAPACITY
        Max weight of the knapsack
    N
        Number of items
    WEIGHT RANGES
        Generate a random weight list between those values
    BENEFIT RANGES
        Generate a random benefit list between those values
    ITERATIONS
        Number of times the algorithm should be run
    ''')
    print(help)


# Remove program name from arguments
args = sys.argv[1:]


def brute_force_knapsack(capacity: int, weights: list, benefits: list, n: int, elements_used: list) -> int:
    # hold the elements of the two combinations  
    case_1 = []
    case_2 = []

    # Base Case
    if n == 0 or capacity <= 0:
        return 0

    # each item's weight can't be more than capacity
    if weights[n - 1] > capacity:
        return brute_force_knapsack(capacity, weights, benefits, n - 1, case_2)

    else:
        case_1.append(n)  # put the element in case_1 and pass case_1
        combination_1 = benefits[n - 1] + brute_force_knapsack(capacity - weights[n - 1], weights, benefits, n - 1,
                                                               case_1)
        # don't put anything in case_2 but pass case_2
        combination_2 = brute_force_knapsack(capacity, weights, benefits, n - 1, case_2)
        # get the max situation between the two combinations
        max_value = max(combination_1, combination_2)
        # if this situation occurs then nth item is included
        if max_value == combination_1:
            elements_used += case_1
        else:
            elements_used += case_2
        return max_value


def top_down_knapsack(capacity: int, weights: list, benefits: list, memo: list, current: int):
    if capacity <= 0 or current >= len(benefits):
        return 0

    if memo[current][capacity] is not None:
        return memo[current][capacity]

    item_taken = 0
    if weights[current] <= capacity:
        item_taken = benefits[current] + top_down_knapsack(memo, weights, benefits,
                                                           capacity - weights[current], current + 1)
    item_not_taken = top_down_knapsack(memo, weights, benefits, capacity, current + 1)

    memo[current][capacity] = max(item_not_taken, item_taken)
    return memo[current][capacity]


def run_from_file():
    capacity, weights, benefits = generate_problem_from_file()
    n = len(benefits)
    elements_used = []
    # TODO RUN THE DESIRED ALGORITHM(S) HERE
    print(f'cap = {capacity} n = {n} weights = {weights} benefits = {benefits}')


def generate_problem_from_file() -> tuple:
    print(f'file is {args[2]}')
    file = open(args[2], 'r')
    capacity = int(file.readline())
    weights, benefits = [], []
    for line in file:
        capacity, b = map(int, line.split(","))
        weights.append(capacity)
        benefits.append(b)
    file.close()
    return capacity, weights, benefits


def run_from_random():
    capacity = int(args[2])
    n = int(args[3])
    weights, benefits = generate_problem_from_random(n)
    # TODO RUN THE DESIRED ALGORITHM(S) HERE
    print(f'cap = {capacity} n = {n} weights = {weights} benefits = {benefits}')


def generate_problem_from_random(n: int) -> tuple:
    low_weight, high_weight = map(int, args[4].split(sep="-"))
    low_benefit, high_benefit = map(int, args[5].split(sep="-"))
    rng = np.random.default_rng()
    weights = list(rng.integers(low=low_weight, high=high_weight, size=n))
    benefits = list(rng.integers(low=low_benefit, high=high_benefit, size=n))
    return weights, benefits


def main():
    if '-a' in args:
        run_from_file()

    elif '-p' in args:
        run_from_random()

    else:
        show_usage()


if __name__ == "__main__":
    main()
