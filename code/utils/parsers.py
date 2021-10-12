from flask_restful import reqparse


def get_user_credential_parser():	
	_user_parser = reqparse.RequestParser()
	_user_parser.add_argument('username', type=str, required=True, help="Please provide the username")
	_user_parser.add_argument('password', type=str, required=True, help="Please provide the password.")

	return _user_parser


def get_city_parser(is_post=False):	
	_city_parser = reqparse.RequestParser()
	_city_parser.add_argument('city_name', type=str, required=is_post, help="Please provide the city name.")
	_city_parser.add_argument('pincode', type=int, required=is_post, help="Please provide city pincode.")

	if not is_post:
		_city_parser.add_argument('city_id', type=int, required=True, help="Please provide city id.")

	return _city_parser

def get_movie_parser(is_post=False):	
	_movie_parser = reqparse.RequestParser()
	_movie_parser.add_argument('movie_name', type=str, required=is_post, help="Please provide the movie name (30 chars max).")
	_movie_parser.add_argument('description', type=str, required=is_post, help="Please provide movie description (60 chars max).")

	if not is_post:
		_movie_parser.add_argument('movie_id', type=int, required=True, help="Please provide movie id.")

	return _movie_parser

def get_cinema_parser(is_post=False):	
	_cinema_parser = reqparse.RequestParser()
	_cinema_parser.add_argument('cinema_name', type=str, required=is_post, help="Please provide the cinema name (60 chars max).")
	_cinema_parser.add_argument('total_screens', type=int, required=is_post, help="Please provide total screens.")
	_cinema_parser.add_argument('city_id', type=int, required=is_post, help="Please provide city id of city where cinema exists.")

	if not is_post:
		_cinema_parser.add_argument('cinema_id', type=int, required=True, help="Please provide cinema id.")

	return _cinema_parser