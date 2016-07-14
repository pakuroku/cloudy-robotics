import serial

WheelSpeed = 120
TurnSpeed = 150
RampSpeed = 150	#Ramp is a tentative name, could be rise/fall or incline/decline

TSMin = 100			#TurnSpeed Min constant
TSMax = 200 			#TurnSpeed Max constant

RSMin = 100			#RampSpeed Min constant
RSMax = 200 			#RampSpeed Max constant

ser = serial.Serial("/dev/ttyUSB1", 115200)
#print 'Opened serial port'
ser2 = serial.Serial("/dev/ttyUSB0", 115200)
class MotorControl():
	def forward(self):
		ser.write('H' + chr(2) + chr(WheelSpeed) + chr(2) + chr(WheelSpeed))
		
	def backward(self):
		ser.write('H' + chr(0) + chr(WheelSpeed) + chr(0) + chr(WheelSpeed))
		
	def turnLeft(self):
		ser.write('H' + chr(0) + chr(WheelSpeed) + chr(2) + chr(WheelSpeed))	
	
	def turnRight(self):
		ser.write('H' + chr(2) + chr(WheelSpeed) + chr(0) + chr(WheelSpeed))
		
	def rotateLeft(self):
		ser2.write('H' + chr(0) + chr(0) + chr(0) + chr(TurnSpeed))
		
	def rotateRight(self):
		ser2.write('H' + chr(0) + chr(0) + chr(2) + chr(TurnSpeed))
		
	def rampUp(self):
		ser2.write('H' + chr(0) + chr(RampSpeed) + chr(0) + chr(0))
	
	def rampDown(self):
		ser2.write('H' + chr(2) + chr(RampSpeed) + chr(0) + chr(0))
		
	def stopWheels(self):
		ser.write('H' + chr(2) + chr(0) + chr(2) + chr(0))
		ser.write('Z')
		
	def stopPlatform(self):
		ser2.write('H' + chr(2) + chr(0) + chr(2) + chr(0))
		ser2.write('Z')