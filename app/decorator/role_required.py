import json
from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

# solo saber si tiene el rol

def role_required(required_role):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            try:
                current_user = json.loads(get_jwt_identity())

                if current_user.get('role') != required_role:
                    return jsonify({"message": "No tienes permisos para acceder a este recurso"}), 403

                return fn(*args, **kwargs)
            except Exception as e:
                return jsonify({"message": f"Error en la autenticación: {str(e)}"}), 500
        return wrapper
    return decorator