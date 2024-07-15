
# necessary Imports
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.pokemon import Pokemon, PokemonCreate
from crud.pokemon import create_pokemon, get_pokemon, get_pokemons
from db.session import get_db

router = APIRouter()
# Endpoints to post pokemons and get pokemons
@router.post("/pokemons/", response_model=Pokemon)
async def create_new_pokemon(pokemon: PokemonCreate, db: AsyncSession = Depends(get_db)):
    return await create_pokemon(db, pokemon)

@router.get("/pokemons/", response_model=List[Pokemon])
async def read_pokemons(name: Optional[str] = None, type: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    pokemons = await get_pokemons(db)
    if name:
        pokemons = [pokemon for pokemon in pokemons if name.lower() in pokemon.name.lower()]
    if type:
        pokemons = [pokemon for pokemon in pokemons if type.lower() in [t.lower() for t in pokemon.types]]
    return pokemons
# Endpoints to get a pokemon by id and get all pokemons
@router.get("/pokemons/all", response_model=List[Pokemon])
async def read_all_pokemons(db: AsyncSession = Depends(get_db)):
    return await get_pokemons(db)