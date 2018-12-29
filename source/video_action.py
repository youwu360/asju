import cv2
import random
import numpy as np


def get_all_frames(video_path, img_cnt=240, subregion=None):
    cap = cv2.VideoCapture(video_path)

    imgs = []

    idx = 0
    while cap.isOpened():
        ret, frame = cap.read()

        if ret:

            idx += 1
            if len(imgs) < img_cnt:
                imgs.append(frame)
            elif random.random() <= img_cnt / idx:
                v = random.randint(0, img_cnt - 1)
                imgs[v] = frame
        else:
            break
    cap.release()
    return crop(imgs, subregion)


def crop(imgs, subregion):
    if imgs is None or subregion is None:
        return imgs

    ret = []
    for img in imgs:
        ret.append(np.array(img[subregion[0][1]:subregion[1][1], subregion[0][0]:subregion[1][0]], dtype=np.uint8))
        # cv2.imshow("000", ret[len(ret) - 1])
        # cv2.waitKey(0)
    return ret

