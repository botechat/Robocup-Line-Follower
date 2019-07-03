#!/usr/bin/env python3
# coding: utf-8
import ev3dev.ev3 as ev3
from ev3dev.ev3 import *
from enum import Enum
#from multiprocessing import Process
from time import sleep
from time import time
class Robot_US:
    def __init__(self,out1,out2,in1):

        self.lm1 = ev3.LargeMotor(out1); assert self.lm1.connected
        self.lm2 = ev3.LargeMotor(out2); assert self.lm2.connected
        self.us = ev3.UltrasonicSensor(in1); assert self.us.connected

    def stop(self,time):
        self.lm1.run_timed(speed_sp = 0, time_sp = time, stop_action = 'coast')
        self.lm2.run_timed(speed_sp = 0, time_sp = time, stop_action = 'coast')

    def go_forward(self,speed,pos):
        self.lm1.run_to_rel_pos(speed_sp = speed, position_sp = -pos)
        self.lm2.run_to_rel_pos(speed_sp = speed, position_sp = -pos)
        self.lm1.wait_while("running")
        self.lm2.wait_while("running")

    def curva_esquerda(self,v_curva,pos_esq):
        self.lm1.run_to_rel_pos(position_sp = pos_esq, speed_sp = v_curva)
        self.lm2.run_to_rel_pos(position_sp =  -pos_esq, speed_sp = v_curva)
        self.lm1.wait_while("running")
        self.lm2.wait_while("running")

    def curva_direita(self,v_curva, pos_dir):
        self.lm1.run_to_rel_pos(position_sp = -pos_dir, speed_sp = v_curva)
        self.lm2.run_to_rel_pos(position_sp = pos_dir, speed_sp = v_curva)
        self.lm2.wait_while("running")
        self.lm1.wait_while("running")
    def desvia_do_obstaculo(self, speed_reta,speed_curva,posret,pesq, pdir):
        Robot_US.curva_direita(self,speed_curva,0.50*pdir)
        Robot_US.go_forward(self,speed_reta,0.55*posret)
        Robot_US.curva_esquerda(self,speed_curva,0.47*pesq)
        Robot_US.go_forward(self,speed_reta,0.45*posret)
        Robot_US.curva_esquerda(self,speed_curva,0.5*pesq)
        Robot_US.go_forward(self,speed_reta,0.55*posret)
        Robot_US.curva_direita(self,speed_curva,0.5*pdir)
        Robot_US.go_forward(self,speed_reta,-0.15*posret) #vai pra trás

    def encontrar_obstaculo(self):
        global posicao_dir
        global posicao_esq
        self.us.mode = 'US-DIST-CM'
        print(self.us.value())
        if(self.us.value()<=140):
            print("entrou")
            Robot_US.desvia_do_obstaculo(self, 150,60,950, 800, 800)
            print("desviou")

corsinha2  = Robot_US("outB", "outD", "in1")
Sound.speak("Hello, how are you?")
while(1):
    print("loop")
    corsinha2.lm1.run_forever(speed_sp = -100)
    corsinha2.lm2.run_forever(speed_sp = -100)
    corsinha2.encontrar_obstaculo()




