#!/usr/bin/env python
# license removed for brevity
import rospy
from arbotix_python.arbotix import ArbotiX
from arbotix_python.ax12 import *
from sensor_msgs.msg import Joy

turret = ArbotiX()

# Notes:
# In data.axes the axes we care about are the ones of the right joystick
# Those are at index 3 for Left/Right Axis stick right and
# index 4 for Up/Down Axis stick right

# Rotate (parameters will change when servo is swapped out for mx-12a)
# middle 510, max right 0, max left 1023
maxLeft = 1023
maxRight = 0

# Tilt: all the way down is pos 210, straight is pos 510, up is pos 810
tiltUpperLimit = 810
tiltLowerLimit = 210
maxSpeed =  100 # Actually up to 400
minSpeed = 0

def callback(data):
	rospy.loginfo(data.buttons)
	
	# Relax
	if data.buttons[1] == 1:
		turret.disableTorque(1)
		turret.disableTorque(2)
	if data.buttons[2] == 1:
		turret.enableTorque(1)
		turret.enableTorque(2)
	
	# Reset
	if data.buttons[0] == 1:
		turret.setSpeed(1, maxSpeed)
		turret.setSpeed(2, maxSpeed)
		turret.setPosition(1, 510)
		turret.setPosition(2, 510)
		while turret.isMoving(1) or turret.isMoving(2):
			pass
		
	# Set speed
	turret.setSpeed(1, int(abs(data.axes[3])*maxSpeed))
	turret.setSpeed(2, int(abs(data.axes[4])*maxSpeed))
	
	# Rotate Turret
	if data.axes[3] > 0.05 :
		turret.setPosition(1, maxRight)
	elif data.axes[3] < -0.05 :
		turret.setPosition(1, maxLeft)
	else:
		turret.setPosition(1, turret.getPosition(1))

	# Tilt Turret
	if data.axes[4] > 0.1 :
		turret.setPosition(2, tiltUpperLimit)
	elif data.axes[4] < -0.1 :
		turret.setPosition(2, tiltLowerLimit)
	else:
		turret.setPosition(2, turret.getPosition(2))


def listener():

	# Create a node called listener
    rospy.init_node('listener', anonymous=True)

	# Subscribe to topic joy
    rospy.Subscriber("joy", Joy, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
