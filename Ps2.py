import sys

from VcdReader import VcdReader
from SerialDecoder import SerialDecoder

class Ps2KeyDecoder:
    
    @staticmethod
    def make(code):
        code = '%X' % code
        return {'1C': 'A', '32': 'B', '21': 'C', '23': 'D', '24': 'E', '2B': 'F', '34': 'G', '33': 'H', '43': 'I', '3B': 'J', '42': 'K', '4B': 'L', '3A': 'M', '31': 'N', '44': 'O', '4D': 'P', '15': 'Q', '2D': 'R', '1B': 'S', '2C': 'T', '3C': 'U', '2A': 'V', '1D': 'W', '22': 'X', '35': 'Y', '1A': 'Z', '45': '0', '16': '1', '1E': '2', '26': '3', '25': '4', '2E': '5', '36': '6', '3D': '7', '3E': '8', '46': '9', '0E': '`', '4E': '-', '55': '=', '5D': '\\', '66': 'BKSP', '29': 'SPACE', '0D': 'TAB', '58': 'CAPS', '12': 'L SHFT', '14': 'L CTRL', 'E0,1F': 'L GUI', '11': 'L ALT', '59': 'R SHFT', 'E0,14': 'R CTRL', 'E0,27': 'R GUI', 'E0,11': 'R ALT', 'E0,2F': 'APPS', '5A': 'ENTER', '76': 'ESC', '5': 'F1', '6': 'F2', '4': 'F3', '0C': 'F4', '3': 'F5', '0B': 'F6', '83': 'F7', '0A': 'F8', '1': 'F9', '9': 'F10', '78': 'F11', '7': 'F12', 'E0,12,E0,7C': 'PRNT SCRN', '7E': 'SCROLL', 'E1,14,77,E1,F0,14,F0,77"': 'PAUSE', '54': '[', 'E0,70': 'INSERT', 'E0,6C': 'HOME', 'E0,7D': 'PG UP', 'E0,71': 'DELETE', 'E0,69': 'END', 'E0,7A': 'PG DN', 'E0,75': 'U ARROW', 'E0,6B': 'L ARROW', 'E0,72': 'D ARROW', 'E0,74': 'R ARROW', '77': 'NUM', 'E0,4A': 'KP /', '7C': 'KP *', '7B': 'KP -', '79': 'KP +', 'E0,5A': 'KP EN', '71': 'KP .', '70': 'KP 0', '69': 'KP 1', '72': 'KP 2', '7A': 'KP 3', '6B': 'KP 4', '73': 'KP 5', '74': 'KP 6', '6C': 'KP 7', '75': 'KP 8', '7D': 'KP 9', '5B': ']', '4C': ';', '52': '\'', '41': ',', '49': '.', '4A': '/'}[code]

class Ps2SerialDecoder(SerialDecoder):
    
    def __init__(self):
        SerialDecoder.__init__(self, parityBit=True, lsbFirst=True)
    
    def onValue(self, value):
        sys.stdout.write('%s ==> %s' % (value, Ps2KeyDecoder.make(value)))

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
