![GitHub last commit](https://img.shields.io/github/last-commit/yuhi-sa/op3_walk)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/yuhi-sa/op3_walk)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/yuhi-sa/op3_walk)
![GitHub top language](https://img.shields.io/github/languages/top/yuhi-sa/op3_walk)
![GitHub language count](https://img.shields.io/github/languages/count/yuhi-sa/op3_walk)
# op3_walk
[ROBOTIS OP3](https://emanual.robotis.com/docs/en/platform/op3/simulation/)にGazeboシミュレーション内で強化学習を用いて歩行獲得させるROSパッケージ．  
ROS package for [ROBOTIS OP3](https://emanual.robotis.com/docs/en/platform/op3/simulation/) to acquire walking using reinforcement learning  

<img width="767" alt="Screen Shot 2021-09-19 at 13 48 08" src="https://user-images.githubusercontent.com/62089243/133915805-6b610b84-f68f-4902-aacd-979466303707.png">

# Environment
- [Ubuntu 16.04 LTS](https://wiki.ubuntu.com/XenialXerus/ReleaseNotes/Ja#Ubuntu_16.04.2BMG4wwDCmMPMw7TD8MMk-)
- [ROS kinetic](http://wiki.ros.org/ja/kinetic/Installation/Ubuntu)

# How to Use
## 1. Install ROS Kinetic
- [Ubuntu install of ROS Kinetic](http://wiki.ros.org/kinetic/Installation/Ubuntu)

## 2. Install the package to run OP3 in the Gazebo environment
- [Installing ROBOTIS ROS Packages](https://emanual.robotis.com/docs/en/platform/op3/recovery/#installing-robotis-ros-packages)

## 3. Install this package
```
$ cd ~/catkin_ws/src
$ git clone clone URL
$ cd ..
$ catkin_make
```

## 4. Launch
1. Start Ros
```bash
$ roscore
```
2. Start OBOTIS-OP3 in Gazebo
```bash
$ roslaunch op3_gazebo robotis_world.launch
```
3. Start this package
```bash
# activate (python2 env)
$ rosrun op3_controller controller.py

# activate (python3 env)
$ rosrun op3_controller learning.py
```

# Reference
- [ROBOTIS OP3 e-Manual](https://emanual.robotis.com/docs/en/platform/op3/simulation/)
- [ROBOTIS-GIT/ROBOTIS-OP3](https://github.com/ROBOTIS-GIT/ROBOTIS-OP3)
