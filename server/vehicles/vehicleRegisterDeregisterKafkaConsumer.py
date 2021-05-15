from confluent_kafka import Consumer, KafkaError
from vehicles.repository.vehiclesMongo import insertRegisterDeregisterMsg
from vehicles.utils import vehicleConstants


# Persists each register / deregister event in DB
def persistKafkaMsgInDB(msg):
    # This method inserts a document in mongodb collection
    # corresponding to register / deregister event
    insertRegisterDeregisterMsg(msg)


settings = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'mygroup',
    'client.id': 'client-1',
    'enable.auto.commit': True,
    'session.timeout.ms': 6000,
    'default.topic.config': {'auto.offset.reset': 'smallest'}
}

c = Consumer(settings)
c.subscribe([vehicleConstants.KAFKA_TOPIC_VEHICLE_REGISTER_DEREGISTER])

try:
    while True:
        msg = c.poll(0.1)
        if msg is None:
            continue
        elif not msg.error():
            print('Received message: {0}'.format(msg.value()))
        elif msg.error().code() == KafkaError._PARTITION_EOF:
            print('End of partition reached {0}/{1}'
                  .format(msg.topic(), msg.partition()))
        else:
            print('Error occured: {0}'.format(msg.error().str()))
        print(msg)
        persistKafkaMsgInDB(msg)

except KeyboardInterrupt:
    pass

finally:
    c.close()
