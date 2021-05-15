"""
Business logic layer of vehicles endpoint
"""
import json

import arrow
import haversine
from vehicles.repository.vehiclesData import vehiclesData
from vehicles.utils import vehicleConstants
from vehicles.utils.compassBearing import calculate_initial_compass_bearing
from vehicles.utils.exceptions.vehicleExceptions import VehicleGenericException, \
    VehicleRedisException, VehicleKafkaException

class vehiclesLogic:
    """
        vehiclesLogic class
    """
    @staticmethod
    def getVehicles():
        """
            getVehicles method
        """
        try:
            vehDict = vehiclesData.getVehicles()
            return vehDict
        except (VehicleRedisException, VehicleKafkaException) as e:
            raise VehicleGenericException(e.message) from e

    @staticmethod
    def registerVehicle(id):
        """
            registerVehicle method
        """
        try:
            if vehiclesData.isVehicleRegistered(id):
                return vehicleConstants.VEHICLE_ALREADY_REGISTERED
            else:
                vehiclesData.createVehicle(id)
                return vehicleConstants.SUCCESS
        except (VehicleRedisException, VehicleKafkaException) as e:
            raise VehicleGenericException(e.message) from e

    @staticmethod
    def deregisterVehicle(id):
        """
            deregisterVehicle method
        """
        try:
            if vehiclesData.isVehicleRegistered(id):
                vehiclesData.deleteVehicle(id)
                return vehicleConstants.SUCCESS
            else:
                return vehicleConstants.VEHICLE_NOT_REGISTERED
        except (VehicleRedisException, VehicleKafkaException) as e:
            raise VehicleGenericException(e.message) from e

    @staticmethod
    def updateLocation(id, locDict):
        """
            updateLocation method
        """
        try:
            if vehiclesData.isVehicleRegistered(id):
                # Calculate distance between current location to update and
                # door2door office coordinates
                # Disregard location update if distance from door2door is
                # greater than 3.5 km (it indicates vehicle is outside city boundaries)
                locTuple1 = (float(locDict['lat']), float(locDict['lng']))
                # coordinates of door2door office
                locTuple2 = (vehicleConstants.DOOR2DOOR_LATITUDE,
                             vehicleConstants.DOOR2DOOR_LONGITUDE)
                distance = haversine.haversine(locTuple1, locTuple2)

                if distance <= 3.5:
                    prevLocStr = vehiclesData.getLocationFromRedis(id)
                    if prevLocStr != "":
                        prevLocDict = json.loads(prevLocStr)
                        prevAtDateTime = arrow.get(prevLocDict['at']).datetime
                        nextAtDateTime = arrow.get(locDict['at']).datetime
                        timeDiffBtwnLocUpdates = (nextAtDateTime - prevAtDateTime).total_seconds()
                    if prevLocStr == "" or timeDiffBtwnLocUpdates >= 3:
                        pointNext = (float(locDict['lat']), float(locDict['lng']))
                        if prevLocStr == "":
                            pointPrev = pointNext
                        else:
                            pointPrev = (float(prevLocDict['lat']), float(prevLocDict['lng']))

                        # calculate_initial_compass_bearing() has been taken from
                        # https://gist.github.com/jeromer/2005586
                        bearing = calculate_initial_compass_bearing(pointPrev, pointNext)
                        locDict['bearing'] = bearing
                        locDict['id'] = id
                        locStr = json.dumps(locDict)
                        vehiclesData.updateLocation(id, locStr)
                        return vehicleConstants.SUCCESS
                    elif timeDiffBtwnLocUpdates < 0:
                        return vehicleConstants.VEHICLE_UPDATE_FOR_OLDER_TIMESTAMP
                    else:
                        return vehicleConstants.VEHICLE_UPDATE_WITHIN_3_SECONDS
                else:
                    return vehicleConstants.VEHICLE_OUTSIDE_CITY_BOUNDARY
            else:
                return vehicleConstants.VEHICLE_NOT_REGISTERED
        except (VehicleRedisException, VehicleKafkaException) as e:
            raise VehicleGenericException(e.message) from e
