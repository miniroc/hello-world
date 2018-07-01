#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import math
import string
import random
import base64
import json
import logging
import paho.mqtt.publish as publish
#from __future__ import print_fucntion

def randomword(length):
    '''get random letter as an ID'''
    #python3 requires ascii_lowercase
    return ''.join(random.choice(string.lowercase) for i in range(length))


def publish_str():
    '''publish a string to a broker'''
    for x in range(3):
#  time.sleep(1)
        time.sleep(random.randint(0, 5))
        
        encodedfile = "publish string message from raspi"
        
        packet_size = 30000
        id = randomword(8)
        start = 0
        end = packet_size
        length = len(encodedfile)
        pos = 0
        no_of_packets = math.ceil(length/packet_size)

        #payload type: "STRING", "PICTURE","OTHER"
        data = {"msg_type": "STRING",
                "id": id,
                "data": encodedfile,
                "pos":pos,
                "size":no_of_packets}

        msgs = [{'topic':"node1",
                 'payload':json.JSONEncoder().encode(data),
                 'qos':0,
                 'retain':False}]
        publish.multiple(msgs,
                         hostname="broker.shiftr.io",
                         port=1883,
                         client_id="raspi",
                         auth={'username':"miniroc_shiftr", 'password':"abcd1234"})
        logging.debug("published multiple messages")
        print("published multiple messages")

    return


def publish_img():
    '''publish an image to broker'''

    logging.debug("publish picture begin...")
    print("publish picture begin...")

    with open("pic.jpg", "rb") as f:
        filedata = f.read()

    #encode the image byte as Base64 to avoid some unexpected effect
    #by some characters may be mis-interprated as special meaning.
    #Base64 encoded are perfectly compatible with any channel. use A-Z
    #and a-z and 0-9 and + and / to encode 6 bits, use = for padding
    encodedfile = base64.b64encode(filedata)

# split data into chunks of size 3000
    packet_size = 30000
    id = randomword(8)
    start = 0
    end = packet_size
    length = len(encodedfile)
    pos = 0
    no_of_packets = math.ceil(length/packet_size)

    #while start <= 0:
    while start <= len(encodedfile):
        #payload type: "STRING", "PICTURE","OTHER"
        data = {"msg_type": "PICTURE",
                "id": id,
                "data": encodedfile[start:end],
                "pos":pos,
                "size":no_of_packets}
        #print(encodedfile[start:end])
        #publish.multiple to publish a dict or tuple.
        #dict format msg={'topic':"<topic>",'payload':"<payload>",'qos':<qos>,'retain':<retain>}
        #tuple format ("<topic>","<payload>",qos,retain)
        msgs = [{'topic': "node1",
                 'payload': json.JSONEncoder().encode(data),  #need to use jason for network transport
                 'qos': 0,
                 'retain': False}]
        logging.debug(msgs)
        publish.multiple(msgs, hostname="broker.shiftr.io", port=1883, client_id="raspi", auth={'username': "miniroc_shiftr", 'password': "abcd1234"})
        logging.debug("published one chunk")
        start += packet_size
        end += packet_size
        pos += 1
        time.sleep(1)

    logging.debug("publish picture done")
    print("publish picture done")
    return

def publish_upgrade_package():
    '''publish an upgrade package to broker'''

    logging.debug("publish upgrade package begin...")
    print("publish upgrade package begin...")

    with open("upgrade.pkg", "rb") as f:  # change to correct suffix
        filedata = f.read()

    #encode the image byte as Base64 to avoid some unexpected effect
    #by some characters may be mis-interprated as special meaning.
    #Base64 encoded are perfectly compatible with any channel. use A-Z
    #and a-z and 0-9 and + and / to encode 6 bits, use = for padding
    encodedfile = base64.b64encode(filedata)

# split data into chunks of size 3000
    packet_size = 30000
    id = randomword(8)
    start = 0
    end = packet_size
    length = len(encodedfile)
    pos = 0
    no_of_packets = math.ceil(length/packet_size)

    #while start <= 0:
    while start <= len(encodedfile):
        #payload type: "STRING", "PICTURE","UPGRADE_PACKAGE","OTHER"
        data = {"msg_type": "UPGRADE_PACKAGE",
                "id": id,
                "data": encodedfile[start:end],
                "pos":pos,
                "size":no_of_packets}
        #print(encodedfile[start:end])
        #publish.multiple to publish a dict or tuple.
        #dict format msg={'topic':"<topic>",'payload':"<payload>",'qos':<qos>,'retain':<retain>}
        #tuple format ("<topic>","<payload>",qos,retain)
        msgs = [{'topic': "node1",
                 'payload': json.JSONEncoder().encode(data),  #need to use jason for network transport
                 'qos': 0,
                 'retain': False}]
        logging.debug(msgs)
        publish.multiple(msgs, hostname="broker.shiftr.io", port=1883, client_id="raspi", auth={'username': "miniroc_shiftr", 'password': "abcd1234"})
        logging.debug("published one chunk")
        start += packet_size
        end += packet_size
        pos += 1
        time.sleep(1)

    logging.debug("publish upgrade package done")
    print("publish upgrade package done")
    return

def main():
    logging.basicConfig(filename='publish.log', filemode='w', level=logging.WARNING, format='%(levelname)s:%(asctime)s:%(message)s')
    #publish_str()
    publish_img()
    #publish_upgrade_package()
    return


if __name__ == "__main__":
    main()