from functools import wraps
from flask import request
from flask_api import status


# Authentication decorator
def check_mandatory_token(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if 'x-access-token' in request.headers:
            access_token = request.headers.get('x-access-token')
            valid = False
            if (access_token == "123"):
                valid = True
            if not valid:
                return {"message": "Token is invalid."}, status.HTTP_403_FORBIDDEN
        else:
            return {"message": "No token found in header"}, status.HTTP_403_FORBIDDEN
        return f(*args, **kwargs)
    return decorator