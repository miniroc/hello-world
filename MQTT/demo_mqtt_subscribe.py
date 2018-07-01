#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import json
import base64
import logging
import paho.mqtt.client as mqttClient
#from __future__ import print_fucntion


def on_connect(client, userdata, flags, rc):
    '''call back function'''
    if rc == 0:
        #subscribe topic
        client.subscribe("node1")
        logging.debug("connected to broker")
        print('connected to broker')
    else:
        loging.info("Connection failed")
    return

def on_string_message(payload_msg):
    '''process string type payload message'''
    print("message received: %s", payload_msg["data"])
    return


def on_picture_message(payload_msg):
    '''process picture type payload message'''

    global package

    if package.has_key(payload_msg["id"]) == False:
        package[payload_msg["id"]] = {"count":0, "total":payload_msg["size"],
                                      "pieces":{}, "id": payload_msg["id"]}
        package[payload_msg["id"]]["pieces"][payload_msg["pos"]] = payload_msg["data"]
    else:
        package[payload_msg["id"]]["pieces"][payload_msg["pos"]] = payload_msg["data"]
        package[payload_msg["id"]]["count"] += 1  #'count' starts from 0, stops at (n-1)
        logging.debug("count %d", package[payload_msg["id"]]["count"])


    if package[payload_msg["id"]]["count"] == package[payload_msg["id"]]["total"]:
        str_pkg = ""
        logging.debug("final count %d", package[payload_msg["id"]]["count"])
        logging.debug("final total %d", package[payload_msg["id"]]["total"])

        for i in range(package[payload_msg["id"]]["count"]+1):  # count starts from 0, stops at (n-1), range produces 0~('count'-1), need ('count'+1).
            str_pkg = str_pkg + package[payload_msg["id"]]["pieces"][i]
            logging.debug(str_pkg)
        with open("img_received.jpg", "wb") as f:
            imgbyte = bytearray(str_pkg, 'ascii')
            f.write(base64.b64decode(imgbyte))
            print("received picture message")
    return


def on_upgrade_package_message(payload_msg):
    '''process upgrade package type payload message'''

    global package

    if package.has_key(payload_msg["id"]) == False:
        package[payload_msg["id"]] = {"count":0, "total":payload_msg["size"],
                                      "pieces":{}, "id": payload_msg["id"]}
        package[payload_msg["id"]]["pieces"][payload_msg["pos"]] = payload_msg["data"]
    else:
        package[payload_msg["id"]]["pieces"][payload_msg["pos"]] = payload_msg["data"]
        package[payload_msg["id"]]["count"] += 1  #'count' starts from 0, stops at (n-1)
        logging.debug("count %d", package[payload_msg["id"]]["count"])


    if package[payload_msg["id"]]["count"] == package[payload_msg["id"]]["total"]:
        str_pkg = ""
        logging.debug("final count %d", package[payload_msg["id"]]["count"])
        logging.debug("final total %d", package[payload_msg["id"]]["total"])

        for i in range(package[payload_msg["id"]]["count"]+1):  # count starts from 0, stops at (n-1), range produces 0~('count'-1), need ('count'+1).
            str_pkg = str_pkg + package[payload_msg["id"]]["pieces"][i]
            logging.debug(str_pkg)
        with open("upgrade_package_received.pkg", "wb") as f:
            imgbyte = bytearray(str_pkg, 'ascii')
            f.write(base64.b64decode(imgbyte))
            print("receive upgrade package")
    return

  #dict_item = dict(message.payload)
  #dict_list.append(dict_item)
  #dict_list.insert(dict_item['pos'],dict_item), # insert in order
#  img_pieces[dict_item['pos']]=dict_item['data']
#  for x in dict_list:
#    if dict_item['pos'] < x['pos']:
#      dict_list.insert(dict_list.index(x),dict_item['pos'])  # add in order

#  if int(dict_item['pos']) >= int(dict_item['size'])-1  #received all of the segmented files
#    for x in dict_list:
#      img_string.append(x['data'])
#      with open('pic_received.jpg','wb') as f:
#        f.write(base64.b64decode(img_string))

def on_message(client, userdata, message):
    '''call back function'''
    payload = json.loads(message.payload.decode('ascii'))  # or ascii or utf-8  code
    logging.debug(payload["data"])
    msg_type = payload["msg_type"]
    #payload type: "STRING", "PICTURE","UPGRADE_PACKAGE","OTHER"
    logging.debug(msg_type)
    if(msg_type == "STRING"):
        on_string_message(payload)
    elif(msg_type == "PICTURE"):
        on_picture_message(payload)
    elif(msg_type == "UPGRADE_PACKAGE"):
        on_upgrade_package_message(payload)
    elif(msg_type == "OTHER"):
        print("not support message type.")
    else:
        print("message type error")
    return

def main():
    broker_address = "broker.shiftr.io"
    port = 1883
    user = "miniroc_shiftr"
    password = "abcd1234"

    client = mqttClient.Client("Kevin-Raspi", False)
    client.username_pw_set(user, password=password)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker_address, port=port)
    client.loop_start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("exiting")
        client.disconnect()
        client.loop_stop()
    return

package = {}

if __name__ == "__main__":
    logging.basicConfig(filename="subscriber.log", filemode='w',
				level=logging.WARNING, format='%(levelname)s:%(asctime)s:%(message)s')
    # execute only if run as a script
    main()
