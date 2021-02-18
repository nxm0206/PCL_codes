# -*- coding: UTF-8 -*-

import imageio
from glob import glob
import cv2

def addlabel(file_dir):
    img = cv2.imread(file_dir)

    height, width, layers = img.shape
    # print(height, width)

    font = cv2.FONT_HERSHEY_PLAIN
    bottomLeftCornerOfText = (10, 20)
    fontScale = 1
    fontColor = (254, 254, 254)
    lineType = 1

    cv2.putText(img, 'wavelength = '+file_dir[33:37]+' nm',
        bottomLeftCornerOfText,
        font,
        fontScale,
        fontColor,
        lineType)

    return img

def create_gif(image_list, gif_name):
    frames = []
    for image_name in image_list:
        img = addlabel(image_name)
        frames.append(img)
    # Save them as frames into a gif
    imageio.mimsave(gif_name, frames, 'GIF', duration=1)

    return


def main():
    image_list = glob('D:/measurement_data/20201223/GIF/*.jpg')
    gif_name = 'D:/measurement_data/20201223/256OPA_farfield.gif'
    create_gif(image_list, gif_name)


if __name__ == "__main__":
    main()