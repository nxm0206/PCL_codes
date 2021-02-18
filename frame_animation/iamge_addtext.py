import numpy as np
import cv2

filename='D:/measurement_data/20201111/infrared_camera/top_left_1024/1530.bmp'
img = cv2.imread(filename)

height, width, layers = img.shape
print(height, width)

font = cv2.FONT_HERSHEY_PLAIN
bottomLeftCornerOfText = (100,220)
fontScale = 1
fontColor = (10, 100, 10)
lineType = 1

cv2.putText(img, 'wavelength = '+filename[59:63]+' nm',
    bottomLeftCornerOfText,
    font,
    fontScale,
    fontColor,
    lineType)

#Display the image
cv2.imshow("img", img)
cv2.waitKey(0)