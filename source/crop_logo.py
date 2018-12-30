from pathlib import Path
import cv2
import video_action
import corner_point
import logo_detector


base = Path(__file__).resolve().parents[1]
path = str(base.joinpath('videos/haokan3.mp4'))
res = corner_point.get_corner_points(path)

cropped_frames = video_action.get_all_frames(path, img_cnt=500, sub_region=res)
logo_img = logo_detector.detect(cropped_frames)

cv2.imwrite(str(base.joinpath('logos/haokan3.jpg')), logo_img)
