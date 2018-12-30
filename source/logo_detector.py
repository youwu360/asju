import cv2
import numpy as np


def detect(imgs):
    arr = np.array(imgs)
    var = np.array(np.array(np.sqrt(np.var(arr, 0))).astype(int), dtype=np.uint8)

    grey_img = cv2.cvtColor(var, cv2.COLOR_BGR2GRAY)
    _, bin_img = cv2.threshold(grey_img, 30, 255, cv2.THRESH_BINARY_INV)
    dilate_img = cv2.dilate(bin_img, (3, 3))
    cv2.imshow('dilate_img', dilate_img)
    cv2.waitKey(0)

    zero_one = dilate_img // 255
    repeated = np.repeat(zero_one[:, :, np.newaxis], 3, axis=2)

    median = np.median(imgs, axis=0)
    logo = median * repeated

    x_list = []
    y_list = []

    for y in range(zero_one.shape[0]):
        for x in range(zero_one.shape[1]):
            if zero_one[y][x] != 0:
                x_list.append(x)
                y_list.append(y)

    r = 0.001
    x2 = int(np.quantile(x_list, r))
    x98 = int(np.quantile(x_list, 1 - r))
    y2 = int(np.quantile(y_list, r))
    y98 = int(np.quantile(y_list, 1 - r))

    compact = np.array(logo[y2:y98, x2:x98], dtype=np.uint8)
    return compact

