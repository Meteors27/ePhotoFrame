from lib.microdot_asyncio import Microdot, send_file
from lib.microdot_asyncio_websocket import with_websocket
import machine, os, time
from lib.ePaper import EPaper


def wifiInit(essid="ePaper", password="88888888"):
    import network

    wlan = network.WLAN(network.AP_IF)
    wlan.config(essid=essid, password=password)
    wlan.active(True)
    print("WiFi AP started")


app = Microdot()
machine.freq(240_000_000)
ePaper = EPaper()
ePaper.init()
wifiInit()


@app.route("/")
def index(request):
    return send_file("ditherExample.html")


@app.route("/dither.js")
def dither(request):
    return send_file("dither.js")


@app.route("/upload.js")
def getImageData(request):
    return send_file("upload.js")


@app.route("/echo")
@with_websocket
async def echo(request, ws):
    ePaper.sendCommand(0x10)
    await ws.send("ready")
    for i in range(ePaper.height):
        await ws.send(str(i))
        data = await ws.receive()
        print(f"{i}/{ePaper.height}")
        ePaper.sendData(data)
    # close connection
    await ws.send("done")
    await ws.close()
    ePaper.display()


app.run(port=8080)
