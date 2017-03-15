import paho.mqtt.publish as publish
from tentacle_pi.TSL2561 import TSL2561
topic = "raspBerry/test"
publish(topic, payload=None, qos=0, retain=False)
