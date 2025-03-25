FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . /code/

# Expose ports
EXPOSE 9000 9001 9002 9003 9004 9005 9006 9007 9008 9009 9010

# Command to run multiple Django runserver instances
CMD python manage.py runserver 0.0.0.0:9000 & \
    python manage.py runserver 0.0.0.0:9001 & \
    python manage.py runserver 0.0.0.0:9002 & \
    python manage.py runserver 0.0.0.0:9003 & \
    python manage.py runserver 0.0.0.0:9004 & \
    python manage.py runserver 0.0.0.0:9005 & \
    python manage.py runserver 0.0.0.0:9006 & \
    python manage.py runserver 0.0.0.0:9007 & \
    python manage.py runserver 0.0.0.0:9008 & \
    python manage.py runserver 0.0.0.0:9009 & \
    python manage.py runserver 0.0.0.0:9010