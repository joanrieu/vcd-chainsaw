import serial
import time

ser = serial.Serial('/dev/ttyACM0', 115200)
tab = [-1, -1, -1, -1, -1, -1, -1, -1] 
file = open("data.vcd", "w")
file.write("$timescale 1ps $end\n")
file.write("$var wire 1 A Digital0 $end\n")
file.write("$var wire 1 B Digital1 $end\n")
file.write("$var wire 1 C Digital2 $end\n")
file.write("$var wire 1 D Digital3 $end\n")
file.write("$var wire 1 E Digital4 $end\n")
file.write("$var wire 1 F Digital5 $end\n")
file.write("$var wire 1 G Digital6 $end\n")
file.write("$var wire 1 H Digital7 $end\n")

t = time.time()
value = -1

while True:
    try:
        oldvalue = value
        value = ser.readline().strip()
        if value != '':
            value = int(value)
            if oldvalue != value:
                file.write("#%d\n"% (1000*(time.time() - t)))
                for i in range(8):
                    tmp = (value & 1<<i)>>i
                    if tab[i] != tmp:
                        tab[i] = tmp
                        file.write("%d%s\n" % (tab[i], chr(ord("A") + i)))
    except ValueError:
        pass
    except KeyboardInterrupt:
        file.write("#%d\n"% (1000*(time.time() - t)))
        raise

