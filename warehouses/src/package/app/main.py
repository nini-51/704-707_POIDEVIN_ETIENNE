import paho.mqtt.client as paho
import sys

broker="mqtt.warehouse.local"
port=1883
id=sys.argv[0]
status=sys.argv[1]

#create function for callback
def on_publish(client,userdata,result):
    print("data published \n")
    pass

if(len(sys.argv)!=2):
    exit("les arguments ne sont pas bons !")

#create client object
client1= paho.Client("1)
#assign function to callback
client1.on_publish = on_publish
#establish connection
client1.connect(broker, 1883, 60)
ret= client1.publish("test",","+str(id)+","+status)
