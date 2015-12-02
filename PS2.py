class Ps2Decoder: 
     
    def __init__(self, odd_parity_bit=True): 
        self.state = 0 
        self.states = [ 
            self.readStart, 
            self.readData, 
            self.readData, 
            self.readData, 
             self.readData, 
             self.readData, 
             self.readData, 
             self.readData, 
             self.readData
         ] 
		if parity_bit:
            self.states.append(self.readOddParity)
        self.states.append(self.readStop)
      
    def read(self, bit): 
        self.states[self.state](self) 
        self.state = (self.state + 1) % len(self.states) 
      
	%Bit de start
    def readStart(self, bit): 
        assert bit == 0 
        value = 0 
     
	%Resting value to 0
    def readData(self, bit): 
        value = value << 1 | bit & 1 
    
	%Bit de odd parity
    def readOddParity(self, bit): 
        assert bit == 0 #?
        self.values.append(self.value)
     
	%Bit de stop == 1
    def readStop(self, bit): 
        assert bit == 1 