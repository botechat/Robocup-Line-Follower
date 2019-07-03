#!/usr/bin/env python3
# coding: utf-8
import ev3dev.ev3 as ev3
from ev3dev.ev3 import *
from enum import Enum
#from multiprocessing import Process
from time import sleep
from time import time


class Robot:
    def __init__(self,out1,out2,out3):

        self.lm1 = ev3.LargeMotor(out1); assert self.lm1.connected
        self.lm2 = ev3.LargeMotor(out2); assert self.lm2.connected
        self.garramotor = ev3.MediumMotor(out3);assert self.garramotor.connected

    def go_forward(self,speed,time):
        self.lm1.run_timed(speed_sp = speed, time_sp = time, stop_action = 'coast')
        self.lm2.run_timed(speed_sp = speed, time_sp = time, stop_action = 'coast')
        self.lm1.wait_while("running")
        self.lm2.wait_while("running")
    def mexe_garra(self, speed, time):
        self.garramotor.run_timed(speed_sp=speed, time_sp=time, stop_action = 'coast')
        self.garramotor.wait_while("running")

    
Corsa = Robot("outB", "outD", "outC")
Sound.speak('Hello, I am Corsa')
Corsa.go_forward(-200, 2000)
Corsa.mexe_garra(100, 2000)
Corsa.mexe_garra(-100, 2000)



