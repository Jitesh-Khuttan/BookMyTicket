from code.db.alchemy_db import db
from sqlalchemy.dialects.postgresql import JSON, TIME, DATE
from sqlalchemy.ext.mutable import MutableDict

import string
from datetime import datetime


class Booking(db.Model):

    __tablename__ = "booking"
    cinema_id = db.Column(
        db.Integer, db.ForeignKey("cinema.cinema_id"), primary_key=True
    )
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.movie_id"), primary_key=True)

    # Additional Fields
    asof_date = db.Column(DATE(), nullable=False)
    timing = db.Column(TIME(), nullable=False)
    # screen = db.Column(db.Integer, nullable=False)
    seats = db.Column(MutableDict.as_mutable(JSON))

    # Relationships
    cinema = db.relationship("Cinema", back_populates="movies")
    movie = db.relationship("Movie", back_populates="cinemas")

    def __init__(self, cinema_id, movie_id, asof_date, timing, total_rows=6):
        self.cinema_id = cinema_id
        self.movie_id = movie_id
        self.asof_date = datetime.strptime(asof_date, "%Y-%m-%d").date()
        self.timing = datetime.strptime(timing, "%H:%M").time()
        self.seats = {
            f"{s}{n}": False
            for s in string.ascii_uppercase[:total_rows]
            for n in range(1, 11)
        }

    def to_json(self):
        availability = {}
        for k, v in self.seats.items():
            availability.setdefault("Unavailable" if v else "Available", []).append(k)

        result = {
            "asof_date": self.asof_date.strftime("%Y-%m-%d"),
            "timing": self.timing.strftime("%H:%M"),
            "seats": availability,
        }
        result.update(self.movie.to_json(city_info=False))
        return result

    def add_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def __eq__(self, association):
        return (
            self.cinema_id == association.cinema_id
            and self.movie_id == association.movie_id
            and self.asof_date == association.asof_date
            and self.timing == association.timing
        )

    @classmethod
    def find_by_id(cls, cinema_id, movie_id):
        return cls.query.filter_by(cinema_id=cinema_id, movie_id=movie_id).first()

    @classmethod
    def find_by_show(cls, cinema_id, movie_id, asof_date, timing):
        asof_date, timing = (
            datetime.strptime(asof_date, "%Y-%m-%d").date(),
            datetime.strptime(timing, "%H:%M").time(),
        )
        return cls.query.filter_by(
            cinema_id=cinema_id, movie_id=movie_id, asof_date=asof_date, timing=timing
        ).first()
