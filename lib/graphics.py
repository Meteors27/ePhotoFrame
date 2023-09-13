from lib.ePaper import EPaper


def displayBattery(batteryLevel, epd: EPaper):
    import framebuf

    def drawBatteryOutline():
        fbuf.rect(0, 0, 20 * ratio, 10 * ratio, EPaper.black, True)
        fbuf.rect(
            brush_size,
            brush_size,
            20 * ratio - brush_size * 2,
            10 * ratio - brush_size * 2,
            EPaper.white,
            True,
        )

    def drawBatteryLevel():
        fbuf.rect(
            brush_size * 2,
            brush_size * 2,
            int((20 * ratio - brush_size * 4) * batteryLevel),
            10 * ratio - brush_size * 4,
            EPaper.green
            if batteryLevel > 0.5
            else EPaper.orange
            if batteryLevel > 0.2
            else EPaper.red,
            True,
        )

    def drawBatteryCap():
        fbuf.rect(20 * ratio, 3 * ratio, 1 * ratio, 4 * ratio, EPaper.black, True)

    ratio = 10
    x_size = 21 * ratio
    y_size = 10 * ratio
    brush_size = 5
    fbuf = framebuf.FrameBuffer(
        bytearray(int(x_size * y_size / 2)),
        x_size,
        y_size,
        framebuf.GS4_HMSB,
    )

    fbuf.fill(EPaper.white)
    drawBatteryOutline()
    drawBatteryLevel()
    drawBatteryCap()

    epd.drawPixelStart()

    x_min = int((EPaper.width - x_size) / 2)  # 295
    x_max = int((EPaper.width + x_size) / 2)  # 505
    y_min = int((EPaper.height - y_size) / 2)  # 190
    y_max = int((EPaper.height + y_size) / 2)  # 290
    for y in range(EPaper.height):
        for x in range(EPaper.width):
            if x_min <= x < x_max and y_min <= y < y_max:
                epd.drawPixel(fbuf.pixel(x - x_min, y - y_min))
            else:
                epd.drawPixel(EPaper.white)
    epd.drawEnd()

    epd.sleep()


if __name__ == "__main__":
    epd = EPaper()
    epd.init()
    displayBattery(0.5, epd)
