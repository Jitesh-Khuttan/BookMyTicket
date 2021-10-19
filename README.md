# BookMyTicket
This is a REST API of a movie ticketing application implemented in flask.

## How to execute on a local system:
> export PYTHONPATH=$PYTHONPATH:PATH_TO_DOWNLOADED_PROJECT  
> source venv/bin/activate  
> python code/app.py 

By default, application will use SQLlite when executed on local system. If you want to connect to your postgresql, please set the DATABASE_URL environment variable with connection string.
> Eg:- postgresql://database_username:password@localhost/databasename

## Postman Collection
Postman collection has been uploaded as the part of project itself. It consists of all the endpoints that application exposes. Collection uses an environment which consist of few variables. <b> {{base_url}} </b> by default points to heroku url (where this app is hosted - https://bookmyticket-flask.herokuapp.com). If running on a local system, please change this variable to your localhost url. (Eg:- http://127.0.0.1:5000/)

## Entity-Relationship Diagram
The normalized database design of the application has also been uploaded as part of the project. Please have a look to understand the low level design better.

## Project Details:
Following are traits of the application:
- User Sign up and login.
- Ability to view all the movies playing in your city.
- Ability to check all cinemas in which a movie is playing along with all the showtimes.
- For each showtime, check the availability of seats.
- Ability to book a ticket. (No payment gateway integration done as of now. Assume tickets can be booked for free).

## API Documentation
1. User API:
    - <b> /user/register </b> [POST]: This endpoint is used to register users for accessing the API.  
      <b> payload fields: </b> username, password  
      <b> required </b>: username, password     
      Eg:- `{ "username": "jkhuttan", "password": "qwerty" }`  

    - <b> /login </b> [POST]: This endpoint is used to login into the application. Returns back the JWT token, which is primarily used to access the protected endpoints.
      <b> payload fields: </b> username, password  
      <b> required </b>: username, password  
      Eg:- `{ "username": "jkhuttan", "password": "qwerty" }`  

    - <b> /user/\<string:username\> </b> [GET]: This endpoint returns the user id & username registered in the DB. 
  
2. City API:
      - <b> /cities </b> [GET] (<i><b> public access </b> </i>): This endpoint is used to find all the cities supported by the application.  
    
      - <b> /city </b> [POST] (<i><b> protected & admin access required </b> </i>): This endpoint is used to add city to the application. Let's say if our business expands to multiple regions, we will use this endpoint to add city information.  
        <b> payload fields: </b> city_name (str), pincode (int)  
        <b> required </b>: city_name, pincode  
        Eg:- `{ "city_name": "Chandigarh", "pincode": 160014 }`  
  
      - <b> /city </b> [PATCH] (<i><b> protected & admin access required </b> </i>): This endpoint is used to update city information.  
        <b> payload fields: </b> city_id (int), city_name (str), pincode (int)  
        <b> required </b>: city_id, (city_name, pincode - atleast one required) .  
        Eg:- `{ "city_id": 1, "city_name": "Chandigarh", "pincode": 160015 }`  
    
      - <b> /city/\<identifier\> </b> [GET] (<i><b> public access </b> </i>): This endpoint is used to find out city information. It also lists down all the cinemas in city & the movies playing in city. <b>"identifier" </b> can either be city name or city id.
  
3. Movie API:
      - <b> /movie </b> [POST] (<i><b> protected & admin access required </b> </i>): This endpoint is used to add movie to the application. Any new movie that comes in the market is first added to database using this API.  
        <b> payload fields: </b> movie_name (str), description (str)  
        <b> required </b>: movie_name, description  
        Eg:- `{ "movie_name": "Avengers", "description": "An excellent Marvels movie with multiple heroes!!" }`  
    
     - <b> /movie </b> [PATCH] (<i><b> protected & admin access required </b> </i>): This endpoint is used to update any information regarding movie.  
        <b> payload fields: </b> movie_id (int), movie_name (str), description (str)   
        <b> required </b>: movie_id, (movie_name, description - atleast one required)   
        Eg:- `{ "movie_id": 1, "description": "An excellent Marvels movie with great heroes!" }`  

     - <b> /movie/\<identifier\> </b> [GET] (<i><b> public access </b> </i>): This endpoint is used to get information regarding movie. It lists down all the cities in which this movie is currently running, along with the cinemas in each city. <b>"identifier"</b> can either be movie name or movie id.
    
    - <b> /movie/city/activate </b> [PUT] (<i><b> protected & admin access required </b> </i>): This endpoint is used to activate the movie in some city. Let's say some movie 'X' comes in the market, so admin has to explicitily activate it in the cities where the movie is allowed to play.  
        <b> payload fields: </b> movie_id (int), city_id (int)  
        <b> required </b>: movie_id, city_id  
        Eg:- `{ "movie_id": 1, "city_id": 2 }` 
    
    - <b> /movie/city/deactivate </b> [PUT] (<i><b> protected & admin access required </b> </i>): This endpoint is used to deactivate the movie in some city. Let's say the government decides to take down (or ban) some movie in some city. All the admin has to do is deactivate it in order to take the movie down in particular city from the application.  
        <b> payload fields: </b> movie_id (int), city_id (int)  
        <b> required </b>: movie_id, city_id  
        Eg:- `{ "movie_id": 1, "city_id": 2 }` 
    
    - <b> /movie/cinema/activate </b> [POST] (<i><b> protected & admin access required </b> </i>): This endpoint is used to add show in particular cinema.  
        <b> payload fields: </b> movie_id (int), cinema_id (int), asof_date (str: YYYY-MM-DD), timing (str: HH:MM)  
        <b> required </b>: movie_id, cinema_id, asof_date, timing    
        Eg:- `{ "movie_id": 1, "cinema_id": 2,  "asof_date": "2021-10-20", "timing": "5:30"}
 
4. Cinema API:
      - <b> /cinema </b> [POST] (<i><b> protected & admin access required </b> </i>): This endpoint is used to add cinema into some particular city.
        <b> payload fields: </b> cinema_name (str), total_screens (int), city_id (int)   
        <b> required </b>: cinema_name, total_screens, city_id     
        Eg:- `{ "cinema_name": "Picadilly", "total_screens": 4, "city_id": 1 }`  
  
      - <b> /cinema </b> [PATCH] (<i><b> protected & admin access required </b> </i>): This endpoint is used to update cinema information.  
        <b> payload fields: </b> cinema_id (int), total_screens (int), city_id (int)  
        <b> required </b>: cinema_id, (total_screens, city_id - atleast one required) .  
        Eg:- `{ "cinema_id": 1, "total_screens": 5 }`  
    
      - <b> /cinema/\<int:identifier\> </b> [GET] (<i><b> public access </b> </i>): This endpoint is used to find out cinema information. It lists down all the playing movies along with showtimes.  
    
5. Booking API:
      - <b> /bookticket </b> [POST] (<i><b> protected & login access required (any user) </b> </i>): This endpoint is used to book tickets for a show.  
        <b> payload fields: </b> movie_id (int), cinema_id (int), asof_date (str: YYYY-MM-DD), timing (str: HH:MM), seats (list)   
        <b> required </b>: movie_id, cinema_id, asof_date, timing, seats    
        Eg:- `{ "movie_id": 1, "cinema_id": 1, "asof_date": "2021-10-20", "timing": "5:30", "seats": ["A1", "A2"] }`   
    
