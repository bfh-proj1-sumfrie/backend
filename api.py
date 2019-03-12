from src import create_api

if __name__ == '__main__':
    api = create_api()
    api.run(debug=True)
