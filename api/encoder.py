import datetime
import decimal


# JSON encoder function for SQLAlchemy special classes
def alchemy_encoder(obj):
    if isinstance(obj, datetime.date):
        return obj.isoformat()

    # display binary as hex so it's human readable @todo use a faster soultion if this does not perform well enough
    if isinstance(obj, (bytes, bytearray)):
        return ''.join('{:02x}'.format(x) for x in obj)

    elif isinstance(obj, decimal.Decimal):
        return float(obj)
