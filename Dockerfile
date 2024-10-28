# Use an official Python runtime as a base image
FROM python:3.12

# Set environment variables to prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Install Poetry
RUN pip install poetry

# Set the working directory in the container
WORKDIR /app

# Copy only the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock ./

# Install dependencies with Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy the rest of the application code
COPY . .

# Expose port 80 to the outside world
EXPOSE 80

# Run the application with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
