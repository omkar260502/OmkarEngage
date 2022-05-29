import cv2
import numpy as np
import dlib

webcam = True

cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


def empty(a):
    pass


cv2.namedWindow("BGR")
cv2.resizeWindow("BGR", 640, 240)
cv2.createTrackbar("Blue", 'BGR', 0, 255, empty)
cv2.createTrackbar("Green", 'BGR', 0, 255, empty)
cv2.createTrackbar("Red", 'BGR', 0, 255, empty)
cv2.createTrackbar("Eye", 'BGR', 1, 5, empty)
cv2.createTrackbar("Face Filter", 'BGR', 1, 5, empty)


def createBox(img, points, scale=5, masked=False, cropped=True):
    if masked:
        mask = np.zeros_like(img)
        mask = cv2.fillPoly(mask, [points], (255, 255, 255))
        img = cv2.bitwise_and(img, mask)
        #cv2.imshow('Mask', img)

    if cropped:
        bbox = cv2.boundingRect(points)
        x, y, w, h = bbox
        imgCrop = img[y:y+h, x:x+w]
        imgCrop = cv2.resize(imgCrop, (0, 0), None, scale, scale)
        return imgCrop
    else:
        return mask


while True:

    # if webcam:
    #     sucess, img = cap.read()
    # else:
    #     img = cv2.imread('1.jpg')

    img = cv2.imread('1.jpg')
    img = cv2.resize(img, (700, 700), None, 0.5, 0.5)
    imgOriginal = img.copy()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector(imgGray)

    for face in faces:
        x1, y1 = face.left(), face.top()
        x2, y2 = face.right(), face.bottom()
        #imgOriginal = cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        landmarks = predictor(imgGray, face)
        myPoints = []
        for n in range(68):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            myPoints.append([x, y])
            # cv2.circle(imgOriginal, (x, y), 5, (50, 50, 255), cv2.FILLED)
            # cv2.putText(imgOriginal, str(n), (x, y-10),cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (0, 0, 255), 1)
        myPoints = np.array(myPoints)
        imgFace = createBox(
            img, myPoints[0:27], 3, masked=True, cropped=False)

        imgLips = createBox(
            img, myPoints[48:61], 3, masked=True, cropped=False)

        imgColorLips = np.zeros_like(imgLips)
        imgColorFace = np.zeros_like(imgFace)
        facefilter = cv2.getTrackbarPos("Face Filter", 'BGR')
        b = cv2.getTrackbarPos('Blue', 'BGR')
        g = cv2.getTrackbarPos('Green', 'BGR')
        r = cv2.getTrackbarPos('Red', 'BGR')
        imgColorLips[:] = b, g, r
        imgColorLips = cv2.bitwise_and(imgLips, imgColorLips)
        imgColorLips = cv2.GaussianBlur(imgColorLips, (7, 7), 10)

        # Nicche k 2 uda dene k black n white karte also add gray to line 88/89
        #imgOriginalGray = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2GRAY)
        #imgOriginalGray = cv2.cvtColor(imgOriginalGray, cv2.COLOR_GRAY2BGR)
        imgColorLips = cv2.addWeighted(
            imgOriginal, 1, imgColorLips, 0.289, 0)

        if facefilter == 1:
            imgColorFace = imgColorLips
        elif facefilter == 2:
            imgColorFace[:] = 255, 255, 255
            imgColorFace = cv2.bitwise_and(imgFace, imgColorFace)
            imgColorLips = cv2.GaussianBlur(imgColorFace, (7, 7), 10)
            imgColorFace = cv2.addWeighted(
                imgOriginal, 1, imgColorFace, 0.289, 0)
        elif facefilter == 3:
            imgColorFace[:] = 0, 0, 0
            imgColorFace = cv2.bitwise_and(imgFace, imgColorFace)
            imgColorLips = cv2.GaussianBlur(imgColorFace, (7, 7), 10)
            imgColorFace = cv2.addWeighted(
                imgColorLips, 1, imgColorFace, 0.002, 0)
        elif facefilter == 4:
            imgColorFace[:] = 0, 0, 0
            imgColorFace = cv2.bitwise_and(imgFace, imgColorFace)
            imgColorLips = cv2.GaussianBlur(imgColorFace, (7, 7), 10)
            imgColorFace = cv2.addWeighted(
                imgColorLips, 1, imgColorFace, 0.289, 0)
        elif facefilter == 5:
            imgColorFace[:] = 0, 0, 0
            imgColorFace = cv2.bitwise_and(imgFace, imgColorFace)
            imgColorLips = cv2.GaussianBlur(imgColorFace, (7, 7), 10)
            imgColorFace = cv2.addWeighted(
                imgColorLips, 1, imgColorFace, 0.289, 0)

        cv2.imshow('BGR', imgColorFace)
        #cv2.imshow('upper', imgFaceUpper)

        #cv2.imshow('Lips', imgFaceLower)

        print(myPoints)

    cv2.imshow("Originial", imgOriginal)
    cv2.waitKey(1)
