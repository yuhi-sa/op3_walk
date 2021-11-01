#!/usr/bin/env python
# coding: utf-8

import numpy as np
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
import pyautogui as pag
import os
import time

def Videomake(episode):
    print('録画スタート')
    img_dir_name="./op3_movie"+episode
    os.makedirs(img_dir_name, exist_ok=True)

    img_list = []
    img_No = 0
    movie_time=40
    FPS=64
    photo_no=FPS*movie_time

    for i in range(0, photo_no, 1):
        img_No = img_No + 1
        img    = pag.screenshot()
        img    = np.asarray(img)
        img    = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
        img_output = '{}/{:010d}.png'.format(img_dir_name, img_No)
        cv2.imwrite(img_output, img)
        img_list.append(img_output)

    # Create videos from saved images
    fourcc = cv2.VideoWriter_fourcc('m','p','4', 'v')
    video  = cv2.VideoWriter(img_dir_name+'desktop_capture.mp4', fourcc, FPS, (3840, 1080))# Need to change depending on screen size
    for s in img_list:
        img = cv2.imread(s)
        video.write(img)
    video.release()
    print('Finish')