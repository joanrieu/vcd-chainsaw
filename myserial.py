class SerialDecoder:
    
    def __init__(self, parity_bit=False, two_stop_bits=False):
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
        if parity_bit:
            self.states.append(self.readParity)
        self.states.append(self.readStop)
        if two_stop_bits:
            self.states.append(self.readStop2)
    
    def read(self, bit):
        self.states[self.state](self)
        self.state = (self.state + 1) % len(self.states)
    
    def readStart(self, bit):
        assert bit == 0
        self.value = 0
    
    def readData(self, bit):
        self.value = self.value << 1 | bit & 1
    
    def readParity(self, bit):
        pass #assert bit == ?
    
    def readStop(self, bit):
        assert bit == 1
        self.values.append(self.value)
    
    def readStop2(self, bit):
        assert bit == 1