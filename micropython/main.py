def connectWiFi(ssid: str, password: str):
    import network
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        print("connecting to network...")
        wlan.active(True)
        wlan.config(reconnects=5)
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            raise RuntimeError("Cannot connect to wifi")
    print("network config: ", wlan.ifconfig())

    
def createWiFi(ssid: str):
    import network
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, channel=11)
    ap.active(True)
    print(ap.ifconfig())


# connectWiFi("fastlab_ladder", "888888888")
createWiFi("william")

from microdot import Microdot

app = Microdot()

htmldoc = '''
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>选择、压缩和裁切照片</title>
  <link rel="stylesheet" href="https://unpkg.com/cropperjs/dist/cropper.min.css">
  <style>
    body {
      text-align: center;
    }
    input[type="file"] {
      display: none;
    }
    label {
      display: inline-block;
      padding: 10px 20px;
      background-color: #ccc;
      cursor: pointer;
    }
    #selected-image {
      max-width: 800px;
      max-height: 600px;
      margin-top: 20px;
    }
  </style>
</head>
<body>
  <h1>选择、压缩和裁切照片</h1>
  <input type="file" id="file-input" accept="image/*">
  <label for="file-input">选择照片</label>
  <img id="selected-image" src="#" alt="选择的照片">

  <script src="https://unpkg.com/compressorjs"></script>
  <script src="https://unpkg.com/cropperjs"></script>
  <script>
    document.getElementById('file-input').addEventListener('change', function (event) {
      var file = event.target.files[0];
      var image = document.getElementById('selected-image');

      var compressor = new Compressor(file, {
        quality: 0.8,
        maxWidth: 800,
        maxHeight: 600,
        success: function (compressedResult) {
          var cropper = new Cropper(image, {
            aspectRatio: 4 / 3,
            crop: function (event) {
              var canvas = cropper.getCroppedCanvas({
                width: 800,
                height: 600
              });
              image.src = canvas.toDataURL('image/jpeg');
            }
          });

          cropper.replace(compressedResult);
        }
      });
    });
  </script>
</body>
</html>
'''


@app.route('/')
def hello(request):
    return htmldoc, 200, {'Content-Type': 'text/html'}


@app.route('/shutdown')
def shutdown(request):
    request.app.shutdown()
    return 'The server is shutting down...'


app.run(debug=True)