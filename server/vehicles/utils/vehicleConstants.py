# Coordinates of Door2Door office
DOOR2DOOR_LATITUDE = 52.53
DOOR2DOOR_LONGITUDE = 13.403

# Statuses returned by logic layer
VEHICLE_ALREADY_REGISTERED = "VEHICLE ALREADY REGISTERED"
SUCCESS = "SUCCESS"
VEHICLE_NOT_REGISTERED = "VEHICLE NOT REGISTERED"
VEHICLE_OUTSIDE_CITY_BOUNDARY = "VEHICLE OUTSIDE CITY BOUNDARY"
VEHICLE_UPDATE_WITHIN_3_SECONDS = "LOCATION UPDATE WITHIN 3 SECONDS OF PREVIOUS UPDATE"
VEHICLE_UPDATE_FOR_OLDER_TIMESTAMP = "LOCATION UPDATE TIMESTAMP OLDER THAN PREVIOUS TIMESTAMP"

# Kafka config for local environment
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092,localhost:9092"
KAFKA_TOPIC_VEHICLE_REGISTER_DEREGISTER = "vehicle-register-deregister"
KAFKA_TOPIC_VEHICLE_LOCATION_UPDATE = "vehicle-location-updates"

# Mongodb config for local environment
MONGO_HOSTNAME = "localhost"
MONGO_PORT_NUMBER = 27017
MONGO_DBNAME = "vehicles-db"
