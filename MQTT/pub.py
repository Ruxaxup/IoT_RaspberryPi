import sys
import paho.mqtt.publish as publish

canal = "raspberryPi/instruction/"
host = "148.202.23.200"
mensaje = sys.argv[1]
if len(sys.argv) > 2:
    mac = sys.argv[2]
else:
    mac =""
print mensaje
publish.single(canal+str(mac), mensaje, hostname=host)
