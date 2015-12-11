from pprint import pprint
import re
import sys

verbose = False

class VcdReader:
    """
    Reads a VCD file line by line and calls self.onTime and self.onWireValue
    when either a new time block is read or a wire has a new value.
    
    This class should be used as a parent class.
    Start the reading process by calling the run function.
    """
    
    def __init__(self, file):
        self.file = file
    
    def run(self):
        """Starts reading the file line by line."""
        for line in self.file:
            line = line.strip()
            if len(line) > 0:
                if not self.tryReadLine(line):
                    if verbose:
                        sys.stderr.write("skipping: `%s'\n" % line);
    
    def tryReadLine(self, line):
        """Tries to interpret one VCD line."""
        return self.tryReadTime(line) or self.tryReadWire(line)

    def tryReadTime(self, line):
        """
        Tries to interpret a VCD line as a VCD time header.
        Calls self.onTime if successful.
        """
        time = re.match('^#(\d+)$', line)
        if not time:
            return False
        self.onTime(int(time.group(1)))
        return True
    
    def tryReadWire(self, line):
        """
        Tries to interpret a VCD line as a wire value change.
        Calls self.onWireValue if successful.
        """
        wire = re.match('^(0|1)(\w+)$', line)
        if not wire:
            return False
        name = wire.group(2)
        value = wire.group(1)
        self.onWireValue(name, int(value))
        return True
    
    def onTime(self, time):
        """Called when a new timestamp is read."""
        pass
    
    def onWireValue(self, name, value):
        """Called when a wire value changes."""
        pass
