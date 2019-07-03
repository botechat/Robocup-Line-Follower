#!/usr/bin/env python3
# coding: utf-8
import ev3dev.ev3 as ev3
from ev3dev.ev3 import *
from enum import Enum
#from multiprocessing import Process
from time import sleep
from time import time

class Robot:
    #def __init__(self,out1,out2,in1,in2,in3, in4):
    def __init__(self,out1,out2,in1,in2,in3, in4):

        self.lm1 = ev3.LargeMotor(out1); assert self.lm1.connected
        self.lm2 = ev3.LargeMotor(out2); assert self.lm2.connected
        self.se = ev3.ColorSensor(in1); assert self.se.connected
        self.sm = ev3.ColorSensor(in2); assert self.sm.connected
        self.sd = ev3.ColorSensor(in3); assert self.sd.connected
        self.us = ev3.UltrasonicSensor(in4); assert self.us.connected

    def go_forward(self,speed,time):
        self.lm1.run_timed(speed_sp = speed, time_sp = time, stop_action = 'coast')
        self.lm2.run_timed(speed_sp = speed, time_sp = time, stop_action = 'coast')

    def stop(self,time):
        self.lm1.run_timed(speed_sp = 0, time_sp = time, stop_action = 'coast')
        self.lm2.run_timed(speed_sp = 0, time_sp = time, stop_action = 'coast')

    def curva_esquerda(self,v_curva,pos_esq):
        print("curva esquerda")
        Robot.verificaCor(self)
        Robot.verificaEstado(self)
        print(esquerdo, " ", meio, " ", direito, " ", estado)
        self.lm2.run_to_rel_pos(position_sp = pos_esq, speed_sp = v_curva)
        self.lm1.run_to_rel_pos(position_sp = -pos_esq, speed_sp = v_curva)
        Robot.verificaCor(self)
        Robot.verificaEstado(self)

    def curva_direita(self,v_curva, pos_dir):
        print("curva direita")
        Robot.verificaCor(self)
        Robot.verificaEstado(self)
        print(esquerdo, " ", meio, " ", direito, " ", estado)
        self.lm2.run_to_rel_pos(position_sp =  -pos_dir, speed_sp = v_curva)
        self.lm1.run_to_rel_pos(position_sp =  pos_dir, speed_sp = v_curva)
        Robot.verificaCor(self)
        Robot.verificaEstado(self)

    def resgate(self):
    def
