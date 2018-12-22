import cv2
import numpy as np
import random

img_cnt = 30
idx = 0

cap = cv2.VideoCapture("videos/haokan.mp4")
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        idx += 1

        if random.random() <= img_cnt / idx:
            v = random.randint(0, img_cnt)
            cv2.imwrite("images/fotolia_processed/%d.jpg" % v, frame)
    else:
        break

cap.release()
cv2.destroyAllWindows()
