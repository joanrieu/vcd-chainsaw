import sys

from VcdReader import VcdReader
from SerialDecoder import SerialDecoder

verbose = False

class UartSerialDecoder(SerialDecoder):
    """
    Displays bytes transmitted on the serial communication.
    """
    
    def onByte(self, byte):
        """
        Displays one raw byte.
        Implements SerialDecoder.onByte.
        """
        sys.stdout.write(chr(byte))

class UartVcdReader(VcdReader):
    """
    Converts UART wire state to bits.
    """
    
    lastTime = None
    lastDataValue = None
    
    def __init__(self, file, dataName, baudRate, dataBits, bitOrder, parityBit, stopBits):
        """
        file: VCD file
        dataName(str): name of the data wire in the VCD file
        baudRate(int): speed of the serial communication
        The other parameters are passed through to SerialDecoder.
        """
        VcdReader.__init__(self, file)
        self.dataName = dataName
        self.period = 1. / baudRate
        self.decoder = UartSerialDecoder(dataBits, bitOrder, parityBit, stopBits)
    
    def onTime(self, time):
        """
        Computes the time of transmission and sends the correct amount of bits
        to UartSerialDecoder.
        """
        if self.lastTime is None:
            self.lastTime = float(time)
        else:
            while self.lastTime < time:
                self.decoder.read(self.lastDataValue)
                self.lastTime += 1e6 * self.period # TODO read the VCD timescale in VcdReader
    
    def onWireValue(self, name, value):
        """
        Updates the last known value of the data wire.
        """
        if name is self.dataName:
            self.lastDataValue = value

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file = open(sys.argv[1])
    else:
        file = sys.stdin
    UartVcdReader(file, 'A', 32000, 8, SerialDecoder.LSB_TO_MSB, SerialDecoder.PARITY_ODD, 1).run()
