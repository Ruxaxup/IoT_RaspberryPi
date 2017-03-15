import RPi.GPIO as GPIO
import sys
import socket
import fcntl
import struct
import os
from uuid import getnode as get_mac
from sensorsmodule import *

class RaspController(object):
	
	def __init__(self, subTopic):
                #Where is the board subscribed
                self.subTopic = subTopic
                #instructions per board
                self.instructionSet = {}
                #instructions executed by all boards
                self.globalInstructions = []
                #net interfaces and mac dictionary
                self.NetAndMAC = {}
                #net interfaces and IP dictionary
                self.NetAndIP = {}
                #Initialize all sensors
		self.sModule = SensorsModule()

        	#Get Internet interfaces and its MAC address
                self.getNetInterfacesAndMACs()
                print self.NetAndMAC
                #if not self.NetAndMAC:
                    #Cant getIP :c
                if self.NetAndMAC:
                    self.getNetsIP()
                    print self.NetAndIP
                else:
                    print "This board doesn't support Internet connection or the module is disconnected."

		print "Raspberry initialized"
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(11,GPIO.OUT)
		#register raspberry instruction set for MQTT
		self.addInstructionToRaspberry('discover',"Retrieves information about IoT devices connected to the topic")
		self.addInstructionToRaspberry('turnOnLED',"Turns on a LED on pin #4 of the raspberry pi b+ board")
		self.addInstructionToRaspberry('turnOffLED',"Turns off a LED on pin #4 of the raspberry pi b+ board")
		self.addInstructionToRaspberry('getInstructions',"Retrieves the list of instructions of the board")
		#instructionSet('playSound',"Plays a .wav audio file")

                #After you registry the instructions, indicate which ones are global
		self.globalInstructions.append("discover")
    
	def getNetInterfacesAndMACs(self):
        	self.interfaces = os.listdir('/sys/class/net/')
            	if not self.interfaces:
                	print "No Internet interfaces have been found."
        	for x in self.interfaces:
            		path = '/sys/class/net/' + str(x) + '/address'
            		if os.path.exists(path):
                		with open(path, 'r') as f:
                    			try:
                        			self.NetAndMAC[x] = f.readline().strip('\n')
                        			f.close()
                    			except:
                        			print path + " does not exist."

	def getNetsIP(self):            
            	for x in self.interfaces:
                    	tempIP = self.getIPAddress(str(x))
                    	if tempIP:
                        	self.NetAndIP[x] = tempIP
                        else:
                            self.NetAndIP[x] = "n/a"

	def getIPAddress(self,ifname):
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        		return socket.inet_ntoa(fcntl.ioctl(
            		s.fileno(),
            		0x8915, #SIOCGIFADDR
            		struct.pack('256s', ifname[:15])
            		)[20:24])
		except IOError:			
			print str(IOError)
			return None
    
    	#We would like to retrieve eth0 or wlan0 MAC address    
	def getNetAndMACDictionary(self):
		return self.NetAndMAC
	
	def canExecuteInstruction(self, mac):
		for key,value in self.NetAndMAC.iteritems():
			if mac == value:
				return True
		return False

	def checkConnectedSensors(self):
		print "Checking connection"

	def readSensors(self):
		print "%0.1f" % self.sModule.readTemperature()
		print "%0.1f" % self.sModule.readPressure()
		print "%s" % self.sModule.readLight()

	def turnOnLED(self):
		GPIO.output(11,GPIO.HIGH)

	def turnOffLED(self):
		GPIO.output(11,GPIO.LOW)

	def getSensorsModule(self):
		return self.sModule

        def addInstructionToRaspberry(self, instruction, description):
                self.instructionSet[instruction] = description

        def getInstructions(self):
                cadena = 'You can use one of the following topics to send instructions to this board:\n'
                for key, value in self.NetAndMAC.iteritems():
                        cadena += '\t*{0}\n'.format(self.subTopic + value)
                cadena += "Instruction set:\n"
                for key,value in self.instructionSet.items():
                        cadena += key + ", "
                return cadena[:-1]

        def isGlobalInstruction(self,instruction):
                if instruction in self.globalInstructions:                        
                        return True
        
        def executeInstruction(self, instruction):
                if not self.instructionSet:
                            return "This IoT device have no instructions defined to execute"
                if instruction in self.instructionSet:
                            #execute instructions
                            if instruction == "discover":
                                    #discover
                                    return self.discoverInstruction()
                            elif instruction == "turnOnLED":
                                    self.turnOnLED()
                                    return "LED on pin #4 is ON"
                            elif instruction == "turnOffLED":
                                    self.turnOffLED()
                                    return "LED on pin #4 is OFF"
                            elif instruction == "getInstructions":
                                    return self.getInstructions()
                else:
                            return "This instruction is not supported. Execute 'getInstructions' for a better approach"

        def discoverInstruction(self):
                discover = "Net Interfaces:\n"
                for key, value in self.NetAndMAC.iteritems():
                    discover += 'Interface {0}\t| MAC: {1}\t| IP: {2}\n'.format(key, value, self.NetAndIP[key])
                #discover += self.NetAndMAC + '|' + self.IP_Address
                discover += self.getInstructions()
                return discover

	def hasInternetConnection(self):
		REMOTE_SERVER = "148.202.23.200"
		try:
			s = socket.create_connection((REMOTE_SERVER,1883),2)
			return True
		except:
			pass
		return False
