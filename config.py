from flask_jwt_extended import JWTManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import timedelta  # Import timedelta from datetime module

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:root@localhost/Fintech2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'ABCDEF'  # Change this to a secret key of your choice
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=48)  # Example expiration time for the access token

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
