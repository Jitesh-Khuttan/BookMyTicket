from code.db.alchemy_db import db
from code.models.city import City


class Cinema(db.Model):

    __tablename__ = "cinema"
    cinema_id = db.Column(db.Integer, primary_key=True)
    cinema_name = db.Column(db.String(60), nullable=False)
    total_screens = db.Column(db.Integer, nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey("city.city_id"), nullable=False)

    def to_json(self, city_info=True):
        result =  {
            "cinema_id": self.cinema_id,
            "cinema_name": self.cinema_name,
            "total_screens": self.total_screens,
        }

        if city_info:
            result.update({
                "city_id": self.city.city_id,
                "city_name": self.city.city_name,
            })
        return result

    def add_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, cinema_id):
        return cls.query.filter_by(cinema_id=cinema_id).first()

    @classmethod
    def find_by_name(cls, cinema_name):
        return cls.query.filter_by(cinema_name=cinema_name).all()
