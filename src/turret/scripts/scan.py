#!/usr/bin/env python
# license removed for brevity
import rospy
from arbotix_python.arbotix import ArbotiX
from arbotix_python.ax12 import *
from sensor_msgs.msg import Joy

turret = ArbotiX()

def scan():		
	# Set speed
	print turret.setSpeed(1, 50)
	print turret.setSpeed(2, 50)

	

	print turret.getSpeed(1)
	# Put in initial position
	turret.setPosition(1, 510)
	turret.setPosition(2, 510)
	while turret.isMoving(1) or turret.isMoving(2): rospy.sleep(0.5)
	
	raw_input("Please enter something")
	

		
	# Do a scan cycle
	currentPosition = 0
	for value in range(400, 600, 50):
		turret.setPosition(2, value)
		while turret.isMoving(2): rospy.sleep(0.5)
		if currentPosition == 0:
			turret.setPosition(1, 1023)
			currentPosition = 1023
			while turret.isMoving(1): rospy.sleep(0.5)
		else:
			turret.setPosition(1, 0)
			currentPosition = 0
			while turret.isMoving(1): rospy.sleep(0.5)

if __name__ == '__main__':
    rospy.init_node('listener', anonymous=True)
    scan()
