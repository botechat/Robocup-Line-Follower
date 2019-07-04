#!/usr/bin/env python3
# coding: utf-8
import ev3dev.ev3 as ev3
from ev3dev.ev3 import *
from enum import Enum
#from multiprocessing import Process
from time import sleep
from time import time

class States(Enum):
    CurvaVerdeEsquerda = -3
    VerdeEsquerda = -2
    Esquerda = -1
    Reto = 0
    Direita = 1
    VerdeDireita = 2
    CurvaVerdeDireita = 3
    VerdeMeiaVolta = 4
    MeiaVolta = 5
    Obstaculo = 6
    Reler = 7

class Robot:
    def __init__(self,out1,out2,in1,in2,in3):

        self.lm1 = ev3.LargeMotor(out1); assert self.lm1.connected
        self.lm2 = ev3.LargeMotor(out2); assert self.lm2.connected
        self.se = ev3.ColorSensor(in1); assert self.se.connected
        self.sm = ev3.ColorSensor(in2); assert self.sm.connected
        self.sd = ev3.ColorSensor(in3); assert self.sd.connected
        #self.su = ev3.UltrasonicSensor(in4); assert self.su.connected

    def go_forward(self,speed):
        self.lm1.run_forever(speed_sp = -speed)
        self.lm2.run_forever(speed_sp = -speed)

    def go_back(self,speed):
        self.lm1.run_forever(speed_sp = speed)
        self.lm2.run_forever(speed_sp = speed)

    def turn_left(self,v_curva):
        self.lm2.run_forever(speed_sp = -v_curva)
        self.lm1.run_forever(speed_sp = v_curva)

    def turn_right(self,v_curva):
        self.lm2.run_forever(speed_sp = v_curva)
        self.lm1.run_forever(speed_sp = -v_curva)

    def stop(self,time):
        self.lm1.run_timed(speed_sp = 0, time_sp = time, stop_action = 'coast')
        self.lm2.run_timed(speed_sp = 0, time_sp = time, stop_action = 'coast')
        self.lm1.wait_while("running")
        self.lm2.wait_while("running")

    def verificaIntensidade(self):
        global esquerdo
        global meio
        global direito
        global trigger
        left = self.se.reflected_light_intensity
        middle = self.sm.reflected_light_intensity
        right = self.sd.reflected_light_intensity

        if(left < trigger):
            esquerdo = 1
        else:
            esquerdo = 0

        if(middle < trigger):
            meio = 1
        else:
            meio = 0

        if(right < trigger):
            direito = 1
        else:
            direito = 0

        print(left, middle, right, trigger, esquerdo, direito)

    def seguirLinha(self,speed_reta,speed_curva):
        global esquerdo
        global meio
        global direito
        while(True):
            Robot.verificaIntensidade(self)
            if(esquerdo == 0 and direito == 0):
                Robot.go_forward(self,speed_reta)
            elif(esquerdo == 0 and direito == 1):
                Robot.turn_right(self,speed_curva)
            elif(esquerdo == 1 and direito == 0):
                Robot.turn_left(self,speed_curva)
            elif(esquerdo == 1 and direito == 1):
                Robot.stop(self,100)


esquerdo = 0
direito = 0
meio = 0
e = 0
d = 0
estado = States(0)
left = [0,0,0]
right = [0,0,0]
middle = [0,0,0]
branco = [0,0,0,0,0,0]
branco_direito = [0,0,0,0,0,0]
branco_meio = [0,0,0,0,0,0]
preto = [0,0,0,0,0,0]
preto_direito = [0,0,0,0,0,0]
preto_meio = [0,0,0,0,0,0]
verde = [0,0,0,0,0,0]
verde_direito = [0,0,0,0,0,0]
desviou = 0
trigger = 28

#with open('estados.txt', "w") as arquivo:
#    arquivo.write("BEGIN")

Corsa = Robot('outB','outD','in2','in3','in4')
Sound.speak('Hello, I am Corsa')
Corsa.seguirLinha(150,90)



