import cv2
import numpy as np
import lib.RectangleRegion


def has_logo(imgs):
    shape = imgs[0].shape
    zero_one = get_zero_one(imgs)
    y_acc = np.sum(zero_one, axis=1)

    median = np.median(y_acc)
    y_acc = y_acc - median

    '''
    sum the pixels by y axis
    and get smallest region of pixels
    '''
    y_list = []
    new_seg = True
    for i in range(len(y_acc)):
        if y_acc[i] != 0:
            if new_seg:
                y_list.append([i, i])
                new_seg = False
            else:
                y_list[len(y_list) - 1][1] = i
        else:
            new_seg = True

    rectangle = lib.RectangleRegion.RectangleRegion()
    regions = []
    for y0_y1 in y_list:

        rectangle.clear()
        for y in range(y0_y1[0], y0_y1[1] + 1):
            for x in range(shape[1]):
                if zero_one[y][x] != 0:
                    rectangle.add_point([y, x])

        regions.append(rectangle.get_region())

    merged_regions = merge_region(regions)

    for [[y0, x0], [y1, x1]] in merged_regions:
        if y0 < y1 and x0 < x1 and (x1 - x0 + 1) / (y1 - y0 + 1) > 1.68:
            return True

    return False


def merge_region(regions):

    ret = []
    ret.append(regions[0])
    for i in range(1, len(regions)):
        [[y0, x0], [y1, x1]] = ret[-1]
        [[Y0, X0], [Y1, X1]] = regions[i]

        ny0 = min(y0, Y0)
        nx0 = min(x0, X0)
        ny1 = max(y1, Y1)
        nx1 = max(x1, X1)
        area0 = (y1 - y0 + 1) * (x1 - x0 + 1)
        area1 = (Y1 - Y0 + 1) * (X1 - X0 + 1)
        area_new = (ny1 - ny0 + 1) * (nx1 - nx0 + 1)

        print("ratio: %s " % (area0 + area1) / area_new)

    return ret


def get_zero_one(imgs):
    arr = np.array(imgs)
    var = np.array(np.array(np.sqrt(np.var(arr, 0))).astype(int), dtype=np.uint8)

    grey_img = cv2.cvtColor(var, cv2.COLOR_BGR2GRAY)
    _, bin_img = cv2.threshold(grey_img, 30, 255, cv2.THRESH_BINARY_INV)
    dilate_img = cv2.dilate(bin_img, (3, 3))
    cv2.imshow('dilate_img', dilate_img)
    cv2.waitKey(0)

    zero_one = dilate_img // 255
    return zero_one


def get_quantile(zero_one, r=0.001):
    x_list = []
    y_list = []

    for y in range(zero_one.shape[0]):
        for x in range(zero_one.shape[1]):
            if zero_one[y][x] != 0:
                x_list.append(x)
                y_list.append(y)

    x_low = int(np.quantile(x_list, r))
    x_high = int(np.quantile(x_list, 1 - r))
    y_low = int(np.quantile(y_list, r))
    y_high = int(np.quantile(y_list, 1 - r))
    return x_low, x_high, y_low, y_high


def detect(imgs):
    shape = imgs[0].shape
    zero_one = get_zero_one(imgs)
    x_low, x_high, y_low, y_high = get_quantile(zero_one, r=0.001)

    repeated = np.repeat(zero_one[:, :, np.newaxis], 3, axis=2)

    median = np.median(imgs, axis=0)
    logo = median * repeated

    compact = np.array(logo[max(0, y_low - 2):min(shape[0], y_high + 2), max(0, x_low - 2):min(shape[1], x_high + 2)],
                       dtype=np.uint8)
    return compact

