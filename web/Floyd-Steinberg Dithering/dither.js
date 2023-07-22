const colorPalette = [
    [0, 0, 0],       // Black
    [255, 255, 255], // White
    [255, 0, 0],     // Red
    [0, 255, 0],     // Green
    [0, 0, 255],     // Blue
    [255, 255, 0],   // Yellow
    [255, 125, 0]    // Orange
];

// 弗洛伊德-斯坦伯格抖动算法
function floydSteinbergDithering(imageData) {
    const width = imageData.width;
    const height = imageData.height;
    const data = imageData.data;

    for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
            const index = (y * width + x) * 4;

            // 获取最近的颜色
            const oldR = data[index];
            const oldG = data[index + 1];
            const oldB = data[index + 2];
            const nearestColor = getNearestColor([oldR, oldG, oldB]);

            // 设置像素颜色
            data[index] = nearestColor[0];
            data[index + 1] = nearestColor[1];
            data[index + 2] = nearestColor[2];

            // 计算误差并传播到相邻像素
            const errR = oldR - nearestColor[0];
            const errG = oldG - nearestColor[1];
            const errB = oldB - nearestColor[2];

            distributeError(data, width, height, x, y, errR, errG, errB);
        }
    }
}

// 获取最近的颜色
function getNearestColor(rgb) {
    let minDist = Number.MAX_VALUE;
    let nearestColor = colorPalette[0];

    for (const color of colorPalette) {
        const dist = colorDistanceSquared(rgb, color);
        if (dist < minDist) {
            minDist = dist;
            nearestColor = color;
        }
    }

    return nearestColor;
}

// 计算颜色距离的平方
function colorDistanceSquared(color1, color2) {
    const dR = color1[0] - color2[0];
    const dG = color1[1] - color2[1];
    const dB = color1[2] - color2[2];
    return dR * dR + dG * dG + dB * dB;
}

// 传播误差
function distributeError(data, width, height, x, y, errR, errG, errB) {
    const offsets = [
        { x: 1, y: 0, weight: 7 / 16 },
        { x: -1, y: 1, weight: 3 / 16 },
        { x: 0, y: 1, weight: 5 / 16 },
        { x: 1, y: 1, weight: 1 / 16 }
    ];

    for (const offset of offsets) {
        const newX = x + offset.x;
        const newY = y + offset.y;

        if (newX >= 0 && newX < width && newY >= 0 && newY < height) {
            const index = (newY * width + newX) * 4;

            data[index] += errR * offset.weight;
            data[index + 1] += errG * offset.weight;
            data[index + 2] += errB * offset.weight;
        }
    }
}

// 加载图像并应用抖动算法
function loadAndApplyDithering(imageURL) {
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');

    const img = new Image();
    img.crossOrigin = 'anonymous';
    img.onload = function () {
        canvas.width = img.width;
        canvas.height = img.height;
        ctx.drawImage(img, 0, 0);

        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        floydSteinbergDithering(imageData);
        ctx.putImageData(imageData, 0, 0);
    };
    img.src = imageURL;
}