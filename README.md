# BookMyTicket
This is a REST API of a movie ticketing application implemented in flask.

## How to execute on a local system:
> export PYTHONPATH=$PYTHONPATH:PATH_TO_DOWNLOADED_PROJECT  
> source venv/bin/activate  
> python code/app.py 

By default, application will use SQLlite when executed on local system. If you want to connect to your postgresql, please set the DATABASE_URL environment variable with connection string.
> Eg:- postgresql://database_username:password@localhost/databasename

## Postman Collection
Postman collection has been uploaded as the part of project itself. It consists of all the endpoints that application exposes. Collection uses an environment which consist of few variables. <b> {{base_url}} </b> by default points to heroku url (where this app is hosted). If running on a local system, please change this variable to your localhost url. (Eg:- http://127.0.0.1:5000/)

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
      - <b> /city </b> [POST] (<i><b> protected & admin access required </b> </i>): This endpoint is used to add city to the application. Let's say if our business expands to multiple regions, we will use this endpoint to add city information.  
        <b> payload fields: </b> city_name (str), pincode (int)  
        <b> required </b>: city_name, pincode  
        Eg:- `{ "city_name": "Chandigarh", "pincode": 160014 }`  
  
      - <b> /city </b> [PATCH] (<i><b> protected & admin access required </b> </i>): This endpoint is used to update city information.  
        <b> payload fields: </b> city_id (int), city_name (str), pincode (int)  
        <b> required </b>: city_id, (city_name, pincode) - atleast one required.  
        Eg:- `{ "city_id": 1, "city_name": "Chandigarh", "pincode": 160015 }`  



