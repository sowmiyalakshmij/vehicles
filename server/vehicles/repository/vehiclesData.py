# use redis as datastore
import redis
import json
from confluent_kafka import Producer
import socket

class vehiclesDataRedis :
    rds = redis.Redis(decode_responses=True)
    kafkaProducer = Producer({'bootstrap.servers': "localhost:9092,localhost:9092",
        'client.id': socket.gethostname()})

    @staticmethod
    def getVehicles() :
        keys = vehiclesDataRedis.rds.keys()
        data = {}
        for k in keys : 
            data[k] = vehiclesDataRedis.rds.get(k)
        
        return data

    @staticmethod
    def createVehicle(id = id) :
        vehiclesDataRedis.rds.set(id, "")

        kafkaPayload = {"id" : id, "action" : "REGISTER"}
        vehiclesDataRedis.kafkaProducer.produce("vehicle-register-deregister", key=id, value=json.dumps(kafkaPayload))

    @staticmethod
    def deleteVehicle(id) :
        vehiclesDataRedis.rds.delete(id)
        
        kafkaPayload = {"id" : id, "action" : "DEREGISTER"}
        vehiclesDataRedis.kafkaProducer.produce("vehicle-register-deregister", key=id, value=json.dumps(kafkaPayload))

    @staticmethod
    def getLocationFromRedis(id) :
        return vehiclesDataRedis.rds.get(id)

    @staticmethod
    def updateLocation(id, val) :
        #previousLocFromRedis = vehiclesDataRedis.rds.get(id)
        #vehiclesDataRedis.rds.set(id + '-PREVIOUS', previousLocFromRedis)
        vehiclesDataRedis.rds.set(id, val)

        vehiclesDataRedis.kafkaProducer.produce("vehicle-location-updates", key=id, value=val)

    @staticmethod
    def isVehicleRegistered(id) :
        return vehiclesDataRedis.rds.keys(id)