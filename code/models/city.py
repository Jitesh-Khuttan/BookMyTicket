from code.db.alchemy_db import db


class City(db.Model):

    __tablename__ = "city"
    city_id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(20), nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    cinemas = db.relationship("Cinema", backref="city", lazy=True)
    movies = db.relationship("CityMovieAssociation", back_populates="city")

    def to_json(self):
        return {
            "city_id": self.city_id,
            "city_name": self.city_name,
            "pincode": self.pincode,
            "cinemas": [c.to_json(city_info=False) for c in self.cinemas],
        }

    def add_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, city_id):
        return cls.query.filter_by(city_id=city_id).first()

    @classmethod
    def find_by_name(cls, city_name):
        return cls.query.filter_by(city_name=city_name).all()


if __name__ == "__main__":
    # How to add many to many association objects

    from code.models.movie import Movie
    from code.models.city_movie_association import CityMovieAssociation

    chd = City(city_name="Chandigarh", pincode=123456)
    avenger = Movie(movie_name="Avengers", description="Action Movie")
    association = CityMovieAssociation(is_active=True)
    association.movie = avenger
    chd.movies.append(association)
