import re

class UartDecoder:
    
    def __init__(self):
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
            self.readData,
            self.readStop,
            self.readStop2
        ]
    
    def read(self, bit):
        self.states[self.state](self)
        self.state = (self.state + 1) % len(self.states)
    
    def readStart(self, bit):
        assert bit == 0
        value = 0
    
    def readData(self, bit):
        value = value << 1 | bit & 1
    
    def readStop(self, bit):
        assert bit == 1
        self.values.append(self.value)
    
    def readStop2(self, bit):
        assert bit == 1
