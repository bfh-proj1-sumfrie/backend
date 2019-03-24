from api import create_api

# only used for serving with gunicorn on heroku

application = create_api()
