from vehicles.repository.vehiclesData import vehiclesData
from vehicles.utils.compassBearing import calculate_initial_compass_bearing
import json
import haversine
from vehicles.utils import vehicleConstants

class vehiclesLogic :
    @staticmethod
    def getVehicles() :
        vehDict = vehiclesData.getVehicles()
        return vehDict
    
    @staticmethod
    def registerVehicle(id) :
        if vehiclesData.isVehicleRegistered(id) :
            return vehicleConstants.VEHICLE_ALREADY_REGISTERED
        else :
            vehiclesData.createVehicle(id)
            return vehicleConstants.SUCCESS

    @staticmethod
    def deregisterVehicle(id) :
        if vehiclesData.isVehicleRegistered(id) :
            vehiclesData.deleteVehicle(id)
            return vehicleConstants.SUCCESS
        else :
            return vehicleConstants.VEHICLE_NOT_REGISTERED

    @staticmethod
    def updateLocation(id, locDict) :
        if vehiclesData.isVehicleRegistered(id) :
            # Calculate distance between current location to update and
            # door2door office coordinates
            # Disregard location update if distance from door2door is
            # greater than 3.5 km (it indicates vehicle is outside city boundaries)
            locTuple1 = (float(locDict['lat']), float(locDict['lng']))
            locTuple2 = (vehicleConstants.DOOR2DOOR_LATITUDE, vehicleConstants.DOOR2DOOR_LONGITUDE) # coordinates of door2door office
            distance = haversine.haversine(locTuple1, locTuple2)
            if distance <= 3.5 :
                pointNext = (float(locDict['lat']), float(locDict['lng']))
                prevLocStr = vehiclesData.getLocationFromRedis(id)
                if prevLocStr == "" :
                    pointPrev = pointNext
                else :
                    prevLocDict = json.loads(prevLocStr)
                    pointPrev = (float(prevLocDict['lat']), float(prevLocDict['lng']))
                
                # calculate_initial_compass_bearing() has been taken from https://gist.github.com/jeromer/2005586
                bearing = calculate_initial_compass_bearing(pointPrev, pointNext)
                locDict['bearing'] = bearing
                locDict['id'] = id
                locStr = json.dumps(locDict)
                vehiclesData.updateLocation(id, locStr)
                return vehicleConstants.SUCCESS
            else :
                return vehicleConstants.VEHICLE_OUTSIDE_CITY_BOUNDARY
        else :
                return vehicleConstants.VEHICLE_NOT_REGISTERED
