#!/usr/bin/env python
# coding: utf-8
import rospy
import time
import matplotlib.pyplot as plt
import numpy as np
import rospy
import math
import sys
import csv
import threading
from datetime import datetime
from std_srvs.srv import Empty

from std_msgs.msg import Float64
from std_msgs.msg import String
from op3_controller.msg import Command 
from gazebo_msgs.msg import ModelStates
from gazebo_msgs.msg import ModelState
from transform import quaternion_to_euler_zyx 

from function import Agent
from motion import Motion
from videomake import Videomake

import torch
from torch import nn
from torch import optim
import torch.nn.functional as F

def reset(time_record):
    print('############## Welcome New World ##############')

    # Reset Pose
    pub   = rospy.Publisher('command_pub', Command, queue_size=1)
    array = motion.motion(100)
    pub.publish(array)
    time.sleep(1)

    # Reset world
    reset_world = rospy.ServiceProxy('/gazebo/reset_world',Empty)
    reset_world()

    # First Position
    pub   = rospy.Publisher('command_pub', Command, queue_size=1)
    array = motion.motion(100)
    pub.publish(array)

    time.sleep(2)
    return time_record

def callback(data):
    # Initialize next_state
    if len(agent.next_state)>0:
        agent.next_state = []

    # Get State
    agent.next_state.append(data.pose[1].position.x)
    agent.next_state.append(data.pose[1].position.y)
    agent.next_state.append(data.pose[1].position.z)
    agent.next_state.append(data.pose[1].orientation.x)
    agent.next_state.append(data.pose[1].orientation.y)
    agent.next_state.append(data.pose[1].orientation.z)
    agent.next_state.append(data.pose[1].orientation.w)
    agent.next_state.append(data.twist[1].linear.x)
    agent.next_state.append(data.twist[1].linear.y)
    agent.next_state.append(data.twist[1].linear.z)
    agent.next_state.append(data.twist[1].angular.x)
    agent.next_state.append(data.twist[1].angular.y)
    agent.next_state.append(data.twist[1].angular.z)

def learning(next_state,time_record):
    distance = next_state[0]
    gosa = abs(next_state[1])
    high = next_state[2]

    next_state = torch.unsqueeze(torch.from_numpy(np.array(next_state)).type(torch.FloatTensor), 0)

    if high >=0.145 and distance-agent.distance_old >= 0:
        reward = (distance-agent.distance_old)*1000
    elif high >=0.145 and distance-agent.distance_old < 0:
        reward = (distance-agent.distance_old)*10
    elif high < 0.145:
        reward = -2 + (distance-agent.distance_old)*10
    
    print('試行数:', agent.episode-1, '回数：', agent.trial, '報酬：', reward, '距離：', distance)

    reward = torch.unsqueeze(torch.from_numpy(np.array(reward)).type(torch.FloatTensor), 0)

    if agent.state is not None:
        agent.memorize(next_state, reward)
        agent.update_q_function()

    agent.state = next_state
    agent.distance_old = distance

    # Record Movie
    pub2 = rospy.Publisher('recorder', String, queue_size=1)
    if (agent.episode%200) -2 == 0:
        if not agent.last_index == agent.episode:
            data = str(agent.last_index)
            pub2.publish(data)
            agent.last_index = agent.episode
    
    # Reset
    if time_record > (agent.start_time+20) or agent.episode==1 or high < 0.145:
        print('############## Reset ##############')
        agent.start_time = reset(time_record)
        agent.trial = 0
        agent.episode = agent.episode+1
        agent.history.append(distance)

    # Decide Action
    if agent.state is not None:
        agent.action = agent.get_action(agent.episode)

    # Publish Action
    pub = rospy.Publisher('command_pub', Command, queue_size=1)
    array = motion.motion(agent.action)
    pub.publish(array)

    agent.trial = agent.trial +1


def controller():
    # Node Name Declaration
    rospy.init_node('controller', anonymous=True)

    # Initialize
    pub = rospy.Publisher('command_pub', Command, queue_size=1)
    array = motion.motion(100)
    pub.publish(array)

    # Subscriber
    sub = rospy.Subscriber('gazebo/model_states', ModelStates, callback)
    rate = rospy.Rate(1000)

    while not rospy.is_shutdown():
        time_record = rospy.get_time()
        if len(agent.next_state) > 0:
            learning(agent.next_state,time_record)
        time.sleep(0.025)
        rate.sleep()

########################################################################################

if __name__ == '__main__':
    try:
        global agent
        global motion

        num_states  = 13
        num_actions = 3
        agent       = Agent(num_states, num_actions)
        array       = Command()
        motion      = Motion(array)

        controller()
    except rospy.ROSInitException:
        pass