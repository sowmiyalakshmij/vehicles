import json
import socket

import redis
from confluent_kafka import Producer
from vehicles.utils import vehicleConstants
from vehicles.utils.exceptions.vehicleExceptions import VehicleRedisException, VehicleKafkaException


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
class vehiclesData:
    try :
        rds = redis.Redis(host='redis', port=6379, decode_responses=True)
    except :
        raise VehicleRedisException
    
    try :
        kafkaProducer = Producer({'bootstrap.servers': vehicleConstants.KAFKA_BOOTSTRAP_SERVERS,
                              'client.id': socket.gethostname()})
    except :
        raise VehicleKafkaException

    @staticmethod
    def getVehicles():
        try:
            keys = vehiclesData.rds.keys()
            data = {}
            for k in keys:
                data[k] = vehiclesData.rds.get(k)
        except:
            raise VehicleRedisException
        return data

    @staticmethod
    def createVehicle(id=id):
        try:
            # Add entry in redis for vehicle registration
            vehiclesData.rds.set(id, "")
        except:
            raise VehicleRedisException
        try:
            # Emit event to kafka topic corresponding to vehicle registration
            kafkaPayload = {"id": id, "action": "REGISTER"}
            vehiclesData.kafkaProducer.produce(vehicleConstants.KAFKA_TOPIC_VEHICLE_REGISTER_DEREGISTER, key=id,
                                               value=json.dumps(kafkaPayload))
        except:
            raise VehicleKafkaException

    @staticmethod
    def deleteVehicle(id):
        try:
            # Delete entry from redis to indicate vehicle deregistration
            vehiclesData.rds.delete(id)
        except:
            raise VehicleRedisException

        try:
            # Emit event to kafka topic corresponding to vehicle deregistration
            kafkaPayload = {"id": id, "action": "DEREGISTER"}
            vehiclesData.kafkaProducer.produce(vehicleConstants.KAFKA_TOPIC_VEHICLE_REGISTER_DEREGISTER, key=id,
                                               value=json.dumps(kafkaPayload))
        except:
            raise VehicleKafkaException

    @staticmethod
    def getLocationFromRedis(id):
        try:
            return vehiclesData.rds.get(id)
        except:
            raise VehicleRedisException

    @staticmethod
    def updateLocation(id, val):
        try:
            # Update redis with new location details
            vehiclesData.rds.set(id, val)
        except:
            raise VehicleRedisException

        try:
            # Emit event to kafka topic corresponding to vehicle location update
            vehiclesData.kafkaProducer.produce(vehicleConstants.KAFKA_TOPIC_VEHICLE_LOCATION_UPDATE, key=id, value=val)
        except:
            raise VehicleKafkaException

    @staticmethod
    def isVehicleRegistered(id):
        try:
            return vehiclesData.rds.keys(id)
        except:
            raise VehicleRedisException
