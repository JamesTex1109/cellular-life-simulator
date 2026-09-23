#!/usr/bin/env python3
"""
=============================================================================
Title : cellular_life.py
Description : Cellular Life Simulator for single line testing
Author : James Carrington
Date : 4/20/2026
Version : 1.0
Usage : python3 cellular_life.py -i <input_file> -o <output_file> -p <processor_count>
Notes : Requires math, os, sys, and argparse modules.
Python Version: 3.x.x
=============================================================================
"""
import argparse
import math
import os
import sys

#<i> input file path
def valid_input(file_path):
    if not file_path:
        raise argparse.ArgumentTypeError(f"Input file Error")
    if not os.path.isfile(file_path):
        raise argparse.ArgumentTypeError(f"Input file Error")
    if not os.access(file_path, os.R_OK):
        raise argparse.ArgumentTypeError(f"Input file Error")
    return file_path

#<o> output file path
def valid_output(file_path):
    if not file_path:
        raise argparse.ArgumentTypeError(f"Output file Error")
    
    dir_name = os.path.dirname(file_path)
    if dir_name and not os.path.exists(dir_name):
        raise argparse.ArgumentTypeError(f"Directory Error file doesn't exist.")
    
    return file_path

#<p> validate processor number
def valid_processor_number(value):
    try:
        num = int(value)
        if num <= 0:
            raise argparse.ArgumentTypeError(f"Error:Processor number must be positive")
        return num
    except ValueError:
        raise argparse.ArgumentTypeError(f"Error: Processor number must be a number")
    
#Matriix load function
def load_matrix(file_path):
        matrix = []
        with open(file_path, 'r') as file:
            for line in file:
                row = list(line.strip())
                matrix.append(row)
        return matrix
    
#Print matrix function
def isPrime(number):
        if number <= 1:
            return False
        for i in range(2, math.isqrt(number) + 1):
            if number % i == 0:
                return False
        return True
    
#Fibonacci function
def is_perfect_square(n):
    s = int(math.sqrt(n))
    return s * s == n
def is_fibonacci(n):
    if n < 0:
        return False
    return is_perfect_square(5 * n * n + 4) or is_perfect_square(5 * n * n - 4)

#Power of 2 function
def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0

#Start of stage 1.3
#Rule 1-3
def get_symbol_value(symbol):
    values = {
        'O': 3, 
        'o': 1,
        'X': -3,
        'x': -1,
        '.': 0,
    }
    return values.get(symbol, 0)
def calculate_influence(matrix, r, c):
    inner_sum = 0
    outer_sum = 0

    rows = len(matrix)
    cols = len(matrix[0])
#Rule 1
    for dr in range(-2, 3):
        for dc in range(-2, 3):
            if dr == 0 and dc == 0:
                continue
            nr = r + dr
            nc = c + dc
            if nr < 0 or nc < 0 or nr >= rows or nc >= cols:
                continue
            
            score = get_symbol_value(matrix[nr][nc])
            if abs(dr) <= 1 and abs(dc) <= 1:
                inner_sum += score
            else:
                outer_sum += score 
    #Rule 3
    influence_score = (2 * inner_sum) + outer_sum

    return influence_score, inner_sum, outer_sum

#Main function and rule 4-8  
def main():
    print("Cellular Life Simulator")
    parser = argparse.ArgumentParser(description="Cellular Life Simulator")
    parser.add_argument("-i", type=valid_input, required=True)
    parser.add_argument("-o", type=valid_output, required=True)
    parser.add_argument("-p", type=valid_processor_number, default=1)

    args = parser.parse_args()
    

    input_file = args.i
    output_file = args.o
    process_count = args.p
    
    matrix = load_matrix(input_file)

    # Validate input and output file paths
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        sys.exit(1)
    
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        print(f"Error: Output directory '{output_dir}' does not exist.")
        sys.exit(1)
#Rule 4-8
    for iteration in range(100):
        next_matrix = [row.copy() for row in matrix]
        for r in range(len(matrix)):
            for c in range(len(matrix[0])):
                current_symbol = matrix[r][c]
                influence_score, inner_sum, outer_sum = calculate_influence(
                    matrix, r, c)
                # rule 4
                if current_symbol == 'O':
                    if is_power_of_two(influence_score):
                        next_matrix[r][c] = '.'
                    elif outer_sum < 2:
                        next_matrix[r][c] = 'o'
                    else:
                        next_matrix[r][c] = 'O'
                        # rule 5
                elif current_symbol == 'o':
                    if is_fibonacci(inner_sum):
                        next_matrix[r][c] = 'O'
                    elif influence_score <= 0:
                        next_matrix[r][c] = '.'
                    else:
                        next_matrix[r][c] = 'o'
                        # rule 6
                elif current_symbol == '.':  # dead cell
                    if isPrime(influence_score):
                        next_matrix[r][c] = 'o'
                    elif influence_score < 0 and isPrime(abs(influence_score)):
                        next_matrix[r][c] = 'x'
                    else:
                        next_matrix[r][c] = '.'
                        # rule 7
                elif current_symbol == 'x':
                    if inner_sum < 0 and is_fibonacci(abs(inner_sum)):
                        next_matrix[r][c] = 'X'
                    elif influence_score >= 0:
                        next_matrix[r][c] = '.'
                    else:
                        next_matrix[r][c] = 'x'
                        # rule 8
                elif current_symbol == 'X':
                    if influence_score < 0 and is_power_of_two(abs(influence_score)):
                        next_matrix[r][c] = '.'
                    elif outer_sum > -2:
                        next_matrix[r][c] = 'x'
                    else:
                        next_matrix[r][c] = 'X'

        matrix = next_matrix

    with open(output_file, "w") as f:
        for row in matrix:
            f.write("".join(row) + "\n")
if __name__ == "__main__":
    main()
