#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from kobuki_msgs.msg import BumperEvent

rospy.init_node('vel_bumper')
vel_x = rospy.get_param('~vel_x', 0.5)
vel_rot = rospy.get_param('~vel_rot', 1.0)
pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10)

def callback(bumper):
    back_vel = Twist()
    back_vel.linear.x = -vel_x
    r = rospy.Rate(10.0)
    for i in range(5):
        pub.publish(back_vel)
        r.sleep()
    
sub = rospy.Subscriber('/mobile_base/events/bumper', BumperEvent, callback, queue_size=1)

while not rospy.is_shutdown():
    vel = Twist()
    direction = raw_input('w: forward, s: backward, a:left, d:right > ')
    if 'w' in direction:
        vel.linear.x = vel_x
    if 's' in direction:
        vel.linear.x = -vel_x
    if 'a' in direction:
        vel.angular.z = vel_rot
    if 'd' in direction:
        vel.angular.z = -vel_rot
    if 'q' in direction:
        break
    print vel
    r = rospy.Rate(10.0)
    for i in range(10):
        pub.publish(vel)
        r.sleep()
