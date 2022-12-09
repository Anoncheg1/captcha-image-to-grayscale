import os
import preprocess

import cv2

import cv2 as cv

import numpy as np

from grayscale import remove_background_colours
from grayscale import show_two_images

# 6 и б отличаются
# т и г тяжело отличить
# п и н тяжело отличить
# нету e
# Press the green button in the gutter to run the script.
ALPHABET = ['2', '4', '5', '6', '7', '8', '9', 'б', 'в', 'г', 'д', 'ж', 'к', 'л', 'м', 'н', 'п', 'р', 'с', 'т']


# https://bestofphp.com/repo/Gregwar-Captcha-php-image-processing


def clear_captcha(img):
    img2 = remove_background_colours(copy.copy(img))
    gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    if not np.array_equal(img2, img):            
        # gray = cv.GaussianBlur(gray, (5, 5), 0)
        # -- remove thin lines
        kernel = np.ones((2, 2), np.uint8)
        opening = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)
        gray = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
        gray = cv2.bitwise_or(gray, gray)

    ret3, gray = cv.threshold(gray, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

    w, h = gray.shape[:2]
    # -- invert colours
    if cv2.countNonZero(gray) < ((w * h) // 2):
        gray = cv2.bitwise_not(gray)
    return gray


if __name__ == '__main__':
    import copy
    w = []
    p = 'jpg2'
    for i, x in enumerate(os.listdir(p)):
        if i  < 20:
            continue
        solv = x[0:5]
        file = os.path.join(p, x)
        # inv = [4, 8, 67, 72, 80, 95]

        img: np.ndarray = cv.imread(file)

        gray = clear_captcha(img)

        img2 = cv.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        print("ii", i, img.shape, img2.shape)
        show_two_images(img, img2)
        # from matplotlib import pyplot as plt
        # plt.imshow(img2)
        # plt.show()
