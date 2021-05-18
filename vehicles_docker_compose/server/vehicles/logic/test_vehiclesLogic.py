from vehicles.logic.vehiclesLogic import vehiclesLogic
from vehicles.utils import vehicleConstants

def test_registerVehicle() :
    try :
        # Ensure "TEST_VEH_1" is not already registered
        testVehId1 = "TEST_VEH_1"
        deregisterStatus = vehiclesLogic.deregisterVehicle(testVehId1)

        # Register new vehicle "TEST_VEH_1"
        registerStatus = vehiclesLogic.registerVehicle(testVehId1)
        assert(registerStatus == vehicleConstants.SUCCESS)

        # Register already registered vehicle
        registerStatus = vehiclesLogic.registerVehicle(testVehId1)
        assert(registerStatus == vehicleConstants.VEHICLE_ALREADY_REGISTERED)

        deregisterStatus = vehiclesLogic.deregisterVehicle(testVehId1)

        # TODO : Add assertions for exceptions
    except :
        assert (True == False)

def test_deregisterVehicle() :
    try :
        # Ensure "TEST_VEH_1" is already registered
        testVehId2 = "TEST_VEH_2"
        registerStatus = vehiclesLogic.registerVehicle(testVehId2)

        # Deregister vehicle "TEST_VEH_1"
        deregisterStatus = vehiclesLogic.deregisterVehicle(testVehId2)
        assert(deregisterStatus == vehicleConstants.SUCCESS)

        # Degister unegistered vehicle
        deregisterStatus = vehiclesLogic.deregisterVehicle(testVehId2)
        assert(deregisterStatus == vehicleConstants.VEHICLE_NOT_REGISTERED)
    except :
        assert (True == False)   

def test_updateLocation() :
    try :
        # Ensure "TEST_VEH_1" is not already registered
        # call updateLocation on "TEST_VEH_1"
        # return value should be vehicleConstants.VEHICLE_NOT_REGISTERED
        testVehId3 = "TEST_VEH_3"
        deregisterStatus = vehiclesLogic.deregisterVehicle(testVehId3)

        # valid Location - within 3.5 km radius from door2door
        locDict = {
            "lat" : "52.531",
            "lng" : "13.403",
            "at" : "2019-09-01T12:59:13.5123Z"
        }
        updateStatus = vehiclesLogic.updateLocation(testVehId3, locDict)
        assert(updateStatus == vehicleConstants.VEHICLE_NOT_REGISTERED)

        # Register "TEST_VEH_1"
        # call updateLocation on "TEST_VEH_1" with valid location
        # return value should be vehicleConstants.SUCCESS
        vehiclesLogic.registerVehicle(testVehId3)
        updateStatus = vehiclesLogic.updateLocation(testVehId3, locDict)
        assert(updateStatus == vehicleConstants.SUCCESS)

        # call updateLocation on "TEST_VEH_1" again with the same at value
        # Return value should be vehicleConstants.VEHICLE_UPDATE_WITHIN_3_SECONDS
        updateStatus = vehiclesLogic.updateLocation(testVehId3, locDict)
        assert(updateStatus == vehicleConstants.VEHICLE_UPDATE_WITHIN_3_SECONDS)

        # call updateLocation on "TEST_VEH_1" again with an older timestamp
        # Return value should be vehicleConstants.VEHICLE_UPDATE_FOR_OLDER_TIMESTAMP
        locDict["at"] = "2019-09-01T12:58:13.5123Z"
        updateStatus = vehiclesLogic.updateLocation(testVehId3, locDict)
        assert(updateStatus == vehicleConstants.VEHICLE_UPDATE_FOR_OLDER_TIMESTAMP)

        # call updateLocation on "TEST_VEH_1" again with coordinates outside city boundary
        # Return value should be vehicleConstants.VEHICLE_OUTSIDE_CITY_BOUNDARY
        locDict["at"] = "2019-09-01T13:00:13.5123Z"
        locDict["lat"] = "2.531"
        updateStatus = vehiclesLogic.updateLocation(testVehId3, locDict)
        assert(updateStatus == vehicleConstants.VEHICLE_OUTSIDE_CITY_BOUNDARY)
    except :
        assert (True == False)

def test_getVehicles() :
    try :
        # Call getVehicles
        vehDict = vehiclesLogic.getVehicles()

        # Register 1 new vehicle
        testVehId4 = "TEST_VEH_4"
        vehiclesLogic.registerVehicle(testVehId4)

        # Call getVehicles and check if count of vehicles returned by
        # getVehicles increased by 1
        vehDict1 = vehiclesLogic.getVehicles()
        assert (len(vehDict1) == len(vehDict) + 1)

        # Deregister vehicle
        vehiclesLogic.deregisterVehicle(testVehId4)
    except :
        assert (True == False)


