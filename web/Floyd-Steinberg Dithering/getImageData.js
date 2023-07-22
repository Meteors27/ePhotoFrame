// 加载图像到Canvas并获取像素数据
function getImageDataAsArray(imageElement) {
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');

    canvas.width = imageElement.width;
    canvas.height = imageElement.height;
    ctx.drawImage(imageElement, 0, 0);

    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const pixelArray = imageDataTo2DArray(imageData);

    return pixelArray;
}

// 将ImageData转换为二维数组
function imageDataTo2DArray(imageData) {
    const width = imageData.width;
    const height = imageData.height;
    const data = imageData.data;

    const pixelArray = [];
    for (let y = 0; y < height; y++) {
        const row = [];
        for (let x = 0; x < width; x++) {
            const index = (y * width + x) * 4;
            const red = data[index];
            const green = data[index + 1];
            const blue = data[index + 2];
            const alpha = data[index + 3];
            row.push([red, green, blue, alpha]);
        }
        pixelArray.push(row);
    }

    return pixelArray;
}

// 获取图像元素
// const imageElement = document.getElementById('imageElement');

// // 图像加载完成后获取数据并进行处理
// imageElement.onload = function () {
//     const pixelArray = getImageDataAsArray(imageElement);
//     console.log(pixelArray);

//     // 在这里可以对像素数据进行进一步处理
// };