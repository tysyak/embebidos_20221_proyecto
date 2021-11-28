#!/usr/bin/env python3

from signal import pause
from threading import Thread

class Bluetooth(Thread):
    def __init__(self, bluetooth, servo):
        Thread.__init__(self)
        self.bd = bluetooth
        self.servo = servo

    def dpad(self, pos):
        if pos.top:
            self.servo.max()
            print("Abriendo con BT")
        elif pos.bottom:
            self.servo.min()
            print("Cerrando con BT")
        else:
            pass

    def bluetooth_main(self):
        self.bd.when_pressed = self.dpad

        pause()

    def run(self):
        self.bluetooth_main()
