#!/usr/bin/python3

import argparse
import textwrap

# Argument handler
parser = argparse.ArgumentParser(
    prog='contenedor.py',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent('''
    NAME
        Python 3 Knapsack Problem Analysis
    SYNOPSIS
        contenedor.py [-h] algorithm -a file.txt
        contenedor.py [-h] algorithm -p capacity N weights benefits iterations
    DESCRIPTION
    METHOD
        Desired algorithm to solve the problem.
        1 = 
        2 = 
        3 = 
    FILE '''))

parser.add_argument('algorithm', metavar='algorithm', type=int,
                    help=textwrap.dedent('''
                    Algorithm to solve the knapsack problem'''))

# parser.add_argument('-a', metavar=', -a', help='Argument to run the program with data on txt file')

parser.add_argument('file', metavar='file.txt', type=argparse.FileType("r"),
                    help='Text file with the knapsack problem in the correct format')

parser.add_argument('iterations', metavar='iterations', type=int,
                    help='Number of times the algorithm should be run')

args = parser.parse_args()


def read_file(file=args.file) -> tuple:
    capacity = int(file.readline())
    weights, benefits = [], []
    for line in file:
        capacity, b = map(int, line.split(","))
        weights.append(capacity)
        benefits.append(b)
    args.file.close()
    return capacity, weights, benefits


def brute_force_knapsack(capacity: int, n: int, weights: list, benefits: list, elements_used: list):
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
        combination_1 = benefits[n - 1] + brute_force_knapsack(capacity - weights[n - 1],
                                                               weights, benefits, n - 1, case_1)
        # don't put anything in case_2 but pass case_2
        combination_2 = brute_force_knapsack(capacity, weights, benefits, n - 1, case_2)
        # get the max situation between the two combinations
        max_value = max(combination_1, combination_2)
        # if this situacion occurs then nth item is included
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


def main():
    capacity, weights, benefits = read_file()
    n = len(benefits)
    elements_used = []
    # memo = [[0 * len(benefits)] * len(weights)]
    # print(top_down_knapsack(capacity, weights, benefits, memo, 0)
    print(brute_force_knapsack(capacity, n, weights, benefits, elements_used))
    elements_used.sort()
    print(elements_used)


if __name__ == "__main__":
    main()
