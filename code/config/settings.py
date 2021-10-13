import os
from code.db.path import db_dir_path
from code.db.alchemy_db import db
from flask_jwt_extended import JWTManager
from flask import jsonify

def add_app_settings(app):
	secret_key = 'hZ5vo1y39Md2BUf9YztpTs0WYkJnWDKs'
	app.config['JWT_SECRET_KEY'] = secret_key
	app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', f"sqlite:///{db_dir_path}/data.db")
	print(app.config['SQLALCHEMY_DATABASE_URI'])
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	app.config['PROPAGATE_EXCEPTIONS'] = True

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

def add_jwt_callbacks(jwt):
	@jwt.expired_token_loader
	def my_expired_token_callback(jwt_header, jwt_payload):
		return jsonify({"message": "Token expired! Please login again."}), 401

	@jwt.invalid_token_loader
	def my_invalid_token_callback(invalid_reason):
		return jsonify({"message": "Invalid token given!"}), 401

	return jwt
