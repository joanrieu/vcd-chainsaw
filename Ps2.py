import sys

from VcdReader import VcdReader
from SerialDecoder import SerialDecoder

class Ps2SerialDecoder(SerialDecoder):
    
    KEY_MAKE = {'1C': 'A', '32': 'B', '21': 'C', '23': 'D', '24': 'E', '2B': 'F', '34': 'G', '33': 'H', '43': 'I', '3B': 'J', '42': 'K', '4B': 'L', '3A': 'M', '31': 'N', '44': 'O', '4D': 'P', '15': 'Q', '2D': 'R', '1B': 'S', '2C': 'T', '3C': 'U', '2A': 'V', '1D': 'W', '22': 'X', '35': 'Y', '1A': 'Z', '45': '0', '16': '1', '1E': '2', '26': '3', '25': '4', '2E': '5', '36': '6', '3D': '7', '3E': '8', '46': '9', '0E': '`', '4E': '-', '55': '=', '5D': '\\', '66': 'BKSP', '29': 'SPACE', '0D': 'TAB', '58': 'CAPS', '12': 'L SHFT', '14': 'L CTRL', 'E0,1F': 'L GUI', '11': 'L ALT', '59': 'R SHFT', 'E0,14': 'R CTRL', 'E0,27': 'R GUI', 'E0,11': 'R ALT', 'E0,2F': 'APPS', '5A': 'ENTER', '76': 'ESC', '5': 'F1', '6': 'F2', '4': 'F3', '0C': 'F4', '3': 'F5', '0B': 'F6', '83': 'F7', '0A': 'F8', '1': 'F9', '9': 'F10', '78': 'F11', '7': 'F12', 'E0,12,E0,7C': 'PRNT SCRN', '7E': 'SCROLL', 'E1,14,77,E1,F0,14,F0,77"': 'PAUSE', '54': '[', 'E0,70': 'INSERT', 'E0,6C': 'HOME', 'E0,7D': 'PG UP', 'E0,71': 'DELETE', 'E0,69': 'END', 'E0,7A': 'PG DN', 'E0,75': 'U ARROW', 'E0,6B': 'L ARROW', 'E0,72': 'D ARROW', 'E0,74': 'R ARROW', '77': 'NUM', 'E0,4A': 'KP /', '7C': 'KP *', '7B': 'KP -', '79': 'KP +', 'E0,5A': 'KP EN', '71': 'KP .', '70': 'KP 0', '69': 'KP 1', '72': 'KP 2', '7A': 'KP 3', '6B': 'KP 4', '73': 'KP 5', '74': 'KP 6', '6C': 'KP 7', '75': 'KP 8', '7D': 'KP 9', '5B': ']', '4C': ';', '52': '\'', '41': ',', '49': '.', '4A': '/'}
    KEY_BREAK = {'F0,1C': 'A', 'F0,32': 'B', 'F0,21': 'C', 'F0,23': 'D', 'F0,24': 'E', 'F0,2B': 'F', 'F0,34': 'G', 'F0,33': 'H', 'F0,43': 'I', 'F0,3B': 'J', 'F0,42': 'K', 'F0,4B': 'L', 'F0,3A': 'M', 'F0,31': 'N', 'F0,44': 'O', 'F0,4D': 'P', 'F0,15': 'Q', 'F0,2D': 'R', 'F0,1B': 'S', 'F0,2C': 'T', 'F0,3C': 'U', 'F0,2A': 'V', 'F0,1D': 'W', 'F0,22': 'X', 'F0,35': 'Y', 'F0,1A': 'Z', 'F0,45': '0', 'F0,16': '1', 'F0,1E': '2', 'F0,26': '3', 'F0,25': '4', 'F0,2E': '5', 'F0,36': '6', 'F0,3D': '7', 'F0,3E': '8', 'F0,46': '9', 'F0,0E': '`', 'F0,4E': '-', 'FO,55': '#ERROR!', 'F0,5D': '\\', 'F0,66': 'BKSP', 'F0,29': 'SPACE', 'F0,0D': 'TAB', 'F0,58': 'CAPS', 'FO,12': 'L SHFT', 'FO,14': 'L CTRL', 'E0,F0,1F': 'L GUI', 'F0,11': 'L ALT', 'F0,59': 'R SHFT', 'E0,F0,14': 'R CTRL', 'E0,F0,27': 'R GUI', 'E0,F0,11': 'R ALT', 'E0,F0,2F': 'APPS', 'F0,5A': 'ENTER', 'F0,76': 'ESC', 'F0,05': 'F1', 'F0,06': 'F2', 'F0,04': 'F3', 'F0,0C': 'F4', 'F0,03': 'F5', 'F0,0B': 'F6', 'F0,83': 'F7', 'F0,0A': 'F8', 'F0,01': 'F9', 'F0,09': 'F10', 'F0,78': 'F11', 'F0,07': 'F12', 'E0,F0,7C,E0,F0,12': 'PRNT SCRN', 'F0,7E': 'SCROLL', 'FO,54': '[', 'E0,F0,70': 'INSERT', 'E0,F0,6C': 'HOME', 'E0,F0,7D': 'PG UP', 'E0,F0,71': 'DELETE', 'E0,F0,69': 'END', 'E0,F0,7A': 'PG DN', 'E0,F0,75': 'U ARROW', 'E0,F0,6B': 'L ARROW', 'E0,F0,72': 'D ARROW', 'E0,F0,74': 'R ARROW', 'F0,77': 'NUM', 'E0,F0,4A': 'KP /', 'F0,7C': 'KP *', 'F0,7B': 'KP -', 'F0,79': 'KP +', 'E0,F0,5A': 'KP EN', 'F0,71': 'KP .', 'F0,70': 'KP 0', 'F0,69': 'KP 1', 'F0,72': 'KP 2', 'F0,7A': 'KP 3', 'F0,6B': 'KP 4', 'F0,73': 'KP 5', 'F0,74': 'KP 6', 'F0,6C': 'KP 7', 'F0,75': 'KP 8', 'F0,7D': 'KP 9', 'F0,5B': ']', 'F0,4C': ';', 'F0,52': '\'', 'F0,41': ',', 'F0,49': '.', 'F0,4A': '/'}
    
    bytes = []
    
    def __init__(self):
        SerialDecoder.__init__(self, parityBit=True, evenParity=False, lsbFirst=True)
    
    def onByte(self, byte):
        self.bytes.append(byte)
        code = ','.join(['%X' % byte for byte in self.bytes])
        processed = True
        if code in self.KEY_MAKE:
            key = self.KEY_MAKE[code]
            sys.stdout.write(key + ' pressed\n')
        elif code in self.KEY_BREAK:
            key = self.KEY_BREAK[code]
            sys.stdout.write(key + ' released\n')
        else:
            processed = False
        if processed:
            self.bytes = []

class Ps2VcdReader(VcdReader):
    
    decoder = Ps2SerialDecoder()
    
    lastClockValue = None
    lastDataValue = None
    
    def __init__(self, file, clockName, dataName):
        VcdReader.__init__(self, file)
        self.clockName = clockName
        self.dataName = dataName
    
    def onWireValue(self, name, value):
        if name is self.clockName:
            if not value and self.lastClockValue:
                self.onData(self.lastDataValue)
            self.lastClockValue = value
        elif name is self.dataName:
            self.lastDataValue = value
    
    def onData(self, data):
        self.decoder.read(data)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file = open(sys.argv[1])
    else:
        file = sys.stdin
    Ps2VcdReader(file, 'A', 'B').run()
