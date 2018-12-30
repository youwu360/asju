import cv2
import random
import numpy as np


def get_all_frames(video_path, img_cnt=0, sub_region=None):
    cap = cv2.VideoCapture(video_path)

    imgs = []

    idx = 0
    while cap.isOpened():
        ret, frame = cap.read()

        if ret:

            idx += 1
            if img_cnt <= 0 or len(imgs) < img_cnt:
                imgs.append(frame)
            elif random.random() <= img_cnt / idx:
                v = random.randint(0, img_cnt - 1)
                imgs[v] = frame
        else:
            break
    cap.release()
    return crop(imgs, sub_region)


def crop(imgs, sub_region):
    if imgs is None or sub_region is None:
        return imgs

    ret = []
    for img in imgs:
        ret.append(np.array(img[sub_region[0][1]:sub_region[1][1], sub_region[0][0]:sub_region[1][0]], dtype=np.uint8))
        # cv2.imshow("000", ret[len(ret) - 1])
        # cv2.waitKey(0)
    return ret

