from code.db.alchemy_db import db 

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer)

    @classmethod
    def find_by_id(cls, user_id):
        return cls.query.filter_by(admin_id=user_id).first()
