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
                    Algorithm to solve the knapsack problem'''))

parser.add_argument('file', metavar='file.txt', type=argparse.FileType("r"),
                    help='Text file with the knapsack problem in the correct format')

args = parser.parse_args()


def main():
    pass


if __name__ == "__main__":
    main()
