from flask import Flask, request
from flask_cors import CORS
import flaskServer.database.models as DB
from flaskServer.database import db 
from flask_migrate import Migrate
import hashlib



def encrypt_string(hash_string):
    sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature


def server()->Flask:
    app = Flask(__name__)
    CORS(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = db.dbUrl
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    DB.db.init_app(app)
    migrate=Migrate(app,DB.db)

    
    @app.route("/hello")
    def hello():
        return {"listen to this":"https://youtu.be/3h4kS6y8hpE?feature=shared"}

    @app.route("/user",methods=['POST','GET'])
    def handleUser():
        if request.method=='POST':
            if request.is_json:
                data=request.get_json()
                newUser=DB.UserModel(userid=data['userid'],fname=data['fname'],lname=data['lname'],carid=data['carid'],phno=data['phno'],password=data['password'],id=encrypt_string(data['phno']))
                DB.db.session.add(newUser)
                DB.db.session.commit()
                return {"HeadsUp":f"user {newUser.userid} has been created successfully"}
            else:
                return {"HeadsUp":"Error in sending JSON request payload"}
        elif request.method=='GET':
            users=DB.UserModel.query.all()
            res=[
                {
                    "userid":user.userid,
                    "fname":user.fname,
                    "lname":user.lname,
                    "carid":user.carid,
                    "phno":user.phno,
                    "password":user.password
                }for user in users
            ]
            return {"count":len(res),"users":res}
        
    @app.route("/car",methods=['POST','GET'])
    def handleCar():
        if request.method=='POST':
            if request.is_json:
                data=request.get_json()
                newCar=DB.CarModel(carid=data['carid'],lastusedDate=data['lastusedDate'],available=data['available'],id=encrypt_string(data['carid']))
                DB.db.session.add(newCar)
                DB.db.session.commit()
                return {"HeadsUp":f"car {newCar.carid} has been created successfully"}
            else:
                return {"HeadsUp":"Error in sending JSON request payload"}
        elif request.method=='GET':
            cars=DB.CarModel.query.all()
            res=[
                {
                    "carid":car.carid,
                    "lastusedDate":car.lastusedDate,
                    "available":car.available
                }for car in cars
            ]
            return {"count":len(res),"cars":res}
        

    return app


app=server()