from tentacle_pi.MPL115A2 import MPL115A2
from tentacle_pi.TSL2561 import TSL2561
from sensor import Sensor
import HTU21DF

class SensorsModule(object):
	
	def __init__(self):
		self.sensorArray = list()
		#Initialize all sensors
		self.tsl = TSL2561(0x39,"/dev/i2c-1")
		self.tsl.enable_autogain()
		self.tsl.set_time(0x00)

		self.mpl = MPL115A2(0x60,"/dev/i2c-1")


		"""Add sensors metadata to Array. This has to be done manually
		because you need to set up the part number of the sensor used.
		Therefore, you have to add each measure information which means
		the kind of reading you are sensing (like light, pressure, noise, etc...)
		and the reading unity (e.g.: for temperature you can measure using
		celsius or farenheit, so you have to specify C or F according to
		the case).
		"""
		tmpSensor = Sensor(partNumber = "TSL2561")
		tmpSensor.addToMetadata(readingType = "light", readingUnit = "lumens")
		self.sensorArray.append(tmpSensor)
		tmpSensor = Sensor(partNumber = "MPL115A2")
		tmpSensor.addToMetadata(readingType = "pressure", readingUnit = "kPa")
		tmpSensor.addToMetadata(readingType = "temperature", readingUnit = "C")
		self.sensorArray.append(tmpSensor)
		print "Sensors module started. " + str(len(self.sensorArray))

	def readTemperature(self):
		return self.mpl.temperature()
	def readPressure(self):
		#MPL returns pressure in single units, we ought to convert
		#to thousands units diving by 1000
		presion = self.mpl.pressure() / 1000
		return presion
	def readLight(self):
		return self.tsl.lux()
	def readNoise(self):
		return -1
	def readHumidity(self):
		return -1
	def getSensorArray(self):
		return self.sensorArray

