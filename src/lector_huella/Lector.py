#!/usr/bin/env python3
import time
from os import popen
from threading import Thread
from pyfingerprint.pyfingerprint import PyFingerprint

class Lector(Thread):
    def __init__(self,  led_status_r, led_status_g, tele_bot, servo, tty=None):
        """!
        Esta clase se encarga de realizar las acciones del lector de huella
        digital como:
        - Dar de alta la huella
        - Borrar Huella
        - Verificar existencia de la huella
        - Abrir cerradura si la huella coincide con la base de datos

        @param led_status_r Instancia de led de estado roja
        @param led_status_g Instancia de led de estado verde
        @param tele_bot Bot de telegram
        @param servo Servomotor a controlar
        @param tty Puerto serial USB de lector de huella, por defecto es /dev/ttyUSBX
        """
        Thread.__init__(self)
        cmd = 'ls /dev/ | grep ttyUSB'
        if not tty:
            self.tty = '/dev/' + popen(cmd).read().replace("\n","")
        else:
            self.tty = tty
        self.finger = PyFingerprint(self.tty, 57600, 0xFFFFFFFF, 0x00000000)
        self.led_status_r = led_status_r
        self.led_status_g = led_status_g
        self.tele_bot = tele_bot
        self.servo = servo
        # self.message = message

    def guardar_huella(self):
        """!
        metodo para salvar huella en la memoria del lector
        """
        count = 10
        self.led_status_g.on()
        while (count <= 0 and not self.finger.readImage()):
            time.sleep(0.5)
            count = count - 1
        self.led_status_g.off()
        self.finger.convertImage(0x01)

        result = self.finger.searchTemplate()
        positionNumber = result[0]

        if ( positionNumber >= 0 ):
            self.led_status_g.blink(on_time=0.2, off_time=0.2, n=3)
            return 'Ya esta registrada de la huella'

        self.led_status_g.off()
        time.sleep(2)
        self.led_status_g.on()
        count = 10
        self.led_status_g.on()
        while (count <= 0 and not self.finger.readImage()):
            time.sleep(0.5)
            count = count - 1
        self.led_status_g.off()
        self.finger.convertImage(0x02)

        if ( self.finger.compareCharacteristics() == 0 ):
            return 'No son la misma huella, intentelo de nuevo...'

        self.finger.createTemplate()
        positionNumber = self.finger..storeTemplate()
        return 'Se registro la huella exitosamente'

    def verificar_huella(self):
        """!
        Metodo que verifica la existencia de la huella
        """
        count = 10
        self.led_status_g.on()
        while (count <= 0 and not self.finger.readImage()):
            time.sleep(0.5)
            count = count - 1
        self.led_status_g.off()
        self.finger.convertImage(0x01)
        result = self.finger.searchTemplate()

        positionNumber = result[0]
        accuracyScore = result[1]

        if ( positionNumber == -1 ):
            return "Verificación fallida"
        else:
            return "Verificación confirmada"

    def controlar_puerta(self):
        """!
        Metodo que controla la puerta si se coincide la huella con alguna de la
        BD del lector
        """
        while True:
            print('Waiting for finger...')

            ## Wait that finger is read
            while ( self.finger.readImage() == False ):
                pass

            ## Converts read image to characteristics and stores it in charbuffer 1
            self.finger.convertImage(0x01)

            ## Checks if finger is already enrolled
            result = self.finger.searchTemplate()
            positionNumber = result[0]

            if ( positionNumber >= 0 ):
                self.led_status_g.blink(on_time=0.25, off_time=0.25, n=3)
                if self.servo.value == -1.0:
                    self.servo.max()
                else:
                    self.servo.min()
            else:
                self.led_status_r.blink(on_time=0.25, off_time=0.25, n=3)
            time.sleep(3)

    def run(self):
        """!
        Ejecuta el escucha del lector en un hilo de ejecucion
        """
        self.controlar_puerta()
