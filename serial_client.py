import asyncio
import serial
import serial_asyncio
import sys

from decorators import logged, timethis

@logged
class SerialHandler(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        self.logger.debug(transport)
        self.transport.serial.rts = False  # You can manipulate Serial object via transport
        transport.write(b'Hello, World!\n')  # Write serial data via transport

    def data_received(self, data):
        self.logger.info(repr(data))
        #print('data received', repr(data))
        #if b'\n' in data:
        #    self.transport.close()

    def connection_lost(self, exc):
        self.logger.debug("port closed")
        #print('port closed')
        self.transport.loop.stop()

    def pause_writing(self):
        self.logger.debug("pause writing")
        #print('pause writing')
        print(self.transport.get_write_buffer_size())

    def resume_writing(self):
        print(self.transport.get_write_buffer_size())
        #print('resume writing')
        self.logger.debug("resume writing")

    async def write(self, data):
        data = '\\x02' + data
        self.transport.write(data)


@logged
class SerialClient():
    def __init__(self, port):
        self.port = port
        self.connection = 0

        self.rr = []
        self.rr_ = []
        self.rg = []
        self.wr_reg = []

        self.read_from = 0

        self.sleep_time = 0.01
        self.async_timeout = 0.25

        import serial

        # configure the serial connections (the parameters differs on the device you are connecting to)
        self.ser = serial.Serial(
            port=self.port,
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )

        #self.ser.write(b"hello world\n")


        #loop = asyncio.get_event_loop()
        #r, w = serial_asyncio.open_serial_connection(loop, self.port, baudrate=115200)

        #loop.run_until_complete(coro)
        #loop.run_forever()
        #loop.close()

