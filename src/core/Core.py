#!/usr/bin/env python3

import time
import telebot
import os
from signal import pause
from gpiozero import Servo, LED, DistanceSensor, LightSensor
from pyfingerprint.pyfingerprint import PyFingerprint
from gas.Gas import Gas
from threading import Thread
from time import sleep
from core.BD import BD

class Core:
    def __init__(self):
        self.status_led_ok = LED(3)
        self.status_led_error = LED(4)
        self.led_gen_status = LED(2)
        self.servo_motor = Servo(17)
        self.servo_motor.min()
        self.gas_sensor = LightSensor(21)
        self.__key_api_telegram = os.getenv("TELEGRAM_API")
        self.tele_bot = telebot.TeleBot(self.__key_api_telegram)
        self.bd = BD()
        self.mod_gas = Gas(self.gas_sensor, self.led_gen_status, self.tele_bot, self.bd)

    def telebot_msg_handler(self):
        bot = self.tele_bot

        @bot.message_handler(commands=['abrir'])
        def abrir(message):
            self.abrir_cerradura()
            msg = "Abierto"
            bot.reply_to(message, msg)

        @bot.message_handler(commands=['cerrar'])
        def cerrar(message):
            self.cerrar_cerradura()
            msg = "Cerrado"
            bot.reply_to(message, msg)

        @bot.message_handler(func=lambda message: True)
        def echo_message(message):
            bot.reply_to(message, "Tu chat id es:" + message.chat.id) # Valor del comando por defecto
            sleep(1)
            bot.reply_to(message, message.chat.id)


        bot.infinity_polling()

    def start(self):
        Thread(target=self.mod_gas.sensor_listener).start()
        self.cerrar_cerradura()
        self.status_led_ok.blink(on_time=0.5,off_time=3,)
        self.telebot_msg_handler()

    def abrir_cerradura(self):
        self.servo_motor.max()

    def cerrar_cerradura(self):
        self.servo_motor.min()
