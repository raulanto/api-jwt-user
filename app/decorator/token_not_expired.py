import datetime
from functools import wraps

from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

#saber si el token expiro
def token_not_expired(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            jwt_data = get_jwt()
            if jwt_data["exp"] < datetime.utcnow().timestamp():
                return jsonify({"message": "El token ha expirado"}), 401
            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify({"message": f"Error en la validación del token: {str(e)}"}), 500
    return wrapper