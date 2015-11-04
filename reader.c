#include <avr/io.h>

char value=0;

#define FOSC 16000000 // material
#define UBRR 0// 0=> BAUD=2M 1=> BAUD=1M

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

unsigned char USART_Receive( void ) {
    //Wait for data to be received
    while ( !(UCSR0A & (1<<RXC0)) );

    //Get and return received data from buffer
    return UDR0;
}
int charToInt(char* text) {
    return atoi(text);
}
char* intToChar(int ent, char* res) {
    return (char* )itoa(ent, res, 10);
}
void print_string(char* mess) {
    char i = 0;
    while (mess[i] != '\n') {
        USART_Transmit(mess[i]);
        i++;
    }
    USART_Transmit(mess[i]);
}

/*char* listen(char* text) {

  char i = 0;
  char com = 0;
  do {
    com =  USART_Receive();
    USART_Transmit(com);
    text[i] = com;
    i++;
  } while (com != '\r');
  USART_Transmit('\n');
  text[i++] = '\n';

  return text;

}*/

void setup() {
    DDRB &= ~_BV(1);
    DDRB &= ~_BV(2);
}

char digitalRead() {
    return PORTB & 3;
}

int main() {
    USART_Init(UBRR);
    setup();
    char mess[9];

    while (1) {
        value = digitalRead();
        USART_Transmit(value);
        //intToChar(value, mess);
        //print_string(mess);
    }
}
