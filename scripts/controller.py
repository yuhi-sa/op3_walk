#!/usr/bin/env python
# coding: utf-8
import rospy
import time
import matplotlib.pyplot as plt
import numpy as np

from std_msgs.msg import Float64
from op3_controller.msg import Command 

def callback(data):
    # Publisher Definition (topic name, type, size)
    head_pan    = rospy.Publisher('/robotis_op3/head_pan_position/command', Float64, queue_size=1)
    head_tilt   = rospy.Publisher('/robotis_op3/head_tilt_position/command', Float64, queue_size=1)
    l_el        = rospy.Publisher('robotis_op3/l_el_position/command', Float64, queue_size=1)
    r_el        = rospy.Publisher('robotis_op3/r_el_position/command', Float64, queue_size=1)
    l_sho_pitch = rospy.Publisher('robotis_op3/l_sho_pitch_position/command', Float64, queue_size=1)
    l_sho_roll  = rospy.Publisher('robotis_op3/l_sho_roll_position/command', Float64, queue_size=1)
    r_sho_pitch = rospy.Publisher('robotis_op3/r_sho_pitch_position/command', Float64, queue_size=1)
    r_sho_roll  = rospy.Publisher('robotis_op3/r_sho_roll_position/command', Float64, queue_size=1)
    l_hip_pitch = rospy.Publisher('robotis_op3/l_hip_pitch_position/command', Float64, queue_size=1)
    l_hip_roll  = rospy.Publisher('robotis_op3/l_hip_roll_position/command', Float64, queue_size=1)
    l_hip_yaw   = rospy.Publisher('robotis_op3/l_hip_yaw_position/command', Float64, queue_size=1)
    r_hip_pitch = rospy.Publisher('robotis_op3/r_hip_pitch_position/command', Float64, queue_size=1)
    r_hip_roll  = rospy.Publisher('robotis_op3/r_hip_roll_position/command', Float64, queue_size=1)
    r_hip_yaw   = rospy.Publisher('robotis_op3/r_hip_yaw_position/command', Float64, queue_size=1)
    l_knee      = rospy.Publisher('robotis_op3/l_knee_position/command', Float64, queue_size=1)
    r_knee      = rospy.Publisher('robotis_op3/r_knee_position/command', Float64, queue_size=1)
    l_ank_pitch = rospy.Publisher('robotis_op3/l_ank_pitch_position/command', Float64, queue_size=1)
    l_ank_roll  = rospy.Publisher('robotis_op3/l_ank_roll_position/command', Float64, queue_size=1)  
    r_ank_pitch = rospy.Publisher('robotis_op3/r_ank_pitch_position/command', Float64, queue_size=1)
    r_ank_roll  = rospy.Publisher('robotis_op3/r_ank_roll_position/command', Float64, queue_size=1)     

    # Publisher Data Publish
    l_el.publish(data.l_el)
    r_el.publish(data.r_el)
    l_sho_pitch.publish(data.l_sho_pitch)
    l_sho_roll.publish(data.l_sho_roll)
    r_sho_pitch.publish(data.r_sho_pitch)
    r_sho_roll.publish(data.r_sho_roll)
    l_hip_pitch.publish(data.l_hip_pitch)
    l_hip_roll.publish(data.l_hip_roll)
    l_hip_yaw.publish(data.l_hip_yaw)
    r_hip_pitch.publish(data.r_hip_pitch)
    r_hip_roll.publish(data.r_hip_roll)
    r_hip_yaw.publish(data.r_hip_yaw)
    l_knee.publish(data.l_knee)
    r_knee.publish(data.r_knee)
    head_pan.publish(0.00)
    head_tilt.publish(0.00)
    l_ank_pitch.publish(0.95)
    l_ank_roll.publish(0.00)
    r_ank_pitch.publish(-0.95)
    r_ank_roll.publish(0.00)


def controller():
    # Initialize Node
    rospy.init_node('controller', anonymous=True)
    # Subscriber
    sub = rospy.Subscriber('command_pub', Command, callback)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        rate.sleep()

if __name__ == '__main__':
    try:
        controller()
    except rospy.ROSInitException:
        pass