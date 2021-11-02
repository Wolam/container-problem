#!/usr/bin/python3

import argparse
import textwrap

# Argument handler
parser = argparse.ArgumentParser(
    prog='contenedor.py',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent('''
    NAME
        Python 3 brute_force_knapSack Problem Analysis
    SYNOPSIS
        contenedor.py [-h] algorithm -a file.txt
        contenedor.py [-h] algorithm -p W N weights benefits iterations
    DESCRIPTION
    METHOD
        Desired algorithm to solve the problem.
        1 = 
        2 = 
        3 = 
    FILE '''))

parser.add_argument('algorithm', metavar='algorithm', type=int,
                    help=textwrap.dedent('''
                    Algorithm to solve the brute_force_knapSack problem'''))

# parser.add_argument('-a', metavar=', -a', help='Argument to run the program with data on txt file')

parser.add_argument('file', metavar='file.txt', type=argparse.FileType("r"),
                    help='Text file with the brute_force_knapSack problem in the correct format')

parser.add_argument('iterations', metavar='iterations', type=int,
                    help='Number of times the algorithm should be run')

args = parser.parse_args()

def parse_file(file=args.file) -> list:
    arr = []
    for line in file:
        data = line.replace('\n', "").split(",")
        arr.append(list(map(int, data)))
    args.file.close()
    return arr

def brute_force_knapSack(W, weights, benefits, n, elements_used):
    # hold the elements of the two combinations  
    case_1 = []
    case_2 = []
 
    # Base Case
    if n == 0 or W <= 0:
        return 0
 
    # each item's weight can't be more than W
    if (weights[n-1] > W):
        return brute_force_knapSack(W, weights, benefits, n-1, case_2)

    else:
        case_1.append(n) # put the element in case_1 and pass case_1 
        combination_1 = benefits[n-1] + brute_force_knapSack(W-weights[n-1], weights, benefits, n-1, case_1)
        # don't put anything in case_2 but pass case_2
        combination_2 = brute_force_knapSack(W, weights, benefits, n-1, case_2)
        # get the max situation between the two combinations
        max_value = max(combination_1, combination_2)
        # if this situacion occurs then nth item is included
        if max_value == combination_1:
            elements_used += case_1
        else:
            elements_used += case_2
        return max_value

def main():
    data = parse_file()
    W = data[0][0]
    weights = [row[0] for row in data[1:]]
    benefits = [row[1] for row in data[1:]]
    n = len(benefits)
    elements_used = []
    print(brute_force_knapSack(W, weights, benefits, n, elements_used))
    elements_used.sort()
    print(elements_used)

if __name__ == "__main__":
    main()
