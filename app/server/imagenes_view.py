import json
import os

import flask_jwt_extended
from flask import request, current_app
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from werkzeug.utils import secure_filename

from app import db
from app.models import Image
from app.models import User
from config import Config


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


class UploadImage(Resource):
    @jwt_required()
    def post(self):
        # Obtener el usuario a partir del token
        user_id = get_jwt_identity()
        jsonid=(json.loads(user_id))
        user = User.query.get(jsonid['id'])
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

            # Verificar si el archivo ya existe
            if os.path.exists(filepath):
                return {"message": "El archivo ya existe"}, 400

            file.save(filepath)
            # Crear un nuevo registro de imagen asociado al usuario
            new_image = Image(filename=filename, filepath=filepath, usuario_id=user.id)
            db.session.add(new_image)
            db.session.commit()

            return {"message": "Imagen subida exitosamente"}

        return {"message": "Extensión de archivo no permitida"}, 400



class GetImages(Resource):
    @jwt_required()

    def get(self):
        try:
            image_name = request.args.get('filename')
            if image_name:
                images = Image.query.filter_by(filename=image_name).all()
            else:
                images = Image.query.all()
            return {"images": [image.to_dict() for image in images]}, 200
        except flask_jwt_extended.exceptions.NoAuthorizationError:
            return {"message": "Missing Authorization Header"}, 401
