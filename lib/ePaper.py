from math import e
from machine import SPI, Pin
import time, machine


class EPaper(object):
    def __init__(
        self, busy=12, rst=13, dc=14, cs=15, sck=10, mosi=11, baudrate=8_000_000
    ):
        self.busy = Pin(busy, Pin.IN)
        self.rst = Pin(rst, Pin.OUT, value=1)
        self.dc = Pin(dc, Pin.OUT)
        self.cs = Pin(cs, Pin.OUT, value=1)
        self.spi = SPI(
            1,
            baudrate=baudrate,
            polarity=0,
            phase=0,
            sck=Pin(sck),
            mosi=Pin(mosi),
        )
        self.height = 480
        self.width = 800
        print(
            f"EPaper Info: \n\tbusy: {self.busy}, \n\trst: {self.rst}, \n\tdc: {self.dc}, \n\tcs: {self.cs}, \n\tspi: {self.spi}"
        )

    def sendCommand(self, cmd):
        self.dc.low()
        self.cs.low()
        if isinstance(cmd, int):
            cmd = bytearray([cmd])
        self.spi.write(bytearray(cmd))
        self.cs.high()

    def sendData(self, data):
        self.dc.high()
        self.cs.low()
        if isinstance(data, int):
            data = bytearray([data])
        self.spi.write(bytearray(data))
        self.cs.high()

    def wait(self):
        # print("ePaper is busy, please wait...")
        while self.busy.value() == 0:
            time.sleep_ms(1)
        # print("ePaper is available")

    def display(self):
        print("Displaying...")
        # power on
        self.sendCommand(0x04)
        self.wait()
        # display refresh
        self.sendCommand(0x12)
        self.sendData(0x00)  # FIXME
        self.wait()
        # power off
        self.sendCommand(0x02)
        self.sendData(0x00)
        self.wait()

    def reset(self):
        self.rst.high()
        time.sleep_ms(20)
        self.rst.low()
        time.sleep_ms(2)
        self.rst.high()
        time.sleep_ms(20)
        print("Reset successfully.")

    def init(self):
        self.reset()
        self.wait()
        time.sleep_ms(30)
        self.sendCommand(0xAA)  # CMDH
        self.sendData(0x49)
        self.sendData(0x55)
        self.sendData(0x20)
        self.sendData(0x08)
        self.sendData(0x09)
        self.sendData(0x18)
        self.sendCommand(0x01)
        self.sendData(0x3F)
        self.sendData(0x00)
        self.sendData(0x32)
        self.sendData(0x2A)
        self.sendData(0x0E)
        self.sendData(0x2A)
        self.sendCommand(0x00)
        self.sendData(0x5F)
        self.sendData(0x69)
        self.sendCommand(0x03)
        self.sendData(0x00)
        self.sendData(0x54)
        self.sendData(0x00)
        self.sendData(0x44)
        self.sendCommand(0x05)
        self.sendData(0x40)
        self.sendData(0x1F)
        self.sendData(0x1F)
        self.sendData(0x2C)
        self.sendCommand(0x06)
        self.sendData(0x6F)
        self.sendData(0x1F)
        self.sendData(0x1F)
        self.sendData(0x22)
        self.sendCommand(0x08)
        self.sendData(0x6F)
        self.sendData(0x1F)
        self.sendData(0x1F)
        self.sendData(0x22)
        self.sendCommand(0x13)  # IPC
        self.sendData(0x00)
        self.sendData(0x04)
        self.sendCommand(0x30)
        self.sendData(0x3C)
        self.sendCommand(0x41)  # TSE
        self.sendData(0x00)
        self.sendCommand(0x50)
        self.sendData(0x3F)
        self.sendCommand(0x60)
        self.sendData(0x02)
        self.sendData(0x00)
        self.sendCommand(0x61)
        self.sendData(0x03)
        self.sendData(0x20)
        self.sendData(0x01)
        self.sendData(0xE0)
        self.sendCommand(0x82)
        self.sendData(0x1E)
        self.sendCommand(0x84)
        self.sendData(0x00)
        self.sendCommand(0x86)  # AGID
        self.sendData(0x00)
        self.sendCommand(0xE3)
        self.sendData(0x2F)
        self.sendCommand(0xE0)  # CCSET
        self.sendData(0x00)
        self.sendCommand(0xE6)  # TSSET
        self.sendData(0x00)
        print("Init successfully.")

    def clear(self, color=0x11):
        self.sendCommand(0x10)
        # self.dc.high()
        # self.cs.low()
        for i in range(int(self.height) * int(self.width / 2)):
            # self.spi.write(bytearray([color]))
            self.sendData(color)
            # self.spi.write(b"\x44")
        # self.cs.high()

        self.display()
        print("Clear successfully.")

    def sleep(self):
        self.sendCommand(0x07)
        self.sendData(0xA5)
        time.sleep_ms(100)
        self.rst.low()
        self.cs.low()
        self.dc.low()
        print("Enter sleep")

    # def draw(self, image, hStart=0, wStart=0, width=800, height=480):
    #     self.sendCommand(0x10)
    #     for h in range(height):
    #         for w in range(int(width / 2)):
    #             if (
    #                 hStart <= h < hStart + height
    #                 and wStart / 2 <= w < (wStart + width) / 2
    #             ):
    #                 self.__sendDataArray(image[h])
    #             else:
    #                 self.sendData(0x11)
    #     self.display()


if __name__ == "__main__":
    ePaper = EPaper()
    ePaper.init()
    ePaper.clear()
    ePaper.sleep()
