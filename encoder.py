from pid import PID
import gaugette.rotary_encoder
import string
import serial
import time


###################### Pin Mapping Begins ######################
A_PIN_1 = 2
B_PIN_1 = 3  # originally 9 but that pin was an I2C pin
A_PIN_2 = 0
B_PIN_2 = 1
###################### Pin Mapping Ends ######################

encoder1 = gaugette.rotary_encoder.RotaryEncoder(A_PIN_2,B_PIN_2)
encoder2 = gaugette.rotary_encoder.RotaryEncoder(A_PIN_2,B_PIN_2)

###################### Global Variables Begin ######################

global count1 
global count2 
global desiredcount1
global desiredcount2
global prevcount1 
global prevcount2        
global currentcount1 
global currentcount2
global initialcount1
global initialcount2

###################### Global Variables End ######################

def encodercount():
	count1 = 0
	currentcount1 = 0
	desiredcount1 = 33
#	prevcount1 = 0
	initialcount1 = 0
	
	count2 = 0
	currentcount2 = 0
	desiredcount2 = 33
#	prevcount2 = 0
	initialcount2 = 0

	while True:
		delta1 = encoder1.get_delta()
		delta2 = encoder2.get_delta()
		if delta1 != 0:
			count1 = count1 + delta1
			currentcount1 = count1
			if abs(currentcount1-initialcount1) > desiredcount1:
				print ('{:15}{count}'.format('enc count1', count = count1))
				print ('Reached end, exiting count function')
				currentcount1 = 0
				break
		elif delta2 != 0:
			count2 = count2 + delta2
			currentcount2 = count2
			print ('{:15}{count}'.format('enc count2', count = count2))
			if abs(currentcount2-initialcount2) > desiredcount2:
				print ('Reached end, exiting count function')
				currentcount2 = 0
				break
				
def encoder_Turn():
	count1 = 0
	currentcount1 = 0
	desiredcount1 = 33
#	prevcount1 = 0
	initialcount1 = 0
	
	while True:
		delta1 = encoder1.get_delta()
		if delta1 != 0:
			count1 = count1 + delta1
			currentcount1 = count1
			if abs(currentcount1-initialcount1) > desiredcount1:
				print ('{:15}{count}'.format('enc count1', count = count1))
				print ('Reached end, exiting count function')
				currentcount1 = 0
				break
				
def encoder_Ramp():
	count2 = 0
	currentcount2 = 0
	desiredcount2 = 33
#	prevcount2 = 0
	initialcount2 = 0
	
	while True:
		delta2 = encoder2.get_delta()
		if delta2 != 0:
			count2 = count2 + delta2
			currentcount2 = count2
			print ('{:15}{count}'.format('enc count2', count = count2))
			if abs(currentcount2-initialcount2) > desiredcount2:
				print ('Reached end, exiting count function')
				currentcount2 = 0
				break
				
def feedback_Turn(desiredValue):
	pid = PID()
	ser2 = serial.Serial("/dev/ttyUSB0", 115200) #ser2 for consistency
	count1 = 0
	currentcount1 = 0
	desiredcount1 = 33
#	prevcount1 = 0
	initialcount1 = 0
	pid.SetKp(1.1)
	pid.SetDesired(desiredValue)
		while True:
		delta1 = encoder1.get_delta()
		if delta1 != 0:
			count1 = count1 + delta1
			currentcount1 = count1
			error = pid.desired-abs(currentcount1)
			if abs(currentcount1-initialcount1) > desiredcount1:
				print ('{:15}{count}'.format('enc count1', count = count1))
				print ('Reached end, exiting count function')
				currentcount1 = 0
				break
	
def feedback_Ramp(desiredValue):
	pid = PID()
	ser2 = serial.Serial("/dev/ttyUSB0", 115200) #ser2 for consistency
	count2 = 0
	currentcount2 = 0
	desiredcount2 = 33
#	prevcount2 = 0
	initialcount2 = 0	
	pid.SetKp(1.1)
	pid.SetDesired(desiredValue)
	while True:
		delta2 = encoder2.get_delta()
		if delta2 != 0:
			count2 = count2 + delta2
			currentcount2 = count2
			print ('{:15}{count}'.format('enc count2', count = count2))
			if abs(currentcount2-initialcount2) > desiredcount2:
				print ('Reached end, exiting count function')
				currentcount2 = 0
				break
				
