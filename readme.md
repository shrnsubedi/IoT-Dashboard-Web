# Project Introduction

IoT dashboard is a...

# Pre-requisites

- Python >= 3.8
- pip (Bundled with Python. Install if bundled version is not working)
- Postgres Database >=12

# Installation and Setup

1. Clone the project onto your machine and cd into the folder:
   ```bash
   $ git clone https://github.com/shrnsubedi/IoT-Dashboard-Web.git
   ```
2. Create a virtual environment in python 3 and activate it:

   ```bash
   $ python3 -m venv env
   ```

   ```bash
   $ source env/bin/activate
   ```

   \_If activated the env_name will be appear in terminal

<br/>

4.  Install all the dependencies mentioned in the requirements.txt file:
    ```bash
    (venv)$ pip install -r requirements.txt
    ```

<br/>

5. Run the following command to install pre-commit hooks.

   ```bash
   (venv)$ pre-commit install
   ```

   _Due to presence of pre-commit hooks, it is not allowed to commit code with formatting errors. The errors will be listed out while trying to commit the code. Some of these errors will be formatted automatically while some may require you to fix them manually. The formatters used are black, flake8 and isort. Please follow the respective style guides while pushing your code._

<br/>

6. Create a new database in postgres. The credentials of the database must be specified in the env file in next step.

<br/>

7. Creat an .env file in iot_dashboard/.env and paste the following:

   ```
       These options are obtained while configuring the databse (Required)
        DATABASE_NAME=iot
        DATABASE_USER=postgres
        DATABASE_PASSWORD=postgres
        DATABASE_HOST=localhost
        DATABASE_PORT=5432

       Set debug=True while in development only
        DEBUG_SETTING=True

       Set a random string as secret key
        SECRET_KEY=<random-string>
   ```

<br/>

8. Run migrations on the database:
   ```bash
   (venv)$ python manage.py migrate
   ```

<br/>

9. Run the localserver and visit ( 127.0.0.1:8000 )

    ```bash
    (venv)$ python manage.py runserver
    ```

10. To commit your changes checkout a branch from the master branch and push.
