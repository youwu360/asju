
from pathlib import Path
import cv2
import video_action
import numpy as np


base = Path(__file__).resolve().parents[1]
file_name = 'haokan6.mp4'
path = base.joinpath('videos/' + file_name)
frames = video_action.get_all_frames(str(path))


template = cv2.imread(str(base.joinpath('logos/haokan3.jpg')))
shape = template.shape

indicator = np.ones((shape[0], shape[1]))
for i in range(shape[0]):
    for j in range(shape[1]):
        if np.sum(template[i][j]) != 0:
            indicator[i][j] = 0

indicators = np.repeat(indicator[:, :, np.newaxis], 3, axis=2)


x_list = []
y_list = []

counter = 0
for frame in frames:
    counter += 1
    if counter % 13 != 0:
        continue

    result = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
    y, x = np.unravel_index(result.argmax(), result.shape)
    x_list.append(x)
    y_list.append(y)
    print(x, y)

x = int(np.median(x_list))
y = int(np.median(y_list))

print(x, y)

for frame in frames:
    frame[y:y + shape[0], x:x + shape[1]] = frame[y:y + shape[0], x:x + shape[1]] * indicators
    cv2.imshow("frame", frame)
    cv2.waitKey(0)


