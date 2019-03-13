from api import create_api

app = create_api()

if __name__ == '__main__':
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True)
