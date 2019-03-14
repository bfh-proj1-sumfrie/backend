import datetime
import decimal
import base64


# JSON encoder function for SQLAlchemy special classes
def alchemy_encoder(obj):
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    # some bytes fields need to be cast to base64 so we don't loose data while in transfer
    if isinstance(obj, (bytes, bytearray)):
        return str(base64.b64encode(obj))
    elif isinstance(obj, decimal.Decimal):
        return float(obj)
