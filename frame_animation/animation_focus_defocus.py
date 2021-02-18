
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

filename_list1 = glob('D:/measurement_data/20201112/infrared_camera/defocus_scan/*.bmp')

filename_list2 = glob('D:/measurement_data/20201112/infrared_camera/focus_scan/*.bmp')

for i in range(len(filename_list1)):

    img1 = cv2.imread(filename_list1[i])
    # print(type(img1))
    img2 = cv2.imread(filename_list2[i])
    height1, width1, layers1 = img1.shape
    height2, width2, layers2 = img2.shape
    size = (width1, height1+height2)
    img = np.concatenate((img1,img2),axis = 0)
    # print(type(img))

    cv2.putText(img, 'wavelength = ' + filename_list1[i][58:62] + ' nm',
                bottomLeftCornerOfText,
                font,
                fontScale,
                fontColor,
                lineType)

    cv2.putText(img, 'out of focus',
                bottomLeftCornerOfText1,
                font,
                fontScale,
                fontColor1,
                lineType)

    cv2.putText(img, 'in focus',
                bottomLeftCornerOfText2,
                font,
                fontScale,
                fontColor1,
                lineType)


    img_array.append(img)
dir = 'D:/measurement_data/video/'
out = cv2.VideoWriter(dir+'SOI_64_antenna_defocused_vs_focused.avi', cv2.VideoWriter_fourcc(*'DIVX'), 8, size)

for i in range(len(img_array)):
    out.write(img_array[i])
out.release()