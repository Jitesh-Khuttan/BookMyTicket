import os
from flask import Flask
from urls import initialize_urls
from code.config.settings import add_app_settings, initialize_database, initialize_jwt

app = Flask(__name__)
app = add_app_settings(app)
app = initialize_database(app)
app = initialize_urls(app)
jwt = initialize_jwt(app)

if __name__ == "__main__":
    app.run(port=9000)
