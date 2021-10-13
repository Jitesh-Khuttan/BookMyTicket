from code.db.alchemy_db import db


class Movie(db.Model):

    __tablename__ = "movie"
    movie_id = db.Column(db.Integer, primary_key=True)
    movie_name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(60), nullable=False)
    cities = db.relationship("CityMovieAssociation", back_populates="movie")
    cinemas = db.relationship("Booking", back_populates="movie")

    def to_json(self, city_info=True, cinema_info=True):
        result = {
            "movie_id": self.movie_id,
            "movie_name": self.movie_name,
            "description": self.description,
        }
        if city_info:
            result.update(
                {
                    "cities": [
                        association.city.to_json(cinema_info=False, movie_info=False)
                        for association in self.cities
                        if association.is_active
                    ]
                }
            )

            if cinema_info:
                for city_json in result["cities"]:
                    city_id = city_json["city_id"]
                    for association in self.cinemas:
                        if association.cinema.city_id == city_id:
                            city_json.setdefault("cinemas", []).append(association.cinema.to_json(city_info=False, movie_info=False))


        return result

    def add_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, movie_id):
        return cls.query.filter_by(movie_id=movie_id).first()

    @classmethod
    def find_by_name(cls, movie_name):
        return cls.query.filter_by(movie_name=movie_name).all()
