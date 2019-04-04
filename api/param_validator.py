import os
from flask_restful import abort


def validate_pagesize_param(page_size):
    max_page_size = os.environ.get('PAGINATION_PAGE_SIZE_MAX', 100)

    if page_size > max_page_size:
        abort(400, error='The pageSize parameter cannot be greater than: ' + str(max_page_size))
