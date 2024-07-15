import asyncio
import aiohttp
import os
import sys
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import async_session
from crud.pokemon import create_pokemon
from schemas.pokemon import PokemonCreate
from core.config import settings

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Function to fetch pokemons from the pokeapi
async def fetch_pokemons():
    async with aiohttp.ClientSession() as session:
        async with session.get(settings.POKEAPI_URL) as response:
            data = await response.json()
            return data['results']

# Main function to fetch pokemons and save them to the database
async def main():
    pokemons = await fetch_pokemons()
    async with async_session() as db:
        for poke in pokemons:
            async with aiohttp.ClientSession() as session:
                async with session.get(poke['url']) as response:
                    poke_data = await response.json()
                    new_pokemon = PokemonCreate(
                        name=poke_data['name'],
                        image=poke_data['sprites']['front_default'],
                        types=[t['type']['name'] for t in poke_data['types']]
                    )
                    await create_pokemon(db, new_pokemon)

if __name__ == "__main__":
    asyncio.run(main())
