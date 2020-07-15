from functools import wraps

from flask import abort
from flask_jwt import current_identity


def permission_required(authority_required):
    """
    :param authority_required:
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_identity.check_authority(authority_required):
                abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator
