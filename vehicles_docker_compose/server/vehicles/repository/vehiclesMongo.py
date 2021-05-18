import json

from pymongo import MongoClient
from vehicles.utils import vehicleConstants

mongoClient = MongoClient(vehicleConstants.MONGO_HOSTNAME, vehicleConstants.MONGO_PORT_NUMBER)
vehiclesDb = mongoClient[vehicleConstants.MONGO_DBNAME]


# This method inserts a document into vehicle collection
# corresponding to register / deregister event
def insertRegisterDeregisterMsg(msg):
    msgDict = json.loads(msg.value())
    vehiclesDb.vehicle.insert_one(msgDict)
    print("REGISTER INSERTED")


# This method inserts a document into vehicleLocation collection
# corresponding to location update
def insertVehicleLocationMsg(msg):
    msgDict = json.loads(msg.value())
    vehiclesDb.vehicleLocation.insert_one(msgDict)
    print("LOCATION INSER")
