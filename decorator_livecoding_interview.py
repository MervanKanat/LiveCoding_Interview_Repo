import time

# This script performs the following tasks:
# 1. Calculates the sum of numbers up to a given number.
# 2. Calculates the sum of squares of numbers up to a given number.
# 3. Uses n = 10000000 for testing.
# 4. Measures the execution time of these functions using a decorator.

# Define the timing decorator
def timeit_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.5f} seconds")
        return result
    return wrapper

# Apply the decorator to sum_numbers function
@timeit_decorator
def sum_numbers(n):
    total = 0
    for i in range(1, n + 1):
        total += i
    return total

# Apply the decorator to sum_of_squares function
@timeit_decorator
def sum_of_squares(n):
    total = 0
    for i in range(1, n + 1):
        total += i ** 2
    return total

n = 10000000

# Call the functions to get their results and timings
sum_result = sum_numbers(n)
print("sum_numbers Total:", sum_result)

sum_squares_result = sum_of_squares(n)
print("sum_of_squares Total of Squares:", sum_squares_result)
