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
    Obstaculo = 5

class Robot:
    #def __init__(self,out1,out2,in1,in2,in3, in4):
    def __init__(self,out1,out2,in1,in2,in3):

        self.lm1 = ev3.LargeMotor(out1); assert self.lm1.connected
        self.lm2 = ev3.LargeMotor(out2); assert self.lm2.connected
        self.se = ev3.ColorSensor(in1); assert self.se.connected
        self.sm = ev3.ColorSensor(in2); assert self.sm.connected
        self.sd = ev3.ColorSensor(in3); assert self.sd.connected


    def go_forward(self,speed):
        Robot.verificaCor(self)
        Robot.verificaEstado(self)
        self.lm1.run_forever(speed_sp = -speed)
        self.lm2.run_forever(speed_sp = -speed)
        Robot.verificaCor(self)
        Robot.verificaEstado(self)

    def stop(self,time):
        self.lm1.run_timed(speed_sp = 0, time_sp = time, stop_action = 'coast')
        self.lm2.run_timed(speed_sp = 0, time_sp = time, stop_action = 'coast')

    def abrirAprendizadoPreto(self):
        global preto
        with open('preto.txt', "r") as ft:            # a lista de aprendizado serah "azul, verde, vermelho"
            preto = ft.read().split(',')              # aqui, criamos uma lista de strings, cada elemento eh a cor
            preto.pop()
            preto = [int(x) for x in preto]     # tornamos as strings em inteiros

    def abrirAprendizadoPreto_direito(self):
        global preto_direito
        with open('preto_direito.txt', "r") as ft:            # a lista de aprendizado serah "azul, verde, vermelho"
            preto_direito = ft.read().split(',')              # aqui, criamos uma lista de strings, cada elemento eh a cor
            preto_direito.pop()
            preto_direito = [int(x) for x in preto_direito]     # tornamos as strings em inteiros

    def abrirAprendizadoPreto_meio(self):
        global preto_meio
        with open('preto_meio.txt', "r") as ft:            # a lista de aprendizado serah "azul, verde, vermelho"
            preto_meio = ft.read().split(',')              # aqui, criamos uma lista de strings, cada elemento eh a cor
            preto_meio.pop()
            preto_meio = [int(x) for x in preto_meio]     # tornamos as strings em inteiros

    def abrirAprendizadoVerde(self):
        global verde
        with open('verde.txt', "r") as ft:            # a lista de aprendizado serah "azul, verde, vermelho"
            verde = ft.read().split(',')              # aqui, criamos uma lista de strings, cada elemento eh a cor
            verde.pop()
            verde = [int(x) for x in verde]     # tornamos as strings em inteiros
    def abrirAprendizadoVerde_direito(self):
        global verde_direito
        with open('verde_direito.txt', "r") as ft:            # a lista de aprendizado serah "azul, verde, vermelho"
            verde_direito = ft.read().split(',')              # aqui, criamos uma lista de strings, cada elemento eh a cor
            verde_direito.pop()
            verde_direito = [int(x) for x in verde_direito]     # tornamos as strings em inteiros

    def verificaCor(self):
        # 1 preto e 0 branco
        global branco
        global branco_meio
        global branco_direito
        global preto
        global preto_meio
        global preto_direito
        global left
        global right
        global middle
        global esquerdo
        global direito
        global meio
        global verde
        global verde_direito
        left = self.se.raw
        right = self.sd.raw
        middle = self.sm.raw
        if preto_meio[0]-10<=middle[0] and preto_meio[1]+10>=middle[0] and preto_meio[2]-10<=middle[1] and preto_meio[3]+10>=middle[1] and preto_meio[4]-10<=middle[2] and preto_meio[5]+10>=middle[2]:
            meio = 1

        else:
            meio = 0


        if preto[0]-10<=left[0] and preto[1]+10>=left[0] and preto[2]-10<=left[1] and preto[3]+10>=left[1] and preto[4]-10<=left[2] and preto[5]+10>=left[2]:
            esquerdo = 1

        elif verde[0] - 5<=left[0] and verde[1] + 5>=left[0] and verde[2] - 5<=left[1] and verde[3] + 5>=left[1] and verde[4] - 5<=left[2] and verde[5] + 5>=left[2]:
            esquerdo = 2

        else:
            esquerdo = 0

        if preto_direito[0]-10<=right[0] and preto_direito[1]+10>=right[0] and preto_direito[2]-10<=right[1] and preto_direito[3]+10>=right[1] and preto_direito[4]-10<=right[2] and preto_direito[5]+10>=right[2]:
            direito = 1

        elif verde_direito[0] - 5<=right[0] and verde_direito[1] + 5>=right[0] and verde_direito[2] - 5<=right[1] and verde_direito[3] + 5>=right[1] and verde_direito[4] - 5<=right[2] and verde_direito[5] + 5>=right[2]:
            direito = 2

        else:
            direito = 0

    def escrever_estados(self):
        with open('estados.txt', "a") as arquivo:
            arquivo.write(str(esquerdo))
            arquivo.write(" ")
            arquivo.write(",")
            arquivo.write(" ")
            arquivo.write(str(meio))
            arquivo.write(" ")
            arquivo.write(",")
            arquivo.write(" ")
            arquivo.write(str(direito))
            arquivo.write(" ")
            arquivo.write(",")
            arquivo.write(" ")
            arquivo.write(str(estado))
            arquivo.write("\n")

    def verificaEstado(self):
        global esquerdo
        global direito
        global meio
        global estado
        global estadoant
        estadoant = estado
        if(estado == States(-3)):
            if(esquerdo == 1 and meio == 1 and direito == 0): #PPB
                estado = States(-3)
            elif(esquerdo == 1 and meio == 1 and direito == 1): #PPP
                estado = States(-3)
            elif(esquerdo == 1 and meio == 0 and direito == 1): #PBP
                estado = States(-3)
                #Transição para Andar Reto na função LineFollower

        elif(estado == States(-2)):
            if(esquerdo == 2 and meio == 1 and direito == 0): #VPB
                estado = States(-2)
            elif(esquerdo == 2 and meio == 0 and direito == 1): #VBP
                estado = States(-2)
            elif(esquerdo == 0 and meio == 1 and direito == 0): #BPB
                estado = States(0)
            elif(esquerdo == 0 and meio == 0 and direito == 0): #BBB
                estado = States(0)
            elif(esquerdo == 1 and meio == 1 and direito == 0): #PPB
                estado = States(-3)
            elif(esquerdo == 1 and meio == 1 and direito == 1): #PPP
                estado = States(-3)
            elif(esquerdo == 1 and meio == 0 and direito == 1): #PBP
                estado = States(-3)

        elif(estado == States(-1)):
            #if(esquerdo == 0 and meio == 0 and direito == 0): #BBB
            #    estado = States(0)
            if(esquerdo != 1 and meio == 1 and direito != 1): #BPB
                estado = States(0)
            elif(esquerdo == 1 and meio == 0 and direito == 0): #PBB
                estado = States(-1)
            elif(esquerdo == 1 and meio == 1 and direito == 0): #PPB
                estado = States(-1)
            #TODO analisar os verdes e os casos de baixo
            elif(esquerdo == 1 and meio == 1 and direito == 0): #PBP
                estado = States(0)
            elif(esquerdo == 1 and meio == 1 and direito == 1): #PPP
                 estado = States(0)
            elif(esquerdo == 0 and meio == 1 and direito == 1): #BPP ??
                 estado = States(0)
            #BBP e BPP não tem transição direta -> viram para a direita

        elif(estado == States(0)):
            if(esquerdo == 0 and meio == 0 and direito == 0): #BBB
                estado = States(0)
            elif(esquerdo == 0 and meio == 1 and direito == 0): #BPB
                estado = States(0)
            elif(esquerdo == 0 and meio == 1 and direito == 1): #BPP
                estado = States(0)
            elif(esquerdo == 1 and meio == 1 and direito == 0): #PPB
                estado = States(0)
            elif(esquerdo == 1 and meio == 1 and direito == 1): #PPP
                estado = States(0)
            elif(esquerdo == 0 and meio == 0 and direito == 1): #BBP
                estado = States(1)
            elif(esquerdo == 1 and meio == 0 and direito == 0): #PBB
                estado = States(-1)
            elif(esquerdo == 2 and meio == 1 and direito == 0): #VPB
                estado = States(-2)
            elif(esquerdo == 0 and meio == 1 and direito == 2): #BPV
                estado = States(2)
                #TODO caso PPV e VPP (quando ele entra torto tlgd)
            elif(esquerdo == 2 and meio == 1 and direito == 2): #VPV
                estado = States(4)
            elif(esquerdo == 2 and meio == 0 and direito == 2): #VBV
                estado = States(4)
            elif(esquerdo == 1 and meio == 0 and direito == 1): #PBP
                estado = States(0)
            elif(esquerdo == 1 and meio == 1 and direito == 1): #PPP
                estado = States(0)
            elif(esquerdo == 1 and meio == 0 and direito == 2): #PBV
                estado = States(2)
            elif(esquerdo == 2 and meio == 0 and direito == 1): #VBP
                estado = States(-2)


        elif(estado == States(1)):
            #if(esquerdo == 0 and meio == 0 and direito == 0): #BBB
            #    estado = States(0)
            if(esquerdo != 1 and meio == 1 and direito != 1): #BPB
                estado = States(0)
            elif(esquerdo == 0 and meio == 0 and direito == 1): #BBP
                estado = States(1)
            elif(esquerdo == 0 and meio == 1 and direito == 1): #BPP
                estado = States(1)
            #TODO analisar os casos com verde e os dois de baixo
            elif(esquerdo == 1 and meio == 1 and direito == 0): #PBP
                estado = States(0)
            elif(esquerdo == 1 and meio == 1 and direito == 1): #PPP
                estado = States(0)
            elif(esquerdo == 1 and meio == 1 and direito == 0): #PPB ??
                estado = States(0)
            #PBB e PPB não tem transição direta -> viram para a esquerda

        elif(estado == States(2)):
            if(esquerdo == 0 and meio == 1 and direito == 2): #BPV
                estado = States(2)
            elif(esquerdo == 1 and meio == 0 and direito == 2): #PBV
                estado = States(2)
            elif(esquerdo == 0 and meio == 1 and direito == 0): #BPB
                estado = States(0)
            elif(esquerdo == 0 and meio == 1 and direito == 1): #BPP
                estado = States(3)
            elif(esquerdo == 1 and meio == 1 and direito == 1): #PPP
                estado = States(3)
            elif(esquerdo == 1 and meio == 0 and direito == 1): #PBP
                estado = States(3)

        elif(estado == States(3)):
            if(esquerdo == 0 and meio == 1 and direito == 1): #BPP
                estado = States(3)
            elif(esquerdo == 1 and meio == 1 and direito == 1): #PPP
                estado = States(3)
            elif(esquerdo == 1 and meio == 0 and direito == 1): #PBP
                estado = States(3)
                #Transição para Andar Reto na função LineFollower

        elif(estado == States(4)):
            if(esquerdo == 2 and meio == 1 and direito == 2): #VPV
                estado = States(4)
            elif(esquerdo == 2 and meio == 0 and direito == 2): #VBV
                estado = States(4)
            else: #TODO aqui tb
                estado = States(0)

        Robot.escrever_estados(self)

    def curva_esquerda(self,v_curva):
        #print("curva esquerda")
        while(not(meio == 1)):
            Robot.verificaCor(self)
            Robot.verificaEstado(self)
            #print(esquerdo, " ", meio, " ", direito, " ", estado)
            self.lm2.run_forever(speed_sp = -v_curva)
            self.lm1.run_forever(speed_sp = v_curva)
            Robot.verificaCor(self)
            Robot.verificaEstado(self)
        Robot.stop(self,0.05)

    def curva_esquerda1(self,v_curva):
        #print("curva esquerda")
        while(not(meio == 0)):
            Robot.verificaCor(self)
            Robot.verificaEstado(self)
            #print(esquerdo, " ", meio, " ", direito, " ", estado)
            self.lm2.run_forever(speed_sp = -v_curva)
            self.lm1.run_forever(speed_sp = v_curva)
            Robot.verificaCor(self)
            Robot.verificaEstado(self)
        Robot.stop(self,0.05)

    def curva_direita(self,v_curva):
        #print("curva direita")
        while(not(meio == 1)):
            Robot.verificaCor(self)
            Robot.verificaEstado(self)
            #print(esquerdo, " ", meio, " ", direito, " ", estado)
            self.lm2.run_forever(speed_sp = v_curva)
            self.lm1.run_forever(speed_sp = -v_curva)
            Robot.verificaCor(self)
            Robot.verificaEstado(self)
        Robot.stop(self,0.05)
    def curva_direita1(self,v_curva):
        #print("curva direita")
        while(not(meio == 0)):
            Robot.verificaCor(self)
            Robot.verificaEstado(self)
            #print(esquerdo, " ", meio, " ", direito, " ", estado)
            self.lm2.run_forever(speed_sp = v_curva)
            self.lm1.run_forever(speed_sp = -v_curva)
            Robot.verificaCor(self)
            Robot.verificaEstado(self)
        Robot.stop(self,0.05)
    def meia_volta(self, sp_curv):
        Robot.stop(self,0.1)
        if(meio == 1):
            Sound.speak("meio1").wait()
            while(not(meio == 0)):
                Robot.curva_direita1(self,sp_curv)
            Sound.speak("branco1").wait()
            while(not(meio == 1)):
                Robot.curva_direita(self,sp_curv)
            Sound.speak("preto1").wait()
            while(not(meio == 0)):
                Robot.curva_direita1(self,sp_curv)
            Sound.speak("branco2").wait()
            while(not(meio == 1)):
                Robot.curva_direita(self,sp_curv)
            Sound.speak("preto3").wait()
            Sound.speak("cabo talquei").wait()
        elif(meio == 0):
            Sound.speak("lendobranco").wait()
            while(not(meio == 1)):
                Robot.curva_direita(self,sp_curv)
            while(not(meio == 0)):
                Robot.curva_direita1(self,sp_curv)
            while(not(meio == 1)):
                Robot.curva_direita(self,sp_curv)
        estado = States(0)
    def follow_line(self,speed_reta,speed_curva):
        while(True):
            global left
            global right
            global esquerdo
            global meio
            global direito
            global estado
            #Robot.encontrar_obstaculo(self)
            Robot.verificaCor(self)
            Robot.verificaEstado(self)
            print(esquerdo, " ", meio, " ", direito, " ", estado)
            if(estado == States(-3) == estadoant): #CurvaVerdeEsquerda
                Robot.stop(self,0.1)
                if(meio == 1):
                    while(not(meio == 0)):
                        Robot.curva_esquerda1(self,speed_curva)
                    while(not(meio == 1)):
                        Robot.curva_esquerda(self,speed_curva)
                elif(meio == 0):
                    while(not(meio == 1)):
                        Robot.curva_esquerda(self,speed_curva)
                estado = States(0)
            elif(estado == States(-2) == estadoant): #VerdeEsquerda
                Robot.verificaCor(self)
                Robot.verificaEstado(self)
                Robot.go_forward(self,speed_reta)
                Robot.verificaCor(self)
                Robot.verificaEstado(self)
            elif(estado == States(-1) == estadoant): #Esquerda
                Robot.stop(self,0.1)
                if(meio == 1):
                    Robot.curva_esquerda1(self,speed_curva)
                elif(meio == 0):
                    Robot.curva_esquerda(self,speed_curva)
                Robot.verificaCor(self)
                Robot.verificaEstado(self)
            elif(estado == States(0) == estadoant): #Reto
                Robot.verificaCor(self)
                Robot.verificaEstado(self)
                Robot.go_forward(self,speed_reta)
                Robot.verificaCor(self)
                Robot.verificaEstado(self)
            elif(estado == States(1) == estadoant): #Direita
                Robot.stop(self,0.1)
                if(meio == 1):
                    Robot.curva_direita1(self,speed_curva)
                elif(meio == 0):
                    Robot.curva_direita(self,speed_curva)
                Robot.verificaCor(self)
                Robot.verificaEstado(self)
            elif(estado == States(2) == estadoant): #VerdeDireita
                Robot.verificaCor(self)
                Robot.verificaEstado(self)
                Robot.go_forward(self,speed_reta)
                Robot.verificaCor(self)
                Robot.verificaEstado(self)
            elif(estado == States(3) == estadoant): #CurvaVerdeDireita
                Robot.stop(self,0.1)
                if(meio == 1):
                    while(not(meio == 0)):
                        Robot.curva_direita1(self,speed_curva)
                    while(not(meio == 1)):
                        Robot.curva_direita(self,speed_curva)
                elif(meio == 0):
                    while(not(meio == 1)):
                        Robot.curva_direita(self,speed_curva)
                estado = States(0)

            elif(estado == States(4) == estadoant): #VerdeMeiaVolta
                Robot.stop(self,0.1)
                if(meio == 1):
                    while(not(meio == 0)):
                        Robot.curva_direita1(self,speed_curva)
                    while(not(meio == 1)):
                        Robot.curva_direita(self,speed_curva)
                    while(not(meio == 0)):
                        Robot.curva_direita1(self,speed_curva)
                    while(not(meio == 1)):
                        Robot.curva_direita(self,speed_curva)
                elif(meio == 0):
                    while(not(meio == 1)):
                        Robot.curva_direita(self,speed_curva)
                    while(not(meio == 0)):
                        Robot.curva_direita1(self,speed_curva)
                    while(not(meio == 1)):
                        Robot.curva_direita(self,speed_curva)
                estado = States(0)


esquerdo = 0
direito = 0
meio = 1
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
Corsa = Robot('outB','outD','in2','in3','in4')
Sound.speak('Hello, I am Corsa').wait()
Sound.speak('ATTENTION ATTENTION').wait()
Corsa.abrirAprendizadoPreto()
Corsa.abrirAprendizadoVerde()
Corsa.abrirAprendizadoPreto_meio()
Corsa.abrirAprendizadoPreto_direito()
Corsa.abrirAprendizadoVerde_direito()
Corsa.meia_volta(70)



