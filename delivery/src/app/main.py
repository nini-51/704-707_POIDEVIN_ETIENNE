#!/usr/bin/env python
import pika, gpxpy, json, sys, os
from datetime import datetime
from time import sleep

def create_channel(server):
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=server))
        return connection, connection.channel()
    except:
        sys.exit(1)

def fetch_gpx(track_file):
    try:
        with open(track_file, "r") as gpx_file:
            return gpxpy.parse(gpx_file)
    except (OSError, gpxpy.gpx.GPXXMLSyntaxException) as e:
        print(f'[error]: {e}')
        sys.exit(1)

def pickup(package, channel):
    content = {
        'type': 'pickup',
        'package_id': package,
        'delivery_id': DELIVERY_ID,
        'timestamp': datetime.now().isoformat()
    }
    channel.basic_publish(exchange='', routing_key='delivery', body=json.dumps(content))

def update_gps(coords, packages, channel):
    content = {
        'type': 'gps',
        'package_list': packages,
        'coords': (coords.latitude, coords.longitude),
        'delivery_id': DELIVERY_ID,
        'timestamp': datetime.now().isoformat()
    }
    channel.basic_publish(exchange='', routing_key='delivery', body=json.dumps(content))

def deliver(package, state, channel):
    content = {
        'type': 'deliver',
        'package_id': package,
        'state': state,
        'delivery_id': DELIVERY_ID,
        'timestamp': datetime.now().isoformat()
    }
    channel.basic_publish(exchange='', routing_key='delivery', body=json.dumps(content))

def main():
    try:
        packages = sys.argv[1:]
    except IndexError:
        print('[error]: no package defined')
        sys.exit(1)

    # init connection with amqp server
    connection, channel = create_channel(AMQP_SERVER)

    # register all pacakges to pickup
    for package in packages:
        pickup(package, channel)
        sleep(1)

    # send coords update from the track_file to amqp server
    for track in fetch_gpx(f"/app/tracks/{TRACK}").tracks:
        for segment in track.segments:
            for point in segment.points:
                update_gps(point, packages, channel)
                sleep(1)

    # deliver packages to destination
    for package in packages:
        deliver(package, 'delivered', channel)
        sleep(1)

    # close connection with amqp server
    connection.close()

if __name__ == '__main__':
    try:
        DELIVERY_ID = os.environ['DELIVERY_ID']
    except KeyError:
        print('[error]: `DELIVERY_ID` environment variable required')
        sys.exit(1)

    try:
        AMQP_SERVER = os.environ['AMQP_SERVER']
    except KeyError:
        print('[error]: `AMQP_SERVER` environment variable required')
        sys.exit(1)

    try:
        TRACK = os.environ['TRACK']
    except KeyError:
        print('[error]: `TRACK` environment variable required')
        sys.exit(1)

    main()
