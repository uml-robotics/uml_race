#!/usr/bin/env python
import roslib; roslib.load_manifest('uml_race')
import rospy

max_speed = 5.0

goal_x = -25.0
goal_y = -14.0
goal_e =   2.0

start_time = None

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from math import sqrt
import os

def toS(t):
    return float(t.secs)+float(t.nsecs) / 1000000000.0

def quit(reason):
    print reason
    rospy.signal_shutdown(reason)

def distance(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    return sqrt(dx*dx + dy*dy)

def got_cmd_vel(msg):
    global start_time

    if msg.linear.y > 0 or msg.linear.z > 0:
        quit("Error: Move in bad direction")

    if msg.linear.x > max_speed:
        quit("Error: speed limit exceeded")

    if start_time == None and msg.linear.x != 0:
        start_time = rospy.Time.now()
        print "Start moving at %s" % toS(start_time)

def got_odom(msg):
    global start_time

    d = distance(msg.pose.pose.position.x, msg.pose.pose.position.y, 
                 goal_x, goal_y)

    if start_time != None and d < goal_e:
        duration = rospy.Time.now() - start_time
        quit("Finished in %fs" % toS(duration))

rospy.init_node('referee')

rospy.Subscriber('cmd_vel', Twist, got_cmd_vel)
rospy.Subscriber('base_pose_ground_truth', Odometry, got_odom)

rospy.spin()
