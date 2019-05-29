# Backend
[![Build Status](https://travis-ci.org/bfh-proj1-sumfrie/backend.svg?branch=master)](https://travis-ci.org/bfh-proj1-sumfrie/backend)
[![Coverage Status](https://coveralls.io/repos/github/bfh-proj1-sumfrie/backend/badge.svg?branch=master)](https://coveralls.io/github/bfh-proj1-sumfrie/backend?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/9f9264ad8861e1227d26/maintainability)](https://codeclimate.com/github/bfh-proj1-sumfrie/backend/maintainability)
[![Updates](https://pyup.io/repos/github/bfh-proj1-sumfrie/backend/shield.svg)](https://pyup.io/repos/github/bfh-proj1-sumfrie/backend/)
![GitHub tag (latest SemVer)](https://img.shields.io/github/tag/bfh-proj1-sumfrie/backend.svg)

This project is the backend API used for our project 1 at the BFH.
It acts as a proxy for querying a MariaDB.

## Up and Running

### Manual Setup
1) Clone this repository
3) Change to your virtual env
4) Install dependencies: `pip install -r requirements.txt`
5) Install flask to use its cli
6) Configuration: The following environment variables must be set
 ```bash 
    DB_USERNAME # the db username
    DB_PASSWORD # db password of the user
    DB_HOST # the host where the db is running
    DB_DATABASE # the name of the database
    DB_CHARSET # the charset (utf8 in our case)
    PAGINATION_PAGE_SIZE_MAX # you can set the max page size the clients can define. Defaults to 100.
    LIMITER_PER_DAY_VAL # Sets the request rate limit per endpoint per day. Default 10000
    LIMITER_PER_HOUR_VAL # Sets the request rate limit per endpoint per hour. Default 500  
    DB_QUERY_TIMEOUT # Set the databse query timeout in seconds. Default 60
 ```
6) Run it: `FLASK_APP=api.api flask run`

### Docker Compose Setup (preferred)
1) Start it: `docker-compose up`
2) open `localhost:5000`

If you need to rebuild e.g. after adding new dependencies run `docker-compose up --build` 
to trigger a container rebuild

When building the containers the database will automatically be populated with test data.

### API Docs
You can find the API docs in the wiki of this repository.

https://github.com/bfh-proj1-sumfrie/backend/wiki

## CI/CD
This project is automatically tested and linted on Travis CI.
It uses flake8 for linting. To run the linting process install flake8 and run it as follows:
`flake8 src api.py test` from the root directory.

To run the tests install `pip install nose` and run `nosetests`.

## Testing

The test need to run against an sql database. To run them, start the docker environment
and then trigger the tests: `nosetests`.
Make sure you installed: `nostests, `

Since only reading queries are allowed, we don't need to revert the db
on every test.

If you want to know the test coverage: `nosetests --with-cov --cov api/ test/`
You need to have the package nose-cov installed `pip install nose-cov`

## Versioning
Tagging MUST follow [semantic versioning](https://semver.org/).