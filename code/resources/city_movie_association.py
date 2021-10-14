import re
from flask_jwt_extended import jwt_required, get_jwt
from flask_restful import Resource
from code.models.city import City
from code.models.city_movie_association import CityMovieAssociation
from code.models.booking import Booking
from code.models.movie import Movie
from code.utils.parsers import get_city_movie_association_parser

import logging

_cm_parser = get_city_movie_association_parser()

def activate_deactivate_movie(request_data, activate=True):
    movie_id, city_id = request_data["movie_id"], request_data["city_id"]

    movie = Movie.find_by_id(movie_id)
    city = City.find_by_id(city_id)

    if movie and city:
        cm_association = CityMovieAssociation.find_by_id(city_id, movie_id)
        if cm_association:
            cm_association.is_active = True if activate else False
        else:
            cm_association = CityMovieAssociation(city_id, movie_id, is_active=True if activate else False)
        
        # CASE FOR DEACTIVATION - if a movie is already playing in few cities & now is being marked as inactive,
        # We should find all cinemas in this particular city & remove the movie for those.
        if not activate:
            for cinema in movie.cinemas:
                mc_association = Booking.find_by_id(cinema.cinema_id, movie.movie_id)
                if mc_association:
                    mc_association.delete_from_db()

        cm_association.add_to_db()
        return {"message": f"Movie '{movie.movie_name}' {'activated' if activate else 'deactivated'} in City '{city.city_name}'."}
    else:
        return {"message": "Please provide valid city & movie ids."}


class ActivateMovieInCity(Resource):
    
    @jwt_required()
    def put(self):
        claims = get_jwt()
        if not claims["is_admin"]:
            return {"message": "Operation is only permitted for the admins."}
        
        request_data = _cm_parser.parse_args()
        try:
            response = activate_deactivate_movie(request_data, activate=True)
            return response
        except Exception as exp:
            logging.error(f"ERROR:- {str(exp)}")
            return {"message": "Some error occured while processing the request."}


class DeactivateMovieInCity(Resource):

    @jwt_required() 
    def put(self):
        claims = get_jwt()
        if not claims["is_admin"]:
            return {"message": "Operation is only permitted for the admins."}
        
        request_data = _cm_parser.parse_args()
        try:
            response = activate_deactivate_movie(request_data, activate=False)
            return response
        except Exception as exp:
            logging.error(f"ERROR:- {str(exp)}")
            return {"message": "Some error occured while processing the request."}