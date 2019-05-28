from api import api

# Only for debugging while developing
app = api.create_api()
app.run(host='0.0.0.0', debug=True)
