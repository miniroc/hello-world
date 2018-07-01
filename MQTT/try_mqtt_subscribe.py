import paho.mqtt.client as mqttClient
import time

def on_connect(client, userdata, flags, rc):
  if rc == 0:
    print("connected to broker")
    global Connected
    Connected = True
  else:
    print("Connection failed")

def on_message(client, userdata, message):
  print "message received: "+message.payload

Connected = False

broker_address = "broker.shiftr.io"
port = 1883
user = "miniroc_shiftr"
password = "abcd1234"

client = mqttClient.Client("Kevin-Raspi",False)
client.username_pw_set(user,password=password)
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address,port=port)
client.loop_start()

while Connected != True:
  time.sleep(0.1)

client.subscribe("try")

try:
  while True:
    time.sleep(1)
    client.
except KeyboardInterrupt:
  print"exiting"
  client.disconnect()
  client.loop_stop()
