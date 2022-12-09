import numpy as np
import cv2 as cv


def remove_background_colours(img):
    characters = []
    backs = []

    color = ('b', 'g', 'r')
    res = []
    for i, col in enumerate(color):
        # -- calc hist
        histr = cv.calcHist([img], [i], None, [256], [0, 256])

        # from matplotlib import pyplot as plt
        # plt.plot(histr, color=col)
        # plt.xlim([0, 256])
        # plt.show()
        # -- if not background -> skip colour
        if histr.max() < 1000:
            print("max() < 1000")
            continue
        # -- find background colour range
        back = list(histr).index(histr.max())
        back_low = back - 10
        back_upper = back + 10
        back_low = 0 if back_low < 0 else back_low
        back_upper = 255 if back_upper > 255 else back_upper
        # -- remove background from hisogram to be able to find character colour
        print("back_low, back_upper", back_low, back_upper)
        for j in range(back_low, back_upper + 1):
            histr[j] = 0
        for j in range(back_low, back_upper + 1):
            histr[j] = 0

        # if histr.max() < 50:
        #     print("continue")
        #     continue

        # character colour at histogram as a most common colour after background
        character = list(histr).index(histr.max())

        characters.append(character)
        backs.append(back)
        # if background and character is too close - do nothing
        if abs(character - back) < 50:  # or character < 10 or character > 240:
            print("continue!!!", abs(character - back) < 50 or character < 10 or character > 240)
            continue

        res.append((i, character, back))
    # detect if it is inverted captcha without background
    if len(res) == 3 and 124 <= res[0][2] <= 128 and 124 <= res[1][2] <= 128 and 124 <= res[2][2] <= 128:
            # and 230 <= res[0][1] or res[0][1] <= 128 and 124 <= res[1][1] <= 128 and 124 <= res[2][1] <= 128:
        print("do nothing!!!!")
        return img  # do nothing
    # pain not character area to background
    bool_indexes = []
    for i, character, back in res:
        # get character mask
        a1 = img[:, :, i] > (character - 20)
        a2 = img[:, :, i] < (character + 20)
        bool_indexes.append(np.logical_and(a1, a2))
        # np.place(img[:, :, i], img[:, :, i] < (character - 10), back)
        # np.place(img[:, :, i], img[:, :, i] > (character + 10), back)
        print("character", character, "back", back)
    # -- found area with character as a merge of colours
    v = bool_indexes[0]
    if len(bool_indexes) >= 2:
        v = np.logical_and(v, bool_indexes[1])
    if len(bool_indexes) == 3:
        v = np.logical_and(v, bool_indexes[2])
    # -- invert to get not characters area
    v = np.logical_not(v)

    for g in res:
        img[v, g[0]] = g[2]
    # for i in range(img.shape[-1]):
    #     img[v, i] = res[i]
    # plt.plot(histr, color=col)
    # plt.xlim([0, 256])
    # plt.show()
    for i, col in enumerate(color):
        # -- calc hist
        histr = cv.calcHist([img], [i], None, [256], [0, 256])

        # from matplotlib import pyplot as plt
        # plt.plot(histr, color=col)
        # plt.xlim([0, 256])
        # plt.show()

    return img


def show_two_images(img1, img2, how='horizontal'):
    if how == 'horizontal':
        numpy_concat = np.concatenate((img1, img2), axis=1)  # horizontal
    else:
        numpy_concat = np.concatenate((img1, img2), axis=0)  # vertical

    cv.imshow('image', numpy_concat)  # show image in window
    cv.waitKey(0)  # wait for any key indefinitely
    cv.destroyAllWindows()  # close window q
