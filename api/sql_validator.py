from moz_sql_parser import parse, format
import os


def validate_sql(sql):
    parsed = parse(sql)
    page_size = os.environ.get('PAGE_SIZE', 10)
    if 'limit' in parsed.keys():
        if parsed['limit'] > page_size:
            parsed['limit'] = page_size
    else:
        # set a limit if not present to avoid too heavy queries
        parsed['limit'] = page_size

    return format(parsed)
