import sys

from VcdReader import VcdReader
from SerialDecoder import SerialDecoder

class Ps2SerialDecoder(SerialDecoder):
    
    def __init__(self):
        SerialDecoder.__init__(self, parityBit=True, lsbFirst=True)
    
    def onValue(self, value):
        sys.stderr.write('value: %d' % value)

class Ps2VcdReader(VcdReader):
    
    clockName = 'A'
    dataName = 'B'
    
    decoder = Ps2SerialDecoder()
    
    lastClockValue = None
    lastDataValue = None
    
    def onWireValue(self, name, value):
        if name is self.clockName:
            if not value and self.lastClockValue:
                self.onData(self.lastDataValue)
            self.lastClockValue = value
        elif name is self.dataName:
            self.lastDataValue = value
    
    def onData(self, data):
        self.decoder.read(data)

if __name__ == "__main__":
    Ps2VcdReader(open("ps2.vcd"))
