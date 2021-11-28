#!/usr/bin/env python3

import os
import time
import click
import telebot
from threading import Thread, Event
from signal import pause
from bluedot import BlueDot
from gpiozero import Servo, LED, DistanceSensor, LightSensor, Button
from pyfingerprint.pyfingerprint import PyFingerprint
from gas.Gas import Gas
from bluetooth.Bluetooth import Bluetooth
from threading import Thread
from time import sleep
from core.BD import BD
from core.Assistant import Asistente
from google.assistant.embedded.v1alpha2 import (
    embedded_assistant_pb2,
    embedded_assistant_pb2_grpc
)
try:
    from . import (
        assistant_helpers,
        audio_helpers,
        browser_helpers,
        device_helpers
    )
except (SystemError, ImportError):
    import assistant_helpers
    import audio_helpers
    import browser_helpers
    import device_helpers


ASSISTANT_API_ENDPOINT = 'embeddedassistant.googleapis.com'
END_OF_UTTERANCE = embedded_assistant_pb2.AssistResponse.END_OF_UTTERANCE
DIALOG_FOLLOW_ON = embedded_assistant_pb2.DialogStateOut.DIALOG_FOLLOW_ON
CLOSE_MICROPHONE = embedded_assistant_pb2.DialogStateOut.CLOSE_MICROPHONE
PLAYING = embedded_assistant_pb2.ScreenOutConfig.PLAYING
DEFAULT_GRPC_DEADLINE = 60 * 3 + 5

class Core(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.shutdown_flag = Event()
        self.bd = BlueDot()
        self.status_led_ok = LED(3)
        self.status_led_error = LED(4)
        self.led_gen_status = LED(2)
        self.servo_motor = Servo(17)
        self.servo_motor.min()
        self.gas_sensor = LightSensor(21)
        self.interruptor = Button(14)
        self.distancia_sensor = DistanceSensor(echo=20, trigger=16)
        self.__key_api_telegram = os.getenv("TELEGRAM_API")
        self.bluetooth = Bluetooth(self.bd, self.servo_motor)
        self.tele_bot = telebot.TeleBot(self.__key_api_telegram)
        self.bd = BD()
        self.mod_gas = Gas(self.gas_sensor, self.led_gen_status, self.tele_bot,
                           self.bd, self.shutdown_flag)


    def telebot_msg_handler(self):
        bot = self.tele_bot

        @bot.message_handler(commands=['abrir'])
        def abrir(message):
            print("Abrir con cliente Telegram")
            self.abrir_cerradura()
            msg = "Abierto"
            bot.reply_to(message, msg)

        @bot.message_handler(commands=['cerrar'])
        def cerrar(message):
            print("Cerrar con cliente Telegram")
            self.cerrar_cerradura()
            msg = "Cerrado"
            bot.reply_to(message, msg)

        @bot.message_handler(func=lambda message: True)
        def echo_message(message):
            print("Enviando datos del chat id...")
            bot.reply_to(message, "Tu chat id es:")
            sleep(1)
            bot.reply_to(message, message.chat.id)

        bot.infinity_polling()

    def run(self):
        self.mod_gas.start()
        print("Iniciando Modulo de Bluetooth")
        self.bluetooth.start()
        self.abrir_cerradura()
        # self.asistente()
        print("Iniciando Modulo de Telegram")
        self.telebot_msg_handler()
        self.status_led_ok.blink(on_time=0.5, off_time=5)

    def abrir_cerradura(self):
        self.servo_motor.max()

    def cerrar_cerradura(self):
        self.servo_motor.min()
