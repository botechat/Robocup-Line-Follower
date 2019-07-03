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

class Robot:
    def __init__(self,out1,out2,in1,in2,in3,in4):

        self.lm1 = ev3.LargeMotor(out1); assert self.lm1.connected
        self.lm2 = ev3.LargeMotor(out2); assert self.lm2.connected
        self.se = ev3.ColorSensor(in1); assert self.se.connected
        self.sm = ev3.ColorSensor(in2); assert self.sm.connected
        self.sd = ev3.ColorSensor(in3); assert self.sd.connected
        self.su = ev3.UltrasonicSensor(in4); assert self.su.connected

    def go_forward(self,speed):
        Robot.verificaCor(self)
        Robot.verificaEstado(self)
        self.lm1.run_forever(speed_sp = -speed)
        self.lm2.run_forever(speed_sp = -speed)
        Robot.verificaCor(self)
        Robot.verificaEstado(self)

    def curva_esquerda(self,v_curva):
        print("curva esquerda")
        while(not(meio == 1)):
            Robot.verificaCor(self)
            Robot.verificaEstado(self)
            self.lm2.run_forever(speed_sp = -v_curva)
            self.lm1.run_forever(speed_sp = v_curva)
            Robot.verificaCor(self)
            Robot.verificaEstado(self)
        Robot.stop(self,100)
        #Robot.corrige_reto(self,100,150) #tempo mínimo

    def curva_esquerda1(self,v_curva):
        print("curva esquerda")
        while(not(meio == 0)):
            Robot.verificaCor(self)
            Robot.verificaEstado(self)
            self.lm2.run_forever(speed_sp = -v_curva)
            self.lm1.run_forever(speed_sp = v_curva)
            Robot.verificaCor(self)
            Robot.verificaEstado(self)
        Robot.stop(self,100)
        #Robot.corrige_reto(self,100,150) #tempo mínimo

    def curva_direita(self,v_curva):
        print("curva direita")
        while(not(meio == 1)):
            Robot.verificaCor(self)
            Robot.verificaEstado(self)
            self.lm2.run_forever(speed_sp = v_curva)
            self.lm1.run_forever(speed_sp = -v_curva)
            Robot.verificaCor(self)
            Robot.verificaEstado(self)
        Robot.stop(self,100)
        #Robot.corrige_reto(self,100,150) #tempo mínimo

    def curva_direita1(self,v_curva):
        print("curva direita")
        while(not(meio == 0)):
            Robot.verificaCor(self)
            Robot.verificaEstado(self)
            self.lm2.run_forever(speed_sp = v_curva)
            self.lm1.run_forever(speed_sp = -v_curva)
            Robot.verificaCor(self)
            Robot.verificaEstado(self)
        Robot.stop(self,100)
        #Robot.corrige_reto(self,100,150) #tempo mínimo

    def go_forward_obstaculo(self,speed,pos):
        self.lm1.run_to_rel_pos(speed_sp = speed, position_sp = -pos)
        self.lm2.run_to_rel_pos(speed_sp = speed, position_sp = -pos)
        self.lm1.wait_while("running")
        self.lm2.wait_while("running")

    def curva_esquerda_obstaculo(self,v_curva,pos_esq):
        self.lm1.run_to_rel_pos(position_sp = pos_esq, speed_sp = v_curva)
        self.lm2.run_to_rel_pos(position_sp =  -pos_esq, speed_sp = v_curva)
        self.lm1.wait_while("running")
        self.lm2.wait_while("running")

    def curva_direita_obstaculo(self,v_curva, pos_dir):
        self.lm1.run_to_rel_pos(position_sp = -pos_dir, speed_sp = v_curva)
        self.lm2.run_to_rel_pos(position_sp = pos_dir, speed_sp = v_curva)
        self.lm2.wait_while("running")
        self.lm1.wait_while("running")

    def meia_volta(self, sp_curv):
        Robot.stop(self,100)
        if(meio == 1):
            while(meio == 1):
                Robot.curva_direita1(self,sp_curv)
            while(meio == 0):
                Robot.curva_direita(self,sp_curv)
            while(meio == 1):
                Robot.curva_direita1(self,sp_curv)
            while(meio == 0):
                Robot.curva_direita(self,sp_curv)
        elif(meio == 0):
            while(meio == 0):
                Robot.curva_direita(self,sp_curv)
            while(meio == 1):
                Robot.curva_direita1(self,sp_curv)
            while(meio == 0):
                Robot.curva_direita(self,sp_curv)
        estado = States(0)

    def corrige_reto(self,speed,time):
        self.lm1.run_timed(speed_sp = -speed, time_sp = time)
        self.lm2.run_timed(speed_sp = -speed,time_sp = time)

    def corrige_tras(self,speed,time):
        self.lm1.run_timed(speed_sp = speed, time_sp = time)
        self.lm2.run_timed(speed_sp = speed,time_sp = time)

    def corrige_direita(self,speed,time):
        self.lm2.run_timed(speed_sp = -v_curva,time_sp = time)
        self.lm1.run_timed(speed_sp = v_curva,time_sp = time)

    def corrige_esquerda(self,speed,time):
        self.lm2.run_timed(speed_sp = v_curva,time_sp = time)
        self.lm1.run_timed(speed_sp = -v_curva,time_sp = time)

    def stop(self,time):
        self.lm1.run_timed(speed_sp = 0, time_sp = time, stop_action = 'coast')
        self.lm2.run_timed(speed_sp = 0, time_sp = time, stop_action = 'coast')

    def abrirAprendizadoBranco(self):
        global branco
        with open('calibrar/textos/branco.txt', "r") as ft:            # a lista de aprendizado serah "azul, verde, vermelho"
            branco = ft.read().split(',')              # aqui, criamos uma lista de strings, cada elemento eh a cor
            branco.pop()
            branco = [int(x) for x in branco]     # tornamos as strings em inteiros

    def abrirAprendizadoBranco_meio(self):
        global branco_meio
        with open('calibrar/textos/branco_meio.txt', "r") as ft:            # a lista de aprendizado serah "azul, verde, vermelho"
            branco_meio = ft.read().split(',')              # aqui, criamos uma lista de strings, cada elemento eh a cor
            branco_meio.pop()
            branco_meio = [int(x) for x in branco_meio]     # tornamos as strings em inteiros

    def abrirAprendizadoBranco_direito(self):
        global branco_direito
        with open('calibrar/textos/branco_direito.txt', "r") as ft:            # a lista de aprendizado serah "azul, verde, vermelho"
            branco_direito = ft.read().split(',')              # aqui, criamos uma lista de strings, cada elemento eh a cor
            branco_direito.pop()
            branco_direito = [int(x) for x in branco_direito]     # tornamos as strings em inteiros

    def abrirAprendizadoPreto(self):
        global preto
        with open('calibrar/textos/preto.txt', "r") as ft:            # a lista de aprendizado serah "azul, verde, vermelho"
            preto = ft.read().split(',')              # aqui, criamos uma lista de strings, cada elemento eh a cor
            preto.pop()
            preto = [int(x) for x in preto]     # tornamos as strings em inteiros

    def abrirAprendizadoPreto_direito(self):
        global preto_direito
        with open('calibrar/textos/preto_direito.txt', "r") as ft:            # a lista de aprendizado serah "azul, verde, vermelho"
            preto_direito = ft.read().split(',')              # aqui, criamos uma lista de strings, cada elemento eh a cor
            preto_direito.pop()
            preto_direito = [int(x) for x in preto_direito]     # tornamos as strings em inteiros

    def abrirAprendizadoPreto_meio(self):
        global preto_meio
        with open('calibrar/textos/preto_meio.txt', "r") as ft:            # a lista de aprendizado serah "azul, verde, vermelho"
            preto_meio = ft.read().split(',')              # aqui, criamos uma lista de strings, cada elemento eh a cor
            preto_meio.pop()
            preto_meio = [int(x) for x in preto_meio]     # tornamos as strings em inteiros

    def abrirAprendizadoVerde(self):
        global verde
        with open('calibrar/textos/verde.txt', "r") as ft:            # a lista de aprendizado serah "azul, verde, vermelho"
            verde = ft.read().split(',')              # aqui, criamos uma lista de strings, cada elemento eh a cor
            verde.pop()
            verde = [int(x) for x in verde]     # tornamos as strings em inteiros

    def abrirAprendizadoVerde_direito(self):
        global verde_direito
        with open('calibrar/textos/verde_direito.txt', "r") as ft:            # a lista de aprendizado serah "azul, verde, vermelho"
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
        global direitoant
        global esquerdoant
        global e
        global m
        global d
        left = self.se.raw
        right = self.sd.raw
        middle = self.sm.raw
        esquerdoant = e
        direitoant = d
        if preto_meio[0]-10<=middle[0] and preto_meio[1]+10>=middle[0] and preto_meio[2]-10<=middle[1] and preto_meio[3]+10>=middle[1] and preto_meio[4]-10<=middle[2] and preto_meio[5]+10>=middle[2]:
            meio = 1

        elif branco_meio[0]-10<=middle[0] and branco_meio[1]+10>=middle[0] and branco_meio[2]-10<=middle[1] and branco_meio[3]+10>=middle[1] and branco_meio[4]-10<=middle[2] and branco_meio[5]+10>=middle[2]:
            meio = 0


        if preto[0]-10<=left[0] and preto[1]+10>=left[0] and preto[2]-10<=left[1] and preto[3]+10>=left[1] and preto[4]-10<=left[2] and preto[5]+10>=left[2]:
            e = 1

        elif verde[0] - 5<=left[0] and verde[1] + 5>=left[0] and verde[2] - 5<=left[1] and verde[3] + 5>=left[1] and verde[4] - 5<=left[2] and verde[5] + 5>=left[2]:
            e = 2

        elif branco[0]-10<=left[0] and branco[1]+10>=left[0] and branco[2]-10<=left[1] and branco[3]+10>=left[1] and branco[4]-10<=left[2] and branco[5]+10>=left[2]:
            e = 0

        if preto_direito[0]-10<=right[0] and preto_direito[1]+10>=right[0] and preto_direito[2]-10<=right[1] and preto_direito[3]+10>=right[1] and preto_direito[4]-10<=right[2] and preto_direito[5]+10>=right[2]:
            d = 1

        elif verde_direito[0] - 5<=right[0] and verde_direito[1] + 5>=right[0] and verde_direito[2] - 5<=right[1] and verde_direito[3] + 5>=right[1] and verde_direito[4] - 5<=right[2] and verde_direito[5] + 5>=right[2]:
            d = 2

        elif branco_direito[0]-10<=right[0] and branco_direito[1]+10>=right[0] and branco_direito[2]-10<=right[1] and branco_direito[3]+10>=right[1] and branco_direito[4]-10<=right[2] and branco_direito[5]+10>=right[2]:
            d = 0



        if d == direitoant:  #fazer duas verificações para ter mais precisão
            direito = d
        if e == esquerdoant:
            esquerdo = e

    '''def escrever_estados(self):
        with open('estados.txt', "a") as arquivo:l
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
            arquivo.write("\n")'''

    def verificaEstado(self):
        global esquerdo
        global direito
        global meio
        global estado
        global estadoant
        global desviou
        estadoant = estado

        #Robot.verificaDistancia(self,135)

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
            elif(direito == 2):
                estado = States(4)

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
            elif(esquerdo == 1 and meio == 0 and direito == 1): #PBP
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
            elif(esquerdo == 1 and meio == 0 and direito == 1): #PBP
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
            elif(esquerdo == 2):
                estado = States(4)

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
            elif(esquerdo == 0 or direito == 0): #B-B
                estado = States(0)
            elif(esquerdo == 1 or direito == 1): #P - P ou B - P ou P - B
                estado = States(5)



        '''elif(estado == States(6)):
            if(desviou == 1):
                desviou = 0
                estado = States(0)'''

        print(esquerdo, " ", meio, " ", direito, " ", estado)
        #Robot.escrever_estados(self)

    def verificaDistancia(self,distancia_limite):
        global estado
        self.su.mode = 'US-DIST-CM'
        if(self.su.value() <= distancia_limite):
            estado = States(6)
            Robot.desviaObstaculo(self,150,60,950,800,800)

    def desviaObstaculo(self,speed_reta_obstaculo,speed_curva_obstaculo,posret,posesq,posdir):
        global desviou
        global estado
        if(estado == States(6)):
            Robot.curva_direita_obstaculo(self,speed_curva_obstaculo,0.50*posdir)
            Robot.go_forward_obstaculo(self,speed_reta_obstaculo,0.55*posret)
            Robot.curva_esquerda_obstaculo(self,speed_curva_obstaculo,0.47*posesq)
            Robot.go_forward_obstaculo(self,speed_reta_obstaculo,0.45*posret)
            Robot.curva_esquerda_obstaculo(self,speed_curva_obstaculo,0.5*posesq)
            Robot.go_forward_obstaculo(self,speed_reta_obstaculo,0.75*posret)
            Robot.curva_direita_obstaculo(self,speed_curva_obstaculo,0.5*posdir)
            Robot.go_forward_obstaculo(self,speed_reta_obstaculo,-0.15*posret) #vai pra trás
            desviou = 1
            Robot.verificaCor(self)
            Robot.verificaEstado(self)
            if(meio == 0): #voltar a seguir linha
                if(esquerdo == 1):
                    estado = States(-1)
                elif(direito == 1):
                    estado = States(1)
                else:
                    estado = States(0)
            elif(meio == 1):
                estado = States(0)

    def seguirLinha(self,speed_reta,speed_curva):
        while(True):
            global left
            global right
            global esquerdo
            global meio
            global direito
            global estado
            global estadoant
            Robot.verificaCor(self)
            Robot.verificaEstado(self)
            if(estado == States(-3) == estadoant): #CurvaVerdeEsquerda
                Robot.stop(self,100)
                if(meio == 1):
                    while(meio == 1):
                        Robot.curva_esquerda1(self,speed_curva)
                    estado = States(-1)
                elif(meio == 0):
                    estado = States(-1)

            elif(estado == States(-2) == estadoant): #VerdeEsquerda
                Robot.verificaCor(self)
                Robot.verificaEstado(self)
                Robot.go_forward(self,speed_reta)
                Robot.verificaCor(self)
                Robot.verificaEstado(self)

            elif(estado == States(-1) == estadoant): #Esquerda
                Robot.stop(self,100)
                '''if(meio == 1):
                    Robot.curva_esquerda1(self,speed_curva)
                elif(meio == 0):
                    Robot.curva_esquerda(self,speed_curva)'''
                while(not(esquerdo == 0 and meio == 1 and direito == 0)):
                    while(meio == 0):
                        Robot.curva_esquerda(self,speed_curva)
                        if(esquerdo == 0 and meio == 1 and direito == 0):
                            break
                    while(meio == 1):
                        Robot.go_forward(self,speed_reta)
                        if(esquerdo == 0 and meio == 1 and direito == 0):
                            break
                Robot.verificaCor(self)
                Robot.verificaEstado(self)

            elif(estado == States(0) == estadoant): #Reto
                Robot.verificaCor(self)
                Robot.verificaEstado(self)
                Robot.go_forward(self,speed_reta)

            elif(estado == States(1) == estadoant): #Direita
                Robot.stop(self,100)
                '''if(meio == 1):
                    Robot.curva_direita1(self,speed_curva)
                elif(meio == 0):
                    Robot.curva_direita(self,speed_curva)'''
                while(not(esquerdo == 0 and meio == 1 and direito == 0)):
                    while(meio == 0):
                        Robot.curva_direita(self,speed_curva)
                        if(esquerdo == 0 and meio == 1 and direito == 0):
                            break
                    while(meio == 1):
                        Robot.go_forward(self,speed_reta)
                        if(esquerdo == 0 and meio == 1 and direito == 0):
                            break
                Robot.verificaCor(self)
                Robot.verificaEstado(self)

            elif(estado == States(2) == estadoant): #VerdeDireita
                Robot.verificaCor(self)
                Robot.verificaEstado(self)
                Robot.go_forward(self,speed_reta)
                Robot.verificaCor(self)
                Robot.verificaEstado(self)

            elif(estado == States(3) == estadoant): #CurvaVerdeDireita
                Robot.stop(self,100)
                if(meio == 1):
                    while(meio == 1):
                        Robot.curva_direita1(self,speed_curva)
                    estado = States(1)
                elif(meio == 0):
                    estado = States(1)

            elif(estado == States(4) == estadoant): #VerdeMeiaVolta
                Robot.verificaCor(self)
                Robot.verificaEstado(self)
                Robot.go_forward(self,speed_reta)
                Robot.verificaCor(self)
                Robot.verificaEstado(self)

            elif(estado == States(5) == estadoant): #MeiaVolta
                Robot.stop(self,100)
                Robot.meia_volta(self, 70)
                estado = States(0)

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

#with open('estados.txt', "w") as arquivo:
#    arquivo.write("BEGIN")

Corsa = Robot('outB','outD','in2','in3','in4','in1')
Corsa.abrirAprendizadoBranco()
Corsa.abrirAprendizadoPreto()
Corsa.abrirAprendizadoVerde()
Corsa.abrirAprendizadoBranco_meio()
Corsa.abrirAprendizadoPreto_meio()
Corsa.abrirAprendizadoBranco_direito()
Corsa.abrirAprendizadoPreto_direito()
Corsa.abrirAprendizadoVerde_direito()
Sound.speak('Hello, I am Corsa')
Corsa.seguirLinha(90,90)



