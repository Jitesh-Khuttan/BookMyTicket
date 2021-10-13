import os
from flask import Flask
from code.config.settings import add_app_settings, initialize_database, initialize_jwt, add_jwt_callbacks
from code.urls import initialize_urls
from code.models.cinema import Cinema
from code.models.city import City
from code.models.movie import Movie
from code.models.city_movie_association import CityMovieAssociation

app = Flask(__name__)
app = add_app_settings(app)
app = initialize_database(app)
app = initialize_urls(app)
jwt = initialize_jwt(app)
jwt = add_jwt_callbacks(jwt)

if __name__ == "__main__":
    app.run(port=5000)
