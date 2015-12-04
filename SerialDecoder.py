class SerialDecoder:
    """
    Decodes the bytes transmitted bit-by-bit in a serial communication and calls
    self.onByte when a new byte is available.
    
    This class should be used as a parent class.
    Call the read function with each bit read on the the wire.
    """
    
    MSB_TO_LSB = 1
    """Bit order: most significant first, least significant last."""
    
    LSB_TO_MSB = 2
    """Bit order: least significant first, most significant last."""
    
    PARITY_EVEN = 1
    """Parity check: even number of 1s."""
    
    PARITY_ODD = 2
    """Parity check: odd number of 1s."""
    
    def __init__(self, dataBits, bitOrder, parityBit, stopBits):
        """
        dataBits(int): number of interesting bits of data transmitted
        bitOrder(enum): order in which the data bits are transmitted
        parityBit(enum): type of parity check or None if no parity check
        stopBits(int): number of stop bits transmitted
        """
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
        """Reads one bit based on the current state."""
        self.states[self.state](bit)
        self.state = (self.state + 1) % len(self.states)
    
    def readStart(self, bit):
        """Checks the start bit."""
        assert bit == 0
        self.bits = []
    
    def readBitLsbToMsb(self, bit):
        """Reads a most significant bit and puts it in self.bits."""
        self.bits.insert(0, bit)
    
    def readBitMsbToLsb(self, bit):
        """Reads a least significant bit and puts it in self.bits."""
        self.bits.append(bit)
    
    def readParityEven(self, bit):
        """Checks that the parity bit is even."""
        assert sum(self.bits) % 2 == bit
    
    def readParityOdd(self, bit):
        """Checks that the parity bit is odd."""
        assert sum(self.bits) % 2 != bit
    
    def readStop(self, bit):
        """
        Checks the first stop bit.
        Calls self.onByte with the decoded byte.
        """
        assert bit == 1
        byte = int(''.join([str(bit) for bit in self.bits]), 2)
        self.onByte(byte)
    
    def readStop2(self, bit):
        """Checks the second stop bit."""
        assert bit == 1
    
    def onByte(self, byte):
        """Called when a byte has been decoded."""
        pass
