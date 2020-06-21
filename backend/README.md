## Toogethr Assignment Backend
#### ``A simple web application for handling reservation in a parking lot``


Project is based on [`Django Rest Framework`](https://www.django-rest-framework.org/).

### Requirements
* Python >= 3.6.3

### Installing dependencies
* Open a terminal in backend root directory
* Create a virtual environment `venv` folder using `python3.7 -m venv venv` or `virtualenv -p python3.7 venv`
* Activate the virtual environment using `. venv/bin/activate`
* Install dependencies based on `requirements.txt` file using `pip install -r requirements.txt`

### Running the DB
For running the database you can use docker-compose in root folder. just use `docker-compose up -d pgdb`.
It will expose an PostgreSQL on port `5442`.

Database name, username and password are mentioned in `docker-compose.yml`.


### Running The Project On Docker
* Using docker in root directory: `docker-compose up -d --build --force-recreate pgdb`

### Running Manually
##### Creating and migrating the migrations
* Making migrations: `python manage.py makemigrations api && python manage.py makemigrations user`
* Migrating migrations: `python manage.py migrate`
* Populating database: `python manage.py populate_db`
##### Run the project
`python manage.py runserver 0.0.0.0:8000`


### Running tests
* In backend directory run `python manage.py test` for running unit tests.
* For coverage reports in a html file you can run in backend directory:

  ```
  coverage run --source='.' manage.py test
  coverage html
  ```
  open `htmlcov/index.html` with browser
* For having coverage reports in terminal simply run `coverage report` after running the first command in previous section.

### Links
[Django Rest Framework](https://www.django-rest-framework.org/)

[Django](https://www.djangoproject.com/)

[Django Filter](https://django-filter.readthedocs.io/en/stable/)

[Django Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)