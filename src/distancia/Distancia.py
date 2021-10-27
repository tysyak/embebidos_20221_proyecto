#!/usr/bin/env python3
from emoji import emojize
from time import sleep
from signal import pause
from threading import Thread


class Distancia(Thread):
    def __init__(self, dist_sensor, led_status, tele_bot, database, shutdown_flag):
        Thread.__init__(self)
        self.shutdown_flag = shutdown_flag

        self.dist_sensor = dist_sensor
        self.led_status = led_status
        self.tele_bot = tele_bot
        self.__conn = database

    def sensor_listener(self):
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
        self.sensor_listener()
