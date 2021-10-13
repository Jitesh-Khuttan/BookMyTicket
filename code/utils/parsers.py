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

def get_city_movie_association_parser():
	_cm_parser = reqparse.RequestParser()
	_cm_parser.add_argument('city_id', type=int, required=True, help="Please provide city id.")
	_cm_parser.add_argument('movie_id', type=int, required=True, help="Please provide movie id.")

	return _cm_parser

def get_movie_cinema_association_parser():
	_mc_parser = reqparse.RequestParser()
	_mc_parser.add_argument('cinema_id', type=int, required=True, help="Please provide cinema id.")
	_mc_parser.add_argument('movie_id', type=int, required=True, help="Please provide movie id.")
	_mc_parser.add_argument('asof_date', type=str, required=True, help="Please provide asof date (YYYY-MM-DD).")
	_mc_parser.add_argument('timing', type=str, required=True, help="Please provide movie timings (HH:MM).")

	return _mc_parser

def get_book_ticket_parser():
	_ticket_parser = reqparse.RequestParser()
	_ticket_parser.add_argument('cinema_id', type=int, required=True, help="Please provide cinema id.")
	_ticket_parser.add_argument('movie_id', type=int, required=True, help="Please provide movie id.")
	_ticket_parser.add_argument('asof_date', type=str, required=True, help="Please provide asof date (YYYY-MM-DD).")
	_ticket_parser.add_argument('timing', type=str, required=True, help="Please provide movie timings (HH:MM).")
	_ticket_parser.add_argument('seats', action='append', required=True, help="Please provide movie seats to book.")

	return _ticket_parser