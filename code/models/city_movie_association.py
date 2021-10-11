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
    
