import sys

sys.path.append("..")
from lib.microdot import Microdot

app = Microdot()


@app.route("/")
def index(request):
    return "Hello, world!"


@app.route("/upload", methods=["POST"])
def upload(request):
    pass


app.run(port=8080)
