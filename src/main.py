import machine, os, time
from lib.microdot_asyncio import Microdot, send_file
from lib.microdot_asyncio_websocket import with_websocket
from lib.ePaper import EPaper
from lib.INA219 import *  # XXX
from lib.graphics import *


def batteryCheckCallback(t):
    u, i, p = batteryCheck()
    if p < 20:
        displayBattery(p / 100, epd)


def wifiInit(essid="ePaper", password="88888888"):
    import network

    wlan = network.WLAN(network.AP_IF)
    wlan.config(essid=essid, password=password)
    wlan.active(True)
    print("WiFi AP started")


app = Microdot()


@app.route("/")
def index(request):
    return send_file("index.html")


@app.route("/dither.js")
def dither(request):
    return send_file("dither.js")


@app.route("/upload.js")
def upload(request):
    return send_file("upload.js")


@app.route("/script.js")
def script(request):
    return send_file("script.js")


@app.route("/croppie.min.js")
def croppie(request):
    return send_file("croppie.min.js")


@app.route("/jquery.min.js")
def jquery(request):
    return send_file("jquery.min.js")


@app.route("/normalize.min.css")
def normalize(request):
    return send_file("normalize.min.css")


@app.route("/style.css")
def style(request):
    return send_file("style.css")


@app.route("/upload.png")
def uploadpng(request):
    return send_file("upload.png")


@app.route("/multiply.png")
def multiplypng(request):
    return send_file("multiply.png")


@app.route("/battery")
def battery(request):
    u, i, p = batteryCheck()
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    </head>
    <body>
    <h3>voltage: {u} V</h3>
    <h3>current: {i} A</h3>
    <h3>percentage: {p} %</h3>
    </body>
    </html>
    """


@app.route("/echo")
@with_websocket
async def echo(request, ws):
    ePaper.sendCommand(0x10)
    await ws.send("ready")
    for i in range(ePaper.height):
        await ws.send(str(i))
        data = await ws.receive()
        print(f"{i+1}/{ePaper.height}")
        ePaper.sendData(data)
    # close connection
    await ws.send("done")
    await ws.close()
    ePaper.display()
    ePaper.sleep()
    machine.deepsleep()


if __name__ == "__main__":
    machine.freq(240_000_000)
    ePaper = EPaper()
    ePaper.init()
    tim = machine.Timer()
    tim.init(
        period=6000_00, mode=machine.Timer.PERIODIC, callback=batteryCheckCallback
    )  # every 10 minutes run a battery voltage check
    wifiInit()
    app.run(port=80, debug=True)
