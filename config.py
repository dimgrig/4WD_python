import os
from configparser import ConfigParser
import logging
import sys

from metaclasses import MetaSingleton

from descriptors import Discrete, NonBlank, Quantity

class Config(metaclass=MetaSingleton):

    port = NonBlank()

    def __init__(self):
        cfg = ConfigParser()
        cfg.read('config.ini')

        self._LOG = cfg.getint('log','LOG')
        level = cfg.get('log','LOG_level')
        if level == "DEBUG":
            self._LOG_LEVEL = logging.DEBUG
        elif level == "INFO":
            self._LOG_LEVEL = logging.INFO
        elif level == "WARNING":
            self._LOG_LEVEL = logging.WARNING
        elif level == "ERROR":
            self._LOG_LEVEL = logging.ERROR
        elif level == "CRITICAL":
            self._LOG_LEVEL = logging.CRITICAL
        else:
            self._LOG_LEVEL = logging.DEBUG
        std = cfg.getint('log', "STD")
        file = cfg.get('log', "FILE")

        self._OS = cfg.get('system','OS')
        self._NAME = cfg.get('system', 'NAME')


        self.log_init(level, std, file)

        if self._OS == "WIN":
            self.port = 'COM7' #"COM7"
        elif self._OS == "ASTRA" or self._OS == "UBUNTU":
            #sudo dmesg | grep tty
            #ls /dev/serial/by-id/
            sudo_password = '123'
            command = 'chmod 777 /dev/ttyUSB0'
            os.system('echo {}|sudo -S {}'.format(sudo_password, command))
            #self.port = "/dev/serial/by-id/usb-Silicon_Labs_CP2103_USB_to_UART_Bridge_Controller_IAB1306851-if00-port0"
            self.port = "/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0"
            #ln -s /dev/ttyUSB1 ~/.wine/dosdevices/com6


    def log_init(self, level, std, file):
        handlers = []
        if std:
            stdout_handler = logging.StreamHandler(sys.stdout)
            handlers.append(stdout_handler)
        if file:
            file_handler = logging.FileHandler(filename='logs.log')
            handlers.append(file_handler)
        logging.basicConfig(level=level, handlers=handlers, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(self._NAME)

