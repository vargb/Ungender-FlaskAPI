from .models import CarModel
from graphql import GraphQLError

def getAll_resolver(obj,info):
    try:
        cars=CarModel.query.all()
        res=[
                {
                    "Carid":car.carid,
                    "LastUsedDate":car.lastusedDate,
                    "Available":car.available
                }for car in cars
            ]
        return res
    except Exception as error:
        return GraphQLError([str(error)])