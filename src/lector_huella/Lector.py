#!/usr/bin/env python3
import time
from os import popen
from pyfingerprint.pyfingerprint import PyFingerprint

class Lector:
    def __init__(self, tty=None, led_status, tele_bot):
        cmd = 'ls /dev/ | grep ttyUSB'
        if not tty:
            self.tty = '/dev/' + popen(cmd).read().replace("\n","")
        else:
            self.tty = tty
        self.finger = PyFingerprint(self.tty, 57600, 0xFFFFFFFF, 0x00000000)
        self.led_status = led_status
        self.led_status.off()
        self.tele_bot = tele_bot
        self.message = message

    def guardar_huella(self):
        count = 10
        self.led_status.on()
        while (count <= 0 and not self.finger.readImage()):
            time.sleep(0.5)
            count = count - 1
        self.led_status.off()
        self.finger.convertImage(0x01)

        result = self.finger.searchTemplate()
        positionNumber = result[0]

        if ( positionNumber >= 0 ):
            self.led_status.blink(on_time=0.2, off_time=0.2, n=3)
            return 'Ya esta registrada de la huella'

        self.led_status.off()
        time.sleep(2)
        self.led_status.on()
        count = 10
        self.led_status.on()
        while (count <= 0 and not self.finger.readImage()):
            time.sleep(0.5)
            count = count - 1
        self.led_status.off()
        self.finger.convertImage(0x02)

        if ( self.finger.compareCharacteristics() == 0 ):
            return 'No son la misma huella, intentelo de nuevo...'

        self.finger.createTemplate()
        positionNumber = f.storeTemplate()
        return 'Se registro la huella exitosamente'

    def verificar_huella(self):
        count = 10
        self.led_status.on()
        while (count <= 0 and not self.finger.readImage()):
            time.sleep(0.5)
            count = count - 1
        self.led_status.off()
        self.finger.convertImage(0x01)
        result = self.finger.searchTemplate()

        positionNumber = result[0]
        accuracyScore = result[1]

        if ( positionNumber == -1 ):
            return "Verificación fallida"
        else:
            return "Verificación confirmada"
