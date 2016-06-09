#!/usr/bin/python    lets the operating system know which interpreter to parse this program
from socketIO_client import SocketIO # imports the socketIO module for python program
import serial                        # imports the serial python library for wired usb connection from the raspberry pi to the two trex boards
import time                          # needed to implement delay sleep functions

ser = serial.Serial("/dev/ttyUSB0", timeout=1,baudrate=115200) # timeout must be specified otherwise serial will 
															   # freeze the port until it is able to listen to something
ser2 = serial.Serial("/dev/ttyUSB1", timeout=1,baudrate=115200) 

def voltageCheck(socketIO):
	count = 0           # this variable controls how frequently values are sent to the server via socketIO
	resistor_value = 1.0 # resistor value of the current sensing resistor
	while True:              
			voltage = ser2.readline() #reads the voltage value measured by the 2nd T-rex board
            voltage2 = ser.readline()  #reads the voltage value measured by the 1st T-rex board
            try:   # try-except statement to fix buggy float conversion error
			       # if not used, the program will crash after failing the convert to float  
                voltage = float(voltage) #converts both voltage variables to float type
                voltage2 = float(voltage2)            
                resultcurrent = (voltage2 -(voltage))/resistor_value # calculates the current
                resultcurrent = str(abs(resultcurrent))[0:6] # slices the resultcurrent value to only 6 decimal places               
		        count += 1      # increments count
		        if count == 50:  #once count reaches 50 send voltage and current value to app.js nodejs server program via socketIO                      
			        count = 0    #resets count value 
                    socketIO.emit('voltage',voltage2) #sends voltage 
			        socketIO.emit('current', resultcurrent) #sends current

            except ValueError: # if the float conversion fails and a valueerror occurs, print conversion error
                print "conversion error" 
  

socketIO = SocketIO('52.34.97.173', 3000)
if __name__ == "__main__":    # if this program is being run by the command " python voltage.py" then enter this if statement 
        voltageCheck(socketIO) # and execute the voltageCheck function
