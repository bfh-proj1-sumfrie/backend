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
 Code partly adapted from:
 - https://codeandlife.com/2014/12/07/sqlalchemy-results-to-json-the-easy-way/
 """

import datetime
import decimal


# JSON encoder function for SQLAlchemy special classes
# https://codeandlife.com/2014/12/07/sqlalchemy-results-to-json-the-easy-way/
def alchemy_encoder(obj):
    if isinstance(obj, datetime.date):
        return obj.isoformat()

    # display binary as hex so it's human readable
    if isinstance(obj, (bytes, bytearray)):
        return ''.join('{:02x}'.format(x) for x in obj)

    elif isinstance(obj, decimal.Decimal):
        return float(obj)
