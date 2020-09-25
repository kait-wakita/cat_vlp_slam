#!/usr/bin/env python
import rospy, time
from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger, TriggerResponse
from sensor_msgs.msg import Joy
from std_msgs.msg import UInt16


class JoyTwist(object):
    def __init__(self):
        self._joy_sub = rospy.Subscriber('joy', Joy, self.joy_callback, queue_size=1)
        self._twist_pub = rospy.Publisher('cmd_vel', Twist,queue_size=1)
        self._buzzer_pub = rospy.Publisher('buzzer', UInt16, queue_size=1)
        self.joy_twist = Twist()
        
    def joy_callback(self,joy_msg):
        self.joy_twist.linear.x = joy_msg.axes[4] * 0.6
        self.joy_twist.angular.z = joy_msg.axes[3] * 1.0

           
if __name__ == '__main__':
    rospy.init_node('joy_Control')
    jt = JoyTwist()
    vel = Twist()
    
    rospy.wait_for_service('/motor_on')
    rospy.wait_for_service('/motor_off')
    rospy.on_shutdown(rospy.ServiceProxy('/motor_off',Trigger).call)
    rospy.ServiceProxy('/motor_on',Trigger).call()

    rate=rospy.Rate(10)
    while not rospy.is_shutdown():
        alpha = 0.8
        vel.linear.x  = alpha * vel.linear.x  + (1-alpha) * jt.joy_twist.linear.x
        vel.angular.z = alpha * vel.angular.z + (1-alpha) * jt.joy_twist.angular.z
        jt._twist_pub.publish(vel)
        rate.sleep()
