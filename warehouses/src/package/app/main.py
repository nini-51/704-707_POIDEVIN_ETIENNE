import paho.mqtt.client as paho
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

#create function for callback
def on_publish(client,userdata,result):
    print("data published")
    pass

#create client object
client1 = paho.Client(PACKAGE_ID)
#assign function to callback
client1.on_publish = on_publish
#establish connection
try:
    client1.connect(broker, 1883, 60)
except:
    sys.exit(1)

ret = client1.publish(f"test,{PACKAGE_ID},{state}")
