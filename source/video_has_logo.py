from pathlib import Path
import cv2
import video_action
import corner_point
import logo_detector


base = Path(__file__).resolve().parents[1]
path = str(base.joinpath('youku/2.mp4'))

cropped_frames = video_action.get_all_frames(path, img_cnt=100)

haslogo = logo_detector.has_logo(cropped_frames)
