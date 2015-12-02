from pprint import pprint
import re
import sys

class VcdReader:
    
    def __init__(self, file):
        for line in file:
            line = line.strip()
            if len(line) > 0:
                if not self.tryReadLine(line):
                    sys.stderr.write("skipping: `%s'\n" % line);
    
    def tryReadLine(self, line):
        return self.tryReadTime(line) or self.tryReadWire(line)

    def tryReadTime(self, line):
        time = re.match('^#(\d+)$', line)
        if not time:
            return False
        self.onTime(int(time.group(1)))
        return True
    
    def tryReadWire(self, line):
        wire = re.match('^(0|1)(\w+)$', line)
        if not wire:
            return False
        name = wire.group(2)
        value = wire.group(1)
        self.onWireValue(name, int(value))
        return True
    
    def onTime(self, time):
        pass
    
    def onWireValue(self, name, value):
        pass
