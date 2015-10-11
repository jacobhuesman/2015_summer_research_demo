#!/usr/bin/env python
# license removed for brevity
import rospy
from arbotix_python.arbotix import ArbotiX
from sensor_msgs.msg import Joy, JointState
from arbotix_msgs.srv import Enable, SetSpeed
from std_srvs.srv import Empty
from std_msgs.msg import Float64

# turret = ArbotiX()

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
maxSpeed =  1.0
minSpeed = 0.0

pan_pos = 0.0
tilt_pos = 0.0

def jointCallBack(data):
     global pan_pos
     pan_pos = data.position[0]
     global tilt_pos
     tilt_pos = data.position[1]

def callback(data):
    #rospy.wait_for_service('/head_pan_joint/set_speed')
    #rospy.wait_for_service('/head_tilt_join/set_speed')


    # Relax
    if data.buttons[1] == 1:
        rospy.wait_for_service('head_pan_joint/relax')
        rospy.wait_for_service('head_tilt_joint/relax')
        try:
            enable_pan = rospy.ServiceProxy('head_pan_joint/relax', Empty)
            enable_tilt = rospy.ServiceProxy('head_tilt_joint/relax', Empty)
            resp_pan = enable_pan()
            resp_tilt = enable_tilt()
            print "Joints Relaxed"
        except rospy.ServiceException, e:
            print "Service call failed: %s" %e

    if data.buttons[2] == 1:
        rospy.wait_for_service('head_pan_joint/enable')
        rospy.wait_for_service('head_tilt_joint/enable')
        try:
            enable_pan = rospy.ServiceProxy('head_pan_joint/enable', Enable)
            enable_tilt = rospy.ServiceProxy('head_tilt_joint/enable', Enable)
            resp_pan = enable_pan(True)
            resp_tilt = enable_tilt(True)
            print "Joints Enabled"
        except rospy.ServiceException, e:
            print "Service call failed: %s" %e

    # Reset
    if data.buttons[0] == 1:
        rospy.wait_for_service('head_pan_joint/set_speed')
        rospy.wait_for_service('head_tilt_joint/set_speed')

        try:
            set_pan = rospy.ServiceProxy('head_pan_joint/set_speed', SetSpeed)
            set_tilt = rospy.ServiceProxy('head_tilt_joint/set_speed', SetSpeed)
            resp_pan = set_pan(maxSpeed)
            resp_tilt = set_tilt(maxSpeed)
            print resp_pan
            print resp_tilt
        except rospy.ServiceException, e:
            print "Service call failed: %s" %e

        pan_pub = rospy.Publisher('head_pan_joint/command', Float64, queue_size=10)
        tilt_pub = rospy.Publisher('head_tilt_joint/command', Float64, queue_size=10)
        rate = rospy.Rate(10)
        while ((pan_pos >= 0.1 or pan_pos <= -0.1) or (tilt_pos >= 0.1 or tilt_pos <= -0.1)):
            pan_pub.publish(0.0)
            tilt_pub.publish(0.0)
        print "Zeroed"

'''
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

'''

def listener():

    # Create a node called listener
    rospy.init_node('listener', anonymous=True)

	# Subscribe to topic joy
    rospy.Subscriber("joy", Joy, callback)

    # Subscribe to joint states
    rospy.Subscriber("joint_states", JointState, jointCallBack)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
