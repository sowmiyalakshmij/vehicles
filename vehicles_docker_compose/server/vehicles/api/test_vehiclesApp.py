import json


def test_getAllVehicles(app, client) :
    res = client.get('/vehicles')
    assert (res.status_code == 200)

def test_registerVehicle(app, client) :
    try :
        client.delete('/vehicles/TEST_VEH_API_REG')
        res = client.post('/vehicles', json={'id': 'TEST_VEH_API_REG'})
        print(f"res : {res}")
        assert (res.status_code == 204)
        
        res = client.post('/vehicles', json={'id': 'TEST_VEH_API_REG'})
        assert (res.status_code == 409)
    except :
        assert (True == False)
    finally :
        client.delete('/vehicles/TEST_VEH_API_REG')

def test_deregisterVehicle(app, client) :
    try :
        client.post('/vehicles', json={'id': 'TEST_VEH_API_DEREG'})
        res = client.delete('/vehicles/TEST_VEH_API_DEREG')
        assert(res.status_code == 204)

        res = client.delete('/vehicles/TEST_VEH_API_DEREG')
        assert(res.status_code == 409)
    except :
        assert (True == False)

def test_updateVehicleLocation(app, client) :
    try :
        client.delete('/vehicles/TEST_VEH_API_UPD_LOC')
        # Update location for unregistered vehicle
        res = client.post('/vehicles/TEST_VEH_API_UPD_LOC/locations', 
            json={
                "lat" : "52.531",
                "lng" : "13.403",
                "at" : "2019-09-01T12:59:13.5123Z"
            })
        assert (res.status_code == 409)

        # Register vehicle
        client.post('/vehicles', json={'id': 'TEST_VEH_API_UPD_LOC'})

        # Update location for registered vehicle
        res = client.post('/vehicles/TEST_VEH_API_UPD_LOC/locations', 
            json={
                "lat" : "52.531",
                "lng" : "13.403",
                "at" : "2019-09-01T12:59:13.5123Z"
            })
        assert (res.status_code == 204)

        # Update location of vehicle outside city boundary
        res = client.post('/vehicles/TEST_VEH_API_UPD_LOC/locations', 
            json={
                "lat" : "2.531",
                "lng" : "13.403",
                "at" : "2019-09-01T12:59:13.5123Z"
            })
        assert (res.status_code == 200)

        # Update location with older timestamp
        res = client.post('/vehicles/TEST_VEH_API_UPD_LOC/locations', 
            json={
                "lat" : "52.531",
                "lng" : "13.403",
                "at" : "2019-09-01T12:56:13.5123Z"
            })
        assert (res.status_code == 409)

        # Update location within 3 seconds of previous update
        res = client.post('/vehicles/TEST_VEH_API_UPD_LOC/locations', 
            json={
                "lat" : "52.531",
                "lng" : "13.403",
                "at" : "2019-09-01T12:59:13.5123Z"
            })
        assert (res.status_code == 409)

        # Legitimate location update. Should return 204 status code
        res = client.post('/vehicles/TEST_VEH_API_UPD_LOC/locations', 
            json={
                "lat" : "52.531",
                "lng" : "13.403",
                "at" : "2019-09-01T13:01:13.5123Z"
            })
        assert (res.status_code == 204)
    except :
        assert (True == False)
    finally :
        client.delete('/vehicles/TEST_VEH_API_UPD_LOC')
