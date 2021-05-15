from enum import Enum


# Centralise here all the error codes so we know what number is available
class VehicleExceptionCodes(int, Enum):
    VEHICLE_REDIS_EXCEPTION_CODE = 1
    VEHICLE_KAFKA_EXCEPTION_CODE = 2
    VEHICLE_MONGO_EXCEPTION_CODE = 3
    VEHICLE_GENERIC_EXCEPTION_CODE = 4
