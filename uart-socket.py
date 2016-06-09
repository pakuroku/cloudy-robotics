from socketIO_client import SocketIO # imports the socketIO module for python program
import serial # imports the serial python library for wired usb connection from the raspberry pi to the two trex boards
import time   # needed to implement delay sleep functions

state = "Stopped" #states are movingForward, movingBackward, movingLeft, movingRight, Stopped
ser = serial.Serial("/dev/ttyUSB1", 115200) # establishes serial port for trex 1
ser2 = serial.Serial("/dev/ttyUSB0", 115200) # establishes serial port for trex 2

print 'Opened serial ports'
def listener(*args):
	global speed # for the wheel motor speed
    speed = 150 
	global TurnSpeed # for the platform motor speed
	TurnSpeed = 200

	if args[0] == "left": # robot turns left
		ser.write('H' + chr(0) + chr(speed) + chr(2) + chr(speed)) # writes a 5 byte sequence to the 1st Trex that controls the wheel motors
		                                                           # refer to secion 4.4 in the developer's manual for details about this sequence
		state = "movingLeft"
		time.sleep(0.05) # 0.05 seconds of delay
		
	elif args[0] == "right": # robot turns right
		ser.write('H' + chr(2) + chr(speed) + chr(0) + chr(speed))
		state = "movingRight"
		time.sleep(0.05)
		
	elif args[0] == "forward": # robot moves forward
		ser.write('H' + chr(2) + chr(speed) + chr(2) + chr(speed))
		state = "movingForward"
		time.sleep(0.05)
		
	elif args[0] == "backward": # robot moves backwards
		ser.write('H' + chr(0) + chr(speed) + chr(0) + chr(speed))
		state = "movingBackward"
		time.sleep(0.05)
		
	elif args[0] == "speedup": # this command has not been implemented yet into the design
		if speed >= SpeedMax:
			speed = SpeedMax
			print "Max speed reached"
		else:
			speed = speed + 5
			print "speed increased to " + str(speed)

		if state == "movingForward":
			ser.write('H' + chr(2) + chr(speed) + chr(2) + chr(speed))
			time.sleep(0.05)
			ser.write('H' + chr(2) + chr(0) + chr(2) + chr(0))
		elif state == "movingBackward":
			ser.write('H' + chr(0) + chr(speed) + chr(0) + chr(speed))
			time.sleep(0.05)
			ser.write('H' + chr(2) + chr(0) + chr(2) + chr(0))
		elif state == "movingLeft":
			ser.write('H' + chr(0) + chr(speed) + chr(2) + chr(speed))
			time.sleep(0.05)
			ser.write('H' + chr(2) + chr(0) + chr(2) + chr(0))
		elif state == "movingRight":
			ser.write('H' + chr(2) + chr(speed) + chr(0) + chr(speed))
			time.sleep(0.05)
			ser.write('H' + chr(2) + chr(0) + chr(2) + chr(0))

	elif args[0] == "speeddown":  # this command has not been implemented yet into the design
		if speed <= SpeedMin:
			speed = SpeedMin
			print "Min speed reached"
		else:
			speed = speed - 5
			print "speed decreased to " + str(speed)
		if state == "movingForward":
			ser.write('H' + chr(2) + chr(speed) + chr(2) + chr(speed))
		elif state == "movingBackward":
			ser.write('H' + chr(0) + chr(speed) + chr(0) + chr(speed))
		elif state == "movingLeft":
			ser.write('H' + chr(0) + chr(speed) + chr(2) + chr(speed))
		elif state == "movingRight":
			ser.write('H' + chr(2) + chr(speed) + chr(0) + chr(speed))
	
	elif args[0] == "rotateleft": # robot rotates left
		ser2.write('H' + chr(2) + chr(TurnSpeed) + chr(0) + chr(0)) # writes a 5 byte sequence to the 2nd Trex that controls the platform motors
		                                                            # refer to secion 4.4 in the developer's manual for details about this sequence
		time.sleep(0.05)
		
	elif args[0] == "rotateright": # robot rotates right 
		ser2.write('H' + chr(0) + chr(TurnSpeed) + chr(2) + chr(0))
		time.sleep(0.05)

	elif args[0] == "rise": # tablet board rises up 
		ser2.write('H' + chr(2) + chr(0) + chr(2) + chr(TurnSpeed))
		
	elif args[0] == "fall": # tablet board falls down toward the home position 		
		ser2.write('H' + chr(2) + chr(0) + chr(0) + chr(TurnSpeed))
		
	elif args[0] == "stop": # stops all platform and wheel movement for both trex boards
		ser.write('H' + chr(2) + chr(0) + chr(2) + chr(0))
        ser2.write('H' + chr(2) + chr(0) + chr(2) + chr(0))

socketIO = SocketIO('52.34.97.173', 3000) # connects to url at port 3000
socketIO.on('raspberry', listener) # listens for an event called "raspberry" from app.js nodejs server program and then enters the listener function
socketIO.wait(seconds=6000) # waits 6000 seconds until the socketIO connection times out
