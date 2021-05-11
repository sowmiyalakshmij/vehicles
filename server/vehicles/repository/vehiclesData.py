import redis
import json
from confluent_kafka import Producer
import socket
from vehicles.utils import vehicleConstants

# This can be treated as the data layer for vehicles api server
# As only latest location / status of the vehicle would be of interest for consumption
# by the mobile app / web app and have to be broadcasted, only latest vehicle update 
# for each vehicle is kept in redis cache. 
#
# Every successful vehicle register / deregister will emit an event to the
# kafka cluster (topic name : vehicle-register-deregister). A kafka consumer 
# subscribed to this topic will take care of persisting the event in 
# mongodb (collection name : vehicle)
# 
# Every successful location update will emit en event to the kafka 
# cluster (topic name : vehicle-location-updates). A kafka consumer
# subscribed to this topic will take care of persisting the event 
# in mongodb (collection name : vehicleLocation)
#
class vehiclesData :
    rds = redis.Redis(decode_responses=True)
    kafkaProducer = Producer({'bootstrap.servers': vehicleConstants.KAFKA_BOOTSTRAP_SERVERS,
        'client.id': socket.gethostname()})

    @staticmethod
    def getVehicles() :
        keys = vehiclesData.rds.keys()
        data = {}
        for k in keys : 
            data[k] = vehiclesData.rds.get(k)
        return data

    @staticmethod
    def createVehicle(id = id) :
        # Add entry in redis for vehicle registration
        vehiclesData.rds.set(id, "")

        # Emit event to kafka topic corresponding to vehicle registration
        kafkaPayload = {"id" : id, "action" : "REGISTER"}
        vehiclesData.kafkaProducer.produce(vehicleConstants.KAFKA_TOPIC_VEHICLE_REGISTER_DEREGISTER, key=id, value=json.dumps(kafkaPayload))

    @staticmethod
    def deleteVehicle(id) :
        # Delete entry from redis to indicate vehicle deregistration
        vehiclesData.rds.delete(id)
        
        # Emit event to kafka topic corresponding to vehicle deregistration
        kafkaPayload = {"id" : id, "action" : "DEREGISTER"}
        vehiclesData.kafkaProducer.produce(vehicleConstants.KAFKA_TOPIC_VEHICLE_REGISTER_DEREGISTER, key=id, value=json.dumps(kafkaPayload))

    @staticmethod
    def getLocationFromRedis(id) :
        return vehiclesData.rds.get(id)

    @staticmethod
    def updateLocation(id, val) :
        # Update redis with new location details
        vehiclesData.rds.set(id, val)

        # Emit event to kafka topic corresponding to vehicle location update
        vehiclesData.kafkaProducer.produce(vehicleConstants.KAFKA_TOPIC_VEHICLE_LOCATION_UPDATE, key=id, value=val)

    @staticmethod
    def isVehicleRegistered(id) :
        return vehiclesData.rds.keys(id)