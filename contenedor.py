#!/usr/bin/python3
import copy
import sys
import textwrap
import time
from os.path import exists as file_exists
from statistics import mean
from typing import Tuple, List

import matplotlib.pyplot as plt
from numpy import random
from pandas import DataFrame as Df


# Argument usage helper
def show_usage():
    usage = textwrap.dedent('''
    NAME
        Python 3 container Problem Analysis
    SYNOPSIS
        contenedor.py [-h] algorithm -a file.txt iterations
        contenedor.py [-h] algorithm -p capacity N weights benefits iterations
    DESCRIPTION
        Solves a given container problem in a file or a random generated one
        with the possibility of executing a single or multiple algorithms.
    ALGORITHM
        Desired algorithm to solve the problem.
        1 = Brute force algorithm
        2 = Bottom up algorithm
        3 = Top Down using memoization algorithms
        4 = Compare/Run all algorithms
    FILE 
        Text file with the container problem in the correct format
    CAPACITY
        Max weight of the container
    N
        Number of items
    WEIGHT RANGES
        Generate a random weight list between those values
    BENEFIT RANGES
        Generate a random benefit list between those values
    ITERATIONS
        Number of times the algorithm should be run
    ''')
    print(usage)


# Remove program name from arguments
args = sys.argv[1:]

# Algorithm constants
BRUTE_FORCE = 1
BOTTOM_UP = 2
TOP_DOWN = 3
COMPARE_ALL = 4


def brute_force_container(capacity: int, weights: list, benefits: list,
                          current: int, elements_used: list) -> Tuple[int, List]:
    """
    :param capacity: maximum weight of the container
    :param weights: different weights of the elements
    :param benefits: benefits of every element
    :param current: current index being compared in the container
    :param elements_used: element the algorithm choose
    :return: the max value and the list of selected items
    """
    # hold the included elements in the container
    included = []
    # Base Case
    if current == 0 or capacity <= 0:
        return 0, []

    # each item's weight can't be more than capacity
    if weights[current - 1] > capacity:
        return brute_force_container(capacity, weights, benefits, current - 1, elements_used)

    included_benefit, included = brute_force_container(capacity - weights[current - 1],
                                                       weights, benefits, current - 1, included)
    included_benefit += benefits[current - 1]
    included.append(current)  # put the element in included and pass included

    # don't put anything in not_included but pass not_included
    not_included_benefit, not_included = brute_force_container(capacity, weights,
                                                               benefits, current - 1, elements_used)

    # if this situation occurs then nth item is included
    if included_benefit >= not_included_benefit:
        best_benefit = included_benefit
        elements_used = included
    else:
        best_benefit = not_included_benefit
        elements_used = not_included

    return best_benefit, elements_used


def bottom_up_container(capacity: int, weights: list,
                        benefits: list, n: int) -> Tuple[int, list]:
    """
    :param capacity: maximum weight of the container
    :param weights: different weights of the elements
    :param benefits: benefits of every element
    :param n: num of elements
    :return: the max value and the list of selected items
    """
    if n == 0 or capacity <= 0:
        return 0, []

    elements_used = []
    # previously calculated benefits
    memo = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] > w:
                memo[i][w] = memo[i - 1][w]
            else:
                if benefits[i - 1] + memo[i - 1][w - weights[i - 1]] > memo[i - 1][w]:
                    memo[i][w] = benefits[i - 1] + memo[i - 1][w - weights[i - 1]]
                else:
                    memo[i][w] = memo[i - 1][w]    # puts the previous element

    w = capacity
    i = n
    # check from bottom to top
    for _ in range(len(memo)):
        if memo[i][w] != memo[i - 1][w] and i != 0:
            elements_used += [i]
            i -= 1
            w = w - weights[i]
        else:
            i -= 1
    max_value = memo[n][capacity]
    return max_value, elements_used


def top_down_container(capacity: int, weights: list, benefits: list, current: int, memo: list):
    """
    :param capacity: maximum weight of the container
    :param weights: different weights of the elements
    :param benefits: benefits of every element
    :param current: current index being compared in the container
    :param memo: memory of values and items already calculated
    :return: the max value and the list of selected items
    """

    if capacity <= 0 or current >= len(benefits):
        return 0, []

    if memo[current][capacity] is not None:
        return memo[current][capacity]

    included_benefit, included = -1, []
    if weights[current] <= capacity:
        included_benefit, included = top_down_container(capacity - weights[current],
                                                        weights, benefits,
                                                        current + 1, memo)
        included_benefit += benefits[current]

    not_included_benefit, not_included = \
        top_down_container(capacity, weights, benefits, current + 1, memo)

    if included_benefit >= not_included_benefit:
        elements_used = copy.deepcopy(included)
        elements_used.append(current + 1)
        memo[current][capacity] = included_benefit, elements_used

    else:
        elements_used = copy.deepcopy(not_included)
        memo[current][capacity] = not_included_benefit, elements_used

    return memo[current][capacity]


def run_from_file() -> None:
    """
    Get data of file and initializes variables
    :return: None
    """
    capacity, weights, benefits = generate_problem_from_file()
    n = len(benefits)
    algorithm = int(args[0])
    iterations = int(args[3])
    print(f'Capacity: {capacity} N: {n} Weights: {weights} Benefits: {benefits}')
    container_params = (capacity, weights, benefits, n)
    choose_measure(algorithm, iterations, container_params)


def generate_problem_from_file() -> tuple:
    """
    Read data from file and separate in list weights and benefits
    :return: tuple with values (capacity, list of weights and benefits)
    """
    with open(args[2], 'r', encoding='UTF8') as file:
        capacity = int(file.readline())
        weights, benefits = [], []
        for line in file:
            weight, benefit = map(int, line.split(","))
            weights.append(weight)
            benefits.append(benefit)
    file.close()
    return capacity, weights, benefits


def run_from_random() -> None:
    """
    Generate random elements and initializes variables
    :return: None
    """
    algorithm = int(args[0])
    capacity = int(args[2])
    n = int(args[3])
    iterations = int(args[6])
    weights, benefits = generate_problem_from_random(n)
    print(f'Capacity: {capacity} N: {n} Weights: {weights} Benefits: {benefits}')
    container_params = (capacity, weights, benefits, n)
    choose_measure(algorithm, iterations, container_params)


def generate_problem_from_random(n: int) -> tuple:
    """
    Generate random elements with the intervals specified
    :param n: num of elements
    :return: tuple with the list of weights and benefits
    """
    low_weight, high_weight = map(int, args[4].split(sep="-"))
    low_benefit, high_benefit = map(int, args[5].split(sep="-"))
    rng = random.default_rng()
    weights = list(rng.integers(low=low_weight, high=high_weight, size=n))
    benefits = list(rng.integers(low=low_benefit, high=high_benefit, size=n))
    return weights, benefits


def measure(algorithm: callable, parameters: tuple,
            iterations: int) -> float:
    """
    Run time of the algorithm run
    :param algorithm: information of the algorithm
    :param parameters: container parameters used in the algorithm
    :param iterations: number of times the code must be run
    :return: a num with the mean of runtimes
    """
    result, items_used = [], []
    runtimes = []
    for _ in range(iterations):
        begin = time.time()
        result, items_used = algorithm(*parameters)
        end = time.time()
        runtime = end - begin
        runtimes.append(runtime)
    print(f'Result: {result}\nItems used: {items_used}')
    return mean(runtimes)


def measure_brute(iterations: int, container_params: tuple) -> float:
    """
    Calculate the mean time and the maximum result for the container
    :param iterations: number of times the code must be run
    :param container_params: data of the algorithm
    :return: a num with the mean of runtimes
    """
    print('Measuring brute force algorithm...')
    brute_params = *container_params, []
    measures = measure(brute_force_container, brute_params, iterations)
    return measures


def measure_bottom_up(iterations: int, container_params: tuple) -> float:
    """
    Calculate the mean time and the maximum result for the container
    :param iterations: number of times the code must be run
    :param container_params: data of the algorithm
    :return: a num with the mean of runtimes
    """
    print('Measuring bottom up algorithm...')
    measures = measure(bottom_up_container, container_params, iterations)
    return measures


def measure_top_down(iterations: int, container_params: tuple) -> float:
    """
    Calculate the mean time and the maximum result for the container
    :param iterations: number of times the code must be run
    :param container_params: data of the algorithm
    :return: a num with the mean of runtimes
    """
    capacity, weights, benefits, _ = container_params
    memo = [[None for _ in range(capacity + 1)] for _ in range(len(benefits))]
    top_down_params = capacity, weights, benefits, 0, memo
    print('Measuring top down algorithm...')
    measures = measure(top_down_container, top_down_params, iterations)
    return measures


def generate_figure_filename() -> str:
    """
    checks if the filename exists
    :return: string with the name of the new file
    """
    i = 1
    name = 'result_graphs/algorithms_runtimes.png'
    while file_exists(name):
        name = f'result_graphs/algorithms_runtimes({i}).png'
        i += 1
    return name


def graph_data(titles: list, data: list) -> None:
    """
    shows the bar graph with the average results
    :param titles: Name of the algorithms['Brute', 'Bottom Up', 'Top Down']
    :param data: average list of the three algorithms
    :return: None
    """
    plt.bar(titles, data)  # algorithms data
    plt.ylabel('Average of algorithm times')  # Text Y
    plt.xlabel('Types of algorithms')  # Text X
    plt.title('Average times')  # Text Title
    plt.savefig(generate_figure_filename())  # Save graphic


def choose_measure(algorithm: int, iterations: int,
                   container_params: tuple) -> None:
    """
    Choose measure and calculate the time
    :param algorithm: num with the option of algorithm
    :param iterations: number of times the code must be run
    :param container_params: data of the algorithm
    :return: None
    """
    measurers = {
        BRUTE_FORCE: [measure_brute],
        BOTTOM_UP: [measure_bottom_up],
        TOP_DOWN: [measure_top_down],
        COMPARE_ALL: [measure_brute, measure_bottom_up, measure_top_down]
    }.get(algorithm)

    measurements = []
    for measurer in measurers:
        measurements += [measurer(iterations, container_params)]

    if algorithm == COMPARE_ALL:
        titles = ['Brute Force', 'Bottom Up', 'Top Down']
        print("Average times: " + str(measurements))
        print(Df(data=measurements, index=titles, columns=["Averages Times"]))
        graph_data(titles, measurements)
    else:
        print("Average time: " + str(measurements))


def main() -> None:
    """
    Main function choose if run from the file or random data
    :return: None
    """
    if '-a' in args:
        run_from_file()

    elif '-p' in args:
        run_from_random()

    else:
        show_usage()


if __name__ == "__main__":
    main()
