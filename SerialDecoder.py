class SerialDecoder:
    
    def __init__(self, parityBit=False, twoStopBits=False, lsbFirst=False):
        self.state = 0
        self.states = [
            self.readStart,
            self.readData,
            self.readData,
            self.readData,
            self.readData,
            self.readData,
            self.readData,
            self.readData,
            self.readData
        ]
        if parityBit:
            self.states.append(self.readParity)
        self.lsbFirst = lsbFirst
        self.states.append(self.readStop)
        if twoStopBits:
            self.states.append(self.readStop2)
    
    def read(self, bit):
        self.states[self.state](bit)
        self.state = (self.state + 1) % len(self.states)
    
    def readStart(self, bit):
        assert bit == 0
        self.bits = []
    
    def readData(self, bit):
        if self.lsbFirst:
            self.bits.insert(0, bit)
        else:
            self.bits.append(bit)
    
    def readParity(self, bit):
        pass #assert bit == ?
    
    def readStop(self, bit):
        assert bit == 1
        byte = int(''.join([str(bit) for bit in self.bits]), 2)
        self.onByte(byte)
    
    def readStop2(self, bit):
        assert bit == 1
    
    def onByte(self, byte):
        pass
