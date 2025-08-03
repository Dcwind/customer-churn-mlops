# Base Image
# Official, lightweight Python 3.12 image.
FROM python:3.12-slim

# Set the working directory inside the container. All subsequent commands
# will run from this path.
WORKDIR /app

# Copy only the requirements file first to leverage Docker's layer caching.
# This layer will only be rebuilt if the requirements change.
COPY ../requirements.txt .

# Install the production dependencies.
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container.
COPY . .

# Expose Port
# Tell Docker that the container listens on port 8000.
EXPOSE 8000

# The command to run when the container starts. This starts the uvicorn server.
# Using "--host 0.0.0.0" makes the service accessible from outside the container.
CMD ["uvicorn", "deployment.app:app", "--host", "0.0.0.0", "--port", "8000"]
