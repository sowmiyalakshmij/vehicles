import pymongo
import time


mongoClient = pymongo.MongoClient("db", 27018)

vehiclesDb = mongoClient["vehicles-db"]
vehicleColl = vehiclesDb["vehicle"]
vehicleLocColl = vehiclesDb["vehicleLocation"]

vehiclesDb.vehicle.insert_one({"id" : "VEH_SETUP_1"})
