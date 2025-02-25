from flask import Flask
from app.db import db
from config import Config
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_bcrypt import Bcrypt





app = Flask(__name__)
app.config.from_object(Config)


jwt = JWTManager(app)
api = Api(app)
db.init_app(app)
migrate = Migrate(app, db)

bcrypt = Bcrypt(app)

from app.server.auth import Register, Login,Logout,RefreshToken,AdminResource,UserResource
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(RefreshToken, '/refresh_token')
api.add_resource(AdminResource, '/admin')
api.add_resource(UserResource, '/user')

from app.server.imagenes_view import UploadImage,GetImages
api.add_resource(UploadImage, '/upload_image')
api.add_resource(GetImages, '/get_images')



from app.models import Role,User
with app.app_context():
    db.create_all()
    if not Role.query.filter_by(name='admin').first():
        db.session.add(Role(name='admin'))
        db.session.add(Role(name='user'))
        db.session.commit()

    admin_role = Role.query.filter_by(name='admin').first()
    if admin_role and not User.query.filter_by(username='admin').first():
        db.session.add(
            User(username='admin', password=bcrypt.generate_password_hash('admin').decode('utf-8'), role=admin_role))
        db.session.commit()