FROM python:3.12.4

# Install PostgreSQL client and server
RUN apt-get update && \
    apt-get install -y postgresql-client postgresql netcat-openbsd gosu

# Set up PostgreSQL
USER postgres

# Initialize the PostgreSQL data directory
RUN /usr/lib/postgresql/15/bin/initdb -D /var/lib/postgresql/15/data

# Ensure the correct permissions for the PostgreSQL data directory
RUN chown -R postgres:postgres /var/lib/postgresql/15/data

# Start PostgreSQL service, create database, and stop service
RUN /usr/lib/postgresql/15/bin/pg_ctl start -D /var/lib/postgresql/15/data -l /var/lib/postgresql/15/data/logfile && \
    sleep 5 && \
    psql --command "CREATE DATABASE pokemon_db;" && \
    psql --command "GRANT ALL PRIVILEGES ON DATABASE pokemon_db TO postgres;" && \
    /usr/lib/postgresql/15/bin/pg_ctl stop -D /var/lib/postgresql/15/data

# Ensure the correct permissions again after stopping the service
RUN chown -R postgres:postgres /var/lib/postgresql/15/data

# Switch back to the root user
USER root

# Continue with your application setup
WORKDIR /app
COPY . /app

# Install application dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure PostgreSQL is ready before running commands
COPY wait-for-postgres.sh /app/wait-for-postgres.sh
RUN chmod +x /app/wait-for-postgres.sh

# Run database migrations and fetch Pokémon data
USER postgres
RUN /usr/lib/postgresql/15/bin/pg_ctl start -D /var/lib/postgresql/15/data -l /var/lib/postgresql/15/data/logfile && \
    /app/wait-for-postgres.sh && \
    alembic upgrade head && \
    python fetch_pokemons.py && \
    /usr/lib/postgresql/15/bin/pg_ctl stop -D /var/lib/postgresql/15/data

# Ensure the correct permissions again after stopping the service
RUN chown -R postgres:postgres /var/lib/postgresql/15/data

# Switch back to the root user for the application run
USER root

# Expose your application port
EXPOSE 80

# Run your application with gosu to switch to postgres user
CMD ["gosu", "postgres", "/bin/bash", "-c", "/usr/lib/postgresql/15/bin/pg_ctl start -D /var/lib/postgresql/15/data -l /var/lib/postgresql/15/data/logfile && uvicorn main:app --host 0.0.0.0 --port 80"]