from code.db.alchemy_db import db


class Movie(db.Model):

    __tablename__ = "movie"
    movie_id = db.Column(db.Integer, primary_key=True)
    movie_name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(60), nullable=False)
    cities = db.relationship("CityMovieAssociation", back_populates="movie")

    def to_json(self):
        return {"movie_id": self.movie_id, "movie_name": self.movie_name, "description": self.description}

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