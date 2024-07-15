
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.pokemon import Pokemon, PokemonCreate
from crud.pokemon import create_pokemon, get_pokemon, get_pokemons
from db.session import get_db

router = APIRouter()

@router.post("/pokemons/", response_model=Pokemon)
async def create_new_pokemon(pokemon: PokemonCreate, db: AsyncSession = Depends(get_db)):
    return await create_pokemon(db, pokemon)

@router.get("/pokemons/", response_model=List[Pokemon])
async def read_pokemons(name: Optional[str] = None, type: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    return await get_pokemons(db, name, type)
