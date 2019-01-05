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
                if 0 < x < shape[1] - 1 and 0 < y < shape[0] - 1 and np.sum(zero_one[y - 1:y + 2, x - 1:x + 2]) >= 5:
                    rectangle.add_point([y, x])

        regions.append(rectangle.get_region())

    merged_regions = merge_rectangle_region(regions)

    if merged_regions is not None:
        for [[y0, x0], [y1, x1]] in merged_regions:
            lx = x1 - x0 + 1
            ly = y1 - y0 + 1
            if y0 < y1 and x0 < x1 and lx / ly > 1.68 and 0.1 < lx / shape[1] < 0.5 and 0.025 < ly / shape[0] < 0.1:
                return True

    return False


def merge_rectangle_region(regions):

    if regions is None or len(regions) <= 1:
        return regions

    ret = []
    ret.append(regions[0])
    for i in range(1, len(regions)):
        y0 = ret[-1][0][0]
        x0 = ret[-1][0][1]
        y1 = ret[-1][1][0]
        x1 = ret[-1][1][1]

        Y0 = regions[i][0][0]
        X0 = regions[i][0][1]
        Y1 = regions[i][1][0]
        X1 = regions[i][1][1]

        ny0 = min(y0, Y0)
        nx0 = min(x0, X0)
        ny1 = max(y1, Y1)
        nx1 = max(x1, X1)

        area0 = (y1 - y0 + 1) * (x1 - x0 + 1)
        area1 = (Y1 - Y0 + 1) * (X1 - X0 + 1)
        area_new = (ny1 - ny0 + 1) * (nx1 - nx0 + 1)

        ratio = (area0 + area1) / area_new
        print("ratio: %f " % ratio)

        if ratio >= 2/3:
            merged = lib.RectangleRegion.RectangleRegion()
            merged.add_points(ret[-1])
            merged.add_points(regions[i])
            ret[-1] = merged.get_region()
        else:
            ret.append(regions[i])

    return ret


def get_zero_one(imgs):
    arr = np.array(imgs)
    var = np.array(np.array(np.sqrt(np.var(arr, 0))).astype(int), dtype=np.uint8)

    grey_img = cv2.cvtColor(var, cv2.COLOR_BGR2GRAY)
    _, bin_img = cv2.threshold(grey_img, 30, 255, cv2.THRESH_BINARY_INV)
    dilate_img = cv2.dilate(bin_img, kernel=(3, 3), borderType=cv2.BORDER_ISOLATED)
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

