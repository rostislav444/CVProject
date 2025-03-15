FROM python:3.11

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y netcat-openbsd

RUN pip install --upgrade pip

# Copy requirements file
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the project
COPY . /app/

# Make scripts executable
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

# Default command - can be overridden in docker-compose.yml
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]