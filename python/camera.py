import cv2

class VideoCamera(object):
    def __init__(self):
        self.dispW = 960
        self.dispH = 720
        self.video = cv2.VideoCapture('nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method=3 ! video/x-raw, width='+str(self.dispW)+', height='+str(self.dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink')

    def __del__(self):
        self.video.releast()

    def get_frame(self):
        ret, frame = self.video.imread()

        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()