import cv2

class VideoCamera(object):
    def __init__(self):
        self.dispW = 960
        self.dispH = 720
        pipeline = 'nvarguscamerasrc sensor_id=ID ! video/x-raw(memory:NVMM), width=X, height=Y, format=(string)NV12 ! nvvidconv flip-method=3 ! video/x-raw, width='+str(self.dispW)+', height='+str(self.dispH)+', format=I420, appsink max-buffers=1 drop=true'
        self.video = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
        
    def __del__(self):
        self.video.releast()

    def get_frame(self):
        ret, frame = self.video.read()

        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
