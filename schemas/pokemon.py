from pydantic import BaseModel
from typing import List, Optional

# Define the PokemonBase class
class PokemonBase(BaseModel):
    name: str
    image: str
    types: List[str]

# Define the PokemonCreate class
class PokemonCreate(PokemonBase):
    pass

# Define the Pokemon class
class Pokemon(PokemonBase):
    id: int
# Define the PokemonInDB class
    class Config:
        from_attributes = True
