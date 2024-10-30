import os
import threading


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def key_pressed():
    return input() != ''

def stop():
    return threading.Event()