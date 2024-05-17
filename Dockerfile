# Build stage
FROM python:3.9-slim AS build

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Final stage
FROM python:3.9-slim

WORKDIR /app

COPY --from=build /app /app

EXPOSE 5000

CMD ["python", "app.py"]