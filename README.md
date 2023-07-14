# ePhotoFrame
> A smart photo frame project for embedded system course
## 简介
ESP32提供WiFi，用户接入后通过浏览器访问ESP32的网页服务器(`192.168.1.1`)， 上传图片, ESP32将图片保存在SD卡中，然后通过显示屏显示图片。用户可以通过网页服务器上传图片，删除图片，设置显示模式，设置显示时间间隔，设置显示顺序等。

## 网页前端需求
首先在`/upload`页面下实现图片的上传。页面参考[`codepen`](https://codepen.io/chonin/pen/gZwgaj)，但是需要修改以下部分：
- 由于墨水屏是800px*480px，所以要将呈现的图片大小从demo中的1:1改成3:5，并且要提供一个方式让用户选择横竖
- 需要在手机本地进行图片的resize，变成800px*480px
- 通过后端接口然后再上传到ESP32（接口我还没想好！）
- 进阶需求（还不是很明确）：将图片以bmp格式发送至后端；通过Floyd-Steinberg抖动算法对图片进行预处理

### 可以参考的前端设计网站
- [codepen](https://codepen.io/)
- [uiverse](https://uiverse.io/)