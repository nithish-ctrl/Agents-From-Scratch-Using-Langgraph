from typing import Any

def print_value(value: Any)-> None:
    print(f'The value is : {value}')

print_value(42)
print_value("Hello, World!")
print_value([1, 2, 3])