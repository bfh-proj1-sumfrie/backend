import os
from sqlalchemy import create_engine

password = os.environ['DB_PASSWORD']
username = os.environ['DB_USERNAME']
host = os.environ['DB_HOST']
database = os.environ['DB_DATABASE']
charset = os.environ['DB_CHARSET']
port = int(os.environ['DB_PORT'])

engine = create_engine(
    'mysql+pymysql://' + username + ':' + password + '@' + host + '/' + database + '?charset=' + charset,
    connect_args={
        'port': port
    },
    echo=False,
    echo_pool=False
)
