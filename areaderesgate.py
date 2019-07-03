#!/usr/bin/env python3
# coding: utf-8
import ev3dev.ev3 as ev3
from ev3dev.ev3 import *
from enum import Enum
#from multiprocessing import Process
from time import sleep
from time import time
pesq = 800
pdir = 800
vel_curva = 60
comprimento = 0
largura = 0
uma_area = 2000
uma_unidade = 50
onde_ta = 0
ancestral = 0
comprimento = 0
atual = 0
qtos_retoes = 0
paridade = 1 #diz se o robo tem que virar pra esquerda ou pra direita
parede = 0 #parede = 0 indica que a parede esta do lado direito do robo, enquanto parede = 1 indica pared no lado esquerdo (a primeira parede da sala, a do lado da entrada) 
area_de_resgate = 0
achou = 0
onde_ta = 0
voltou=0
coords_robo = [0,0]
orientacao_robo = 0 
coords_area = [0,0]
terminou = 0
class Robot:
    #def __init__(self,out1,out2,in1,in2,in3, in4):
    def __init__(self,out1,out2,out3,out4,in1,in2,in3, in4):

        self.lm1 = ev3.LargeMotor(out1); assert self.lm1.connected
        self.lm2 = ev3.LargeMotor(out2); assert self.lm2.connected
        self.garram = ev3.MediumMotor(out3);assert self.garram.connected
        self.cacambam = ev3.MediumMotor(out4); assert self.cacambam.connected
        self.se = ev3.ColorSensor(in1); assert self.se.connected
        self.sm = ev3.ColorSensor(in2); assert self.sm.connected
        self.sd = ev3.ColorSensor(in3); assert self.sd.connected
        self.us = ev3.UltrasonicSensor(in4); assert self.us.connected
    def go_forward(self,speed, time):
        global uma_unidade
        global coords_robo
        global orientacao_robo
        self.lm1.run_timed(speed_sp = speed, time_sp = time, stop_action = 'coast')
        self.lm2.run_timed(speed_sp = speed, time_sp = time, stop_action = 'coast')
        if(orientacao_robo==0):
            coords_robo[0] += (time/uma_unidade)*(abs(speed))
        elif orientacao_robo==1:
            coords_robo[1]+=(time/uma_unidade)*(abs(speed))
        elif orientacao_robo==2:
            coords_robo[0]-=(time/uma_unidade)*(abs(speed))
        elif orientacao_robo==3:
            coords_robo[1]-=(time/uma_unidade)*(abs(speed))


    def stop(self,time):
        self.lm1.run_timed(speed_sp = 0, time_sp = time, stop_action = 'coast')
        self.lm2.run_timed(speed_sp = 0, time_sp = time, stop_action = 'coast')

    def acha_parede(self, v_curva, noventa):
        Robot.curva_esquerda(self, v_curva, noventa)
        self.us.mode = 'US-DIST-CM'
        if self.us.value()>50:
            parede = 1
        Robot.curva_direita(self, v_curva, noventa)
    def sobe_garra(self):
        self.garram.run_timed(speed_sp=-300, time_sp=2000, stop_action='coast')
        self.garram.wait_while("running")
    def desce_garra(self)
        self.garram.run_timed(speed_sp=300, time_sp=2000, stop_action='coast')
        self.garram.wait_while("running")
    def sobe_cacamba(self):
        self.cacambam.run_timed(speed_sp=300, time_sp=2000, stop_action='coast')
        self.cacambam.wait_while("running")
        self.cacambam.run_timed(speed_sp=-300, time_sp=2000, stop_action='coast')
        self.cacambam.wait_while("running")
    def encontra_orientacao(self, p_onde_virou):
        global orientacao_robo
        if(p_onde_virou==0):
            if(orientacao_robo!=3):
                orientacao_robo+=1
            else:
                orientacao_robo=0
        else:
            if(orientacao_robo!=0):
                orientacao_robo-=1
            else:
                orientacao_robo=3
    def curva_esquerda(self,v_curva,pos_esq):
        self.lm1.run_to_rel_pos(position_sp = pos_esq, speed_sp = v_curva)
        self.lm2.run_to_rel_pos(position_sp =  -pos_esq, speed_sp = v_curva)
        self.lm1.wait_while("running")
        self.lm2.wait_while("running")
        encontra_orientacao(self, 1)

    def curva_direita(self,v_curva, pos_dir):
        self.lm1.run_to_rel_pos(position_sp = -pos_dir, speed_sp = v_curva)
        self.lm2.run_to_rel_pos(position_sp = pos_dir, speed_sp = v_curva)
        self.lm2.wait_while("running")
        self.lm1.wait_while("running")
        encontra_orientacao(self,0)
    def estaciona(self):
        global area_de_resgate
        global parede
        global voltou
        for x in range 6:
            if(parede==1:)
                if(voltou==1):
                    Robot.curva_esquerda(self, 100, (pesq/12))
                    Robot.go_forward(self, 100, uma_area/12)
                elif(area_de_resgate==1 or area_de_resgate==3):
                    Robot.curva_direita(self, 100, (pdir/12))
                    Robot.go_forward(self, 100, uma_area/12)
                elif(area_de_resgate==2):
                    Robot.curva_esquerda(self, 100, (pesq/12))
                    Robot.go_forward(self, 100, uma_area/12)
            else:
                if(voltou==1):
                    Robot.curva_direita(self, 100, (pdir/12))
                    Robot.go_forward(self, 100, uma_area/12)
                if(area_de_resgate==1 or area_de_resgate==3):
                    Robot.curva_esquerda(self, 100, (pdir/12))
                    Robot.go_forward(self, 100, uma_area/12)
                elif(area_de_resgate==2):
                    Robot.curva_direita(self, 100, (pesq/12))
                    Robot.go_forward(self, 100, uma_area/12)

    def retao(self):
        global comprimento
        global largura
        global uma_unidade
        global area_de_resgate
        global canto
        global paridade
        global achou
        global comprimento
        global coords_robo
        global orientacao_robo
        comprimento = 0
        self.us.mode = 'US-DIST-CM'
        while(self.us.value()>50):
            Robot.go_forward(self, 100, uma_unidade)
            comprimento += 1
            if(orientacao_robo==0):
                coords_robo[0]+=1
            else:
                coords_robo[0]-=1
        Robot.go_forward(self, -100,uma_area)
        if(parede==1):
            Robot.curva_esquerda(self, v_curva, pdir)
            Robot.curva_esquerda(self, v_curva, pdir)
            Robot.desce_garra(self)
            Robot.go_forward(self, -100, uma_area)
            Robot.sobe_garra(self)
            Robot.curva_direita(self, v_curva, pesq)
            Robot.curva_direita(self, v_curva, pesq)
        else:
            Robot.curva_direita(self, v_curva, pdir)
            Robot.curva_direita(self, v_curva, pdir)
            Robot.desce_garra(self)
            Robot.go_forward(self, -100, uma_area)
            Robot.sobe_garra(self)
            Robot.curva_esquerda(self, v_curva, pesq)
            Robot.curva_esquerda(self, v_curva, pesq)
        qtos_retoes+=1
        if(paridade==1):
            paridade=0
        else:
            paridade=1
        if(ancestral!=0 and not(comprimento>(ancestral-5) and comprimento<(ancestral+5)) and achou==0):
            if(qtos_retoes==3):
                area_de_resgate = 1
                achou = 1
            else:
                if(paridade==0):
                    area_de_resgate = 2
                    achou = 1
                    Robot.estaciona(self)
                    Robot.sobe_cacamba(self)
                else if(paridade==1):
                    area_de_resgate = 3
                    achou = 1
                    Robot.estaciona(self)
                    Robot.sobe_cacamba(self)
        comprimento = max(ancestral,comprimento)
        ancestral = comprimento
    def volta(self):
        global comprimento
        global largura
        global uma_unidade
        global paridade
        global parede
        if(orientacao_robo==1):
            Robot.curva_esquerda(self, vel_curva, pesq)
        else:
            Robot.curva_direita(self, vel_curva, pdir)
        Robot.desce_garra(self)
        Robot.go_forward(self, -100, comprimento)
        Robot.sobe_garra(self)
        if(area_de_resgate==2):
            if(parede==1):
                Robot.curva_direita(self, vel_curva, pdir)
                Robot.go_forward(self, 100, uma_area)
                Robot.curva_esquerda(self, vel_curva, pesq)
                Robot.go_forward(self, 100, comprimento-uma_area)
            else:
                Robot.curva_esquerda(self, vel_curva, pdir)
                Robot.go_forward(self, 100, uma_area)
                Robot.curva_direita(self, vel_curva, pesq)
                Robot.go_forward(self, 100, comprimento-uma_area)
        else:
            if(parede==0):
                Robot.curva_direita(self, vel_curva, pdir)
                Robot.go_forward(self, 100, uma_area)
                Robot.curva_esquerda(self, vel_curva, pesq)
                Robot.go_forward(self, 100, comprimento-uma_area)
            else:
                Robot.curva_esquerda(self, vel_curva, pdir)
                Robot.go_forward(self, 100, uma_area)
                Robot.curva_direita(self, vel_curva, pesq)
                Robot.go_forward(self, 100, comprimento-uma_area)
        if(parede==1):
                Robot.curva_esquerda(self, v_curva, pdir)
                Robot.curva_esquerda(self, v_curva, pdir)
                Robot.desce_garra(self)
                Robot.go_forward(self, -100, uma_area)
                Robot.sobe_garra(self)
                Robot.curva_direita(self, v_curva, pesq)
                Robot.curva_direita(self, v_curva, pesq)
            else:
                Robot.curva_direita(self, v_curva, pdir)
                Robot.curva_direita(self, v_curva, pdir)
                Robot.desce_garra(self)
                Robot.go_forward(self, -100, uma_area)
                Robot.sobe_garra(self)
                Robot.curva_esquerda(self, v_curva, pesq)
                Robot.curva_esquerda(self, v_curva, pesq)
        Robot.estaciona(self)
        Robot.sobe_cacamba(self)
    def backtracka_p_1(self):
        global qtos_retoes
        global parede
        global paridade
        global uma_area
        global uma_unidade
        global voltou
        global terminou
        qto_volta = qtos_retoes-2
        if(parede==1):
            if(paridade==1):
                Robot.go_forward(self, -100, largura)
                Robot.curva_esquerda(self, v_curva,pesq)
                Robot.go_forward(self, 100, (comprimento-(uma_area/uma_unidade))*uma_unidade)
            else:
                voltou = 1
                Robot.go_forward(self, -100, (largura-(uma_area/uma_unidade))*uma_unidade)
                Robot.curva_direita(self, v_curva,pdir)
                Robot.curva_direita(self, v_curva,pdir)
        else:
            if(paridade==1):
                Robot.go_forward(self, -100, largura)
                Robot.curva_direita(self, v_curva,pdir)
                Robot.go_forward(self, 100, (comprimento-(uma_area/uma_unidade))*uma_unidade)
            else:
                voltou = 1
                Robot.go_forward(self, -100, (largura-(uma_area/uma_unidade))*uma_unidade)
                Robot.curva_esquerda(self, v_curva,pesq)
                Robot.curva_esquerda(self, v_curva,pesq)
        Robot.estaciona(self)
        Robot.sobe_cacamba(self)
        terminou = 1
    def meia_volta(self):
        global comprimento
        global largura
        global uma_unidade
        global paridade
        global parede
        self.us.mode = 'US-DIST-CM'
        if((paridade==0 and parede==0) or (paridade==1 and parede==1)):
            Robot.curva_esquerda(self, vel_curva, pesq)
        else:
            Robot.curva_direita(self, vel_curva, pdir)
        if(self.us.value<50 and achou==0):
            if(paridade==1):
                area_de_resgate=3
                achou=1
            else:
                area_de_resgate=2
                achou=1
            Robot.volta(self)
        elif(self.us.value<50 and area_de_resgate==1):
            Robot.backtracka_p_1(self)
        Robot.go_forward(self, 100, uma_area)
            if((paridade==0 and parede==0) or (paridade==1 and parede==1)):
                Robot.curva_esquerda(self, vel_curva, pesq)
            else:
                Robot.curva_direita(self, vel_curva, pdir)
        largura += uma_area/uma_unidade
    def acha_coord_area(self):
        global coords_area
        global area_de_resgate
        global comprimento
        global largura
        if(parede==1):
            if(area_de_resgate==1):
                coords_area[1]=comprimento
            else if(coords_area==2):
                coords_area[0] = largura
                coords_area[1] = comprimento
            else:
                coords_area[0] = comprimento
        else:
            if(area_de_resgate==1):
                coords_area[1]=comprimento
                coords_area[0]  = largura
            else if(coords_area==2):
                coords_area[1] = comprimento

    def vaievolta(self):
        global area_de_resgate
        global paridade
        global parede
        global uma_area
        global uma_unidade
        if(area==1):
            qtos_vai = largura-3
        if(area==2):
                

Corsa = Robot('outB','outD', 'outC', 'outA', in2','in3','in4', 'in1')
Sound.speak('Hello, I am Corsa').wait()
Sound.speak('ATTENTION ATTENTION').wait()
while(achou==0):
    Corsa.retao()
    Corsa.meia_volta()
if(area_de_resgate==1):
    while(terminou==0):
        Corsa.retao()
        Corsa.meia_volta()