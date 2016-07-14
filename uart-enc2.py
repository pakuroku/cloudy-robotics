#!/usr/bin/python
from socketIO_client import SocketIO
import serial
import time
from encoder import encodercount
from motorcontrol import MotorControl
SpeedMin = 50
SpeedMax = 100
TurnSpeed = 150
speed = 75
state = "Stopped" #states are movingForward, movingBackward, movingLeft, movingRight, Stopped

ser2 = serial.Serial("/dev/ttyUSB0", 115200)
ser = serial.Serial("/dev/ttyUSB1", 115200)
motors = MotorControl()
def listener(*args):
	
	print("{}".format(args[0]))
	
	if args[0] == "left": # turns left
		motors.turnLeft()
		state = "movingLeft"
	elif args[0] == "right": # turns right
		motors.turnRight()
		state = "movingRight"
	elif args[0] == "forward": # moves forward
		motors.forward()
		state = "movingForward"
	elif args[0] == "backward": # moves backwards
		motors.backward()
		state = "movingBackward"
	
	elif args[0] == "rotateleft": #platform rotates left
		motors.rotateLeft()
		encodercount()
		print("Stopping the rotation")
		motors.stopPlatform()

	elif args[0] == "rotateright": # platform rotates right
		motors.rotateRight()
		encodercount()
		print("Stopping the rotation")
		motors.stopPlatform()
	
	elif args[0] == "rise": # tablet board rises up 
		motors.rampUp()
		encodercount()
		print("Stopping the rotation")
		motors.stopPlatform()
		
	elif args[0] == "fall": # tablet board falls down toward the home position 		
		motors.rampDown()
		encodercount()
		print("Stopping the rotation")
		motors.stopPlatform()
		
	elif args[0] == "stop":
		motors.stopWheels()
		motors.stopPlatform()


socketIO = SocketIO('52.34.97.173', 3000) # connects to url at port 3000
socketIO.on('raspberry', listener) # listens for an event called "raspberry" from app.js nodejs server program and then enters the listener function
socketIO.wait(seconds=6000) # waits 6000 seconds until the socketIO connection times out
