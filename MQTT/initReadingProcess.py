import sys
import time
from raspcontroller import *

IoTDevice = RaspController("raspberryPi/instruction/")

try:
        print IoTDevice.getNetAndMACDictionary()
        print IoTDevice.getIPAddress('eth0')
        print IoTDevice.executeInstruction("turnOnLED")
        time.sleep(2)
        print IoTDevice.executeInstruction("turnOffLED")
        print IoTDevice.executeInstruction("discover")
        print IoTDevice.executeInstruction("getInstructions")
        print IoTDevice.isGlobalInstruction("discover")
        print IoTDevice.isGlobalInstruction("turnOnLED")
        print IoTDevice.discoverInstruction()
        print IoTDevice.hasInternetConnection()

except KeyboardInterrupt:
	print "Exit by user."
