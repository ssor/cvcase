import cv2


class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
        self.video_width = self.video.get(3)
        self.video_height = self.video.get(4)

    def __del__(self):
        self.video.release()

    def video_size(self):
        return (self.video_width, self.video_height)

    def get_frame(self, circle=None, line=None, rect=None):
        success, image = self.video.read()
        if circle is not None:
            image = cv2.circle(image, circle.center, circle.radius, circle.color, -1)
        if line is not None:
            image = cv2.line(image, (line.start.x,line.start.y), (line.end.x, line.end.y), line.color, line.thickness)
        if rect is not None:
            image = cv2.rectangle(image, (rect.start.x,rect.start.y), (rect.end.x, rect.end.y), rect.color, rect.thickness)
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        # 对于 python2.7 或者低版本的 numpy 请使用 jpeg.tostring()
        return jpeg.tobytes()
