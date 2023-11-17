from flask import Flask, request,jsonify
import flaskServer.database.models as DB
from flaskServer.database import queries,mutations
from flask_migrate import Migrate
import hashlib
from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, ObjectType, gql,exceptions
from ariadne.explorer import ExplorerGraphiQL


def encrypt_string(hash_string):
    sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

def server(srv:Flask)->Flask:
    DB.db.init_app(srv)
    migrate=Migrate(srv,DB.db)
    
    
    try:
        type_defs=gql(load_schema_from_path("C:\VGBPython\graphql-flask\\flask1\\flaskServer\schema.graphql"))
    except exceptions.GraphQLFileSyntaxError:
        return None
    query=ObjectType("Query")
    mutation=ObjectType("Mutation")
    
    mutation.set_field("register",mutations.register)
    mutation.set_field("signin",mutations.login)
    mutation.set_field("getcar",mutations.getCar)
    mutation.set_field("returncar",mutations.returnCar)
    query.set_field("getAll",queries.getAll_resolver)
    schema = make_executable_schema(type_defs, query, mutation)
    
    @srv.route("/hello")
    def hello():
        return {"listen to this":"https://youtu.be/3h4kS6y8hpE?feature=shared"}

    @srv.route("/user",methods=['POST','GET'])
    def handleUser():
        if request.method=='POST':
            if request.is_json:
                data=request.get_json()
                newUser=DB.UserModel(userid=data['userid'],fname=data['fname'],lname=data['lname'],phno=data['phno'],password=data['password'],id=encrypt_string(data['phno']))
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
        
    @srv.route("/car",methods=['POST','GET'])
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
    
    @srv.route("/graphql",methods=["GET"])
    def graphql_playground():
        return ExplorerGraphiQL().html(None),200
    
    @srv.route("/graphql", methods=["POST"])
    def graphql_server():
        data = request.get_json()
        success, result = graphql_sync(
            schema,
            data,
            context_value=request,
            debug=srv.debug
        )
        status_code = 200 if success else 400
        return jsonify(result), status_code

    return srv
