# Pokémon API Project

This project implements a RESTful API using FastAPI to serve Pokémon data fetched from PokeAPI and stored in a PostgreSQL database.

## Setup Instructions

1. Clone the repository:
```git clonehttps://github.com/Subaarna/Pokemon_assessment-FastAPI-Postgresql-Python.git ```
2. Navigate through the directory
``` cd cd Pokemon_assessment-FastAPI-Postgresql-Python ```
3. Install dependencies
``` pip install -r requirements.txt ```
4. Set up PostgreSQL database:
5. Create a .env file and add the following
```plaintext
  POSTGRES_USER=Your_user
  POSTGRES_PASSWORD=Your_password
  POSTGRES_DB=Database
  POSTGRES_HOST=localhost
  POSTGRES_PORT=Port
  ```
6. Create a Database table with Alembic
``` alembic revision --autogenerate -m "create pokemons table" ```
7. Apply the necessary updates for the database to initiate next step
``` alembic upgrade head ```
8. Fetch all the data from the API
``` pyhon fetch_pokemons.py ```
9. Run the Fast-API server
``` uvicorn main:app --reload ```
10. Load the index.html and enjoy your Pokemon app 🤙
