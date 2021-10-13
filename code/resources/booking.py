from flask_restful import Resource
from code.models.cinema import Cinema
from code.models.movie import Movie
from code.models.booking import Booking
from code.models.city_movie_association import CityMovieAssociation
from code.utils.parsers import (
    get_movie_cinema_association_parser,
    get_book_ticket_parser,
)

from datetime import date, datetime


class BookTicket(Resource):
    
    def patch(self):
        _ticket_parser = get_book_ticket_parser()
        request_data = _ticket_parser.parse_args()
        movie_id, cinema_id, asof_date, timing, seats = [
            request_data[key]
            for key in ("movie_id", "cinema_id", "asof_date", "timing", "seats")
        ]
        show = Booking.find_by_show(cinema_id, movie_id, asof_date, timing)

        if show:
            #Validation check - already booked ticket should not be allowed to book again.
            availability_check = [show.seats[seat_no] for seat_no in seats]
            if True in availability_check:
                return {"message": "Invalid Request:- Trying to book an unavailable seat."}, 400
            
            for seat_no in seats:
                show.seats[seat_no] = True
            show.add_to_db()
            return {"message": f"Seats '{', '.join(seats)}' booked."}, 200
        else:
            return {"message": "No movie show found for the given details!"}, 404

class ActivateMovieCinema(Resource):
    def post(self):
        _cm_parser = get_movie_cinema_association_parser()
        request_data = _cm_parser.parse_args()
        cinema_id, movie_id, asof_date = (
            request_data["cinema_id"],
            request_data["movie_id"],
            request_data["asof_date"],
        )

        # Date for which movie is being played should not be in past.
        if datetime.strptime(asof_date, "%Y-%m-%d").date() < datetime.now().date():
            return {
                "message": f"Invalid date  {asof_date} - you cannot add movie to run in the past."
            }

        movie = Movie.find_by_id(movie_id)
        cinema = Cinema.find_by_id(cinema_id)

        if movie and cinema:
            # Add a check if the movie is allowed to play in this cinema (based on city in which cinema is present)
            cm_assocation = CityMovieAssociation.find_by_id(
                cinema.city_id, movie.movie_id
            )
            if not cm_assocation:
                return {
                    "message": f"Movie '{movie.movie_name}' is not currently playing in '{cinema.city.city_name}' City."
                }, 404
            if cm_assocation and not cm_assocation.is_active:
                return {
                    "message": f"Movie '{movie.movie_name}' is not allowed to play in '{cm_assocation.city.city_name}' City."
                }, 400

            existing_association = Booking.find_by_id(cinema_id, movie_id)
            mc_associtaiton = Booking(**request_data)

            if (
                existing_association
                and mc_associtaiton
                and existing_association == mc_associtaiton
            ):
                return {"message": "This show already exists!"}, 400

            mc_associtaiton.add_to_db()
            return {
                "message": f"Movie '{movie.movie_name}'  added to Cinema '{cinema.cinema_name}'."
            }, 201
            # for date - '{mc_associtaiton}' and timing - ''."}

        else:
            return {"message": "Please provide correct movie and cinema ids."}, 404
