from abc import ABC

from vehicles.utils.exceptions.vehicleExceptionCodes import VehicleExceptionCodes


# Base exception
class VehicleException(Exception, ABC):
    message: str
    code: VehicleExceptionCodes


# To be used when there is any redis related exception / error
class VehicleRedisException(VehicleException):
    message: str
    code: VehicleExceptionCodes

    def __init__(self, message="Redis error", code=VehicleExceptionCodes.VEHICLE_REDIS_EXCEPTION_CODE):
        self.message = message
        self.code = code
        VehicleException.__init__(self, message)


# To be used when there is any kafka related exception / error
class VehicleKafkaException(VehicleException):
    message: str
    code: VehicleExceptionCodes

    def __init__(self, message="Kafka Error", code=VehicleExceptionCodes.VEHICLE_KAFKA_EXCEPTION_CODE):
        self.message = message
        self.code = code
        VehicleException.__init__(self, self.message)


# To be used when there is any kafka related exception / error
class VehicleMongoException(VehicleException):
    message: str
    code: VehicleExceptionCodes

    def __init__(self, message="Mongo Error", code=VehicleExceptionCodes.VEHICLE_MONGO_EXCEPTION_CODE):
        self.message = message
        self.code = code
        VehicleException.__init__(self, self.message)


# To be used as a generic exception class when there is any other exception / error
class VehicleGenericException(VehicleException):
    message: str
    code: VehicleExceptionCodes

    def __init__(self, message="Generic Server Error", code=VehicleExceptionCodes.VEHICLE_GENERIC_EXCEPTION_CODE):
        self.message = message
        self.code = code
        VehicleException.__init__(self, self.message)
