# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Command to run the application
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]