#     AUTOR:    BrincandoComIdeias
#     APRENDA:  https://cursodearduino.net/
#     SKETCH:   Fontes e Baterias para o Pico
#     DATA:     14/12/22

import machine
from utime import sleep as delay 


pinCTRLX = machine.ADC(27)
pinCTRLY = machine.ADC(26)
pinCTRLZ = machine.Pin(22, machine.Pin.IN)

pinGarra = machine.Pin(21)
pinPulso = machine.Pin(20)
pinBraco = machine.Pin(19)
pinBase  = machine.Pin(18)

garra = machine.PWM(pinGarra)
garra.freq(50) #Frequencia do sinal do Servo

pulso = machine.PWM(pinPulso)
pulso.freq(50) #Frequencia do sinal do Servo

braco = machine.PWM(pinBraco)
braco.freq(50) #Frequencia do sinal do Servo

base = machine.PWM(pinBase)
base.freq(50) #Frequencia do sinal do Servo

# Equivalente a função map()
def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

# Converte um angulo no valor de pulso do Servo
def pulsoServo(x):
    if (x <= 0) :
        return 3276 # 1 mS = 0º
    elif (x >= 180) :
        return 6553 # 2 mS = 180º
    else :
        return map(x, 0, 180, 3276, 6553) 

while True:
    
    leituraX = pinCTRLX.read_u16() # 0 ~ 65535
    tensaoX = map(leituraX, 0, 65535, 0, 330)
    anguloX = map(tensaoX, 0, 330, 180, 0)
    
    leituraY = pinCTRLY.read_u16() # 0 ~ 65535
    tensaoY = map(leituraY, 0, 65535, 0, 330)
    anguloY = map(tensaoY, 0, 330, 180, 0)
    
    base.duty_u16(pulsoServo(anguloX))
    braco.duty_u16(pulsoServo(anguloY))
    pulso.duty_u16(pulsoServo(anguloY))
    
    if pinCTRLZ.value():
        garra.duty_u16(pulsoServo(70))
    else:
        garra.duty_u16(pulsoServo(0))
    
    print(f"LeituraX: {leituraX}\t TensãoX: {tensaoX}\t AnguloX: {anguloX}\t LeituraY: {leituraY}\t TensãoY: {tensaoY}\t AnguloY: {anguloY}   ", end='\r')
    
    delay(0.05) # delay de 50mS