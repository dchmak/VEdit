import cv2


class Video:
    def __init__(self, source):
        # open the video source
        self.video = cv2.VideoCapture(source)
        if not self.video.isOpened():
            raise ValueError("Unable to open video source", source)

        # get video source width and height
        self.width = self.video.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)

        self.frame_count = self.video.get(cv2.CAP_PROP_FRAME_COUNT)

    def __del__(self):
        if self.video.isOpened():
            self.video.release()

    def get_frame(self, percent):
        if self.video.isOpened():
            self.video.set(cv2.cv2.CAP_PROP_POS_FRAMES,
                           self.frame_count * percent)
            ret, frame = self.video.read()
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        return (ret, None)
