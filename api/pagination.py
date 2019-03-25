import re
import os
from flask_restful import abort
from api.sanitizer import remove_comments


def paginate_query(sql):
    pagesize = int(os.environ.get('LIMIT_MAX_SIZE', '10'))
    sql = sql.lower().strip()
    sql = remove_comments(sql)
    # paginate selects only!
    if sql[:6] == 'select':
        sql = handle_semicolon(sql)
        limit_params_regex = re.compile('(?!limit)\\d+')
        params = limit_params_regex.findall(sql)
        if len(params) > 0:
            if int(params[0]) > pagesize:
                abort(400, error="LIMIT's cannot be greater than " + str(pagesize))

        else:
            sql += ' limit ' + str(pagesize)

    return sql


def handle_semicolon(sql):
    if sql.count(';') > 1:
        abort(400, error="Only one query allowed!")

    # remove semicolon
    elif sql[-1:] == ';':
        sql = sql[:-1]
    return sql
