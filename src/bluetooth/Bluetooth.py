#!/usr/bin/env python3

from signal import pause
from threading import Thread

class Bluetooth(Thread):
    def __init__(self, bluetooth, servo):
        """!
        Esta clase se encarga de controlar las acciones de la cerradura por bluetooth
        @param bluetooth Recibe una instancia de BlueDot
        @param servo Recibe una instancia de un Servomotor
        """
        Thread.__init__(self)
        self.bd = bluetooth
        self.servo = servo

    def dpad(self, pos):
        """!
        Por zona en la cual se presiona el bluedot, se abre o cierra la cerradura:
        Arrba Abre.
        Abajo Cierra
        """
        if pos.top:
            self.servo.max()
            print("Abriendo con BT")
        elif pos.bottom:
            self.servo.min()
            print("Cerrando con BT")
        else:
            pass

    def bluetooth_main(self):
        """!
        Escucha la entrada de BlueDot
        """
        self.bd.when_pressed = self.dpad

        pause()

    def run(self):
        """!
        Ejecuta la instancia en un hilo de ejecución
        """
        self.bluetooth_main()
