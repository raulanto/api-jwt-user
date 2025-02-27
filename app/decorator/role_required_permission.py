import json
from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required


# buscar si tiene el rol y permiso
def role_required_permission(required_role, required_permission=None):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            try:
                current_user = json.loads(get_jwt_identity())

                if current_user.get('role') != required_role:
                    return jsonify({"message": "No tienes permisos para acceder a este recurso"}), 403

                if required_permission and required_permission not in current_user.get('permissions', []):
                    return jsonify({"message": f"No tienes el permiso de {required_permission} para acceder a este recurso"}), 403

                return fn(*args, **kwargs)
            except Exception as e:
                return jsonify({"message": f"Error en la autenticación: {str(e)}"}), 500
        return wrapper
    return decorator

