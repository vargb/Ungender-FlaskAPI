from .models import CarModel,UserModel,db
import hashlib
from flask import jsonify
from graphql import GraphQLError

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
            return GraphQLError("UserID already exists!")
    except Exception as error:
        return GraphQLError(str(error))
    
def encrypt_string(hash_string):
    sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature