# Backend
[![Build Status](https://travis-ci.org/bfh-proj1-sumfrie/backend.svg?branch=master)](https://travis-ci.org/bfh-proj1-sumfrie/backend)
[![Coverage Status](https://coveralls.io/repos/github/bfh-proj1-sumfrie/backend/badge.svg?branch=master)](https://coveralls.io/github/bfh-proj1-sumfrie/backend?branch=master)

This project is the backend API used for our project 1 at the BFH.
It acts as a proxy for querying a MariaDB.

## Up and Running

### Manual Setup
1) Clone this repository
3) Change to your virtual env
4) Install dependencies: `pip install -r requirements.txt`
5) Database Configuration (Sql)
 The following environment variables must be set:
 ```bash 
    DB_USERNAME # the db username
    DB_PASSWORD # db password of the user
    DB_HOST # the host where the db is running
    DB_DATABASE # the name of the database
    DB_CHARSET # the charset (utf8 in our case)
 ```
6) Run it: `python main.py`

### Docker Compose Setup (preferred)
1) Start it: `docker-compose up`
2) open `localhost:5000`

If you need to rebuild e.g. after adding new dependencies run `docker-compose up --build` 
to trigger a container rebuild

When building the containers the database will automatically be populated with test data.

### Swagger API Docs
You can find the API Docs here: `http://localhost:5000/api/swagger.json`.

If you want to test it using an a swagger interface go to: https://inspector.swagger.io

and use the your swagger link where you host this software `http://myhost.com/api/swagger.json` 

If you are developing make sure to allow CORS request, so you can use `http://127.0.0.1:5000/api/swagger.json`
in the swagger inspector.

## CI/CD
This project is automatically tested and linted on Travis CI.
It uses flake8 for linting. To run the linting process install flake8 and run it as follows:
`flake8 src api.py test` from the root directory.

To run the tests install `pip install nose` and run `nosetests`.

## Testing

The test need to run against an sql database. To run them, start the docker environment
and then trigger the tests: `nosetests`.

Since only reading queries are allowed, we don't need to revert the db
on every test.

If you want to know the test coverage: `nosetests --with-cov --cov api/ test/`
You need to have the package nose-cov installed `pip install nose-cov`

## Versioning
Tagging MUST follow [semantic versioning](https://semver.org/).