# G-Projukti Backend Server

    ## Document

    - Clone the repository
    - Create a`.env` file
    - Make a virtualenv and install all requirements
    - Create a database and add configuration to the .env file
    - Run django migrate commands
    - Run the project with `runserver` command

    # Project API Url

    `http://127.0.0.1:8000/`

    # For Docker Code Run

    1. 'docker-compose build'
        or 'sudo docker-compose build'
        or 'docker-compose up --build'

    2. 'docker-compose up'

    3. celery -A gporjukti_backend_v2 worker -l info
    4. For Deploy Restart:
       1. docker-compose down
       2. docker-compose up -d --build
       3. docker-compose logs -f

# For Celery Run

celery -A gporjukti_backend_v2 worker -l INFO
