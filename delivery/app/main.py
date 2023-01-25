#!/usr/bin/env python
import pika, gpxpy, json, ssl, sys, os
from datetime import datetime

def open_chan(host, credentials, context):

    parameters = pika.ConnectionParameters(
        host=host,
        port=5671,
        credentials=credentials,
        ssl_options=pika.SSLOptions(context))

    connection = pika.BlockingConnection(parameters)
    return connection, connection.channel()

def send_msg(channel, content):
    channel.basic_publish(
        exchange='',
        routing_key='delivery',
        body=json.dumps(content),
        properties=pika.BasicProperties(content_type='application/json'))

def fetch_gpx(track_file):
    try:
        with open(track_file, "r") as gpx_file:
            return gpxpy.parse(gpx_file)
    except (OSError, gpxpy.gpx.GPXXMLSyntaxException) as e:
        print(f'[error]: {e}')
        sys.exit(1)

def forge_pickup(package):
    content = {
        'type': 'pickup',
        'package_id': package,
        'delivery_id': DELIVERY_ID,
        'timestamp': datetime.now().isoformat()
    }
    return content

def forge_update_gps(packages, coords):
    content = {
        'type': 'gps',
        'package_list': packages,
        'coords': (coords.latitude, coords.longitude),
        'delivery_id': DELIVERY_ID,
        'timestamp': datetime.now().isoformat()
    }
    return content

def forge_deliver(package, state):
    content = {
        'type': 'deliver',
        'package_id': package,
        'state': state,
        'delivery_id': DELIVERY_ID,
        'timestamp': datetime.now().isoformat()
    }
    return content

def main():
    try:
        packages = sys.argv[1:]
    except IndexError:
        print('[error]: no package defined')
        sys.exit(1)

    # Creating ssl context
    context = ssl.create_default_context(cafile='/etc/ssl/certs/ca.crt')
    context.verify_mode = ssl.CERT_REQUIRED

    # Define credentials
    credentials = pika.PlainCredentials(DELIVERY_ID, DELIVERY_PWD)

    # Open the channel
    connection, channel = open_chan(AMQP_SERVER, credentials, context)

    # register all pacakges to pickup
    for package in packages:
        send_msg(channel, forge_pickup(package))
        connection.sleep(1)

    # send coords update from the track_file to amqp server
    for track in fetch_gpx(f"/app/tracks/{TRACK}").tracks:
        for segment in track.segments:
            for point in segment.points:
                send_msg(channel, forge_update_gps(packages, point))
                connection.sleep(1)

    # deliver packages to destination
    for package in packages:
        send_msg(channel, forge_deliver(package, 'delivered'))
        connection.sleep(1)

    # close connection with amqp server
    connection.close()

if __name__ == '__main__':
    try:
        DELIVERY_ID = os.environ['DELIVERY_ID']
    except KeyError:
        print('[error]: `DELIVERY_ID` environment variable required')
        sys.exit(1)

    try:
        DELIVERY_PWD = os.environ['DELIVERY_PWD']
    except KeyError:
        print('[error]: `DELIVERY_PWD` environment variable required')
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
