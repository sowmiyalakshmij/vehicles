import pymongo
from pymongo import MongoClient
import json

mongoClient = MongoClient("localhost", 27017)
vehiclesDb = mongoClient['vehicles-db']

def insertRegisterDeregisterMsg(msg) :
    msgDict = json.loads(msg.value())
    
    print(msgDict)
    vehiclesDb.vehicle.insert_one(msgDict)
    print("insert into mongo vehicle collection complete")

def insertVehicleLocationMsg(msg) :
    msgDict = json.loads(msg.value())

    print(msgDict)
    vehiclesDb.vehicleLocation.insert_one(msgDict)
    print("insert into mongo vehicleLocation collection complete")  
