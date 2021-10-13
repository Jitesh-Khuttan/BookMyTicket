from code.db.alchemy_db import db 

# M x N relationship with additonal fields.
class CityMovieAssociation(db.Model): 

    __tablename__ = "city_movie_association"
    city_id = db.Column(db.Integer, db.ForeignKey("city.city_id"), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.movie_id"), primary_key=True)

    #Addtional Columns
    is_active = db.Column(db.Boolean, nullable=False)

    #Relationships
    city = db.relationship("City", back_populates="movies")
    movie = db.relationship("Movie", back_populates="cities")
    
    def __init__(self, city_id, movie_id, is_active):
        self.city_id = city_id
        self.movie_id = movie_id
        self.is_active = is_active

    def add_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, city_id, movie_id):
        return cls.query.filter_by(city_id=city_id, movie_id=movie_id).first()