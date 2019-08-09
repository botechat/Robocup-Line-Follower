#!/usr/bin/env python3
# coding: utf-8
import ev3dev.ev3 as ev3
from ev3dev.ev3 import *
from enum import Enum
#from multiprocessing import Process
from time import sleep
from time import time

class States(Enum):
    Esquerda = -1
    Reto = 0
    Direita = 1
    PID = 2
    Encruzilhada = 3
    MeiaVolta = 4
    Obstaculo = 5

class Robot:
    def __init__(self,out1,out2,in1,in2,in3):

        self.lm1 = ev3.LargeMotor(out1); assert self.lm1.connected
        self.lm2 = ev3.LargeMotor(out2); assert self.lm2.connected
        self.se = ev3.ColorSensor(in1); assert self.se.connected
        self.sm = ev3.ColorSensor(in2); assert self.sm.connected
        self.sd = ev3.ColorSensor(in3); assert self.sd.connected
        #self.su = ev3.UltrasonicSensor(in4); assert self.su.connected

    def encontrarT(self): #encontrar target e trigger
        global target
        global trigger
        black = 0
        for i in range(5):
            Robot.verificaIntensidade(self)
            target += right
            black += middle

        target = target/5
        black = black/5
        trigger = (target + black)/2

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

    def goForward(self,speed):
        self.lm1.run_forever(speed_sp = -speed)
        self.lm2.run_forever(speed_sp = -speed)

    def goBack(self,speed):
        self.lm1.run_forever(speed_sp = speed)
        self.lm2.run_forever(speed_sp = speed)

    def turnLeft(self,v_curva):
        self.lm2.run_forever(speed_sp = -v_curva)
        self.lm1.run_forever(speed_sp = v_curva)

    def turnRight(self,v_curva):
        self.lm2.run_forever(speed_sp = v_curva)
        self.lm1.run_forever(speed_sp = -v_curva)

    def corrigeReto(self,speed,time):
        self.lm1.run_timed(speed_sp = -speed, time_sp = time)
        self.lm2.run_timed(speed_sp = -speed,time_sp = time)
        self.lm1.wait_while("running")
        self.lm2.wait_while("running")

    def corrigeTras(self,speed,time):
        self.lm1.run_timed(speed_sp = speed, time_sp = time)
        self.lm2.run_timed(speed_sp = speed,time_sp = time)
        self.lm1.wait_while("running")
        self.lm2.wait_while("running")

    def corrigeDireita(self,speed,time):
        self.lm2.run_timed(speed_sp = speed,time_sp = time)
        self.lm1.run_timed(speed_sp = -speed,time_sp = time)
        self.lm1.wait_while("running")
        self.lm2.wait_while("running")

    def corrigeEsquerda(self,speed,time):
        self.lm2.run_timed(speed_sp = -speed,time_sp = time)
        self.lm1.run_timed(speed_sp = speed,time_sp = time)
        self.lm1.wait_while("running")
        self.lm2.wait_while("running")

    def stop(self,time):
        self.lm1.run_timed(speed_sp = 0, time_sp = time, stop_action = 'coast')
        self.lm2.run_timed(speed_sp = 0, time_sp = time, stop_action = 'coast')
        self.lm1.wait_while("running")
        self.lm2.wait_while("running")

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

    def esquerda(self,v_curva):
        while(not(meio == 1)):
            Robot.verificaIntensidade(self)
            self.lm2.run_forever(speed_sp = -v_curva)
            self.lm1.run_forever(speed_sp = v_curva)

    def esquerda1(self,v_curva):
        while(not(meio == 0)):
            Robot.verificaIntensidade(self)
            self.lm2.run_forever(speed_sp = -v_curva)
            self.lm1.run_forever(speed_sp = v_curva)

    def curva_esquerda(self,speed_reta,speed_curva):
        while(not(esquerdo == 0 and meio == 1 and direito == 0)):
            while(meio == 0):
                Robot.verificaIntensidade(self)
                Robot.turnLeft(self,speed_curva)
                if(esquerdo == 0 and meio == 1 and direito == 0):
                    break
            while(meio == 1):
                Robot.verificaIntensidade(self)
                Robot.goForward(self,speed_reta)
                if(esquerdo == 0 and meio == 1 and direito == 0):
                    break

    def curva_direita(self,speed_reta,speed_curva):
        while(not(esquerdo == 0 and meio == 1 and direito == 0)):
            while(meio == 0):
                Robot.verificaIntensidade(self)
                Robot.turnRight(self,speed_curva)
                if(esquerdo == 0 and meio == 1 and direito == 0):
                    break
            while(meio == 1):
                Robot.verificaIntensidade(self)
                Robot.goForward(self,speed_reta)
                if(esquerdo == 0 and meio == 1 and direito == 0):
                    break

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

        #if d == direitoant:  #fazer duas verificações para ter mais precisão
        direito = d
        #if e == esquerdoant:
        esquerdo = e

        print(esquerdo, " ", meio, " ", direito)

    def verificaIntensidade(self):
        global esquerdo
        global meio
        global direito
        global left
        global middle
        global right
        global trigger

        left = self.se.reflected_light_intensity
        middle = self.sm.reflected_light_intensity
        right = self.sd.reflected_light_intensity

        if(left < trigger): #preto
            esquerdo = 1
        else: #branco
            esquerdo = 0

        if(middle < trigger): #preto
            meio = 1
        else: #branco
            meio = 0

        if(right < trigger): #preto
            direito = 1
        else: #branco
            direito = 0

        print(left, " ", middle, " ", right, " ", esquerdo, " ", meio, " ", direito)

    def PID(self):
        global esquerdo
        global meio
        global direito
        global target
        global trigger
        global turn
        global errorLeft
        global errorRight
        global errorTotal
        global kp
        global ki
        global kd
        global correction
        global integral
        global derivative
        global lastError
        left = self.se.reflected_light_intensity
        middle = self.sm.reflected_light_intensity
        right = self.sd.reflected_light_intensity

        errorTotal = right - left
        integral += errorTotal
        derivative = errorTotal - lastError
        correction = errorTotal * kp + integral * ki + derivative * kd

        lastError = errorTotal
        #correciton = (error * kp) + (integral * ki) + (derivative * kd)
        #error = target - value
        #integral = integral + error
        #derivative = error - last_error

    def verificaEncruzilhada(self):
        if(esquerdo == 1 and meio == 1 and direito == 0):
            return True
        elif(esquerdo == 1 and meio == 0 and direito == 1):
            return True
        elif(esquerdo == 0 and meio == 1 and direito == 1):
            return True
        elif(esquerdo == 1 and meio == 1 and direito == 1):
            return True
        else:
            return False

    def temCertezaEncruzilhada(self):
        for i in range(5):
            Robot.goForward(self,100)
            Robot.verificaIntensidade(self)
            if(esquerdo == 1 and meio == 1 and direito == 0):
                verdade[i] = True
            elif(esquerdo == 1 and meio == 0 and direito == 1):
                verdade[i] = True
            elif(esquerdo == 0 and meio == 1 and direito == 1):
                verdade[i] = True
            elif(esquerdo == 1 and meio == 1 and direito == 1):
                verdade[i] = True
            else:
                return False

        for i in range(4):
            if(verdade[i] and verdade[i+1]):
                ok = True
            else:
                ok = False
                break
        if ok == True:
            return True
        else:
            return False

    def meiaVolta(self, sp_curv):
        Robot.stop(self,100)
        print("estou fazendo meia volta")
        if(meio == 1):
            while(meio == 1):
                Robot.verificaIntensidade(self)
                Robot.turnRight(self,sp_curv)
            while(meio == 0):
                Robot.verificaIntensidade(self)
                Robot.turnRight(self,sp_curv)
            while(meio == 1):
                Robot.verificaIntensidade(self)
                Robot.turnRight(self,sp_curv)
            while(meio == 0):
                Robot.verificaIntensidade(self)
                Robot.turnRight(self,sp_curv)
        elif(meio == 0):
            while(meio == 0):
                Robot.verificaIntensidade(self)
                Robot.turnRight(self,sp_curv)
            while(meio == 1):
                Robot.verificaIntensidade(self)
                Robot.turnRight(self,sp_curv)
            while(meio == 0):
                Robot.verificaIntensidade(self)
                Robot.turnRight(self,sp_curv)


    def encruzilhada(self,speed_reta,speed_curva):
        global estado
        global esquerdo
        global meio
        global direito
        global errorTotal
        global viraEsquerda
        global viraDireita
        global jaReleu
        jaReleu = True
        viraEsquerda = False
        viraDireita = False
        Robot.reposicionar(self)
        while(Robot.verificaEncruzilhada(self) == False):
            Robot.verificaCor(self)
            Robot.goForward(self,30) #CALIBRAR
            print(esquerdo, " ", meio, " ", direito)
            if(esquerdo == 2):
                viraEsquerda = True
            if(direito == 2):
                viraDireita = True
        if(viraEsquerda == True and viraDireita == False):
            Robot.corrigeReto(self,200,700) #CALIBRAR
            Sound.speak("Left Green")
            Robot.verificaIntensidade(self)
            if(meio == 1):
                while(meio == 1):
                    Robot.verificaIntensidade(self)
                    Robot.turnLeft(self,speed_curva)
                Robot.curva_esquerda(self,speed_reta,speed_curva)
            elif(meio == 0):
                Robot.curva_esquerda(self,speed_reta,speed_curva)
            estado = States(2)
            #Robot.corrigeReto(self,200,600)

        elif(viraEsquerda == False and viraDireita == True):
            Robot.corrigeReto(self,200,700) #CALIBRAR
            Sound.speak("Right Green")
            Robot.verificaIntensidade(self)
            if(meio == 1):
                while(meio == 1):
                    Robot.verificaIntensidade(self)
                    Robot.turnRight(self,speed_curva)
                Robot.curva_direita(self,speed_reta,speed_curva)
            elif(meio == 0):
                Robot.curva_direita(self,speed_reta,speed_curva)
            estado = States(2)
            #Robot.corrigeReto(self,200,600)

        elif(viraEsquerda == True and viraDireita == True):
            Sound.speak("Both Green")
            Robot.corrigeReto(self,100,1000) #CALIBRAR
            Robot.meiaVolta(self,speed_curva) #meia volta

        elif(viraEsquerda == False and viraDireita == False):
            Sound.speak("No Green")
            Robot.corrigeReto(self,200,700) #CALIBRAR
        esquerdo = 0
        meio = 1
        direito = 0
        errorTotal = 0
        estado = States(2)

    def reposicionar(self): #CALIBRAR
        global viraEsquerda
        global viraDireita
        Robot.stop(self,100)
        for i in range(3):
            Robot.corrigeTras(self,100,200)
            Robot.verificaCor(self)
            if(esquerdo == 2):
                viraEsquerda = True
            if(direito == 2):
                viraDireita = True

    def verificaDistancia(self,distancia_limite):
        global estado
        self.su.mode = 'US-DIST-CM'
        if(self.su.value() <= distancia_limite):
            estado = States(5)
            Robot.desviaObstaculo(self,150,80,950,800,800)

    def desviaObstaculo(self,speed_reta_obstaculo,speed_curva_obstaculo,posret,posesq,posdir):
        global estado
        if(estado == States(5)):
            Robot.curva_direita_obstaculo(self,speed_curva_obstaculo,0.50*posdir)
            Robot.go_forward_obstaculo(self,speed_reta_obstaculo,0.55*posret)
            Robot.curva_esquerda_obstaculo(self,speed_curva_obstaculo,0.47*posesq)
            Robot.go_forward_obstaculo(self,speed_reta_obstaculo,0.40*posret)
            Robot.curva_esquerda_obstaculo(self,speed_curva_obstaculo,0.7*posesq)
            Robot.go_forward_obstaculo(self,speed_reta_obstaculo,0.65*posret)
            Robot.curva_direita_obstaculo(self,speed_curva_obstaculo,0.6*posdir)
            Robot.go_forward_obstaculo(self,speed_reta_obstaculo,-0.35*posret) #vai pra trás
            if(meio == 0): #voltar a seguir linha
                if(esquerdo == 1):
                    estado = States(-1)
                elif(direito == 1):
                    estado = States(1)
                else:
                    estado = States(0)
            elif(meio == 1):
                estado = States(0)


    def seguidor(self,speed_reta,speed_curva):
        global correction
        initialSpeed = speed_reta
        if(Robot.verificaEncruzilhada(self) == True):
            Robot.encruzilhada(self,speed_reta,speed_curva)

        self.lm1.run_forever(speed_sp = (initialSpeed - correction))
        self.lm2.run_forever(speed_sp = (initialSpeed + correction))



    def seguirLinha(self,speed_reta,speed_curva):
        global esquerdo
        global meio
        global direito
        global estado
        while(True):
            #Robot.verificaDistancia(self,135) #CALIBRAR
            Robot.verificaIntensidade(self)
            Robot.PID(self)
            Robot.seguidor(self,speed_reta,speed_curva) #CALIBRAR

verdade = [0,0,0,0,0]
turn = 0
esquerdo = 0
direito = 0
meio = 0
trigger = 0 #28 tem que incluir o verde e o preto
kp = 5
ki = 0 #-0.05
kd = 0 #8
target = 0
errorLeft = 0
errorRight = 0
errorTotal = 0
correction = 0
integral = 0
derivative = 0
lastError = 0
estado = States(2)
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
esquerdo = 0
direito = 0
meio = 0
e = 0
d = 0

#with open('estados.txt', "w") as arquivo:
#    arquivo.write("BEGIN")

Corsa = Robot('outB','outD','in2','in3','in4')
Corsa.abrirAprendizadoBranco()
Corsa.abrirAprendizadoPreto()
Corsa.abrirAprendizadoVerde()
Corsa.abrirAprendizadoBranco_meio()
Corsa.abrirAprendizadoPreto_meio()
Corsa.abrirAprendizadoBranco_direito()
Corsa.abrirAprendizadoPreto_direito()
Corsa.abrirAprendizadoVerde_direito()
Corsa.encontrarT()
Corsa.seguirLinha(100,90)

#TODO aplicar máquina de estados antiga quando vê encruzilhada
#TODO erro: Corsa vê encruzilhada quando não tem, e se perde na linha -> limitar tempo
#TODO erro: vira antes de entrar na encruzilhada
#TODO erro: segue torto no branco e erra gap
#TODO obs: talvez a leitura do sensor do meio esteja interferindo nos erros acima listados
#TODO vê encruzilhada, vai para trás e entra na máquina de estados
