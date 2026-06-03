from typing import TypedDict

class Movie(TypedDict):
    Title : str
    year : int
    duration : int

movie1 = Movie(Title="Inception", year= 2010, duration = 150)
print(movie1)

