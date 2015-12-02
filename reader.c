#include <avr/io.h>
#include <string.h>
#include <avr/interrupt.h>

volatile char value=-1;
volatile char boolean = 0;

#define FOSC 16000000 // material
#define BAUD 115200
#define UBRR (FOSC/(8*BAUD))-1

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

void print_string(char* mess) {
    char i = 0;
    while (mess[i] != '\n') {
        USART_Transmit(mess[i]);
        i++;
    }
    USART_Transmit(mess[i]);
}

void setup() {
    //DDRB |= _BV(PB1);
    //DDRB &= ~_BV(PB2);
    //PORTB = (1<<PB7)|(1<<PB6)|(1<<PB1)|(1<<PB0);
    //DDRB = (1<<DDB3)|(1<<DDB2)|(1<<DDB1)|(1<<DDB0);

    DDRB = 1<<PB5;
    PORTB = 0;

    EICRA = 1;
    EIMSK = 1<<INT0;
    PCICR = 1<<PCIE0;
    PCMSK0 |= (1<<PCINT2)|(1<<PCINT3);

    sei();
}

char digitalRead() {
    return (PINB & 12)>>2;
}

ISR(PCINT0_vect)
{
    PORTB ^= _BV(PB5);
    value = digitalRead();
    boolean = 1;
}

int main() {
    USART_Init(UBRR);
    setup();
    char mess[4];
    while (1) {
        if(boolean){
            itoa(value,mess,10);
            strcat(mess,"\r\n");//pour tester avec cu rajouter un \r
            print_string(mess);
            boolean = 0;
        }
    }
}
