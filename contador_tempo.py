#!/usr/bin/env python3
# coding: utf-8
import ev3dev.ev3 as ev3
from ev3dev.ev3 import *
from enum import Enum
#from multiprocessing import Process
import time
import datetime
tempo2 = datetime.datetime.now()
while(True):
    tempo1 = datetime.datetime.now()
    Sound.speak("A").wait()
    elapsed = tempo1 - tempo2
    print(elapsed.seconds)
