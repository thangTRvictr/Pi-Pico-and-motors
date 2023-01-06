import PicoRobotics
import time
import usb_hid
from adafruit_hid.mouse import Mouse
import time
import board
import analogio
from digitalio import DigitalInOut, Direction, Pull #Full range: 3.3v
import os

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
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
directions = ["f","r"]

MAX=24500
MIN=23500
MAXVALUE=
MINVALUE=
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
                    board1.motorOn(3, "r", (MAXVALUE-self.up_down.value)/(MAXVALUE-MAX)*100)
                    board1.motorOn(1, "f", (MAXVALUE-self.left_right.value)/(MAXVALUE-MAX)*100)
                elif self.left_right.value < MIN :
                    print("joystick is down and left")
                    board1.motorOn(3, "r", (MAXVALUE-self.up_down.value)/(MAXVALUE-MAX)*100)
                    board1.motorOn(1, "r", (MIN-self.left_right.value)/(MIN-MINVALUE)*100)
                else :
                    print("joystick is down ")
                    board1.motorOn(3, "r", (MAXVALUE-self.up_down.value)/(MAXVALUE-MAX)*100)
        elif self.up_down.value < MIN :
                if self.left_right.value > MAX :
                    print("joystick is up and right")
                    board1.motorOn(3, "f", (MIN-self.up_down.value)/(MIN-MINVALUE)*100)
                    board1.motorOn(1, "f", (MAXVALUE-self.left_right.value)/(MAXVALUE-MAX)*100)
                elif self.left_right.value <MIN :
                    print("joystick is up and left")
                    board1.motorOn(3, "f", (MIN-self.up_down.value)/(MIN-MINVALUE)*100)
                    board.motorOn(1, "r", (MIN-self.left_right.value)/(MIN-MINVALUE)*100)
                else :
                    print("joystick is up ")
                    board1.motorOn(3, "f", (MIN-self.up_down.value)/(MIN-MINVALUE)*100)
        else :
            if self.left_right.value > MAX :
                print("joystick is right ")
                board1.motorOn(1, "f", (MAXVALUE-self.left_right.value)/(MAXVALUE-MAX)*100)
            elif self.left_right.value > MIN :
                print("joystick is stable ")
                board1.motorOn(1, "r", 0)
                board1.motorOn(2, "r", 0)
                board1.motorOn(3, "r", 0)
            else :
                print("joystick is left ")
                board1.motorOn(1, "r", (MIN-self.left_right.value)/(MIN-MINVALUE)*100)
                
        if self.theta.value > MAX :
            print("joystick rotate right")
        elif self.theta.value < MIN :
            print("joystick rotate left")
       
joy = joy()
mouse = Mouse(usb_hid.devices)

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

while True:
    toggle(led)
    print(joy.up_down.value)
    print(joy.left_right.value)
    print(joy.theta.value)
    print("----------")
    joy.direction()
    if not btn1.value:
        print("zoom in")
        print(btn1.value)
        board1.motorOn(2, "f", 70)
        time.sleep(0.2)
    if not btn2.value:
        print("zoom out")
        print(btn2.value)
        board1.motorOn(2, "r", 70)
        time.sleep(0.2)
    if (btn1.value and btn2.value):
        board1.motorOn(2, "f", 0)
    time.sleep(0.01)