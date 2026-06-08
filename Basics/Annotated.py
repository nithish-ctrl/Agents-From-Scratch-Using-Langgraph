from typing import Annotated

email = Annotated[str, "It has to be a valid email address"]
# The string has after the type gets added to the meta data
print(email.__metadata__) # type: ignore
