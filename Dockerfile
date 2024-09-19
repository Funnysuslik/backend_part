# Use a lightweight Python image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app directory to the container
COPY ./app /app/app

# Copy the alembic directory and alembic.ini file
COPY ./alembic /app/alembic
COPY ./alembic.ini /app/alembic.ini

# Command to run migration and start the app
CMD ["bash", "-c", "ls && alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]