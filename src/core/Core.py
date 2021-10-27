#!/usr/bin/env python3

import time
import os
from signal import pause
from gpiozero import Servo, LED
from pyfingerprint.pyfingerprint import PyFingerprint


class Core:
    def __init__(self):
        self.status_led_ok = LED(3)
        self.status_led_error = LED(4)
        self.servo_motor = Servo(17)
        self.servo_motor.min()
        self.__key_api_telegram = os.getenv("TELEGRAM_API")

    def abrir_cerradura(self):
        self.servo_motor.max()

    def cerrar_cerradura(self):
        self.servo_motor.min()


if __name__ == "__main__":
    cerradura = Core()
    while True:
        time.sleep(2)
        cerradura.abrir_cerradura()
        time.sleep(2)
        cerradura.cerrar_cerradura()
