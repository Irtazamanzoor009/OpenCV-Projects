import numpy as np
import cvzone
import pickle
import cv2 as cv

capture = cv.VideoCapture("carPark.mp4")

width , height = 107, 40

with open("CarParkingPositions","rb") as f:
        posList = pickle.load(f)

def checkParkingSpace(img):
    for pos in posList:
        x,y = pos

        imgCrop = img[y:y+height, x:x+width]
        count = cv.countNonZero(imgCrop)
        cvzone.putTextRect(frame, str(count), (x, y+height - 5), scale=1, thickness=2, offset=0)
        # cv.imshow(str(x*y), imgCrop)

while True:
    if capture.get(cv.CAP_PROP_POS_FRAMES) == capture.get(cv.CAP_PROP_FRAME_COUNT):
        capture.set(cv.CAP_PROP_POS_FRAMES,0)

    isTrue, frame = capture.read()
    

    if not isTrue:
        print("Frame not loaded successfully...")
        break
    frame = cv.resize(frame,(1050,650))

    frameGray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frameBlurr = cv.GaussianBlur(frameGray, (3,3), 1)
    frameThresholding = cv.adaptiveThreshold(frameBlurr, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 25,16)
    frameMedian = cv.medianBlur(frameThresholding, 5)
    kernel = np.ones((3,3), np.uint8)
    frameDilate = cv.dilate(frameMedian, kernel, iterations=1)

    checkParkingSpace(frameDilate)
    for pos in posList:
        cv.rectangle(frame, pos, (pos[0]+width, pos[1]+height) , (255,0,255), 2)


    cv.imshow("Car Parking", frame)
    # cv.imshow("blurr", frameDilate)

    key = cv.waitKey(1)
    if key == ord('q'):
        print("Exiting...")
        break

