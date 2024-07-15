# Example Dockerfile with PostgreSQL installation
FROM python:3.9-slim

# Install PostgreSQL client and server
RUN apt-get update && \
    apt-get install -y postgresql postgresql-contrib

# Set up PostgreSQL (example: create a database and user)
USER postgres
RUN /etc/init.d/postgresql start && \
    psql --command "CREATE USER postgres WITH SUPERUSER PASSWORD 'password';" && \
    createdb -O myuser mydatabase

# Switch back to the root user
USER root

# Continue with your application setup
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

# Expose your application port
EXPOSE 80

# Run your application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
