
import cv2
import numpy as np
from glob import glob

# print(glob('D:/科研资料/数据/20201111/红外相机/左上1024/*.bmp'))
img_array = []

font = cv2.FONT_ITALIC
bottomLeftCornerOfText = (180, 50)
fontScale = 0.3
# bottomLeftCornerOfText = (100, 200)
# fontScale = 0.4
fontColor = (255, 255, 255)
lineType = 1

filename_list = glob('D:/measurement_data/20201112/infrared_camera/defocusing/*.bmp')
# filename_list = glob('D:/measurement_data/20201111/infrared_camera/top_left_1024/*.bmp')


for i in range(len(filename_list)):

    img = cv2.imread(filename_list[i])

    height, width, layers = img.shape

    size = (width, height)

    label = 'moving out of focus'
    # label = 'wavelength = ' + filename_list[i][59:63] + ' nm'
    cv2.putText(img, label,
                bottomLeftCornerOfText,
                font,
                fontScale,
                fontColor,
                lineType)


    img_array.append(img)
dir = 'D:/measurement_data/video/'
out = cv2.VideoWriter(dir+'SOI_64_antenna_defocusing.avi', cv2.VideoWriter_fourcc(*'DIVX'), 20, size)
# out = cv2.VideoWriter(dir+'SOI_1024_antenna_wav_scan.avi', cv2.VideoWriter_fourcc(*'DIVX'), 10, size)

for i in range(len(img_array)):
    out.write(img_array[i])
out.release()