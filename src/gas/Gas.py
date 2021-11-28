#!/usr/bin/env python3

from emoji import emojize
from time import sleep
from signal import pause
from threading import Thread

class Gas(Thread):
    def __init__(self, gas_sensor, led_status, tele_bot, database, shutdown_flag):
        Thread.__init__(self)
        self.shutdown_flag = shutdown_flag

        self.gas_sensor = gas_sensor
        self.led_status = led_status
        self.tele_bot = tele_bot
        self.__conn = database

    def sensor_listener(self):
        while not self.shutdown_flag.is_set():
            if (self.gas_sensor == 0.0):
                records = self.__conn.ejecutar_consulta(
                    """SELECT chat_id FROM alta_notificaciones where
                    humo is true""")
                self.led_status.blink(on_time=0.1,off_time=0.1,n=700)
                if records:
                    for chat_id in records:
                        self.tele_bot.send_message(chat_id, emojize("""
                        Se detecta humo o gas cerca de tu puerta :fuego:
                        """, language='es'))

    def run(self):
        self.sensor_listener()
