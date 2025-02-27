import datetime
import json
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request, get_jwt
from functools import wraps
from app.models import User


def roles_required(*required_roles):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            try:
                current_user = json.loads(get_jwt_identity())

                if current_user.get('role') not in required_roles:
                    return {"message": "No tienes permisos para acceder a este recurso"}, 403

                return fn(*args, **kwargs)
            except Exception as e:
                return {"message": f"Error en la autenticación: {str(e)}"}, 500
        return wrapper
    return decorator

# buscar si tiene el rol y permiso
def role_required_permission(required_role, required_permission=None):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            try:
                current_user = json.loads(get_jwt_identity())
                user_id = get_jwt_identity()
                jsonid = (json.loads(user_id))
                user = User.query.get(jsonid['id'])
                if current_user.get('role') != required_role:
                    return {"message": f"No tiene el  rol {required_role}  para acceder a este recurso"}, 403

                if required_permission:
                    permisos = {perm.name for perm in user.role.permissions}
                    if required_permission not in permisos:
                        return {
                            "message": f"No tienes el permiso {required_permission} para acceder a este recurso"}, 403

                return fn(*args, **kwargs)
            except Exception as e:
                return {"message": f"Error en la autenticación: {str(e)}"}, 500
        return wrapper
    return decorator



def token_not_expired(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            jwt_data = get_jwt()
            if jwt_data["exp"] < datetime.utcnow().timestamp():
                return {"message": "El token ha expirado"}, 401
            return fn(*args, **kwargs)
        except Exception as e:
            return {"message": f"Error en la validación del token: {str(e)}"}, 500
    return wrapper