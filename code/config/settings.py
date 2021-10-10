import os
from code.db.path import db_dir_path
from code.db.alchemy_db import db
from flask_jwt_extended import JWTManager

def add_app_settings(app):
	secret_key = 'family-tree-secret-key'
	app.config['JWT_SECRET_KEY'] = secret_key
	app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', f"sqlite:///{db_dir_path}/data.db")
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

	return app

def initialize_database(app):
	db.init_app(app)

	@app.before_first_request
	def create_tables():
	    "Creates tables if they don't exist."
	    db.create_all()

	return app


def initialize_jwt(app):
	return JWTManager(app)