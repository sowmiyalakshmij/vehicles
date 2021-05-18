from vehicles.repository.vehiclesData import vehiclesData
import json

def test_getVehicles() :
    try :
        # Call getVehicles
        vehDict = vehiclesData.getVehicles()

        # Create 1 new vehicle
        testVehId1 = "TEST_VEH_11"
        vehiclesData.createVehicle(testVehId1)

        # Call getVehicles and check if count of vehicles returned by
        # getVehicles increased by 1
        vehDict1 = vehiclesData.getVehicles()
        assert (len(vehDict1) == len(vehDict) + 1)

        # Deregister vehicle
        vehiclesData.deleteVehicle(testVehId1)
    except :
        assert (True == False)

def test_createVehicle() : 
    try :
        # Ensure "TEST_VEH_22" is not already created
        # by calling deleteVehicle
        testVehId2 = "TEST_VEH_22"
        vehiclesData.deleteVehicle(testVehId2)

        # Do getVehicles before creating new vehicle
        vehData = vehiclesData.getVehicles()

        # Create new vehicle
        vehiclesData.createVehicle(testVehId2)

        # Do getVehicles after creating new vehicle
        vehData1 = vehiclesData.getVehicles()

        # Number of vehicles returned should have increased by 1
        assert (len(vehData1) == len(vehData) + 1)

        # Delete vehicle
        vehiclesData.deleteVehicle(testVehId2)
    except :
        assert (True == False)
    
def test_deleteVehicle() :
    try :
        # Ensure "TEST_VEH_33" has already been created
        testVehId3 = "TEST_VEH_33"
        vehiclesData.createVehicle(testVehId3)

        # Do getVehicles before deleting "TEST_VEH_33"
        vehData = vehiclesData.getVehicles()

        # Delete "TEST_VEH_33"
        vehiclesData.deleteVehicle(testVehId3)

        # Do getVehicles after deleting "TEST_VEH_33"
        vehData1 = vehiclesData.getVehicles()

        # Number of vehilces returned should have decreased by 1
        assert (len(vehData1) == len(vehData) - 1)
    except :
        assert (True == False)

def test_getLocationFromRedis() :
    try :
        # Create a new vehicle
        testVehId4 = "TEST_VEH_44"
        vehiclesData.createVehicle(testVehId4)

        locDict = {
            "lat" : "52.531",
            "lng" : "13.403",
            "at" : "2019-09-01T12:59:13.5123Z"
        }
        locStr = json.dumps(locDict)

        # Update location for created vehicle
        vehiclesData.updateLocation(testVehId4, locStr)

        # Fetch vehicle location using getLocationFromRedis
        locStr1 = vehiclesData.getLocationFromRedis(testVehId4)

        # Location used in updateLocation should match the
        # location returned by getLocationFromRedis
        assert (locStr == locStr1)

        vehiclesData.deleteVehicle(testVehId4)
    except :
        assert (True == False)

def test_updateLocation() :
    try :
        testVehId5 = "TEST_VEH_55"
        vehiclesData.createVehicle(testVehId5)

        locDict = {
            "lat" : "52.531",
            "lng" : "13.403",
            "at" : "2019-09-01T12:59:13.5123Z"
        }
        locStr = json.dumps(locDict)

        # Update location for created vehicle
        vehiclesData.updateLocation(testVehId5, locStr)

        # Fetch vehicle location using getLocationFromRedis
        locStr1 = vehiclesData.getLocationFromRedis(testVehId5)

        # Location used in updateLocation should match the
        # location returned by getLocationFromRedis
        assert (locStr == locStr1)

        # Cleanup by calling deletVehicle
        vehiclesData.deleteVehicle(testVehId5)
    except :
        assert (True == False)

def test_isVehicleRegistered() :
    try :
        # Delete vehicle to ensure vehicle is unregistered
        testVehId6 = "TEST_VEH_66"
        vehiclesData.deleteVehicle(testVehId6)

        # Call isVehicleRegistered and assert that vehicle is not registered
        vehStatus = vehiclesData.isVehicleRegistered(testVehId6)
        assert (len(vehStatus) == 0)

        # Create new vehicle
        vehiclesData.createVehicle(testVehId6)

        # Call isVehicleRegistered and assert that vehicle is registered
        vehStatus = vehiclesData.isVehicleRegistered(testVehId6)
        assert (len(vehStatus) > 0)
    except :
        assert (True == False)
