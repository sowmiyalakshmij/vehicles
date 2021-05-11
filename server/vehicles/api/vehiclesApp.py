from flask import Flask
from flask import request, jsonify, make_response
from http import HTTPStatus
from vehicles.logic.vehiclesLogic import vehiclesLogic
from vehicles.utils import vehicleConstants

app = Flask(__name__)

# Get all vehicles
# localhost:5000/vehicles
@app.route('/vehicles')
def getAllVehicles() :
	vehDict = vehiclesLogic.getVehicles()
	response = make_response(jsonify(vehDict), 200)
	return response

# Register vehicle
# localhost:5000/vehicles POST 
# Request body contains id as shown below
# {
#     "id" : "VEH_100"
# }
@app.route('/vehicles', methods=['POST'])
def registerVehicle():
	vehicle = request.get_json()
	id = vehicle['id']

	registerStatus = vehiclesLogic.registerVehicle(id)
	if registerStatus == vehicleConstants.SUCCESS :
		# Return 204 No Content on success
		response = make_response(jsonify({}), 204)
	elif registerStatus == vehicleConstants.VEHICLE_ALREADY_REGISTERED :
    		response = make_response(jsonify({"error" : "The vehicle you are trying to register \
is already registered. You can start calling update location."}), 409)
	
	return response

# Location update of vehicle
# localhost:5000/vehicles/<id>/locations POST 
# eg : POST localhost:5000/vehicles/VEH_8/locations
# Request body contains lat, lng and at as shown below :
# {
#     "lat" : "12",
#     "lng" : "14",
#     "at" : "2019-09-01T12:00:00Z"
# }
@app.route('/vehicles/<id>/locations', methods=['POST'])
def updateVehicleLocation(id):
	locationInfo = request.get_json()
	updateStatus = vehiclesLogic.updateLocation(id, locationInfo)

	if updateStatus == vehicleConstants.SUCCESS :
		# Return 204 No Content on success
		response = make_response(jsonify({}), 204)
	elif updateStatus == vehicleConstants.VEHICLE_NOT_REGISTERED :
		response = make_response(jsonify({"error" : "Please register vehicle before calling \
location update"}), 409)
	elif updateStatus == vehicleConstants.VEHICLE_OUTSIDE_CITY_BOUNDARY :
    		# If vehicle is outside city boundary, don't update 
			# location. Return 200 No content
    		response = make_response(jsonify({"message" : "Vehicle is outside city boundary. \
Location update discarded."}), 200)
	return response

# De-register vehicle
# localhost:5000/vehicles/<id> DELETE
# eg : DELETE localhost:5000/vehicles/VEH_2
# No request body
@app.route('/vehicles/<id>', methods=['DELETE']) 
def deregisterVehicle(id):
	deregisterStatus = vehiclesLogic.deregisterVehicle(id)
	if deregisterStatus == vehicleConstants.SUCCESS :
		# Return 204 No Content on success
		response = make_response(jsonify({}), 204)
	elif deregisterStatus == vehicleConstants.VEHICLE_NOT_REGISTERED :
    		response = make_response(jsonify({"error" : "The vehicle you are trying to \
derigister is not registered."}), 409)
	return response