#!/usr/local/bin/python3

import os
import time
import logging
from influxdb import InfluxDBClient
from datetime import datetime
import Adafruit_DHT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.debug('start measurement')

HOST = os.getenv('HOST', 'localhost')
PORT = os.getenv('PORT', 8086)
DB = os.getenv('DB', 'smart-home-db')
ROOM = os.getenv('ROOM', 'living room')
SENSOR = os.getenv('SENSOR', Adafruit_DHT.DHT22)
GPIO = os.getenv('GPIO', 4)

def buildMeasurement(name, value, unit, timestamp=str(datetime.utcnow()), room=ROOM):
    return {
            "measurement": str(name),
            "tags": {
                "unit": str(unit),
                "room": str(room)
            },
            "time": str(timestamp),
            "fields": {
                "value": value
            }
        }

def buildHumidity(timestamp, humidity):
    return buildMeasurement('room_humidity', humidity, 'Percent', timestamp)

def buildTemperature(timestamp, temperature):
    return buildMeasurement('room_temperature', temperature, 'Celcius', timestamp)


def measure(client):
    timestamp = datetime.utcnow()
    humidity, temperature = Adafruit_DHT.read_retry(SENSOR, GPIO)
    client.write_points([buildHumidity(timestamp, humidity), buildTemperature(timestamp, temperature)])
    logger.info('measurement stored succesfully: [Time: {}, Humidity: {}, Temperature: {}]'.format(timestamp, humidity, temperature))

client = InfluxDBClient(host=HOST, port=PORT, database=DB)
logger.debug('connected to InfluxDB')

#create DB if not existent
client.create_database(DB)

measure(client)

logger.debug('measurement stored')
