# Backend
[![Build Status](https://travis-ci.org/bfh-proj1-sumfrie/backend.svg?branch=master)](https://travis-ci.org/bfh-proj1-sumfrie/backend)

This project is the backend API used for our project 1 at the BFH.
It acts as a proxy for querying a MariaDB.

## Up and Running

### Manual Setup
1) clone this repository
3) Change to your virtual env
4) Install dependencies: `pip install -r requirements.txt`
5) Run it: `python main.py`

### Docker Compose Setup (preferred)
1) `docker-compose up`
2) Start it: `docker-compose up`
3) open localhost:5000

## CI/CD
This project is automatically tested and linted on Travis CI.
It uses flake8 for linting. To run the linting process install flake8 and run it as follows:
`flake8 src api.py test` from the root directory.

To run the tests install `pip install nose` and run `nosetests`.