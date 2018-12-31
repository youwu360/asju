
from pathlib import Path
import cv2
import video_action
import numpy as np


base = Path(__file__).resolve().parents[1]
file_name = 'haokan6.mp4'
path = base.joinpath('videos/' + file_name)
frames = video_action.get_all_frames(str(path))


template = cv2.imread(str(base.joinpath('logos/haokan5.jpg')))
shape = template.shape

indicator = np.ones((shape[0], shape[1]))
for i in range(shape[0]):
    for j in range(shape[1]):
        if np.sum(template[i][j]) >= 10:
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

new_logo = cv2.imread(str(base.joinpath('logos/haokan5_meitu_2.jpg')))

for frame in frames:
    logo_area = frame[y:y + shape[0], x:x + shape[1], :]
    logo_area = logo_area - template
    print('logo_area.shape')
    print(logo_area.shape)
    # cv2.imshow("logo_area", logo_area)
    # cv2.waitKey(500)

    blured = cv2.blur(logo_area, (9, 9))

    # cv2.imshow("logo_area, blured", logo_area)
    # cv2.waitKey(500)

    # cv2.imshow("new_logo", new_logo)
    # cv2.waitKey(500)

    print('new_logo.shape')
    print(new_logo.shape)

    alpha = 0.5
    comp_logo = cv2.addWeighted(blured, alpha, new_logo, 1 - alpha, 0)
    # cv2.imshow("comp_logo", comp_logo)
    # cv2.waitKey(500)

    frame[y:y + shape[0], x:x + shape[1]] = comp_logo
    cv2.imshow("frame", frame)
    cv2.waitKey(0)


