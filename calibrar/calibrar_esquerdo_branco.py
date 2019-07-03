#!/usr/bin/env python3
# coding: utf-8
import ev3dev.ev3 as ev3
from ev3dev.ev3 import *
#from multiprocessing import Process
from time import sleep
from time import time
cor = ev3.ColorSensor('in2'); assert cor.connected
class Calibracao:
    def __init__(self, color, speed, time):
        self.color = color
        self.speed = speed
        self.time = time
        self.p1 = [1021,-1]
        self.p2 = [1021,-1]
        self.p3 = [1021,-1]
    def calibrate(self,wait_time, repeat):
        for i in range(repeat):
            cor_lida = cor.raw
            self.p1[0] = min(cor.raw[0], self.p1[0])
            self.p1[1] = max(cor.raw[0], self.p1[1])
            self.p2[0] = min(cor.raw[1], self.p2[0])
            self.p2[1] = max(cor.raw[1], self.p2[1])
            self.p3[0] = min(cor.raw[2], self.p3[0])
            self.p3[1] = max(cor.raw[2], self.p3[1])
            sleep(wait_time)
    def escrever(self):
        with open(self.color, "w") as arquivo:
            arquivo.write(str(self.p1[0]))
            arquivo.write(",")
            arquivo.write(str(self.p1[1]))
            arquivo.write(",")
            arquivo.write(str(self.p2[0]))
            arquivo.write(",")
            arquivo.write(str(self.p2[1]))
            arquivo.write(",")
            arquivo.write(str(self.p3[0]))
            arquivo.write(",")
            arquivo.write(str(self.p3[1]))
            arquivo.write(",")
Sound.speak("Calibrate").wait()
Sound.speak("Left White")
branco = Calibracao("textos/branco.txt",0,0)
branco.calibrate(0.1, 100)
branco.escrever()
Sound.speak("Finished")


