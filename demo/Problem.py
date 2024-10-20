import random
from datetime import datetime

class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

def greet(self):
        return f"Hello, my name is {self.name} and I am {self.age} years old."

def calculate_factorial(n):
    if n == 0:
        return 1
    else:
        return n * calculate_factorial(n - 1)

def divide_numbers(a, b):
    return a / b

def process_list(items):
    processed = []
    for i in range(len(items)):
        processed.append(items[i] * 2)
    return processed

def get_current_date():
    return datetime.now().strftime("%d/%m/%Y")

def main():
    # Syntax error: missing parentheses in print function
    print "Welcome to the error-prone Python program!"

    # Runtime error: division by zero
    result = divide_numbers(10, 0)
    print(f"Result of division: {result}")

    # Logical error: off-by-one in loop
    numbers = [1, 2, 3, 4, 5]
    total = 0
    for i in range(1, len(numbers)):
        total += numbers[i]
    print(f"Sum of numbers: {total}")

    # Indentation error
    if True:
    print("This line is incorrectly indented")

    # Name error: undefined variable
    print(f"Undefined variable: {undefined_variable}")

    # Type error: adding incompatible types
    age = 25
    name = "Alice"
    print(f"Age plus name: {age + name}")

    # Attribute error: calling non-existent method
    user = User("Bob", 30)
    user.nonexistent_method()

    # Index error: accessing list index out of range
    my_list = [1, 2, 3]
    print(f"Fourth element: {my_list[3]}")

    # Key error: accessing non-existent dictionary key
    my_dict = {"a": 1, "b": 2}
    print(f"Value of 'c': {my_dict['c']}")

    # Recursive error: maximum recursion depth exceeded
    print(f"Factorial of 1000: {calculate_factorial(1000)}")

    # Logical error: incorrect string formatting
    date = get_current_date()
    print(f"Current date: {date:%Y-%m-%d}")

    # Syntax error: invalid syntax in list comprehension
    squares = [x*x for x in range(10) if x % 2 == 0 else x]

    # Runtime warning: using a bare 'except'
    try:
        risky_operation()
    except:
        pass

if __name__ == "__main__"
    main()