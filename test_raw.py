import usb_hid
import time
import board
import analogio
from digitalio import DigitalInOut, Direction, Pull #Full range: 3.3v
import os
import PicoRobotics
import digitalio


led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
btn1 = DigitalInOut(board.GP1)
btn2 = DigitalInOut(board.GP0)
#joy_up_down = analogio.AnalogIn(board.GP28)
#joy_left_right = analogio.AnalogIn(board.GP27)
#joy_theta = analogio.AnalogIn(board.GP26)
btn1.direction = Direction.INPUT
btn1.pull = Pull.UP
btn2.direction = Direction.INPUT
btn2.pull = Pull.UP
board1 = PicoRobotics.KitronikPicoRobotics()
directions = ["f","r"]

MIN = 25000
MAX = 35000
MAXVALUE = 65000
MINVALUE = 7000
Vit = 70

# Limit switch GPIO pins
limit_switch_1_fw_pin = board.GP3
limit_switch_1_rv_pin = board.GP2

limit_switch_2_fw_pin = board.GP12
limit_switch_2_rv_pin = board.GP13

limit_switch_3_fw_pin = board.GP7
limit_switch_3_rv_pin = board.GP10

# Configure limit switches as inputs with pull-ups
limit_switch_1_fw = digitalio.DigitalInOut(limit_switch_1_fw_pin)
limit_switch_1_fw.switch_to_input(pull=digitalio.Pull.UP)
limit_switch_1_rv = digitalio.DigitalInOut(limit_switch_1_rv_pin)
limit_switch_1_rv.switch_to_input(pull=digitalio.Pull.UP)

limit_switch_2_fw = digitalio.DigitalInOut(limit_switch_2_fw_pin)
limit_switch_2_fw.switch_to_input(pull=digitalio.Pull.UP)
limit_switch_2_rv = digitalio.DigitalInOut(limit_switch_2_rv_pin)
limit_switch_2_rv.switch_to_input(pull=digitalio.Pull.UP)

limit_switch_3_fw = digitalio.DigitalInOut(limit_switch_3_fw_pin)
limit_switch_3_fw.switch_to_input(pull=digitalio.Pull.UP)
limit_switch_3_rv = digitalio.DigitalInOut(limit_switch_3_rv_pin)
limit_switch_3_rv.switch_to_input(pull=digitalio.Pull.UP)

Vit = 70

def toggle(pin):
    pin.value = not pin.value

def check_limit_switches():
    if not limit_switch_1_fw.value:
        print("Limit forward switch 1 is triggered")
        board1.motorOn(1, "f", 0)  # Stop motor 1
        
    if not limit_switch_1_rv.value:
        print("Limit reverse switch 1 is triggered")
        board1.motorOn(1, "r", 0)  # Stop motor 1

    if not limit_switch_2_fw.value:
        print("Limit forward switch 2 is triggered")
        board1.motorOn(2, "f", 0)  # Stop motor 1
        
    if not  limit_switch_2_rv.value:
        print("Limit reverse switch 2 is triggered")
        board1.motorOn(2, "r", 0)  # Stop motor 1

    if not limit_switch_3_fw.value:
        print("Limit forward switch 3 is triggered")
        board1.motorOn(3, "f", 0)  # Stop motor 1
        
    if not limit_switch_3_rv.value:
        print("Limit reverse switch 3 is triggered")
        board1.motorOn(3, "r", 0)  # Stop motor 1

    
#     print("limit1_rv")
#     print(limit1_rv)
#     print("limit1_fw")
#     print(limit1_fw)


class joy:
    def __init__(self):
        self.up_down = analogio.AnalogIn(board.GP28)
        self.left_right = analogio.AnalogIn(board.GP27)
        self.theta = analogio.AnalogIn(board.GP26)
        
    def tension(r):
        return (0.465+(r*(4.16-0.465))/65536)*(1.976/(1.976+0.732))

    def direction(self):
        if self.up_down.value > MAX :
                if self.left_right.value > MAX :
                    print("joystick is down and right")
                    if limit_switch_3_rv.value :
                        board1.motorOn(3, "r", Vit)
                    if limit_switch_1_rv.value :
                        board1.motorOn(1, "r", Vit)
                elif self.left_right.value < MIN :
                    print("joystick is down and left")
                    if limit_switch_3_rv.value :
                        board1.motorOn(3, "r", Vit)
                    if limit_switch_1_fw.value :
                        board1.motorOn(1, "f", Vit)
                else :
                    print("joystick is down ")
                    if limit_switch_3_rv.value :
                        board1.motorOn(3, "r", Vit)
        elif self.up_down.value < MIN :
                if self.left_right.value > MAX :
                    print("joystick is up and right")
                    if limit_switch_3_fw.value :
                        board1.motorOn(3, "f", Vit)
                    if limit_switch_1_rv.value :
                        board1.motorOn(1, "r", Vit)
                elif self.left_right.value < MIN :
                    print("joystick is up and left")
                    if limit_switch_3_fw.value :                    
                        board1.motorOn(3, "f", Vit)
                    if limit_switch_1_fw.value :
                        board1.motorOn(1, "f", Vit)
                else :
                    print("joystick is up ")
                    if limit_switch_3_fw.value :                    
                        board1.motorOn(3, "f", Vit)
        else :
            if self.left_right.value > MAX :
                print("joystick is right ")
                if limit_switch_1_rv.value :
                    board1.motorOn(1, "r", 50)
            elif self.left_right.value > MIN :
                print("joystick is stable ")
                board1.motorOn(1, "r", 0)
                board1.motorOn(3, "r", 0)
            else :
                print("joystick is left ")
                if limit_switch_1_fw.value :
                    board1.motorOn(1, "f", 50)
        if self.theta.value > MAX :
            print("joystick rotate right")
        elif self.theta.value < MIN :
            print("joystick rotate left")

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


while True:
    toggle(led)
    print(joy.up_down.value)
    print(joy.left_right.value)
    print(joy.theta.value)
    print("----------")
    check_limit_switches()

    joy.direction()
    if not btn1.value:
        print("zoom out")
        print(btn1.value)
        board1.motorOn(2, "f", Vit)
        time.sleep(0.2)
    if not btn2.value:
        print("zoom in")
        print(btn2.value)
        board1.motorOn(2, "r", Vit)
        time.sleep(0.2)
    if (btn1.value and btn2.value):
        board1.motorOn(2, "f", 0)
    
    time.sleep(0.1)
