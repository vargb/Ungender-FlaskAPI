import flaskServer.config.config as Config
import jwt
from functools import wraps
from flask import request,jsonify,Response,current_app
from .models import UserModel

dbUrl = (
    "postgresql://"
    + Config.conf.postgres.user
    + ":"
    + Config.conf.postgres.password
    + "@"
    + Config.conf.postgres.host
    + ":"
    + Config.conf.postgres.sqlport
    + "/"
    + Config.conf.postgres.dbname
)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs)->(Response,int):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return jsonify({
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }), 401
        try:
            data=jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user=UserModel.get_by_id(data["phno"])
            if current_user is None:
                return jsonify({
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }), 401
            if not current_user["active"]:
                return jsonify({
                "message":"current user aint active",
                "data":None,
                "error":""
            }),403
        except Exception as e:
            return jsonify({
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }), 500

        return f(current_user, *args, **kwargs)

    return decorated
