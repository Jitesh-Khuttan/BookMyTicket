from flask_restful import Resource
from code.models.city import City
from flask_jwt_extended import jwt_required, get_jwt
from code.utils.parsers import get_city_parser

import logging


class CityRegister(Resource):
    @jwt_required()
    def post(self):
        claims = get_jwt()
        if not claims["is_admin"]:
            return {"message": "Operation is only permitted for the admins."}

        _city_parser = get_city_parser(is_post=True)
        request_data = _city_parser.parse_args()
        city_name, pincode = request_data["city_name"], request_data["pincode"]

        existing_cities = City.find_by_name(city_name)
        if existing_cities:
            existing_pincodes = [c.to_json().get("pincode") for c in existing_cities]
            if pincode in existing_pincodes:
                return {
                    "message": f"'{city_name}' city with pincode '{pincode}' already exists."
                }

        try:
            city = City(**request_data)
            city.add_to_db()
            return {"message": f"Successfully added '{city_name}' city!"}, 201
        except Exception as exp:
            logging.error(f"ERROR: {str(exp)}")
            return {
                "message": "Some error occured when trying to process the request."
            }, 400

    @jwt_required()
    def patch(self):
        claims = get_jwt()
        if not claims["is_admin"]:
            return {"message": "Operation is only permitted for the admins."}
            
        _city_parser = get_city_parser(is_post=False)
        request_data = _city_parser.parse_args()
        city_id = request_data["city_id"]

        city = City.find_by_id(city_id)
        if city:
            if request_data.get("city_name"):
                city.city_name = request_data["city_name"]

            if request_data.get("pincode"):
                city.pincode = request_data["pincode"]
        else:
            return {"message": f"No city found with id - {city_id}."}, 404

        try:
            city.add_to_db()
            return {"message": "Update done successfully!"}, 201
        except Exception as exp:
            logging.error(f"ERROR: {str(exp)}")
            return {
                "message": "Some error occured when trying to process the request."
            }, 400


class CityQuery(Resource):
    def get(self, identifier):
        is_digit = identifier.isdigit()
        city = (
            City.find_by_id(identifier) if is_digit else City.find_by_name(identifier)
        )
        if city:
            return [c.to_json() for c in city] if isinstance(
                city, list
            ) else city.to_json(), 200

        return {
            "message": f"No city with {'id' if is_digit else 'name'} '{identifier}' found!"
        }, 404
