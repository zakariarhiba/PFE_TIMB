import paho.mqtt.client as paho
from time import sleep

broker = "test.mosquitto.org"
port = 1883


def on_publish(client, userdata, result):  # create function for callback
    print("data published \n")
    pass


client1 = paho.Client("control1")  # create client object
client1.on_publish = on_publish  # assign function to callback
client1.connect(broker, port)

while True:
    ret = client1.publish("moniteurCHU/temp", "37")
    ret = client1.publish("moniteurCHU/spio2", "98")
    ret = client1.publish("mntrCHU/plsRate", "66")
    ret = client1.publish("moniteurCHU/humidity", "112")
    sleep(4)
    ret = client1.publish("moniteurCHU/temp", "38")
    ret = client1.publish("moniteurCHU/spio2", "97")
    ret = client1.publish("mntrCHU/plsRate", "68")
    ret = client1.publish("moniteurCHU/humidity", "111")
    sleep(4)
    ret = client1.publish("moniteurCHU/temp", "35")
    ret = client1.publish("moniteurCHU/spio2", "99")
    ret = client1.publish("mntrCHU/plsRate", "72")
    ret = client1.publish("moniteurCHU/humidity", "109")
    sleep(4)
