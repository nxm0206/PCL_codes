import numpy as np
import cv2

import pandas as pd




filename='C:/Users/xiaomin/Desktop/spot.png'
img = cv2.imread(filename, cv2.IMREAD_COLOR)
# print(img)
img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
px = img_gray[100,100]
print(img_gray)

## convert your array into a dataframe
df = pd.DataFrame(img_gray)

## save to xlsx file


filepath ='C:/Users/xiaomin/Desktop/spot_gray.xlsx'
df.to_excel(filepath, index=False)



# height, width, layers = img.shape
# print(height, width)
# print(height, width)
#
# font = cv2.FONT_HERSHEY_PLAIN
# bottomLeftCornerOfText = (100,220)
# fontScale = 1
# fontColor = (10, 100, 10)
# lineType = 1
#
# cv2.putText(img, 'wavelength = '+filename[59:63]+' nm',
#     bottomLeftCornerOfText,
#     font,
#     fontScale,
#     fontColor,
#     lineType)
#
# #Display the image
# cv2.imshow("img", img)
# cv2.waitKey(0)