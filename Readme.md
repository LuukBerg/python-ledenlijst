# prerequisites

  * pipenv
  * python 3.* (3.9.5 tested)
  * docker-compose

# Installation

```
pipenv install
```

# Run the server

start the docker-compose
```
docker-compose up -d
```

start the pipenv shell
```
pipenv shell
cd ledenlijst
```
setup the database (only on first run)
```
python manage.py migrate
```
Run the server
```
python manage.py runserver
```

# Running the tests
```
python manage.py test home/tests
```
