from vehicles.repository.vehiclesData import vehiclesDataRedis
from vehicles.utils.compassBearing import calculate_initial_compass_bearing
import json

class vehiclesLogic :

    @staticmethod
    def getVehicles() :
        vehDict = vehiclesDataRedis.getVehicles()
        return vehDict
    
    @staticmethod
    def registerVehicle(id) :
        if vehiclesDataRedis.isVehicleRegistered(id) :
            return "VEHICLE ALREADY REGISTERED"
        else :
            vehiclesDataRedis.createVehicle(id)
            return "SUCCESS"

    @staticmethod
    def deregisterVehicle(id) :
        if vehiclesDataRedis.isVehicleRegistered(id) :
            vehiclesDataRedis.deleteVehicle(id)
            return "SUCCESS"
        else :
            return "VEHICLE NOT REGISTERED"

    @staticmethod
    def updateLocation(id, locDict) :
        if vehiclesDataRedis.isVehicleRegistered(id) :
            # Dummy bearing calculation
            # bearing = locDict['lat'] + locDict['lng']
            prevLocStr = vehiclesDataRedis.getLocationFromRedis(id)
            prevLocDict = json.loads(prevLocStr)
            print(f"prevLoc : {prevLocDict}")
            print(type(prevLocDict))
            # print(f"lat : {prevLoc["lat"]}  lng : {prevLoc["lng"]}")
            #bearing = calculateBearing()
            pointPrev = (float(prevLocDict['lat']), float(prevLocDict['lng']))
            pointNext = (float(locDict['lat']), float(locDict['lng']))
            bearing = calculate_initial_compass_bearing(pointPrev, pointNext)
            print(f"BEARING : {bearing}")
            locDict['bearing'] = bearing
            locDict['id'] = id
            locStr = json.dumps(locDict)
            vehiclesDataRedis.updateLocation(id, locStr)
            return "SUCCESS"
        else :
            return "VEHICLE NOT REGISTERED"
