
def get_all_frames(video_path, img_cnt = 10000):
    import cv2, random
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
    return imgs
