import json
from flask import make_response, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token, unset_jwt_cookies, get_jwt_identity,
    jwt_required, get_jwt
)
from flask_restful import Resource

from app import db

from app.models.data import Data,Series


class SeriesView(Resource):

    def get(self):
        try:
            series = Series.query.all()
            return {"series data": [serie.to_data_dict() for serie in series]},200
        except Exception as e:
            return {"message": f"Error al obtener las series: {str(e)}"}, 500


    def post(self):
        try:
            data = request.get_json()
            if not data or 'name' not in data or 'description' not in data:
                return {"message": "Faltan datos requeridos"}, 400

            new_serie = Series(name=data['name'], description=data['description'])
            db.session.add(new_serie)
            db.session.commit()
            return {"message": "Serie creada exitosamente"}, 201
        except Exception as e:
            return {"message": f"Error al crear la serie: {str(e)}"}, 500

class DataView(Resource):

    def get(self):
        try:
            data = Data.query.all()
            return {"data": [data.to_dict() for data in data]},200
        except Exception as e:
            return {"message": f"Error al obtener los datos: {str(e)}"}, 500


    def post(self):
        try:
            data = request.get_json()
            if not data or 'value' not in data or 'series_id' not in data:
                return {"message": "Faltan datos requeridos"}, 400

            new_data = Data(value=data['value'], series_id=data['series_id'])
            db.session.add(new_data)
            db.session.commit()
            return {"message": "Dato creado exitosamente"}, 201
        except Exception as e:
            return {"message": f"Error al crear el dato: {str(e)}"}, 500