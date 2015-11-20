from pprint import pprint
import re
import sys

class VcdReader:
    
    def __init__(self, file):
        while True:
            line = file.readline()
            if not self.tryReadLine(line):
                sys.stderr.write("unknown command: " + line);
    
    def tryReadLine(self, line):
        if len(line) == 0:
            return False
        line = line.strip()
        return self.tryReadTime(line) or self.tryReadWire(line)

    def tryReadTime(self, line):
        time = re.match('^#(\d+)$', line)
        if not time:
            return False
        self.readTime(int(time.group(1)))
        return True
    
    def readTime(self, time):
        pass
    
    def tryReadWire(self, line):
        wire = re.match('^(0|1)(\w+)$', line)
        if not wire:
            return False
        name = wire.group(2)
        value = wire.group(1)
        print("Wire " + name + " has value " + value);
        return True

if __name__ == "__main__":
    reader = VcdReader(sys.stdin)
