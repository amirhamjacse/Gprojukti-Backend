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


# for database you can use local db with postgresql

# PostgreSQL: Creating a Database and Restoring a Dump on Ubuntu

## Installing PostgreSQL on Ubuntu

1. **Update package lists:**
   ```sh
   sudo apt update
   ```

2. **Install PostgreSQL:**
   ```sh
   sudo apt install postgresql postgresql-contrib -y
   ```

3. **Start and enable PostgreSQL service:**
   ```sh
   sudo systemctl start postgresql
   sudo systemctl enable postgresql
   ```

4. **Switch to the PostgreSQL user:**
   ```sh
   sudo -i -u postgres
   ```

## Creating a Database in PostgreSQL

1. **Login to PostgreSQL:**
   ```sh
   psql
   ```

2. **Create a new database:**
   ```sql
   CREATE DATABASE mydatabase;
   ```

3. **Verify the creation:**
   ```sql
   \l
   ```
   This lists all databases.

4. **Connect to the database:**
   ```sql
   \c mydatabase;
   ```

## Restoring a Database Dump

1. **Exit PostgreSQL prompt (if inside):**
   ```sh
   \q
   ```

2. **Restore the database from a dump file:**
   ```sh
   pg_restore -U postgres -d mydatabase mydatabase.dump
   ```
   If the dump was created using `pg_dump`, you can use:
   ```sh
   psql -U postgres -d mydatabase -f mydatabase.sql
   ```

3. **Verify the restoration:**
   ```sh
   psql -U postgres -d mydatabase -c "\dt"
   ```
   This lists all tables in the restored database.

## Additional Notes
- Ensure PostgreSQL is installed and running (`sudo systemctl status postgresql`).
- You may need to provide a password if authentication is required.
- Use `pg_dump` to create a database dump:
  ```sh
  pg_dump -U postgres -F c -f mydatabase.dump mydatabase
  ```
  This creates a compressed dump file.
- To drop and recreate the database before restoration:
  ```sql
  DROP DATABASE mydatabase;
  CREATE DATABASE mydatabase;
  ```

use user admin@gmail.com
change password using 
```
python manage.py changepassword admin@gmail.com
```
this user has all permission
