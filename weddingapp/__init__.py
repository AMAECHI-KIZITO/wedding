from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from weddingapp import config
wed = Flask(__name__,instance_relative_config=True) #we instantiated an object for the class Flask
wed.config.from_pyfile('config.py')
wed.config.from_object(config) #here we are saying read the config from our class config
csrf=CSRFProtect(wed)
db=SQLAlchemy(wed)
migrate=Migrate(wed,db)
from weddingapp import models,forms
from weddingapp.routes import user_route,admin_route