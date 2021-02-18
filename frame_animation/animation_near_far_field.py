
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

filename_list1 = glob('D:/measurement_data/20201124/real_space/*.tiff')
print(filename_list1)

filename_list2 = glob('D:/measurement_data/20201125/fourier_space/*.tiff')
print(filename_list2)
count = 0
str_wav = 40
offset = 51
for i in range(len(filename_list1)):

    if count <= 39:
        img1 = cv2.imread(filename_list1[i])
        height1, width1, layer1 = img1.shape
        for m in range(height1):
            for n in range(width1):

                if img1[m, n, 0] >= 30:
                    img1[m, n] = img1[m, n] + 45
                elif img1[m, n, 0] >= 12:
                    img1[m, n] = img1[m, n] + 8
    else:
        img1 = cv2.imread(filename_list1[i])
        height1, width1, layer1 = img1.shape

    img2 = cv2.imread(filename_list2[i+offset])
    height2, width2, layer2= img2.shape
    for m in range(height2):
        for n in range(width2):

            # print(img2[m, n])
            if img2[m, n, 0] >= 127:
                img2[m, n] = [255, 255, 255]
            elif img2[m, n, 0] >= 12:
                img2[m, n] = img2[m, n] * 2

    size = (width1, height1+height2)
    img = np.concatenate((img1,img2),axis = 0)
    # print(type(img))
    # print(filename_list1[i][str_wav:str_wav + 4])
    # print(filename_list2[i+offset][str_wav+3:str_wav + 7])

    cv2.putText(img, 'wavelength = ' + filename_list1[i][str_wav:str_wav+4] + ' nm',
                bottomLeftCornerOfText,
                font,
                fontScale,
                fontColor,
                lineType)

    cv2.putText(img, 'real space',
                bottomLeftCornerOfText1,
                font,
                fontScale,
                fontColor1,
                lineType)

    cv2.putText(img, 'Fourier space',
                bottomLeftCornerOfText2,
                font,
                fontScale,
                fontColor1,
                lineType)


    img_array.append(img)
    count = count+1
dir = 'D:/measurement_data/20201124/'
out = cv2.VideoWriter(dir+'near_and_far_field.avi', cv2.VideoWriter_fourcc(*'DIVX'), 12, size)

for i in range(len(img_array)):
    out.write(img_array[i])
out.release()