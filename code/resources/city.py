from flask_restful import Resource
from code.models.city import City
from flask_jwt_extended import jwt_required
from code.utils.parsers import get_city_parser

import logging

_city_parser = get_city_parser()


class CityRegister(Resource):

    @jwt_required()
    def post(self):
        request_data = _city_parser.parse_args()
        city_name = request_data["city_name"]
        
        if City.find_by_name(city_name):
            return {"message": f"{city_name} city already exists."}

        try:
            city = City(**request_data)
            city.add_to_db()
            return {"message": f"Successfully added {city_name} city!"}, 201
        except Exception as exp:
            logging.error(f"ERROR: {str(exp)}")
            return {"message": "Some error occured when trying to process the request."}, 400


class CityQuery(Resource):
    
    def get(self, identifier):
        try:
            identifier, is_name = int(identifier), False
        except ValueError as ve:
            is_name = True
        city = City.find_by_name(identifier) if is_name else City.find_by_id(identifier)
        if city:
            return [c.to_json() for c in city] if isinstance(city, list) else city.to_json(), 200

        return {"message": f"No city with {'name' if is_name else 'id'} '{identifier}' found!"}, 404


