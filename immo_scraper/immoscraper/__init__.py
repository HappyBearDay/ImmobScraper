import os
from flask import Flask
from flask_bcrypt import Bcrypt
#from immoscraper.config import Config

class Config :
    SECRET_KEY = os.environ.get("FLASK_BLOG_SECRET_KEY")
    

bcrypt = Bcrypt()


def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(Config)

    from immoscraper.main.routes import main
    app.register_blueprint(main)
    return app 