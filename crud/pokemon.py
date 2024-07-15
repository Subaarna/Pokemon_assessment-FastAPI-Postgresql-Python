from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, any_
from models.pokemon import Pokemon as PokemonModel
from schemas.pokemon import PokemonCreate

# Create a new pokemon
async def create_pokemon(db: AsyncSession, pokemon: PokemonCreate):
    db_pokemon = PokemonModel(**pokemon.model_dump())
    db.add(db_pokemon)
    await db.commit()
    await db.refresh(db_pokemon)
    return db_pokemon

# Get a pokemon by id
async def get_pokemon(db: AsyncSession, pokemon_id: int):
    result = await db.execute(select(PokemonModel).where(PokemonModel.id == pokemon_id))
    return result.scalar_one_or_none()
# Get all pokemons
async def get_pokemons(db: AsyncSession, name: Optional[str] = None, type: Optional[str] = None):
    query = select(PokemonModel)
    conditions = []
    if name:
        conditions.append(PokemonModel.name.ilike(f'%{name}%'))
    if type:
        conditions.append(type == any_(PokemonModel.types))
    if conditions:
        query = query.where(and_(*conditions))
    result = await db.execute(query)
    return result.scalars().all()
