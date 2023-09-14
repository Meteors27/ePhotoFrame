function upload() {
    const width = 800;
    const height = 480;
    const canvas = document.getElementById('resultCanvas');
    const ctx = canvas.getContext('2d');
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    var data = imageData.data;
    if (canvas.width < canvas.height) {
        const width = imageData.width;
        const height = imageData.height;

        // 创建一个新的数组来存储转置后的像素数据
        const transposedData = new Uint8ClampedArray(data.length);

        // 执行图像数据的转置
        for (let y = 0; y < height; y++) {
            for (let x = 0; x < width; x++) {
                const sourceIndex = (y * width + x) * 4;
                const targetIndex = (x * height + y) * 4;

                // 将像素数据复制到新数组中
                transposedData[targetIndex] = data[sourceIndex];
                transposedData[targetIndex + 1] = data[sourceIndex + 1];
                transposedData[targetIndex + 2] = data[sourceIndex + 2];
                transposedData[targetIndex + 3] = data[sourceIndex + 3];
            }
        }

        // 创建一个新的 ImageData 对象，将转置后的像素数据放入其中
        const transposedImageData = new ImageData(transposedData, height, width);
        data = transposedImageData.data;
    }
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
        if (Number(event.data) != NaN && Number(event.data) < height && Number(event.data) >= 0) {
            const slicedBuffer = buffer.slice(number * width / 2, (number + 1) * width / 2);
            socket.send(slicedBuffer);
            number++;

            percentage.innerHTML = (number / height * 100).toFixed(0) + '%';
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