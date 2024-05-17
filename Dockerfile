# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# 현재 디렉토리의 모든 파일들을 컨테이너의 /app 디렉토리에 복사한다.
COPY . /app

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
RUN pip install -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]