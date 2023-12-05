# SkyDeck Joystick adapter. Run on steam deck as script to send
# joystick output to the esp32s2. Ensure deck is set to controller
# mode when using

import signal
from xbox360controller import Xbox360Controller
import serial
from deck_joy import Ctrl
from scipy.interpolate import interp1d
import time

m = interp1d([-1, 1],[100, 900])
m2 = interp1d([0, 1],[100, 900])

try:
    ser = serial.Serial('/dev/ttyACM1', 115200, timeout=2)
except:
    ser = serial.Serial('/dev/ttyACM2', 115200, timeout=2)

deck = Xbox360Controller(0, axis_threshold=0.2)

def loop():
    
    lx = str(int(m(deck.axis_l.x))).zfill(3)
    ly = str(int(m(deck.axis_l.y))).zfill(3)

    rx = str(int(m(deck.axis_r.x))).zfill(3)
    ry = str(int(m(deck.axis_r.y))).zfill(3)

    rt = str(int(m2(deck.trigger_r.value))).zfill(3)
    lt = str(int(m2(deck.trigger_l.value))).zfill(3)

    a = str(int(m2(deck.button_a.is_pressed))).zfill(3)
    b = str(int(m2(deck.button_b.is_pressed))).zfill(3)
    x = str(int(m2(deck.button_x.is_pressed))).zfill(3)
    y = str(int(m2(deck.button_y.is_pressed))).zfill(3)

    ls = str(int(m2(deck.button_thumb_l.is_pressed))).zfill(3)
    rs = str(int(m2(deck.button_thumb_r.is_pressed))).zfill(3)

    lb = str(int(m2(deck.button_trigger_l.is_pressed))).zfill(3)
    rb = str(int(m2(deck.button_trigger_r.is_pressed))).zfill(3)

    outputs = ly + lx + ry + rx + lt + rt + lb + rb + ":"

    ser.write(outputs.encode())

    time.sleep(0.001)
    

def main():
    while True:
        loop()

if __name__ == "__main__":
    main()
