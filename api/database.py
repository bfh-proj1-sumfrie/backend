import os


def get_db_connection_uri(is_test=False):

    host = os.environ.get('DB_HOST', 'docker')
    password = os.environ.get('DB_PASSWORD', 'docker')
    username = os.environ.get('DB_USERNAME', 'docker')
    database = os.environ.get('DB_DATABASE', 'docker')
    charset = os.environ.get('DB_CHARSET', 'utf8')

    if is_test:
        host = '127.0.0.1'

    return 'mysql+pymysql://' + username + ':' + password + '@' + host + '/' + database + '?charset=' + charset
