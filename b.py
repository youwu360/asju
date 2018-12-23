import cv2
import random
import numpy as np
from os import listdir
from os.path import isfile, join

img_path = "youku"
extensions = ['.mp4']

shape_dict = {}
imgs = []

sep_val = 1000000
for file in listdir(img_path):
    extension = file[file.find('.'):]
    if extension not in extensions:
        continue

    cap = cv2.VideoCapture(join(img_path, file))
    if cap.isOpened():
        ret, frame = cap.read()
        shape = frame.shape
        shape_val = shape[0] * sep_val + shape[1]

        if shape_val not in shape_dict:
            shape_dict[shape_val] = 0
        shape_dict[shape_val] += 1

    cap.release()

shape_most = None
freq_most = 0
for shape in shape_dict:
    freq = shape_dict[shape]
    if freq > freq_most:
        freq_most = freq
        shape_most = shape

shape0 = shape_most // sep_val
shape1 = shape_most % sep_val

img_cnt = 500
idx = 0
for file in listdir(img_path):
    extension = file[file.find('.'):]
    if extension not in extensions:
        continue

    cap = cv2.VideoCapture(join(img_path, file))

    print(join(img_path, file))
    while cap.isOpened():
        ret, frame = cap.read()

        if ret:
            if frame.shape[0] != shape0 or frame.shape[1] != shape1:
                print("break @ %s" % join(img_path, file))
                break

            idx += 1
            if len(imgs) < img_cnt:
                imgs.append(frame)
            elif random.random() <= img_cnt / idx:
                v = random.randint(0, img_cnt - 1)
                imgs[v] = frame
        else:
            break
    cap.release()

arr = np.array(imgs)
var = np.array(np.array(np.sqrt(np.var(arr, 0))).astype(int), dtype=np.uint8)

grey_img = cv2.cvtColor(var, cv2.COLOR_BGR2GRAY)

cv2.imshow("grey_img", grey_img)
cv2.waitKey(0)

blur_img = cv2.blur(grey_img, (3, 3))
cv2.imshow("blur_img", blur_img)
cv2.waitKey(0)

_, bin_img = cv2.threshold(grey_img, 30, 255, cv2.THRESH_BINARY_INV)
cv2.imshow("bin_img", bin_img)
cv2.waitKey(0)

dilate_img = cv2.dilate(bin_img, (3, 3))
cv2.imshow("dilate_img", dilate_img)
cv2.waitKey(0)

zero_one = dilate_img // 255


x_list = []
y_list = []
none_zero = 0
for y in range(zero_one.shape[0]):
    for x in range(zero_one.shape[1]):
        if zero_one[y][x] != 0:
            none_zero += 1
            x_list.append(x)
            y_list.append(y)

x2 = np.quantile(x_list, 0.02, 0)
x98 = np.quantile(x_list, 0.98, 0)
y2 = np.quantile(y_list, 0.02, 0)
y98 = np.quantile(y_list, 0.98, 0)

none_zero_zrea = (x98 - x2 + 1) * (y98 - y2 + 1)
have_logo = x98 > x2 and y98 > y2
have_logo = have_logo and none_zero_zrea * 10 < shape0 * shape1
have_logo = have_logo and none_zero * 10 > none_zero_zrea

if have_logo:
    print("logo found !")
else:
    print("No logo found !")
    exit(0)

bound = 5
flag_array = np.zeros(zero_one.shape)
flag_array[int(y2) - bound:int(y98) + bound, int(x2) - bound:int(x98) + bound] = 1

zero_one = zero_one * flag_array
repeated = np.repeat(zero_one[:, :, np.newaxis], 3, axis=2)

median = np.median(imgs, axis=0)

logo = median * repeated

cv2.imshow("logo", np.array(logo, dtype=np.uint8))
cv2.waitKey(0)

print("ending !")
