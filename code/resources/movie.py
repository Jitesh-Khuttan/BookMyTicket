from flask_restful import Resource
from code.models.movie import Movie
from flask_jwt_extended import jwt_required, get_jwt
from code.utils.parsers import get_movie_parser
import logging


class MovieRegister(Resource):
    @jwt_required()
    def post(self):
        claims = get_jwt()
        if not claims["is_admin"]:
            return {"message": "Operation is only permitted for the admins."}

        _movie_parser = get_movie_parser(is_post=True)
        request_data = _movie_parser.parse_args()
        movie_name, description = (
            request_data["movie_name"],
            request_data["description"],
        )

        existing_movies = Movie.find_by_name(movie_name)
        if existing_movies:
            exisiting_ids = [m.to_json().get("id") for m in existing_movies]
            logging.warning(
                f"WARNING: Movie with name '{movie_name}' already exists. Existing ID(s) - {', '.join(exisiting_ids)}."
            )

        try:
            movie = Movie(**request_data)
            movie.add_to_db()
            return {"message": f"Successfully added '{movie_name}' movie!"}, 201
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
        
        _movie_parser = get_movie_parser(is_post=False)
        request_data = _movie_parser.parse_args()
        movie_id = request_data["movie_id"]

        movie = Movie.find_by_id(movie_id)
        if movie:
            if request_data.get("movie_name"):
                movie.movie_name = request_data["movie_name"]
            if request_data.get("description"):
                movie.description = request_data["description"]
        else:
            return {"message": f"No movie found with id - {movie_id}."}, 404

        try:
            movie.add_to_db()
            return {"message": "Updated done successfully!"}, 201
        except Exception as exp:
            logging.error(f"ERROR: {str(exp)}")
            return {
                "message": "Some error occured when trying to process the request."
            }, 400


class MovieQuery(Resource):
    def get(self, identifier):
        is_digit = identifier.isdigit()
        movie = (
            Movie.find_by_id(identifier) if is_digit else Movie.find_by_name(identifier)
        )
        if movie:
            return [m.to_json() for m in movie] if isinstance(
                movie, list
            ) else movie.to_json(), 200

        return {
            "message": f"No movie with {'id' if is_digit else 'name'} '{identifier}' found!"
        }, 404
