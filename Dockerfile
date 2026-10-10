# Use official Python lightweight image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY backend/requirements.txt .

# Install dependencies without using cache to keep image small
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code and ML artifacts into the container
COPY backend/ /app/backend/
COPY ml/artifacts/ /app/ml/artifacts/

# Change working directory so uvicorn can correctly locate the 'app' module
WORKDIR /app/backend

# Expose the port for the API
EXPOSE 8000

# Command to run the application (No internet needed from this point onwards)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]