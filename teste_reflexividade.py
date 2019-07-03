#!/usr/bin/env python3
# coding: utf-8
import ev3dev.ev3 as ev3
from ev3dev.ev3 import *
from enum import Enum
#from multiprocessing import Process
from time import sleep
from time import time

sensor = ev3.ColorSensor('in3'); assert sensor.connected

while(True):
    intensidade = sensor.reflected_light_intensity
    print(intensidade)



