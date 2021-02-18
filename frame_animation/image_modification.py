
import cv2
import numpy as np
from glob import glob

img_array = []

font = cv2.FONT_ITALIC
bottomLeftCornerOfText = (120, 50)
bottomLeftCornerOfText1 = (10, 220)
bottomLeftCornerOfText2 = (10, 440)
fontScale = 0.5
fontColor = (255, 255, 255)
fontColor1 = (10, 255, 255)
lineType = 1

filename1 = 'D:/measurement_data/20201124/Fourier_space/1539.tiff'

filename2 = 'D:/measurement_data/20201124/Fourier_space/1540.tiff'

img1 = cv2.imread(filename1)
img2 = cv2.imread(filename2)
height1, width1, layer1 = img1.shape
for m in range(height1):
    for n in range(width1):
        #print(img1[m, n, 0])
        if img2[m, n, 0] >= 127:
            img2[m, n] = [255, 255, 255]
        else:
            img2[m, n] = img2[m, n] * 2



height2, width2, layer2= img2.shape
str_wav = 40
size = (width1, height1+height2)
img = np.concatenate((img1,img2),axis = 0)
    # print(type(img))
str_wav = 40
# cv2.putText(img, 'wavelength = ' + filename1[str_wav:str_wav+4] + ' nm',
#             bottomLeftCornerOfText,
#             font,
#             fontScale,
#             fontColor,
#             lineType)

cv2.putText(img, 'wavelength = ' + filename1[str_wav:str_wav+4] + ' nm',
            bottomLeftCornerOfText1,
            font,
            fontScale,
            fontColor1,
            lineType)

cv2.putText(img, 'wavelength = ' + filename2[str_wav:str_wav+4] + ' nm',
            bottomLeftCornerOfText2,
            font,
            fontScale,
            fontColor1,
            lineType)

cv2.imshow('image',img)
cv2.waitKey(0)
# img_array.append(img)

#     count = count+1
# dir = 'D:/measurement_data/20201124/'
# out = cv2.VideoWriter(dir+'near_and_far_field.avi', cv2.VideoWriter_fourcc(*'DIVX'), 12, size)
#
# for i in range(len(img_array)):
#     out.write(img_array[i])
# out.release()