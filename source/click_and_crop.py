# import the necessary packages
import argparse
import cv2
from pathlib import Path
import video_action
# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
cur = ()
cropping = False

def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, cropping, cur
    cur = (x, y)

    if cropping:
        copy = image_show.copy()
        cv2.rectangle(copy, refPt[0], (x, y), (255, 0, 0), 2)
        cv2.imshow("img", copy)
    else:
        copy = image_show.copy()
        cv2.imshow("img", copy)

    print("Is cropping : %s" % cropping)

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        refPt.append((x, y))
        cropping = False


def get_corner_points(video_path):
    global refPt
    all_frames = video_action.get_all_frames(video_path)

    if all_frames is None or len(all_frames) == 0:
        print('No image get from video !')
        exit(-1)

    img = all_frames[len(all_frames) // 2]
    cv2.namedWindow("img")
    cv2.setMouseCallback("img", click_and_crop)
    cv2.imshow("img", img)

    global image_show
    image_show = img.copy()

    while True:
        # display the image and wait for a keypress
        for img in all_frames:
            key = cv2.waitKey(50) & 0xFF

            # if the 'r' key is pressed, reset the cropping region
            if key == ord("r"):
                image_show = img.copy()
                cv2.imshow("img", img.copy())
                refPt = []

            # if the 'c' key is pressed, break from the loop
            elif key == ord("c"):
                return refPt

            image_show = img.copy()


base = Path(__file__).resolve().parents[1]
path = str(base.joinpath('videos/haokan1.mp4'))

res = get_corner_points(path)
print(res)



