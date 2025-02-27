from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restful import Api

from app.db import db
from app.models import Data, Series
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

jwt = JWTManager(app)
api = Api(app)
db.init_app(app)
migrate = Migrate(app, db)

bcrypt = Bcrypt(app)

from app.server.auth import Register, Login, Logout, RefreshToken, AdminResource, UserResource, UserList

api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(RefreshToken, '/refresh_token')
api.add_resource(AdminResource, '/admin')
api.add_resource(UserResource, '/user')
api.add_resource(UserList, '/users')

from app.server.imagenes_view import UploadImage, GetImages

api.add_resource(UploadImage, '/upload_image')
api.add_resource(GetImages, '/get_images')

from app.server.series_view import SeriesView, DataView

api.add_resource(SeriesView, '/series')
api.add_resource(DataView, '/data')

from app.models import Role, User, Permission, role_permissions

with app.app_context():
    db.create_all()

# crear permiso rol y usuario
    if not Role.query.filter_by(name='admin').first():
        admin_role = Role(name='admin')
        db.session.add(admin_role)
        db.session.commit()

        if not Permission.query.filter_by(name='CRUD').first():
            crud_permission = Permission(name='CRUD')
            db.session.add(crud_permission)
            db.session.commit()

            admin_role.permissions.append(crud_permission)
            db.session.commit()

    admin_role = Role.query.filter_by(name='admin').first()
    if admin_role and not User.query.filter_by(username='admin').first():
        db.session.add(
            User(username='admin', password=bcrypt.generate_password_hash('admin').decode('utf-8'), role=admin_role))
        db.session.commit()
