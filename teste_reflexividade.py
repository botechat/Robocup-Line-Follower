#!/usr/bin/env python3
# coding: utf-8
import ev3dev.ev3 as ev3
from ev3dev.ev3 import *
from enum import Enum
#from multiprocessing import Process
from time import sleep
from time import time

sensor1 = ev3.ColorSensor('in2'); assert sensor1.connected
sensor2 = ev3.ColorSensor('in3'); assert sensor2.connected
sensor3 = ev3.ColorSensor('in4'); assert sensor3.connected
while(True):
    intensidade1 = sensor1.reflected_light_intensity
    intensidade2 = sensor2.reflected_light_intensity
    intensidade3 = sensor3.reflected_light_intensity
    print(intensidade1, " ", intensidade2, " ", intensidade3)



