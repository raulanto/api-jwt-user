import json
import uuid
from datetime import datetime

from flask import make_response, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token, unset_jwt_cookies, get_jwt_identity,
    jwt_required, get_jwt
)
from flask_restful import Resource

from app import bcrypt, db, jwt
from app.errors import error_response
from app.middleware import  role_required_permission, token_not_expired, roles_required
from app.models import User, SesionUsuario

blacklist = set()



@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in blacklist





class Register(Resource):
    def post(self):
        try:
            data = request.get_json()
            if not data or 'username' not in data or 'password' not in data:
                return {"message": "Faltan datos requeridos"}, 400
            hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            if User.query.filter_by(username=data['username']).first():
                return {"message": "El usuario ya existe"}, 400

            new_user = User(username=data['username'], password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return {"message": "Usuario registrado exitosamente"}, 201
        except Exception as e:
            return {"message": f"Error en el registro: {str(e)}"}, 500


class Login(Resource):
    def post(self):
        try:
            data = request.get_json()
            if not data or 'username' not in data or 'password' not in data:
                return {"message": "Faltan datos requeridos"}, 400
            user = User.query.filter_by(username=data['username']).first()
            if user and bcrypt.check_password_hash(user.password, data['password']):
                jti = str(uuid.uuid4())
                identity = json.dumps({"id": user.id, "role": user.role.name})
                access_token = create_access_token(identity=identity,additional_claims={"jti": jti})
                refresh_token = create_refresh_token(identity=identity)

                sesion = SesionUsuario(usuario_id=user.id, token_jti=jti)
                db.session.add(sesion)
                db.session.commit()
                return {
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }, 200

            return {"message": "Credenciales incorrectas"}, 401
        except Exception as e:
            return {"message": f"Error en el login: {str(e)}"}, 500


class Logout(Resource):
    @jwt_required()
    def post(self):
        try:
            jti = get_jwt()["jti"]

            sesion = SesionUsuario.query.filter_by(token_jti=jti).first()
            if not sesion:
                return error_response(400, "No activa la seccion")

            if sesion.fecha_hora_salida:
                return error_response(400, "la seccion ya cerro")

            blacklist.add(jti)
            response = make_response(jsonify({"message": "Logout exitoso"}), 200)
            unset_jwt_cookies(response)

            sesion.fecha_hora_salida = datetime.utcnow()
            db.session.commit()
            return response
        except Exception as e:
            return {"message": f"Error al cerrar sesión: {str(e)}"}, 500


class RefreshToken(Resource):
    @jwt_required(refresh=True)
    def post(self):
        try:
            current_user = json.loads(get_jwt_identity())
            new_access_token = create_access_token(identity=json.dumps(current_user))
            return {"access_token": new_access_token}, 200
        except Exception as e:
            return {"message": f"Error al refrescar el token: {str(e)}"}, 500


class AdminResource(Resource):
    @roles_required('admin')
    def get(self):
        try:
            return {"message": "Bienvenido al panel de administrador"}
        except Exception as e:
            return {"message": f"Error en el panel de administrador: {str(e)}"}, 500


class UserResource(Resource):
    @roles_required('admin', 'user')
    def get(self):
        try:
            return {"message": "Bienvenido al panel de usuario"}
        except Exception as e:
            return {"message": f"Error en el panel de usuario: {str(e)}"}, 500


class UserList(Resource):
    @jwt_required()
    def get(self):
        try:
            users = User.query.all()
            print(users)
            return jsonify({"users": [user.list_json() for user in users]})
        except Exception as e:
            return {"message": f"Error al obtener los usuarios: {str(e)}"}, 500