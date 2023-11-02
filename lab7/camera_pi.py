# Origin : http://blog.miguelgrinberg.com/post/video-streaming-with-flask

import cv2
import base64

class Camera(object):
    def __init__(self):
        if cv2.__version__.startswith('2'):
            PROP_FRAME_WIDTH = cv2.cv.CV_CAP_PROP_FRAME_WIDTH
            PROP_FRAME_HEIGHT = cv2.cv.CV_CAP_PROP_FRAME_HEIGHT
        elif cv2.__version__.startswith('3') or cv2.__version__.startswith('4'):
            PROP_FRAME_WIDTH = cv2.CAP_PROP_FRAME_WIDTH
            PROP_FRAME_HEIGHT = cv2.CAP_PROP_FRAME_HEIGHT

        self.video = cv2.VideoCapture(0, cv2.CAP_V4L)
        #self.video.set(PROP_FRAME_WIDTH, 640)
        #self.video.set(PROP_FRAME_HEIGHT, 480)
        self.video.set(PROP_FRAME_WIDTH, 320)
        self.video.set(PROP_FRAME_HEIGHT, 240)
        # limit buffer size
        # self.video.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    def __del__(self):
        self.video.release()
    def get_frame(self):
        success, image = self.video.read()
        # clear buffer
        # success, image = self.video.read()
        # ret, jpeg = cv2.imencode('.jpg', image)
        # return jpeg.tostring()
        return image

    def get_frame_b64(self):
        success, image = self.video.read()
        # clear buffer
        # success, image = self.video.read()
        # resize image
        image = cv2.resize(image, (120, 90), interpolation=cv2.INTER_AREA)
        ret, jpeg = cv2.imencode('.jpg', image)
        return base64.b64encode(jpeg)
