from .models import CarModel,UserModel,db
import hashlib
from flask import jsonify,request,make_response
from graphql import GraphQLError
from flask_jwt_extended import (JWTManager, jwt_required,  get_jwt_identity,
                                create_access_token, create_refresh_token, 
                                set_access_cookies, set_refresh_cookies, 
                                unset_jwt_cookies,unset_access_cookies)
import datetime

def register(_, info, input):
    try:
        user = UserModel.query.filter_by(userid=input.get("userid")).first()

        if user is None:
            new_user = UserModel(
                userid=input.get("userid"),
                fname=input.get("fname"),
                carid=input.get("carid"),
                lname=input.get("lname"),
                phno=input.get("phno"),
                password=input.get("password"),
                id=encrypt_string(input.get("phno"))
            )
            db.session.add(new_user)
            db.session.commit()
            return new_user
        else:
            return GraphQLError("UserID already present!")
    except Exception as error:
        return GraphQLError(str(error))
    
def encrypt_string(hash_string):
    sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

def login(_,info,input):
    try:
        data=UserModel.query.filter_by(phno=input['phno']).first()
        if data.password!=input.get('password'):
            return GraphQLError("invalid login credentials, check again!")
        access_tokens=create_access_token(identity=input['phno'])
        resp=jsonify({"login":True})
        set_access_cookies(resp,access_tokens)
        return str("successful "+ access_tokens)
    except Exception as error:
        return str(error)
    
# def logout(_,info,input):
#     try:
#         data=UserModel.query.filter_by(phno=input['phno']).first()
#         if data.password!=input.get('password'):
#             return GraphQLError("invalid logout credentials, check again!")
#         unset_access_cookies(get_jwt_identity(input['phno']))
#     except Exception as error:
#         return str(error)

def getCar(_,info,input):
    try:
        user=UserModel.query.filter_by(phno=input['phno']).first()
        car=CarModel.query.filter_by(carid=input['carid']).first()
        if user is None or car is None:
            return GraphQLError("getCar credentials are invalid")
        if car.available:
            user.carid=input.get('carid')
            car.available=False
            db.session.commit()
            return user
        return GraphQLError("Car unavailable, use getAll to get the garage")
    except Exception as error:
        return GraphQLError(error)

def returnCar(_,info,input):
    try:
        user=UserModel.query.filter_by(phno=input['phno']).first()
        car=CarModel.query.filter_by(carid=input['carid']).first()
        if user is None or car is None:
            return GraphQLError("returnCar credentials are invalid")
        if car.available==False:
            user.carid=""
            car.available=True
            car.lastusedDate=datetime.datetime.now()
            db.session.commit()
            return user
        return GraphQLError("yo u dumbass aint got wheels, broke ass bitch, get some then return aight")
    except Exception as error:
        return GraphQLError(error)