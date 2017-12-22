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
            "time": str(datetime.now()),
            "fields": {
                "value": measurement
            }
        }
    ]


json_body = [
    {
        "measurement": "cpu_load_short",
        "tags": {
            "host": "server01",
            "region": "us-west"
        },
        "time": "2013-11-10T23:00:00Z",
        "fields": {
            "value": 0.64
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

#client.drop_database('example')
#client.create_database('example')

#client.write_points(getBody(20))

simulate(client, 100)

result = client.query('select value from room_temperature;')

print("Result: {0}"
    .format(result))
