import machine
from ePaper import EPaper


class ColorBlock(object):
    def __init__(self, color=0x00, width=0, height=0):
        self.color = color
        self.width = width
        self.height = height
        self.h = 0
        self.w = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.h < self.height:
            if self.w < self.width:
                self.w += 1
                return self.color
            else:
                self.h += 1
                self.w = 0
                return self.color
        else:
            raise StopIteration


# from BMPReader import BMPReader
if __name__ == "__main__":
    machine.freq(240_000_000)
    # img = BMPReader("image.bmp")

    ePaper = EPaper()
    ePaper.init()
    ePaper.sendCommand(0x10)
    # ePaper.clear(color=0x44)
    lst = [0x44, 0x22, 0x33, 0x55]
    for i in range(480):
        for color in lst:
            for j in range(200 // 2):
                ePaper.sendData(color)

    ePaper.display()

    # ePaper.draw(img)
    ePaper.sleep()
