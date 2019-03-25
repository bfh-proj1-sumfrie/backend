import re
import os
from flask_restful import abort


def paginate_query(sql, pagesize=os.environ.get('LIMIT_MAX_SIZE', 10)):
    sql = sql.lower().strip()
    sql = handle_semicolon(sql)
    limit_params_regex = re.compile('(?!limit)\\d+')
    params = limit_params_regex.findall(sql)
    if len(params) > 0:
        if int(params[0]) > pagesize:
            abort(400, description="LIMIT's cannot be greater than " + str(pagesize))

    else:
        sql += ' limit 10'

    return sql


def handle_semicolon(sql):
    if sql.count(';') > 1:
        abort(400, description="Only one query allowed!")

    # remove semicolon
    elif sql[-1:] == ';':
        sql = sql[:-1]
    return sql
