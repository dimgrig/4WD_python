# -*- coding: utf-8 -*-
import sys
sys.path.append('uis')
from PyQt5.QtCore import QTimer, QThread, QThreadPool, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QSlider

import zlib

from config import Config
from decorators import logged, timethis, timeblock
from functions import *
from joystick import Joystick
from serial_client import SerialClient, SerialHandler
from Thread import Thread


@logged
class Main(QMainWindow):

    def __init__(self):
        super().__init__()

        self.cfg = Config()

        # Create and set widget layout
        # Main widget container
        self.cw = QWidget()
        self.gl = QGridLayout()
        self.cw.setLayout(self.gl)
        self.setCentralWidget(self.cw)

        # Create joystick
        self.joystick = Joystick()
        self.hsl = QSlider(Qt.Horizontal)
        self.hsl.setMaximum(180)
        self.hsl.setMinimum(0)
        self.hsl.setValue(90)
        self.vsl = QSlider(Qt.Vertical)
        self.vsl.setMaximum(100)
        self.vsl.setMinimum(0)
        self.vsl.setValue(20)


        self.gl.addWidget(self.joystick, 0, 0)
        self.gl.addWidget(self.hsl, 1, 0)
        self.gl.addWidget(self.vsl, 0, 1)

        self.serial_client = SerialClient(self.cfg.port)
        self.readline = ""

        self.threadpool = QThreadPool()

        self.serial_cycle_finished = True
        self.serials_first_com_session = False
        self.serial_timer = QTimer()
        self.serial_timer.timeout.connect(self.serial_cycle_on_timer)
        self.serial_timer.start(200) #200


    def serial_cycle_on_timer(self):
        if self.serial_cycle_finished:
            self.serial_cycle_finished = False
            self.serial_thread = Thread(self.serial_cycle)
            self.serial_thread.signals.finished.connect(self.serial_cycle_on_finish)
            self.threadpool.start(self.serial_thread)

    def serial_cycle_on_finish(self):
        self.serial_cycle_finished = True
        self.serial_first_com_session = True

    def serial_cycle(self):
        self.logger.debug("serial_cycle - angle {} - radius {} - pan {} - tilt {}".format(self.joystick.angle,
          self.joystick.radius, self.hsl.value(), self.vsl.value()))

        #self.joystick.angle = 90
        #self.joystick.radius = 100

        message = '\x02' + int_to_ascii(self.joystick.angle) + int_to_ascii(self.joystick.radius)
        message += int_to_ascii(self.hsl.value())
        message += int_to_ascii(self.vsl.value())
        CRC = sum(bytes(message, "ascii"))
        self.logger.debug("CRC - {}".format(CRC))
        message_bytes = bytes(message, "ascii") + CRC.to_bytes(2, byteorder='big') + bytes('\x03', "ascii")
        self.logger.debug("transmitted message - {}".format(message_bytes))
        self.serial_client.ser.write(message_bytes)

        #\x02000000090020\x02M\x03
        #2000000090020223
        #crc
        #message = b'000000'
        #crc = '0x394605e6   960890342'n


        while self.serial_client.ser.inWaiting():
            for c in self.serial_client.ser.read():
                #print(chr(c))
                self.readline += chr(c)
                if chr(c) == '\x03':
                    try:
                        pass#self.logger.debug("Read: " + ''.join(self.readline))
                    except:
                        pass
                    if (self.readline[0] == '\x02'):
                        message = self.readline[:-1]
                        CRC = sum(bytes(message[:-2], "ascii"))
                        self.logger.debug(CRC.to_bytes(2, byteorder='big'), message[-2:].encode('latin-1'))
                        if (CRC.to_bytes(2, byteorder='big')) == message[-2:].encode('latin-1'):
                            self.logger.info("Received:  Distance={}\tX={}\tY={}\tL={}\tFB_PWM={}\t"
                                              "TURN_PWM={}\tFR_RPM={}\tFL_RPM={}".format(
                                message[1:4], message[4:7], message[7:10], message[10:13],
                                message[13:16], message[16:19], message[19:22], message[22:25]
                            ))
                        else:
                            self.logger.debug("Wrong CRC")
                    else:
                        self.logger.debug("Wrong message")

                    self.readline = ""
                    break

def main():
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())

main()

