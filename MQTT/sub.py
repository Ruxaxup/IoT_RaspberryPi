#!/usr/bin/python

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import pygame
import thread
from raspcontroller import *

serverIP = "148.202.23.200"
subTopic = "raspberryPi/instruction/#"
publishTopic = "raspberryPi/server/"

raspberry = RaspController(subTopic[:-1])

global soundPlayer
#Play a sound using pygame lib
def playSound(file):
    print "Playing sound " , file
    soundPlayer = True
    print "Thread started" , str(soundPlayer)
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    print "Thread finished"
    soundPlayer = False

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(subTopic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #The message that is going to be delivered to the server
    raspResponse = ""
    #Determines if a instruction is executed or not
    execute = False
    print(msg.topic+" "+str(msg.payload))
    instruction = str(msg.payload)

    #Verify if this IoT device must execute the instruction given
    if raspberry.isGlobalInstruction(instruction):
        execute = True
        raspResponse = raspberry.executeInstruction(instruction)        
        #publish to Server
    else:
    #Verify the MAC Address
        tokens = msg.topic.split("/")  
        for token in tokens:
            if token == raspberry.getNetAndMACDictionary():
                execute = True
        if execute:
            raspResponse = raspberry.executeInstruction(instruction)
    #If execute is True, an instruction has been executed so we send a message to server
    if execute:
        print raspResponse
        publish.single(publishTopic+instruction, raspResponse, hostname=serverIP)
    """elif instruction == "sound":
        print "Before thread " ,str(soundPlayer)
        if not soundPlayer:
            thread.start_new_thread( playSound , ("/home/pi/Documents/sound.wav",))
    """
soundPlayer = False
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(serverIP, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
