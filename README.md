# image smart crop(图片智能裁剪)  

## description

Smart crops images uisng OpenCV, forked from `epixelic/python-smart-crop`, and improve more

Uses the algorithms described in https://github.com/thumbor/thumbor/wiki/Detection-algorithms but actually combining both methods. We try to detect faces on the image, then, in any case we detect features. We then combine both results with different weights, so face detection is, in this case 3,33 times stronger than feature detection.

## Installing

Requires python-opencv, install the dependency with `pip install python-opencv`

Install the command using PIP: `pip install git+https://github.com/fizzday/imageCropSmart`

Tested on Debian 8 and Ubuntu WSL and mac 10.13.1

Usage: `smartcrop -W 640 -H 360 -i input.jpg -o output.jpg`

See `smartcrop --help`  

Any Case : you can run the code in `./smartcrop/_init_.py`

## example code  
```python
import smartcrop

img_input = "input.jpg"
img_output = "output.jpg"
img_width = 400
img_height = 300

smartcrop.smart_crop(img_input, img_width, img_height, img_output, None)
```

## example1
- input.jpg  
    ![input.jpg](https://raw.githubusercontent.com/fizzday/imageCropSmart/master/smartcrop/input.jpg)  
    - crop  
    ```
    smartcrop -W 400 -H 300 -i input.jpg -o output.jpg
    ```
    ![output.jpg](https://raw.githubusercontent.com/fizzday/imageCropSmart/master/smartcrop/output.jpg)  
    
## example2
- input2.jpg  
    ![input2.jpg](https://raw.githubusercontent.com/fizzday/imageCropSmart/master/smartcrop/input2.jpg)  
    ```
    smartcrop -W 400 -H 300 -i input2.jpg -o output2.jpg
    ```
    ![output2.jpg](https://raw.githubusercontent.com/fizzday/imageCropSmart/master/smartcrop/output2.jpg) 
