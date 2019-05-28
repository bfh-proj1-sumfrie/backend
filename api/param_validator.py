"""
 Author: Elias Summermatter & Jan Friedli
 Date: 28.05.2019
 Licence:
 This file is part of BloSQL.
 BloSQL is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 BloSQL is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 You should have received a copy of the GNU General Public License
 along with BloSQL.  If not, see <http://www.gnu.org/licenses/>.
 """

import os
from flask_restful import abort


def validate_pagesize_param(page_size):
    max_page_size = os.environ.get('PAGINATION_PAGE_SIZE_MAX', 100)

    if page_size > max_page_size:
        abort(400, message='The pageSize parameter cannot be greater than: ' + str(max_page_size))
