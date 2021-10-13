from flask_restful import Resource

class Root(Resource):

    def get(self):
        return {"message": "Welcome to Book My Ticket!!"}