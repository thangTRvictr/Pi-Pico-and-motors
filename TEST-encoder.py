import usb_hid
import time
import board
import analogio
from digitalio import DigitalInOut, Direction, Pull #Full range: 3.3v
import os
import PicoRobotics
from rp2 import PIO, StateMachine, asm_pio
from machine import Pin
import utime

btn1 = DigitalInOut(board.GP2)
btn2 = DigitalInOut(board.GP3)
#joy_up_down = analogio.AnalogIn(board.GP28)
#joy_left_right = analogio.AnalogIn(board.GP27)
#joy_theta = analogio.AnalogIn(board.GP26)
btn1.direction = Direction.INPUT
btn1.pull = Pull.UP
btn2.direction = Direction.INPUT
btn2.pull = Pull.UP
board1 = PicoRobotics.KitronikPicoRobotics()
led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT

MIN = 25000
MAX = 35000
MAXVALUE = 65000
MINVALUE = 7000

class joy:
    def __init__(self):
        self.up_down = analogio.AnalogIn(board.GP28)
        self.left_right = analogio.AnalogIn(board.GP27)
        self.theta = analogio.AnalogIn(board.GP26)
        #self.acceleration
    def tension(r):
        return (0.465+(r*(4.16-0.465))/65536)*(1.976/(1.976+0.732))

    def direction(self):
        if self.up_down.value > MAX :
                if self.left_right.value > MAX :
                    print("joystick is down and right")
                    board1.motorOn(3, "f", ((self.up_down.value-MAX)/(MAXVALUE-MAX))*100)
                    board1.motorOn(1, "f", ((self.left_right.value-MAX)/(MAXVALUE-MAX))*100)
                elif self.left_right.value < MIN :
                    print("joystick is down and left")
                    board1.motorOn(3, "f", ((self.up_down.value-MAX)/(MAXVALUE-MAX))*100)
                    board1.motorOn(1, "r", ((MIN-self.left_right.value)/(MIN-MINVALUE))*100)
                else :
                    speed= ((self.up_down.value-MAX)/(MAXVALUE-MAX))*100
                    print(f"joystick is down {speed}")
                    board1.motorOn(3, "f",speed)
        elif self.up_down.value < MIN :
                if self.left_right.value > MAX :
                    print("joystick is up and right")
                    board1.motorOn(3, "r", ((MIN-self.up_down.value)/(MIN-MINVALUE))*100)
                    board1.motorOn(1, "f", ((self.left_right.value-MAX)/(MAXVALUE-MAX))*100)
                elif self.left_right.value < MIN :
                    print("joystick is up and left")
                    board1.motorOn(3, "r", ((MIN-self.up_down.value)/(MIN-MINVALUE))*100)
                    board1.motorOn(1, "r", ((MIN-self.left_right.value)/(MIN-MINVALUE))*100)
                else :
                    speed=((MIN-self.up_down.value)/(MIN-MINVALUE))*100
                    print(f"joystick is up {speed}")
                    board1.motorOn(3, "r", speed)
        else :
            if self.left_right.value > MAX :
                speed=((self.left_right.value-MAX)/(MAXVALUE-MAX))*100
                print(f"joystick is right {speed}")
                board1.motorOn(1, "f", speed)
            elif self.left_right.value > MIN :
                print("joystick is stable ")
                board1.motorOn(1, "r", 0)
                board1.motorOn(2, "r", 0)
                board1.motorOn(3, "r", 0)
            else :
                print("joystick is left ")
                board1.motorOn(1, "r", ((MIN-self.left_right.value)/(MIN-MINVALUE))*100)
        if self.theta.value > MAX :
            print("joystick rotate right")
        elif self.theta.value < MIN :
            print("joystick rotate left")


    #def valuetension(self):
         #print("tension of joystick left right is %.2F" %tension(self.left_right.value),"V")
         #print("tension of joystick up down is %.2F" %tension(self.up_down.value),"V")
         #print("tension of joystick theta is %.2F" %tension(self.theta.value),"V")

joy = joy()


led.value = True
time.sleep(1)
led.value = False
n = 1

def toggle(pin):
    if pin.value:
        pin.value = False
    else:
        pin.value = True

def resitor(r):
    return (r*4.7)/65536

def encoder():
    label("start")
    wait(0, pin, 0)         # Wait for CLK to go low
    jmp(pin, "WAIT_HIGH")   # if Data is low
    mov(x, invert(x))           # Increment X
    jmp(x_dec, "nop1")
    label("nop1")
    mov(x, invert(x))
    label("WAIT_HIGH")      # else
    jmp(x_dec, "nop2")          # Decrement X
    label("nop2")
    
    wait(1, pin, 0)         # Wait for CLK to go high
    jmp(pin, "WAIT_LOW")    # if Data is low
    jmp(x_dec, "nop3")          # Decrement X
    label("nop3")
    
    label("WAIT_LOW")       # else
    mov(x, invert(x))           # Increment X
    jmp(x_dec, "nop4")
    label("nop4")
    mov(x, invert(x))
    wrap()
    
sm1 = StateMachine(1, encoder, freq=125_000_000, in_base=Pin(3), jmp_pin=Pin(2))
sm1.active(1)

while True:
    utime.sleep(1)
    sm1.exec("in_(x, 32)")
    x = sm1.get()
    print(x)
    toggle(led)
    print(joy.up_down.value)
    print(joy.left_right.value)
    print(joy.theta.value)
    print("----------")
    joy.direction()
    if not btn1.value:
        print("speep up")
        print(btn1.value)
        n = n / 2
        print(n)
        time.sleep(0.2)
    if not btn2.value:
        print("slow down")
        print(btn2.value)
        n = n * 2
        print(n)
        time.sleep(0.2)
    # break
    # else:
    # print("BTN is up")
    # pass
    time.sleep(0.01)
