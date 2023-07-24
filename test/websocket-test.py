import time
from microdot_asyncio import Microdot, send_file
from microdot_asyncio_websocket import with_websocket
import os

os.chdir("../web/Floyd-Steinberg-Dithering")

app = Microdot()


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
    # TODO:  send draw command to ePaper
    await ws.send("ready")
    for i in range(480):  # TODO: change 480 in the future
        await ws.send(str(i))
        data = await ws.receive()
        print(data)
        time.sleep(0.01)
        # TODO: send data to ePaper

    # close connection
    await ws.send("done")
    await ws.close()


app.run(port=8080)
