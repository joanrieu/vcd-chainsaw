import serial
import sys
import time

# Open serial port
ser = serial.Serial('/dev/ttyACM0', 1000000)

# Initialize wires and wire count
wires = [-1 for i in range(2)]

# Open output file (if given)
if len(sys.argv) > 1:
    file = open(sys.argv[1], "w")
else:
    file = sys.stdout

def wireName(wireId):
    """Computes a VCD wire name (1 char) from a wire number."""
    return chr(ord("A") + wireId)

# Write the chosen time unit
file.write("$timescale 1us $end\n")

# Write the VCD name and description of each wire
for wireId in range(len(wires)):
    file.write("$var wire 1 %c Digital%d $end\n" % (wireName(wireId), wireId))

# Time reference
startTime = time.time()

# This variable contains the int describing all the wires in one
allWires = -1

while True:

    # Read the value of all ports as one integer from the serial port
    allWiresOld = allWires
    allWires = ord(ser.read()[0])
    
    # Skip this value if all wires are identical
    if allWires == allWiresOld:
        continue
    
    # Write the header for the new values
    # TODO Replace this approximate value with a more precise one
    delta = 1e6 * (time.time() - startTime)
    file.write("#%d\n" % (delta))
    
    # Write the value of each wire
    for wireId in range(len(wires)):
        # Extract one wire's state
        wire = (allWires & 1 << wireId) >> wireId
        # Skip unchanged wires
        if wire == wires[wireId]:
            continue
        # Save the new value
        wires[wireId] = wire
        # Write it out
        file.write("%d%s\n" % (wires[wireId], wireName(wireId)))
