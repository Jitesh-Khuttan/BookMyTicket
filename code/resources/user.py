from flask_restful import Resource
from code.utils.parsers import get_user_credential_parser
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token
from hmac import compare_digest
from code.models.user import UserModel
import logging
logging.basicConfig(level=2)

_user_parser = get_user_credential_parser()


class UserRegister(Resource):
    def post(self):
        request_data = _user_parser.parse_args()
        username = request_data['username']

        if UserModel.find_by_username(username):
            return {"message": f"{username} already exists."}

        try:
            UserModel(**request_data).register()
            return {"message": f"{username} successfully registered."}, 201
        except Exception as exp:
            logging.error(f"{exp}")
            return {"message": f"Failed to register."}, 400

class User(Resource):

    def get(self, name):
        user = UserModel.find_by_username(username=name)
        if user:
            return user.to_json()
        return {"message": f"User '{name}' not found!"}, 404

    @jwt_required()
    def delete(self, name):
        user = UserModel.find_by_username(username=name)
        if user:
            user.delete_from_db()
            return {"message": "User deleted!"}, 204
        return {"message": "Only admins can delete the users."}, 401


class UserLogin(Resource):

    def post(self):
        request_data = _user_parser.parse_args()
        user = UserModel.find_by_username(username=request_data['username'])
        if user:
            if compare_digest(request_data['password'], user.password):
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                return {'access_token': access_token, 'refresh_token': refresh_token}, 200
            return {"message": "Invalid credentials!"}, 401

        return {"message": "user not found!"}, 404