from influxdb import InfluxDBClient
from datetime import datetime
import logging
import time
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('starting application')

def getBody(measurement):
    logger.info('measuring {0} °C'.format(measurement))
    return [
        {
            "measurement": "room_temperature",
            "tags": {
                "unit": "Celsius",
                "room": "living room"
            },
            "time": str(datetime.utcnow()),
            "fields": {
                "value": measurement
            }
        }
    ]

def measure(client):
    measurement = 20 + ( 4* (random.random() - .5))
    client.write_points(getBody(measurement))


def simulate(client, max_count):
    for i in range(max_count):
        time.sleep(2)
        measure(client)


client = InfluxDBClient(host='localhost', port=8086, database='example')
logger.info('connected to DB')

# client.drop_database('example')
client.create_database('example')

simulate(client, 100)

result = client.query('select value from room_temperature;')

# print("Result: {0}".format(result))
