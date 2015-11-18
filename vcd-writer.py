
import serial
import time

ser = serial.Serial('/dev/ttyACM0', 2000000)
wires = [-1 for i in range(8)]
file = open("data.vcd", "w")

def wireName(wireId):
    return chr(ord("A") + wireId)

file.write("$timescale 1ns $end\n")

for wireId in range(len(wires)):
    file.write("$var wire 1 %c Digital%d $end\n" % (wireName(wireId), wireId))

startTime = time.time()
allWires = -1

while True:

    # Read the value of all ports as one integer from the serial port
    allWiresOld = allWires
    allWires = ser.readline().strip()
    if len(allWires) == 0:
        continue
    try:
        allWires = int(allWires)
        # Skip this value if all wires are identical
        if allWires == allWiresOld:
            continue
    except ValueError:
        continue
    
    # Write the header for the new values
    # TODO Replace delta with value given by the board
    delta = 1000000 * (time.time() - startTime)
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
