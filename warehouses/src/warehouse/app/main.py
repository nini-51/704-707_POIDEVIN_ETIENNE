#!/usr/bin/env python
import paho.mqtt.subscribe as subscribe
from datetime import datetime
import requests, json
import threading
import sys, os
import time

lock = threading.Lock()
request = []
broker = "mosquitto"

# Load env vars
try:
    WAREHOUSE_ID = os.environ['WAREHOUSE_ID']
except KeyError:
    print(f'[error]: `WAREHOUSE_ID` environment variable required')
    sys.exit(1)

try:
    API_SERVER = os.environ['API_SERVER']
except KeyError:
    print(f'[error]: `API_SERVER` environment variable required')
    sys.exit(1)


def forge_content(payload):
    data = list(payload.decode().split(','))

    # Create content template
    content = {
        'status': 'in transit',
        'warehouse_id': WAREHOUSE_ID,
        'timestamp': datetime.now().isoformat()
    }

    if data[1] == 'init':
        method = 'POST'
        content['package_id'] = data[0]
    else:
        method = 'PUT'

    return content, method, data[0]

# | Package-id
# 	|  warehouse_id
# 	| timestanp (iso 8601)
# 	| satus
# 		|_> in transit
def send(content, method, package_id):
    #block ressource
    lock.acquire()

    try:
        if method == 'POST':
            r = requests.post(f"http://{API_SERVER}/packages", json=content)
        else:
            r = requests.put(f"http://{API_SERVER}/packages/{package_id.lower()}", json=content)
        r.raise_for_status()
    # except requests.HTTPError as error:
    #     print("The video library already exists.") if r.status_code == 409 else print(error)
    except requests.RequestException as error:
        print(error)

    #debloque ressource
    lock.release()

#fonction multi-threadee
def test_connexion():
    while(True):
        r=requests.get(f'http://{API_SERVER}')

        if (r.status_code == requests.codes.ok):
            lock.acquire()
            while(request):
                if(request[0]==post):
                    #POST
                    r = requests.post(request[1], data=request[2])
                else:
                    #PUT
                    r= requests.put(request[1],data=request[2])
                del request[0:3]
            lock.release()
        time.sleep(1)



# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):

    content, method, package_id = forge_content(msg.payload)

    send(content, method, package_id)

    #thread pour double connexion
    x=threading.Thread(target=test_connexion)
    # threads.append(x)
    x.start()

try:
    subscribe.callback(on_message, "package/beacon", qos=2,
        hostname=broker, port=1883, client_id=WAREHOUSE_ID, keepalive=60)
except:
    print("connection failed")
    sys.exit(1)
