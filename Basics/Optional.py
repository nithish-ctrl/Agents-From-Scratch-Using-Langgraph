from typing import Optional 

def greet(name : Optional[str]= None) -> str:
    if name is None :
        return "Hello, random guy!"
    else : 
        return f'Hello, {name}!'


greet1 = greet()
greet2 = greet("Alice")
print(greet1)
print(greet2)
