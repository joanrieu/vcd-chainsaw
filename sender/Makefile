FILES=./sender.c
PROGRAM=./sender.out
BINARY=$(PROGRAM).bin
U=flash:w:$(BINARY)

all: $(FILES)
	avr-gcc -Os -mmcu=atmega328p $(FILES) -o $(PROGRAM)
	avr-objcopy -O binary $(PROGRAM) $(BINARY)
	avrdude -p m328p -c arduino -P /dev/ttyACM0 -U $(U)

clean:
	rm -f *.out *.bin
