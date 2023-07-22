from machine import Pin, SPI
import time

# BUSY.value()
# hspi.write(b'\x04')
# DC.value(0)
class EPaper:
    def __init__(self):
        self.BUSY = Pin(40,Pin.IN,Pin.PULL_UP)
        self.RST = Pin(42,Pin.OUT,value=1) # FIXME
        self.DC = Pin(38,Pin.OUT)
        self.CS = Pin(39,Pin.OUT,value=0)
        self.HSPI = SPI(2, baudrate=80_000_000, sck=Pin(35), mosi=Pin(36), miso=Pin(37))
        # self.HSPI = SPI(1, 1000000, sck=Pin(14), mosi=Pin(13), miso=Pin(12))# , phase=1, polarity=1)
        # self.HSPI = SPI(2, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
        self.height = 480
        self.width = 800
    
    def sendCommand(self, cmd):
        self.DC.value(0)
        # print("sending command: ", bytearray(cmd))
        self.HSPI.write(bytearray(cmd))
        
    def sendData(self, data):
        self.DC.value(1)
        # print("sending data: ", bytearray(data))
        self.HSPI.write(bytearray(data))
        
    def wait(self):
        print("ePaper is busy, please waiting...")
        while(self.BUSY.value() == 0):
            time.sleep_ms(5)
        print("ePaper is available")
        
    def on(self):
        self.sendCommand(b'\x04')
        self.wait()
        self.sendCommand(b'\x12')
        self.sendData(b'\x00')
        self.wait()
        self.sendCommand(b'\x02')
        self.sendData(b'\x00')
        self.wait()
    
    def init(self):
        self.sendCommand(b'\xAA')
        self.sendData(b'\x49\x55\x20\x08\x09\x18')
        self.sendCommand(b'\x01')
        self.sendData(b'\x3F\x00\x32\x2A\x0E\x2A')
        self.sendCommand(b'\x00')
        self.sendData(b'\x5F\x69')
        self.sendCommand(b'\x03')
        self.sendData(b'\x00\x54\x00\x44')
        self.sendCommand(b'\x05')
        self.sendData(b'\x40\x1F\x1F\x2C')
        self.sendCommand(b'\x06')
        self.sendData(b'\x6F\x1F\x1F\x22')
        self.sendCommand(b'\x08')
        self.sendData(b'\x6F\x1F\x1F\x22')
        self.sendCommand(b'\x13')
        self.sendData(b'\x00\x04')
        self.sendCommand(b'\x30')
        self.sendData(b'\x3C')
        self.sendCommand(b'\x41')
        self.sendData(b'\x00')
        self.sendCommand(b'\x50')
        self.sendData(b'\x3F')
        self.sendCommand(b'\x60')
        self.sendData(b'\x02\x00')
        self.sendCommand(b'\x61')
        self.sendData(b'\x03\x20\x01\xE0')
        self.sendCommand(b'\x82')
        self.sendData(b'\x1E')
        self.sendCommand(b'\x84')
        self.sendData(b'\x00')
        self.sendCommand(b'\x86')
        self.sendData(b'\x00')
        self.sendCommand(b'\xE3')
        self.sendData(b'\x2F')
        self.sendCommand(b'\xE0')
        self.sendData(b'\x00')
        self.sendCommand(b'\xE6')
        self.sendData(b'\x00')
        
    def clear(self, color=b'\x44'):
        print("clearing...")
        
        # add
        self.on()
        
        self.sendCommand(b'\x10')
        for i in range(int(self.height) * int(self.width/2)):
            self.sendData(color)
        self.on()
        print("clearing done.")
        
        
ePaper = EPaper()
ePaper.init()
ePaper.clear()




