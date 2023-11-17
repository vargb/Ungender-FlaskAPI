from flask import Flask
from flask_cors import CORS
from flaskServer.database.db import dbUrl
from flask_jwt_extended import JWTManager
from .app import server

srv = Flask(__name__)
CORS(srv)

srv.config["SQLALCHEMY_DATABASE_URI"] = dbUrl
srv.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
srv.config['SECRET_KEY'] = "iwannakillmyself"
srv.config['JWT_TOKEN_LOCATION'] = ['cookies']
srv.config['JWT_COOKIE_CSRF_PROTECT'] = True
srv.config['JWT_CSRF_CHECK_FORM'] = True
jwt = JWTManager(srv)
app=server(srv)