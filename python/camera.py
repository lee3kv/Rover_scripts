import cv2

class VideoCamera(object):
    def __init__(self):
        self.dispW = 960
        self.dispH = 720
        pipeline = "nvarguscamerasrc ! ‘video/x-raw(memory:NVMM), width=1920, height=1080, format=(string)NV12, framerate=(fraction)30/1' ! nvoverlaysink -e"
        self.video = cv2.VideoCapture(pipeline)
        
    def __del__(self):
        self.video.releast()

    def get_frame(self):
        ret, frame = self.video.read()

        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
