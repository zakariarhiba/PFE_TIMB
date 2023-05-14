from email import message
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("tkhrbika/youss")
    client.subscribe("CoreElectronics/reserve")


def on_message(client, userdata, msg):
    topic, message = msg.topic, msg.payload.decode("utf-8")
   
    print(topic + " -> " + str(message))
    
    if topic == "tkhrbika/youss":
        print("yess we did it")
    

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org", 1883, 60)

client.loop_forever()
