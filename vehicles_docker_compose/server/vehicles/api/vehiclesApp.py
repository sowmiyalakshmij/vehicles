"""

Entry point for the flask app
serving /vehicles rest end points

"""

from flask import Flask
from flask import request, jsonify, make_response
from vehicles.logic.vehiclesLogic import vehiclesLogic
from vehicles.utils import vehicleConstants
from vehicles.utils.exceptions.vehicleExceptions import VehicleGenericException

app = Flask(__name__)

@app.route('/vehicles')
def getAllVehicles():

    """
        Get all vehicles
        localhost:5000/vehicles
    """
    try:
        veh_dict = vehiclesLogic.getVehicles()
        response = make_response(jsonify(veh_dict), 200)
        return response
    except VehicleGenericException as server_exception:
        response = make_response(jsonify({"vehicleServerError": server_exception.message}), 500)
        return response



@app.route('/vehicles', methods=['POST'])
def registerVehicle():
    """
        Register vehicle
        localhost:5000/vehicles POST
        Request body contains id as shown below
        {
            "id" : "VEH_100"
        }
    """
    try:
        vehicle = request.get_json()
        vehicle_id = vehicle['id']

        register_status = vehiclesLogic.registerVehicle(vehicle_id)
        if register_status == vehicleConstants.SUCCESS:
            # Return 204 No Content on success
            response = make_response(jsonify({}), 204)
        elif register_status == vehicleConstants.VEHICLE_ALREADY_REGISTERED:
            response = make_response(jsonify({"error": "The vehicle you are trying to register \
is already registered. You can start calling update location."}), 409)
        return response
    except VehicleGenericException as server_exception:
        response = make_response(jsonify({"vehicleServerError": server_exception.message}), 500)
        return response



@app.route('/vehicles/<id>/locations', methods=['POST'])
def updateVehicleLocation(id):
    """
    Location update of vehicle
    localhost:5000/vehicles/<id>/locations POST
    eg : POST localhost:5000/vehicles/VEH_8/locations
    Request body contains lat, lng and at as shown below :
    {
        "lat" : "12",
        "lng" : "14",
        "at" : "2019-09-01T12:00:00Z"
    }
    """
    try:
        location_info = request.get_json()
        update_status = vehiclesLogic.updateLocation(id, location_info)

        if update_status == vehicleConstants.SUCCESS:
            # Return 204 No Content on success
            response = make_response(jsonify({}), 204)
        elif update_status == vehicleConstants.VEHICLE_NOT_REGISTERED:
            response = make_response(jsonify({"error": "Please register vehicle before calling \
location update"}), 409)
        elif update_status == vehicleConstants.VEHICLE_OUTSIDE_CITY_BOUNDARY:
            # If vehicle is outside city boundary, don't update
            # location. Return 200 No content
            response = make_response(jsonify({"message": "Vehicle is outside city boundary. \
Location update discarded."}), 200)
        elif update_status == vehicleConstants.VEHICLE_UPDATE_FOR_OLDER_TIMESTAMP:
            response = make_response(jsonify({"error": "Timestamp of location update older \
than previous timestamp"}), 409)
        elif update_status == vehicleConstants.VEHICLE_UPDATE_WITHIN_3_SECONDS:
            response = make_response(jsonify({"error": "Location update is within 3 seconds \
of previous location update"}), 409)
        return response
    except VehicleGenericException as server_exception:
        response = make_response(jsonify({"vehicleServerError": server_exception.message}), 500)
        return response


@app.route('/vehicles/<id>', methods=['DELETE'])
def deregisterVehicle(id):
    """
    De-register vehicle
    localhost:5000/vehicles/<id> DELETE
    eg : DELETE localhost:5000/vehicles/VEH_2
    No request body
    """
    try:
        deregister_status = vehiclesLogic.deregisterVehicle(id)
        if deregister_status == vehicleConstants.SUCCESS:
            # Return 204 No Content on success
            response = make_response(jsonify({}), 204)
        elif deregister_status == vehicleConstants.VEHICLE_NOT_REGISTERED:
            response = make_response(jsonify({"error": "The vehicle you are trying to \
derigister is not registered."}), 409)
        return response
    except VehicleGenericException as server_exception:
        response = make_response(jsonify({"vehicleServerError": server_exception.message}), 500)
        return response

if __name__ == '__main__':
    app.run(debug=True)