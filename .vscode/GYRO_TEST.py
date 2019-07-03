#!/usr/bin/env python3
# coding: utf-8

import ev3dev.ev3 as ev3
#from multiprocessing import Process
from time import sleep
from time import time
gyro = ev3.GyroSensor('in1','GYRO-ANG')
print(gyro.value())
