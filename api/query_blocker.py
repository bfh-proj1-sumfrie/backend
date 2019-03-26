import re
from flask_restful import abort


def check_query_blacklist(sql):
    # THIS IS NOT MEANT TO BE A SECURITY MECHANISM!
    # simply for telling users that they aren't allowed to run such statements
    blacklist = [
        'delete',
        'update',
        'alter',
        'insert',
        'create',
        'drop',
        'set',
        'add',
        'call',
        'exec',
        'declare',
        'option',
        'read',
        'read_write',
        'rename',
        'replace',
        'truncate'
    ]
    for item in blacklist:
        regex = re.compile('(?:^|\\W)' + item + '(?:$|\\W)')
        if len(re.findall(regex, sql.lower())) > 0:
            abort(401, error="The following keyword is not allowed: " + str(item))
