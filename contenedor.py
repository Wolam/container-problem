#!/usr/bin/python3

from statistics import mean
import sys
import textwrap
import numpy as np
import time
import matplotlib.pyplot as plt

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

# Algorithm constants
BRUTE_FORCE = 1
BOTTOM_UP = 2
TOP_DOWN = 3
COMPARE_ALL = 4


def brute_force_knapsack(capacity: int, weights: list, benefits: list, n: int, elements_used: list) -> int:
    # hold the elements of the two combinations  
    included = []
    # Base Case
    if n == 0 or capacity <= 0:
        return 0, []

    # each item's weight can't be more than capacity
    if weights[n - 1] > capacity:
        return brute_force_knapsack(capacity, weights, benefits, n - 1, elements_used)

    else:
        combination_1, included = brute_force_knapsack(capacity - weights[n - 1], weights, benefits, n - 1,
                                                               included)
        combination_1 += benefits[n - 1]
        included.append(n)  # put the element in included and pass included

        # don't put anything in not_included but pass not_included
        combination_2, not_included = brute_force_knapsack(capacity, weights, benefits, n - 1, elements_used)
        # get the max situation between the two combinations
        max_value = max(combination_1, combination_2)
        # if this situation occurs then nth item is included

        if max_value == combination_1:
            elements_used = included
        else:
            elements_used = not_included

        return max_value, elements_used

def bottom_up_knapsack(capacity: int, weights: list, benefits: list, n: int, elements_used: list) -> int:
    V = [[0 for _ in range(capacity+1)] for _ in range(n + 1)]

    for i in range(1, n+1):
        for w in range(1, capacity+1):
            if weights[i-1] > w:
                V[i][w] = V[i-1][w]
            else:
                if benefits[i-1] + V[i-1][w-weights[i-1]] > V[i-1][w]:
                   V[i][w] = benefits[i-1] + V[i-1][w-weights[i-1]]
                else:
                   V[i][w] = V[i-1][w]

    max_value = V[n][capacity]
    w = capacity
    i = n
    elements_used = []
    for _ in range(len(V)):
        if V[i][w] != V[i-1][w]:
            elements_used += [i]
            i  = i -1
            w = w - weights[i]
        else:
            i = i - 1

    return max_value, elements_used


def top_down_knapsack(capacity: int, weights: list, benefits: list, current: int, memo: list, elements_used: list):
    if capacity <= 0 or current == len(benefits):
        return 0, []

    if memo[current][capacity] is not None:
        return memo[current][capacity]

    included_benefit, included = -1, []
    if weights[current] <= capacity:
        included_benefit, included = top_down_knapsack(capacity - weights[current],
                                                       weights, benefits,
                                                       current + 1, memo, elements_used)
        included_benefit += benefits[current]
        included.append(current + 1)

    not_included_benefit, not_included = \
        top_down_knapsack(capacity, weights, benefits, current + 1, memo, elements_used)

    if included_benefit >= not_included_benefit:
        elements_used = included
        memo[current][capacity] = included_benefit, elements_used

    else:
        elements_used = not_included
        memo[current][capacity] = not_included_benefit, elements_used

    return memo[current][capacity]


def run_from_file():
    capacity, weights, benefits = generate_problem_from_file()
    n = len(benefits)
    algorithm = int(args[0])
    iterations = int(args[3])
    print(f'Capacity: {capacity} N: {n} Weights: {weights} Benefits: {benefits}')
    knapsack_params = (capacity, weights, benefits, n)
    choose_measure(algorithm, iterations, knapsack_params)


def generate_problem_from_file() -> tuple:
    file = open(args[2], 'r')
    capacity = int(file.readline())
    weights, benefits = [], []
    for line in file:
        w, b = map(int, line.split(","))
        weights.append(w)
        benefits.append(b)
    file.close()
    return capacity, weights, benefits


def run_from_random():
    algorithm = int(args[0])
    capacity = int(args[2])
    n = int(args[3])
    iterations = int(args[6])
    weights, benefits = generate_problem_from_random(n)
    print(f'Capacity: {capacity} N: {n} Weights: {weights} Benefits: {benefits}')
    knapsack_params = (capacity, weights, benefits, n)
    choose_measure(algorithm, iterations, knapsack_params)


def generate_problem_from_random(n: int) -> tuple:
    low_weight, high_weight = map(int, args[4].split(sep="-"))
    low_benefit, high_benefit = map(int, args[5].split(sep="-"))
    rng = np.random.default_rng()
    weights = list(rng.integers(low=low_weight, high=high_weight, size=n))
    benefits = list(rng.integers(low=low_benefit, high=high_benefit, size=n))
    return weights, benefits


def measure(num_algorithm, algorithm, iterations: int) -> list:
    runtimes, result, items_used = [], [], []
    for _ in range(iterations):
        begin = time.time()
        result, items_used = algorithm
        end = time.time()
        runtime = end - begin
        runtimes.append(runtime)
    items_used.reverse()
    print(f'Algorithm: {num_algorithm}\n Result: {result}\nItems used: {items_used}')
    return runtimes

def measure_brute(iterations: int, knapsack_params):
    measures = measure(1, brute_force_knapsack(*knapsack_params, elements_used=[]), iterations)
    return measures

def measure_bottom_up(iterations: int, knapsack_params):
    measures = measure(2, bottom_up_knapsack(*knapsack_params, elements_used=[]), iterations)
    return measures

def measure_top_down(iterations: int, knapsack_params):
    capacity, weights, benefits, _ = knapsack_params
    memo = [[None for _ in range(capacity + 1)] for _ in range(len(benefits))]
    knapsack_params = capacity, weights, benefits, 0, memo
    measures = measure(3, top_down_knapsack(*knapsack_params, elements_used=[]), iterations)
    return measures


def grafic_data(x, y):
    plt.bar(x, y)
    plt.ylabel('Average of algorithm times') ## Text Y
    plt.xlabel('Types of algoritms')   ## Text X
    plt.title('Average times of size: ') ## Text Title
    plt.show()   ## Show grafic

def choose_measure(algorithm: int, iterations: int, knapsack_params: tuple):
    measurers = {
        BRUTE_FORCE: {measure_brute},
        BOTTOM_UP: {measure_bottom_up},
        TOP_DOWN: {measure_top_down},
        COMPARE_ALL: {measure_brute, measure_bottom_up, measure_top_down}
    }.get(algorithm)

    measurements = []
    for measurer in measurers:
        measurements += measurer(iterations, knapsack_params)

    if algorithm == COMPARE_ALL:
        average = []
        final_list = lambda measurements, iterations: [measurements[i:i + iterations] for i in range(0, len(measurements), iterations)]
        list_times = final_list(measurements, iterations)
        for i in range(len(list_times)):
            average.append(sum(list_times[i]) / len(list_times[i]))

        print("Average", str(average))
        #print(measurements)
        x = ['Top Down', 'Bottom Up', 'Brute']
        y = average
        #grafic_data(x, y)

    else:
        average = sum(measurements) / len(measurements)
        print("Average", str(average))
        #print(measurements)


def main():
    if '-a' in args:
        run_from_file()

    elif '-p' in args:
        run_from_random()

    else:
        show_usage()


if __name__ == "__main__":
    main()
