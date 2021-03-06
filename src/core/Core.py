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
from lector_huella.Lector import Lector
from threading import Thread
from time import sleep
from core.BD import BD
from core.Assistant import main as ass_main
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
        """!
        Esta clase sirve como compositor e iniciador de cada sensor, inicia y
        decara los componestes que se usará para el embebido.
        """
        Thread.__init__(self)
        self.shutdown_flag = Event()
        self.bd = BlueDot()
        self.status_led_ok = LED(3,active_high=False) # verde
        self.status_led_error = LED(4,active_high=False) # rojo
        self.led_gen_status = LED(2,active_high=False) # azul
        self.servo_motor = Servo(17)
        self.servo_motor.min()
        self.gas_sensor = LightSensor(21)
        self.interruptor_metal = Button(19)
        self.interruptor_plastico = Button(13)
        self.distancia_sensor = DistanceSensor(echo=20, trigger=26)
        # self.asistente = Asistente(self.interruptor_metal)
        self.__key_api_telegram = os.getenv("TELEGRAM_API")
        self.bluetooth = Bluetooth(self.bd, self.servo_motor)
        self.tele_bot = telebot.TeleBot(self.__key_api_telegram)
        self.bd = BD()
        self.lector = Lector(self.status_led_error, self.status_led_ok,
                             self.tele_bot, self.servo_motor, '/dev/ttyUSB0')
        self.mod_gas = Gas(self.gas_sensor, self.led_gen_status, self.tele_bot,
                           self.bd, self.shutdown_flag)


    def telebot_msg_handler(self):
        """!
        Este método es el encargado de enviar y recibir mensajes del bot de telegram
        """
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
        """!
        Aquí se llaman y se ejecuta en cada hilo los procesos de cada sensor
        """
        self.led_gen_status.blink(on_time=1, off_time=5)
        self.mod_gas.start()
        print("\033[32mIniciando Modulo de Bluetooth\033[0m")
        self.bluetooth.start()
        self.abrir_cerradura()
        print("\033[32mIniciando Asistente\033[0m")
        # self.asistente.start()
        Thread(target=ass_main, args=(self.interruptor_metal,)).start()
        Thread(target=self.cerradura).start()
        print("\033[32mIniciando Lector de huella\033[0m")
        self.lector.start()
        print("\033[32mIniciando Modulo de Telegram\033[0m")
        self.telebot_msg_handler()


    def abrir_cerradura(self):
        """!
        Abre la cerradura
        """
        self.servo_motor.max()

    def cerrar_cerradura(self):
        """!
        Cierra la cerradura
        """
        self.servo_motor.min()

    def cambiar_edo(self):
        """!
        Cierra o abre la serradura segun su estado actual
        """
        if self.servo_motor.value == -1.0:
            self.abrir_cerradura()
        else:
            self.cerrar_cerradura()

    def cerradura(self):
        """!
        Escucha del interruptor para cambiar el estado de la cerradura
        """
        while True:
            if self.interruptor_plastico.is_pressed:
                print("Cambia")
                self.cambiar_edo()
                self.interruptor_plastico.wait_for_release()
