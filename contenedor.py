#!/usr/bin/python3

import argparse
import textwrap
import numpy as np

# Argument handler
parserA = argparse.ArgumentParser(
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

parserA.add_argument('algorithm', metavar='algorithm', type=int,
                    help=textwrap.dedent('''
                    Algorithm to solve the knapsack problem'''))

parserA.add_argument('-p', dest='random', action='store_true',
                    help='Argument to run the program with random numbers')

parserA.add_argument('capacity', type=int,
                    help=textwrap.dedent('''
                    Max weight of the knapSack '''))

parserA.add_argument('N', type=int,
                    help=textwrap.dedent('''
                    Number of items'''))

parserA.add_argument('weightRanges', type=str,
                    help=textwrap.dedent('''
                    Generate a random weight list between those values'''))

parserA.add_argument('benefitRanges', type=str,
                    help=textwrap.dedent('''
                    Generate a random benefit list between those values'''))

        

# parserA.add_argument('-a', dest='data', action='store_true',
#                     help='Argument to run the program with data on txt file')

parserA.add_argument('iterations', metavar='iterations', type=int,
                    help='Number of times the algorithm should be run')   

# parserB.add_argument('algorithm', metavar='algorithm', type=int,
#                     help=textwrap.dedent('''
#                     Algorithm to solve the brute_force_knapSack problem'''))             

# parserA.add_argument('file', metavar='file.txt', type=argparse.FileType("r"),
#                     help='Text file with the knapsack problem in the correct format')

argsA = parserA.parse_args()


# def read_file(file=args.file) -> tuple:
#     capacity = int(file.readline())
#     weights, benefits = [], []
#     for line in file:
#         capacity, b = map(int, line.split(","))
#         weights.append(capacity)
#         benefits.append(b)
#     args.file.close()
#     return capacity, weights, benefits

def brute_force_knapsack(capacity: int, weights: list, benefits: list, n: int, elements_used: list) -> int:
    # hold the elements of the two combinations  
    case_1 = []
    case_2 = []

    # Base Case
    if n == 0 or capacity <= 0:
        return 0

    # each item's weight can't be more than capacity
    if (weights[n-1] > capacity):
        return brute_force_knapsack(capacity, weights, benefits, n-1, case_2)

    else:
        case_1.append(n) # put the element in case_1 and pass case_1 
        combination_1 = benefits[n-1] + brute_force_knapsack(capacity-weights[n-1], weights, benefits, n-1, case_1)
        # don't put anything in case_2 but pass case_2
        combination_2 = brute_force_knapsack(capacity, weights, benefits, n-1, case_2)
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

def generate_random_numbers(n: int):
    weight_ranges = str(argsA.weightRanges).split(sep="-")
    weight_ranges = list(map(int, weight_ranges))
    benefit_ranges = str(argsA.benefitRanges).split(sep="-")
    benefit_ranges = list(map(int, benefit_ranges))
    weights = list(np.random.randint(low = weight_ranges[0],high= weight_ranges[1], size=n))
    benefits = list(np.random.randint(low = benefit_ranges[0],high = benefit_ranges[1], size=n))
    return weights, benefits

def main():
    # capacity, weights, benefits = read_file()
    # n = len(benefits)
    # elements_used = []
    # # memo = [[0 * len(benefits)] * len(weights)]
    # # print(top_down_knapsack(capacity, weights, benefits, memo, 0)
    # print(brute_force_knapsack(capacity, n, weights, benefits, elements_used))
    # elements_used.sort()
    # print(elements_used)


    # if argsA.data:   
    #     data = parse_file()
    #     capacity = data[0][0]
    #     weights = [row[0] for row in data[1:]]
    #     benefits = [row[1] for row in data[1:]]
    #     n = len(benefits)
    #     elements_used = []
    #     print(brute_force_knapSack(capacity, weights, benefits, n, elements_used))
    #     elements_used.sort()
    #     print(elements_used)
    
    if argsA.random:
        capacity = argsA.capacity
        n = argsA.N 
        weights, benefits = generate_random_numbers(n)
        elements_used = []
        print(brute_force_knapsack(capacity, weights, benefits, n, elements_used))
        elements_used.sort()
        print(elements_used)

        
if __name__ == "__main__":
    main()
