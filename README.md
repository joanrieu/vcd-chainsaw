# vcd-chainsaw
VCD dumper, UART & PS2 analyser

## Usage

### Generating a VCD dump file

    # upload to the Arduino board
    (cd sender/ && make)
    # generate a VCD file
    python2 sender/VcdWriter.py my_dump.vcd

### Decoding a PS/2 dump

    # display the keypress data contained in the dump file
    python2 interpreter/Ps2.py my_dump.vcd

## Samples

Some sample files are located in the `samples/` directory.
