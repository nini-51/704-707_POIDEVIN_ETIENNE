import paho.mqtt.client as paho
import sys

broker="mosquitto"
port=1883
id=sys.argv[0]
status=sys.argv[1]


def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass


if(len(sys.argv)!=2):
    exit("les arguments ne sont pas bons !")

client1= paho.Client("1")                           #create client object
client1.on_publish = on_publish                          #assign function to callback
client1.connect(broker, 1883, 60)                                 #establish connection
ret= client1.publish("test",","+str(id)+","+status)
