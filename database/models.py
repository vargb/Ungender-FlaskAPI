from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Models(db.Model):
    __abstract__ = True
    id = db.Column(db.String())

    
class UserModel(Models):
    __tablename__ = "users"

    userid = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String())
    lname = db.Column(db.String())
    carid = db.Column(db.String())
    phno = db.Column(db.String(),unique=True)
    password = db.Column(db.String())

    def __init__(self,userid:str, fname:str, lname:str, carid:str, phno:str, password:str,id:str) -> None:
        self.id=id
        self.userid = userid
        self.fname = fname
        self.lname = lname
        self.carid = carid
        self.phno = phno
        self.password = password
    
    def __repr__(self):
        return f"<Car {self.userid}>"


class CarModel(Models):
    __tablename__ = "garage"
    
    carid = db.Column(db.Integer, primary_key=True,unique=True)
    lastusedDate = db.Column(db.String())
    available = db.Column(db.Boolean())

    def __init__(self,carid:str, lastusedDate:str, available:str,id:str) -> None:
        self.id=id
        self.carid = carid
        self.lastusedDate = lastusedDate
        self.available = available
        
    def __repr__(self):
        return f"<Car {self.carid}>"
