from flask_restful import Resource
from code.models.cinema import Cinema
from code.models.city import City
from flask_jwt_extended import jwt_required, get_jwt
from code.utils.parsers import get_cinema_parser

import logging


class CinemaRegister(Resource):
    @jwt_required()
    def post(self):
        claims = get_jwt()
        if not claims["is_admin"]:
            return {"message": "Operation is only permitted for the admins."}
        
        _cinema_parser = get_cinema_parser(is_post=True)
        request_data = _cinema_parser.parse_args()
        cinema_name = request_data["cinema_name"]

        try:
            cinema = Cinema(**request_data)
            if cinema:
                city = City.find_by_id(cinema.city_id)
                if not city:
                    return {
                        "message": f"City with id - {cinema.city_id} does not exist. Please provide valid city id."
                    }, 404
            cinema.add_to_db()
            return {"message": f"Successfully added '{cinema_name}' cinema!"}, 201
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
        
        _cinema_parser = get_cinema_parser(is_post=False)
        request_data = _cinema_parser.parse_args()
        cinema_id = request_data["cinema_id"]

        cinema = Cinema.find_by_id(cinema_id)
        if cinema:
            if request_data.get("cinema_name"):
                cinema.cinema_name = request_data["cinema_name"]

            if request_data.get("city_id"):
                cinema.city_id = request_data["city_id"]

            if request_data.get("total_screens"):
                cinema.total_screens = request_data["total_screens"]
        else:
            return {"message": f"No cinema found with id - {cinema_id}."}, 404

        try:
            cinema.add_to_db()
            return {"message": "Update done successfully!"}, 201
        except Exception as exp:
            logging.error(f"ERROR: {str(exp)}")
            return {
                "message": "Some error occured when trying to process the request."
            }, 400


class CinemaQuery(Resource):
    def get(self, identifier):
        is_digit = identifier.isdigit()
        cinema = (
            Cinema.find_by_id(identifier)
            if is_digit
            else Cinema.find_by_name(identifier)
        )
        if cinema:
            return [c.to_json() for c in cinema] if isinstance(
                cinema, list
            ) else cinema.to_json(), 200

        return {
            "message": f"No cinema with {'id' if is_digit else 'name'} '{identifier}' found!"
        }, 404
