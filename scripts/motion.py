#!/usr/bin/env python
# coding: utf-8
import time
from op3_controller.msg import Command 

class Motion:
    def __init__(self,array):
        self.array = array

    def motion(self,num):
        # Initial State
        if num == 100:
            self.array.l_el        = -0.5
            self.array.r_el        =  0.5
            self.array.l_sho_pitch =  0.8
            self.array.l_sho_roll  =  0.7
            self.array.r_sho_pitch = -0.8
            self.array.r_sho_roll  = -0.7
            self.array.l_hip_pitch = -1.6
            self.array.l_hip_roll  = -0.0
            self.array.l_hip_yaw   =  0.0
            self.array.r_hip_pitch =  1.6
            self.array.r_hip_roll  =  0.0
            self.array.r_hip_yaw   =  0.0
            self.array.l_knee      =  2.2
            self.array.r_knee      = -2.2

        elif num == 0:
            self.array.l_hip_pitch = -1.6
            self.array.r_hip_pitch =  1.6
            self.array.l_sho_roll  =  0.7
            self.array.r_sho_roll  = -0.7

        elif num == 1:
            # pass
            self.array.l_hip_pitch = -1.77
            self.array.l_sho_roll  =  1.0
            self.array.r_sho_roll  = -1.1
    
        elif num == 2:
            # pass
            self.array.r_hip_pitch =  1.77
            self.array.l_sho_roll  =  1.0
            self.array.r_sho_roll  = -1.1
     
        return self.array