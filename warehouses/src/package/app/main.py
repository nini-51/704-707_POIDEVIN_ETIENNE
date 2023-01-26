#!/usr/bin/env python
import paho.mqtt.publish as publish
import sys, os

broker = "mqtt.warehouse.local"

try:
    PACKAGE_ID = os.environ['PACKAGE_ID']
except KeyError:
    print('[error]: `PACKAGE_ID` environment variable required')
    sys.exit(1)

try:
    state = sys.argv[1]
except IndexError:
    print('[error]: `state` argument required')
    sys.exit(1)

# Define QOS level
QOS = 2 if state == 'init' else 1

try:
    # Publish single message
    publish.single("package/beacon", payload=f"{PACKAGE_ID},{state}", qos=QOS,
        hostname=broker, port=1883, client_id=PACKAGE_ID, keepalive=60)
    print("data published")
except:
    print("transmission failed")
    sys.exit(1)
