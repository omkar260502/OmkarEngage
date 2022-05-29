import cv2

face = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
hat = cv2.imread('Filters/images.png')
glass = cv2.imread('Filters/glasses.png')
dog = cv2.imread('Filters/dog.png')


def put_hat(hat, fc, x, y, w, h):
    face_width = w
    face_height = h

    hat_width = face_width + 1
    hat_height = int(0.50 * face_height) + 1

    hat = cv2.resize(hat, (hat_width, hat_height))

    for i in range(hat_height):
        for j in range(hat_width):
            for k in range(3):
                if hat[i][j][k] < 235:
                    fc[y + i - int(0.40 * face_height)
                       ][x + j][k] = hat[i][j][k]
    return fc


def put_glass(glass, fc, x, y, w, h):
    face_width = w
    face_height = h

    hat_width = face_width + 1
    hat_height = int(0.50 * face_height) + 1

    glass = cv2.resize(glass, (hat_width, hat_height))

    for i in range(hat_height):
        for j in range(hat_width):
            for k in range(3):
                if glass[i][j][k] < 235:
                    fc[y + i - int(-0.20 * face_height)][x +
                                                         j][k] = glass[i][j][k]
    return fc


class Video1(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, frame = self.video.read()
        im = frame
        size = 4
        #(rval, im) = webcam.read()
        im = cv2.flip(im, 1, 0)
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        fl = face.detectMultiScale(gray, 1.19, 7)

        for (x, y, w, h) in fl:
            im = put_hat(hat, im, x, y, w, h)
            im = put_glass(glass, im, x, y, w, h)

        frame = im

        ret, jpg = cv2.imencode('.jpg', frame)

        return jpg.tobytes()
