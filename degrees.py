from socketIO_client import SocketIO # imports the socketIO module for python program
import threading					 # needed for the two threads that runs concurrently below
import serial 						 # imports the serial python library for wired usb connection from the raspberry pi to the two trex boards
import time   						 # needed to implement delay sleep functions
import gaugette.rotary_encoder		 # encoder library please refer to rotary_encoder.py at https://github.com/guyc/py-gaugette/tree/master/gaugette
import string						  

A_PIN_1 = 2	 # A_PIN_1,B_PIN_1,A_PIN_2,B_PIN_2 are wiringpi libary pin numbers
B_PIN_1 = 3  # originally 9 but that pin was an I2C pin
A_PIN_2 = 0
B_PIN_2 = 1
#the following are global variables because they need to be accessed by the measureangle thread below!
global count1 												#encoder count variable for horizontal tablet orienter motor encoder
global count2 												#encoder count variable for vertical tablet orienter motor encoder
global prevcount1 											#previous value of encoder1 (horizontal)
global prevcount2        									#previous value of encoder2 (vertical)
global currentcount1 										#current value of encoder1 
global currentcount2										#current value of encoder2
global stopped												#this variable detects when motor stops
global enc1_dir												#direction variable for encoder 1       
global enc2_dir												#direction variable for encoder 2\
global delta1												#change in encoder count1
global delta2												#change in encoder count2
enc1_dir= "CW"												
enc2_dir = "CW"
stopped = True
prevcount1 = 0
prevcount2 = 0
currentcount1 = 0
currentcount2 = 0
delta1 = 0		  
delta2 = 0		   

encoder1 = gaugette.rotary_encoder.RotaryEncoder(A_PIN_1,B_PIN_1)	#initializes encoder1 and binds the wiringpi pins to it
encoder2 = gaugette.rotary_encoder.RotaryEncoder(A_PIN_2,B_PIN_2)	#initializes encoder2 and binds the wiringpi pins to it

ser = serial.Serial("/dev/tty0",timeout=1,baudrate=115200) #intializes serial port to T-rex with orienter encoders

class encoderThread (threading.Thread):    							#this thread increments/decrements encoder counts of the motors      
    def __init__(self,encoder1,encoder2):							#init is a constructor that initializes encoder1 and encoder2 for the thread
        threading.Thread.__init__(self)
        self.encoder1 = encoder1
        self.encoder2 = encoder2
       
    def run(self):												    #run() is an overidden function of the python thread class that measures encoders
        print "Starting " + self.name								
     
        while True:
                
 		delta1 = self.encoder1.get_delta()							#gets the delta values for each incremental changing in the encoders
																	#negative value means opposite direction refer to the gaugette library for more details
		delta2 = self.encoder2.get_delta()
       
                if delta1 !=0 or delta2 !=0:						#when there is a non-zero delta value for any encoder, increment the count
                        
                    if abs(count1) == 1800:							# when the count reaches 2400, the motor has spun rotated one revolution
																	# for more information about finding the amount of counts per one revolution, 
																	# please refer to the developer's manual section 3.5!
						count1 = 0									# resets the count
						
					else:
						count1 = count1 + delta1					# increments the count
						
         	        if abs(count2) == 2400:							# when the count reaches 1800, the motor has spun rotated one revolution
                        count2 = 0
						
                    else:
                        count2 = count2 + delta2					# increments the count
                   
					print '{:15}{count1}'.format('enc1 count', count1 = count1)		# displays the encoder1 count
					print '{:15}{count2}'.format('enc2 count', count2 = count2)	 	# displays the encoder2 count			
                    currentcount1 = count1											# updates the current encoder1 count
                    currentcount2 = count2											# updates the current encoder2 count
                    stopped = False;											    # motor is currently moving (not stopped)
                else:
                    stopped = True;													# if the delta values are zero the motors have stopped

class measureangle(threading.Thread):												#measureangle thread measure the angle based on encoder counts 
																					#and sends the data to the NodeJS server
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        prevcount1=0																#initializes values
        prevcount2=0
        count = 0
        degreetotal1 = 0															#variable for motor1 position in degrees 
        degreetotal2 = 0															#variable for motor2 position in degrees
        while True:
        
            if stopped and count==0:   #if motor has stopped count = 0 condition makes it print degree only once 
                time.sleep(2)          # wait 2 seconds for count to stabilize after motor motion      

                degree1 = (currentcount1-prevcount1)*360/1800	#converts the change in encoder1 count before and after the motor stops to degrees
										                        # 360 is the degree of one revolution divided by 1800 which is the encoder count total for one revolution
                degree2 = (currentcount2-prevcount2)*360/2400	#converts the change in encoder2 count before and after the motor stops to degrees
																# 360 is the degree of one revolution divided by 2400 which is the encoder count total for one revolution
                if degree1 >= 1:								# solves the bug in which the encoders go in the opposite direction by one count just before stopping
                    enc1_dir = "cc"
                else:
                    enc1_dir = "ccw"
                if degree2 >= 1:
                    enc2_dir = "cc"
                else:
                    enc2_dir = "ccw"
                prevcount1 = currentcount1						#assigns the current encoder counts for the next time when the motor stops again for calculation
                prevcount2 = currentcount2
                if abs(degreetotal1) >= 360:					# if degrees go beyond 360 reset the degree
                    degreetotal1 = 0
                else:											# else add the changing in degree of motor position to degreetotal
                    degreetotal1 += degree1
                if abs(degreetotal2) >= 360:
                    degreetotal2 = 0
                else:
                    degreetotal2 += degree2
                degree2_with_dir= str(degreetotal2)+" " + enc1_dir		# concatenate direction to motor position in degrees
                
                socketIO.emit('degree1', degree1_with_dir)				# emit the values to nodeJS server
				socketIO.emit('degree2', degree2_with_dir)	
				print "Change in degree: ",degree1
                print"Current position in degrees",degreetotal1  
                print "Change in degree: ",degree2
                print"Current position in degrees",degreetotal2                                
                count = count+1               							#Increments count. Now for the next iteration, 
																		#the program will NOT go back into this if statement and display the degree values again
            elif stopped and count > 0:  								#if count > 0 do not print degree
                pass
            elif not stopped: 											#motor is moving
                count = 0												#reset the count that when motor stops the degree values are displayed 
                
def main(*argv):							  # main function that starts the two threads
   
	thread1 = encoderThread(encoder1,encoder2)
    thread2 = measureangle()
	thread1.start()
    thread2.start()
	thread1.join()							  
    thread2.join()
if __name__ == "__main__":     				  # if this program is being run by the command " python degree.py" then enter this if statement 
	socketIO = SocketIO('52.34.97.173', 3000) # connects to 52.34.97.173 amazon ec2 server at port 3000
	socketIO.on('raspberry', main)			  # listens for "raspberry" even from nodeJS app.js and then promptly enters the main function
	socketIO.wait(seconds=6000)				  # socketIO conection times out in 6000 seconds



