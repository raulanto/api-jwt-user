from flask import request, jsonify, current_app
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
import os
from werkzeug.utils import secure_filename
from app import db
from app.middleware import role_required
from app.models import Image
from config import Config
from app.models import User

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


class UploadImage(Resource):
    @jwt_required()  # Esto asegura que el usuario esté autenticado
    @role_required('admin')
    def post(self):
        # Obtener el usuario a partir del token
        user_id = get_jwt_identity()
        user = User.query.get(user_id)


        # Verificar si se ha enviado un archivo
        if 'file' not in request.files:
            return {"message": "No se encontró ningún archivo"}, 400

        file = request.files['file']

        # Verificar que se haya seleccionado un archivo
        if file.filename == '':
            return {"message": "No se seleccionó un archivo"}, 400

        # Verificar que la extensión del archivo sea permitida
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Crear un nuevo registro de imagen asociado al usuario
            new_image = Image(filename=filename, filepath=filepath, usuario_id=user.id)
            db.session.add(new_image)
            db.session.commit()

            return {"message": "Imagen subida exitosamente", "image": new_image.to_dict()}, 201

        return {"message": "Extensión de archivo no permitida"}, 400

class GetImages(Resource):
    def get(self):
        images = Image.query.all()
        return {"images": [image.to_dict() for image in images]}, 200
