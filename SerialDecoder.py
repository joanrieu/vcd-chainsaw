class SerialDecoder:
    
    MSB_TO_LSB = 1
    LSB_TO_MSB = 2
    
    PARITY_EVEN = 1
    PARITY_ODD = 2
    
    def __init__(self, dataBits, bitOrder, parityBit, stopBits):
        # Start
        self.state = 0
        self.states = [self.readStart]
        # Data
        for i in range(dataBits):
            if bitOrder is self.MSB_TO_LSB:
                self.states.append(self.readBitMsbToLsb)
            elif bitOrder is self.LSB_TO_MSB:
                self.states.append(self.readBitLsbToMsb)
            else:
                raise ValueError
        # Parity
        if parityBit is self.PARITY_EVEN:
            self.states.append(self.readParityEven)
        elif parityBit is self.PARITY_ODD:
            self.states.append(self.readParityOdd)
        elif parityBit is not None:
            raise ValueError
        # Stop
        for i in range(stopBits):
            if i == 0:
                self.states.append(self.readStop)
            else:
                self.states.append(self.readStop2)
    
    def read(self, bit):
        self.states[self.state](bit)
        self.state = (self.state + 1) % len(self.states)
    
    def readStart(self, bit):
        assert bit == 0
        self.bits = []
    
    def readBitLsbToMsb(self, bit):
        self.bits.insert(0, bit)
    
    def readBitMsbToLsb(self, bit):
        self.bits.append(bit)
    
    def readParityEven(self, bit):
        assert sum(self.bits) % 2 == bit
    
    def readParityOdd(self, bit):
        assert sum(self.bits) % 2 != bit
    
    def readStop(self, bit):
        assert bit == 1
        byte = int(''.join([str(bit) for bit in self.bits]), 2)
        self.onByte(byte)
    
    def readStop2(self, bit):
        assert bit == 1
    
    def onByte(self, byte):
        pass
