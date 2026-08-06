import cv2


class Camera:
    def __init__(self, index, width, height):
        self.capture = cv2.VideoCapture(index)

        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


    def read(self):
        success, frame = self.capture.read()

        if success:
            frame = cv2.flip(frame, 1)

        return success, frame


    def release(self):
        self.capture.release()
