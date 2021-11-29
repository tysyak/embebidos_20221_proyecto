#!/usr/bin/env python3
from emoji import emojize
from time import sleep
from signal import pause
from threading import Thread


class Distancia(Thread):
        """!
    def __init__(self, dist_sensor, led_status, tele_bot, database, shutdown_flag):
        Esta Clase Se encarga de instanciar y controlar el sensor de distancia,
        avisa al usuario si alguien esta cerca de la cerradura.
        @param dist_sensor Instancia del sensor de distancica
        @param led_status Instancua del led de estado
        @param tele_bot Instancia del bot de telegram
        @param database Instancia del controlador de la BD
        @param shutdown_flag Bandera de señales
        """
        Thread.__init__(self)
        self.shutdown_flag = shutdown_flag

        self.dist_sensor = dist_sensor
        self.led_status = led_status
        self.tele_bot = tele_bot
        self.__conn = database

    def sensor_listener(self):
        """!
        Escucha del sensor de distancia que envia mensaje por telegram si
        alguien esta cerca de la puerta
        """
        while not self.shutdown_flag.is_set():
            if (self.dist_sensor.distance < 600):
                records = self.__conn.ejecutar_consulta(
                    """SELECT chat_id FROM alta_notificaciones where
                    proximidad is true""")
                self.led_status.blink(on_time=60, off_time=1, n=1)
                if records:
                    for chat_id in records:
                        self.tele_bot.send_message(chat_id, emojize("""
                        Alguien esta cerca de la puerta :puerta:
                        """, language='es'))

    def run(self):
        """!
        Ejecuta el escucha del sensor de distancia en un hilo de ejecución
        """
        self.sensor_listener()
