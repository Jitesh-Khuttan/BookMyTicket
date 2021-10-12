from flask_restful import Api
from code.resources.user import UserRegister, User, UserLogin
from code.resources.city import CityRegister, CityQuery
from code.resources.movie import MovieRegister, MovieQuery

def initialize_urls(app):
	api = Api(app)

	#User APIs
	api.add_resource(UserRegister, '/user/register')
	api.add_resource(UserLogin, '/login')
	api.add_resource(User, '/user/<string:name>')

	#City APIs
	api.add_resource(CityRegister, '/city')
	api.add_resource(CityQuery, '/city/<identifier>')

	#Movie APIs
	api.add_resource(MovieRegister, '/movie')
	api.add_resource(MovieQuery, '/movie/<identifier>')

	return app