# Backend

This project is the backend API used for our project 1 at the BFH.
It acts as a proxy for querying a MariaDB.

## Up and Running

1) clone this repository
2) Install dependencies: `pip install -r requirements.txt`
3) Run it: `python api.py`

## CI/CD
This project is automatically tested and linted on Travis CI.
It uses flake8 for linting. To run the linting process install flake8 and run it as follows:
`flake8 src api.py test` from the root directory.

To run the tests install `pip install nose` and run `nosetests`.