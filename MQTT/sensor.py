from uuid import getnode as get_mac
class Sensor(object):

    def __init__(self, partNumber):
        self.partNumber = partNumber
        self.metadata = {}

    """
    addToMetadata(readingType = 'temperature', readingUnit = 'C')
    """
    def addToMetadata(self, readingType, readingUnit):
        self.metadata[readingType] =  readingUnit

    def printMetadata(self):
        for key,val in self.metadata.items():
            print key, "=>", val

    def __str__(self):
        cadena = "partNumber;"+self.partNumber
        for key,val in self.metadata.items():
            cadena += ";" + key + ";" + val
        return cadena
