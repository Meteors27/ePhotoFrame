function upload() {
    const canvas = document.getElementById('resultCanvas');
    const ctx = canvas.getContext('2d');
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const data = imageData.data;
    const buffer = dataToBuffer(data);

    const loader = document.getElementById('loader');
    const percentage = document.getElementById('percentage');
    const uploadButton = document.getElementById('uploadButton');

    const socket = new WebSocket('ws://' + location.host + '/echo');

    socket.onopen = function () {
        console.log('WebSocket open');
        loader.style.opacity = 1;
        percentage.style.opacity = 1;
        uploadButton.disabled = true;
        uploadButton.style.backgroundColor = "#aaaaaa";


    };
    socket.onclose = function () {
        console.log('WebSocket close');
    };
    socket.onmessage = function (event) {
        console.log('WebSocket message: ', event.data);
        // if event.data is a number, then it is the number of the slice
        if (Number(event.data) != NaN && Number(event.data) < canvas.height && Number(event.data) >= 0) {
            const slicedBuffer = buffer.slice(number * canvas.width / 2, (number + 1) * canvas.width / 2);
            socket.send(slicedBuffer);
            number++;

            percentage.innerHTML = (number / canvas.height * 100).toFixed(0) + '%';
        }
    };
    let number = 0;

    ////


}





function rbgToByte(r, g, b) {
    const colorMap = {
        "000000": 0b000,
        "ffffff": 0b001,
        "00ff00": 0b010,
        "0000ff": 0b011,
        "ff0000": 0b100,
        "ffff00": 0b101,
        "ff7d00": 0b110,
    };
    function rgbToHex(r, g, b) {
        return ((r << 16) | (g << 8) | b).toString(16).padStart(6, "0");
    }
    const hex = rgbToHex(r, g, b);
    return colorMap[hex];
}

function dataToBuffer(data) {
    let buffer = new ArrayBuffer(data.length / 8); // 4 elements for each pixel, 2 pixels per byte
    let view = new Uint8Array(buffer);
    for (var i = 0; i < data.length / 8; ++i) {
        view[i] = rbgToByte(data[i * 8], data[i * 8 + 1], data[i * 8 + 2]) << 4 | rbgToByte(data[i * 8 + 4], data[i * 8 + 5], data[i * 8 + 6]);
    }
    return buffer;
}