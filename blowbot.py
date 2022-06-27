# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 11:02:34 2022

@author: nghia_sv
"""
import win32gui
import pyautogui
from pynput import mouse, keyboard
import time
from PIL import Image
import numpy as np
from multiprocessing import Process, Manager, Lock

mutex = Lock()
mc = mouse.Controller()
kc = keyboard.Controller()

WINDOW_X = 0
WINDOW_Y = 0
WINDOW_W = 1920
WINDOW_H = 1080

OFFSET_X = 10
OFFSET_Y = 40
MOVE_DX = 475
MOVE_DY = 200

WAIT = 1/10

def on_press(key):
    global flags
    global to_detect_pattern_names
    
    if key == keyboard.Key.f1:
        mutex.acquire()
        flags['auto'] = not flags['auto']
        flags['pattern_index'] = 0
        mutex.release()

def on_release(key):
    global flags
    # if key == keyboard.Key.esc and not flags['auto']:
    if key == keyboard.Key.esc:
        # Stop listener
        print('[INFO] exit')
        mutex.acquire()
        flags['quit'] = True
        mutex.release()
        return False

if __name__ == '__main__':
    #lookup
    pattern = []
    
    for y in range(WINDOW_Y+OFFSET_Y, WINDOW_Y+WINDOW_H, MOVE_DY):
        for x in range(WINDOW_X+OFFSET_X, WINDOW_X+WINDOW_W, MOVE_DX):
            pattern += [(x,y)]
    print(pattern)
    with Manager() as manager:

        flags = manager.dict({
            'auto': False,
            'quit': False,
            'pattern_index': 0,
            })
            
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            
            print('[INFO] ready!')
            while(not flags['quit']):
                if flags['auto']:
                    mutex.acquire()
                    mc.position = pattern[flags['pattern_index']]
                    time.sleep(WAIT)
                    print(pattern[flags['pattern_index']])
                    flags['pattern_index'] = (flags['pattern_index'] + 1) % len(pattern)
                    mutex.release()
            
            listener.join()