#include <avr/io.h>
#include <string.h>
#include <avr/interrupt.h>

/// Serial communication baud rate.
#define BAUD 2000000

/********** BEGIN CODE FROM DOCUMENTATION *************************************/

#define FOSC 16000000 ///< Board clock speed (Hz)

void USART_Init(unsigned int ubrr) {

    UCSR0A &= ~(_BV(FE0) | _BV(DOR0) | _BV(UPE0));
    UCSR0A |= (_BV(UDRE0) | _BV(U2X0));

    //set Baudrate
    UBRR0H = (unsigned char)(ubrr>>8);
    UBRR0L = (unsigned char)ubrr;

    //enable receiver and transmitter
    UCSR0B = (1<<RXEN0)|(1<<TXEN0);

    //Set frame format: 8data, 2stop bit
    UCSR0C = (1<<USBS0)|(3<<UCSZ00);


}

void USART_Transmit( unsigned char data ) {
    //Wait for empty transmit buffer
    while ( !( UCSR0A & (1<<UDRE0)) );

    //Put data into buffer, sends the data (written automatocally in TXB)
    UDR0 = data;
}

/********** END CODE FROM DOCUMENTATION ***************************************/

// True when a value change has been detected and new pin values are available.
volatile char changeDetected = 0;

// Last known value of the pins.
volatile char value;

void setup() {
    // Setup the serial communication.
    USART_Init(FOSC / (8 * BAUD) - 1);
    
    // Do not touch the pins.
    PORTB = 0;
    
    // Enable output only on the LED.
    DDRB = 1 << PB5;
    
    // Setup pin change (PC) interrupt (INT) 0.
    EICRA = 1;
    EIMSK = 1 << INT0;
    PCICR = 1 << PCIE0;
    PCMSK0 |= (1 << PCINT2) | (1 << PCINT3);

    // Enable interrupts.
    sei();
}

/// Handles the pin change (PC) interrupt (INT) 0.
ISR(PCINT0_vect)
{
    // Blink the LED.
    PORTB ^= _BV(PB5);
    
    /// Read pins 3 and 4.
    value = (PINB & 12) >> 2;
    
    // Make the main program send the message.
    changeDetected = 1;
}

// Sends the pin changes to the computer (called in a loop).
void loop() {
    if (changeDetected) {
        changeDetected = 0;
        USART_Transmit(value);
    }
}

// Arduino-style main program.
int main() {
    setup();
    while (1)
        loop();
}
