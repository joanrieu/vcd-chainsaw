import sys

from VcdReader import VcdReader
from SerialDecoder import SerialDecoder

class Ps2SerialDecoder(SerialDecoder):
    """
    Converts a PS2 scan code sequence into the corresponding key press and
    key release infos and displays them.
    """
    
    KEY_MAKE = {'1E': 'A', '30': 'B', '2E': 'C', '20': 'D', '12': 'E', '21': 'F', '22': 'G', '23': 'H', '17': 'I', '24': 'J', '25': 'K', '26': 'L', '32': 'M', '31': 'N', '18': 'O', '19': 'P', '10': 'Q', '13': 'R', '1F': 'S', '14': 'T', '16': 'U', '2F': 'V', '11': 'W', '2D': 'X', '15': 'Y', '2C': 'Z', '0B': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6', '8': '7', '9': '8', '0A': '9', '29': '`', '0C': '-', '0D': '=', '2B': '\\', '0E': 'BKSP', '39': 'SPACE', '0F': 'TAB', '3A': 'CAPS', '2A': 'L SHFT', '1D': 'L CTRL', 'E0,5B': 'L GUI', '38': 'L ALT', '36': 'R SHFT', 'E0,1D': 'R CTRL', 'E0,5C': 'R GUI', 'E0,38': 'R ALT', 'E0,5D': 'APPS', '1C': 'ENTER', '1': 'ESC', '3B': 'F1', '3C': 'F2', '3D': 'F3', '3E': 'F4', '3F': 'F5', '40': 'F6', '41': 'F7', '42': 'F8', '43': 'F9', '44': 'F10', '57': 'F11', '58': 'F12', 'E0,2A,E0,37': 'PRNT SCRN', '46': 'SCROLL', 'E1,1D,45,E1,9D,C5': 'PAUSE', '1A': '[', 'E0,52': 'INSERT', 'E0,47': 'HOME', 'E0,49': 'PG UP', 'E0,53': 'DELETE', 'E0,4F': 'END', 'E0,51': 'PG DN', 'E0,48': 'U ARROW', 'E0,4B': 'L ARROW', 'E0,50': 'D ARROW', 'E0,4D': 'R ARROW', '45': 'NUM', 'E0,35': 'KP /', '37': 'KP *', '4A': 'KP -', '4E': 'KP +', 'E0,1C': 'KP EN', '53': 'KP .', '52': 'KP 0', '4F': 'KP 1', '50': 'KP 2', '51': 'KP 3', '4B': 'KP 4', '4C': 'KP 5', '4D': 'KP 6', '47': 'KP 7', '48': 'KP 8', '49': 'KP 9', '1B': ']', '27': ';', '28': '\'', '33': ',', '34': '.', '35': '/'}
    #KEY_MAKE = {'1C': 'A', '32': 'B', '21': 'C', '23': 'D', '24': 'E', '2B': 'F', '34': 'G', '33': 'H', '43': 'I', '3B': 'J', '42': 'K', '4B': 'L', '3A': 'M', '31': 'N', '44': 'O', '4D': 'P', '15': 'Q', '2D': 'R', '1B': 'S', '2C': 'T', '3C': 'U', '2A': 'V', '1D': 'W', '22': 'X', '35': 'Y', '1A': 'Z', '45': '0', '16': '1', '1E': '2', '26': '3', '25': '4', '2E': '5', '36': '6', '3D': '7', '3E': '8', '46': '9', '0E': '`', '4E': '-', '55': '=', '5D': '\\', '66': 'BKSP', '29': 'SPACE', '0D': 'TAB', '58': 'CAPS', '12': 'L SHFT', '14': 'L CTRL', 'E0,1F': 'L GUI', '11': 'L ALT', '59': 'R SHFT', 'E0,14': 'R CTRL', 'E0,27': 'R GUI', 'E0,11': 'R ALT', 'E0,2F': 'APPS', '5A': 'ENTER', '76': 'ESC', '5': 'F1', '6': 'F2', '4': 'F3', '0C': 'F4', '3': 'F5', '0B': 'F6', '83': 'F7', '0A': 'F8', '1': 'F9', '9': 'F10', '78': 'F11', '7': 'F12', 'E0,12,E0,7C': 'PRNT SCRN', '7E': 'SCROLL', 'E1,14,77,E1,F0,14,F0,77"': 'PAUSE', '54': '[', 'E0,70': 'INSERT', 'E0,6C': 'HOME', 'E0,7D': 'PG UP', 'E0,71': 'DELETE', 'E0,69': 'END', 'E0,7A': 'PG DN', 'E0,75': 'U ARROW', 'E0,6B': 'L ARROW', 'E0,72': 'D ARROW', 'E0,74': 'R ARROW', '77': 'NUM', 'E0,4A': 'KP /', '7C': 'KP *', '7B': 'KP -', '79': 'KP +', 'E0,5A': 'KP EN', '71': 'KP .', '70': 'KP 0', '69': 'KP 1', '72': 'KP 2', '7A': 'KP 3', '6B': 'KP 4', '73': 'KP 5', '74': 'KP 6', '6C': 'KP 7', '75': 'KP 8', '7D': 'KP 9', '5B': ']', '4C': ';', '52': '\'', '41': ',', '49': '.', '4A': '/'}
    """Map from key-press scan code to the key name."""
    
    KEY_BREAK = {'9E': 'A', 'B0': 'B', 'AE': 'C', 'A0': 'D', '92': 'E', 'A1': 'F', 'A2': 'G', 'A3': 'H', '97': 'I', 'A4': 'J', 'A5': 'K', 'A6': 'L', 'B2': 'M', 'B1': 'N', '98': 'O', '99': 'P', '90': 'Q', '93': 'R', '9F': 'S', '94': 'T', '96': 'U', 'AF': 'V', '91': 'W', 'AD': 'X', '95': 'Y', 'AC': 'Z', '8B': '0', '82': '1', '83': '2', '84': '3', '85': '4', '86': '5', '87': '6', '88': '7', '89': '8', '8A': '9', '89': '`', '8C': '-', '8D': '=', 'AB': '\\', '8E': 'BKSP', 'B9': 'SPACE', '8F': 'TAB', 'BA': 'CAPS', 'AA': 'L SHFT', '9D': 'L CTRL', 'E0,DB': 'L GUI', 'B8': 'L ALT', 'B6': 'R SHFT', 'E0,9D': 'R CTRL', 'E0,DC': 'R GUI', 'E0,B8': 'R ALT', 'E0,DD': 'APPS', '9C': 'ENTER', '81': 'ESC', 'BB': 'F1', 'BC': 'F2', 'BD': 'F3', 'BE': 'F4', 'BF': 'F5', 'C0': 'F6', 'C1': 'F7', 'C2': 'F8', 'C3': 'F9', 'C4': 'F10', 'D7': 'F11', 'D8': 'F12', 'E0,B7,E0,AA': 'PRNT SCRN', 'C6': 'SCROLL', '9A': '[', 'E0,D2': 'INSERT', 'E0,97': 'HOME', 'E0,C9': 'PG UP', 'E0,D3': 'DELETE', 'E0,CF': 'END', 'E0,D1': 'PG DN', 'E0,C8': 'U ARROW', 'E0,CB': 'L ARROW', 'E0,D0': 'D ARROW', 'E0,CD': 'R ARROW', 'C5': 'NUM', 'E0,B5': 'KP /', 'B7': 'KP *', 'CA': 'KP -', 'CE': 'KP +', 'E0,9C': 'KP EN', 'D3': 'KP .', 'D2': 'KP 0', 'CF': 'KP 1', 'D0': 'KP 2', 'D1': 'KP 3', 'CB': 'KP 4', 'CC': 'KP 5', 'CD': 'KP 6', 'C7': 'KP 7', 'C8': 'KP 8', 'C9': 'KP 9', '9B': ']', 'A7': ';', 'A8': '\'', 'B3': ',', 'B4': '.', 'B5': '/'}
    #KEY_BREAK = {'F0,1C': 'A', 'F0,32': 'B', 'F0,21': 'C', 'F0,23': 'D', 'F0,24': 'E', 'F0,2B': 'F', 'F0,34': 'G', 'F0,33': 'H', 'F0,43': 'I', 'F0,3B': 'J', 'F0,42': 'K', 'F0,4B': 'L', 'F0,3A': 'M', 'F0,31': 'N', 'F0,44': 'O', 'F0,4D': 'P', 'F0,15': 'Q', 'F0,2D': 'R', 'F0,1B': 'S', 'F0,2C': 'T', 'F0,3C': 'U', 'F0,2A': 'V', 'F0,1D': 'W', 'F0,22': 'X', 'F0,35': 'Y', 'F0,1A': 'Z', 'F0,45': '0', 'F0,16': '1', 'F0,1E': '2', 'F0,26': '3', 'F0,25': '4', 'F0,2E': '5', 'F0,36': '6', 'F0,3D': '7', 'F0,3E': '8', 'F0,46': '9', 'F0,0E': '`', 'F0,4E': '-', 'FO,55': '#ERROR!', 'F0,5D': '\\', 'F0,66': 'BKSP', 'F0,29': 'SPACE', 'F0,0D': 'TAB', 'F0,58': 'CAPS', 'FO,12': 'L SHFT', 'FO,14': 'L CTRL', 'E0,F0,1F': 'L GUI', 'F0,11': 'L ALT', 'F0,59': 'R SHFT', 'E0,F0,14': 'R CTRL', 'E0,F0,27': 'R GUI', 'E0,F0,11': 'R ALT', 'E0,F0,2F': 'APPS', 'F0,5A': 'ENTER', 'F0,76': 'ESC', 'F0,05': 'F1', 'F0,06': 'F2', 'F0,04': 'F3', 'F0,0C': 'F4', 'F0,03': 'F5', 'F0,0B': 'F6', 'F0,83': 'F7', 'F0,0A': 'F8', 'F0,01': 'F9', 'F0,09': 'F10', 'F0,78': 'F11', 'F0,07': 'F12', 'E0,F0,7C,E0,F0,12': 'PRNT SCRN', 'F0,7E': 'SCROLL', 'FO,54': '[', 'E0,F0,70': 'INSERT', 'E0,F0,6C': 'HOME', 'E0,F0,7D': 'PG UP', 'E0,F0,71': 'DELETE', 'E0,F0,69': 'END', 'E0,F0,7A': 'PG DN', 'E0,F0,75': 'U ARROW', 'E0,F0,6B': 'L ARROW', 'E0,F0,72': 'D ARROW', 'E0,F0,74': 'R ARROW', 'F0,77': 'NUM', 'E0,F0,4A': 'KP /', 'F0,7C': 'KP *', 'F0,7B': 'KP -', 'F0,79': 'KP +', 'E0,F0,5A': 'KP EN', 'F0,71': 'KP .', 'F0,70': 'KP 0', 'F0,69': 'KP 1', 'F0,72': 'KP 2', 'F0,7A': 'KP 3', 'F0,6B': 'KP 4', 'F0,73': 'KP 5', 'F0,74': 'KP 6', 'F0,6C': 'KP 7', 'F0,75': 'KP 8', 'F0,7D': 'KP 9', 'F0,5B': ']', 'F0,4C': ';', 'F0,52': '\'', 'F0,41': ',', 'F0,49': '.', 'F0,4A': '/'}
    """Map from key-release scan code to the key name."""
    
    bytes = []
    
    def __init__(self):
        SerialDecoder.__init__(self, 8, SerialDecoder.LSB_TO_MSB, SerialDecoder.PARITY_ODD, 1)
    
    def onByte(self, byte):
        """
        Decodes a scan code or stores it if it is unknown.
        Implements SerialDecoder.onByte.
        """
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
    """
    Converts PS2 wire states to bits.
    """
    
    decoder = Ps2SerialDecoder()
    
    lastClockValue = None
    lastDataValue = None
    
    def __init__(self, file, clockName, dataName):
        """
        file: VCD file
        clockName(str): name of the clock wire in the VCD file
        dataName(str): name of the data wire in the VCD file
        """
        VcdReader.__init__(self, file)
        self.clockName = clockName
        self.dataName = dataName
    
    def onWireValue(self, name, value):
        """
        Detects the falling edge of the clock signal and sends the bit on the
        data wire to the Ps2SerialDecoder.
        """
        if name is self.clockName:
            if not value and self.lastClockValue:
                self.decoder.read(self.lastDataValue)
            self.lastClockValue = value
        elif name is self.dataName:
            self.lastDataValue = value

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file = open(sys.argv[1])
    else:
        file = sys.stdin
    Ps2VcdReader(file, 'A', 'B').run()
