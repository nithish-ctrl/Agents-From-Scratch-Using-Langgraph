from typing import Union

def square(x : Union[int, float]) -> Union[int, float]:
    return x * x

square_int = square(4)
print(square_int)
square_float = square(3.5)
print(square_float)