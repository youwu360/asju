import cv2
import numpy as np


def detect(imgs):
    arr = np.array(imgs)
    var = np.array(np.array(np.sqrt(np.var(arr, 0))).astype(int), dtype=np.uint8)

    grey_img = cv2.cvtColor(var, cv2.COLOR_BGR2GRAY)
    _, bin_img = cv2.threshold(grey_img, 30, 255, cv2.THRESH_BINARY_INV)
    dilate_img = cv2.dilate(bin_img, (3, 3))

    zero_one = dilate_img // 255
    repeated = np.repeat(zero_one[:, :, np.newaxis], 3, axis=2)

    median = np.median(imgs, axis=0)
    logo = median * repeated

    return np.array(logo, dtype=np.uint8)

