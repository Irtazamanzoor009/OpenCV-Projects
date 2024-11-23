import cv2 as cv
from cvzone.HandTrackingModule import HandDetector

camera = cv.VideoCapture(0)
camera.set(3, 1280)
camera.set(4, 720)

detector = HandDetector(detectionCon=0.8)
colorR = 255, 0, 255
cx, cy, w, h = 50, 50, 200, 200
while True:
    isTrue, frame = camera.read()

    if not isTrue:
        print("Frame not loaded correctly...")
        break

    frame = cv.flip(frame, 1)

    hands, frame = detector.findHands(frame)
    if hands:
        hand = hands[0]
        lmList = hand['lmList']
        cursor = lmList[8]
        # print(cursor)
        
        l,_,_ = detector.findDistance(lmList[8][0:2],lmList[12][0:2],frame) # lmlist[8][0:2] means 8 is the tip of first finger and in it x,y total are x,y,z print this as a sample lmlist[8][:]
        # print(l)
        if l < 40:        
            if cx-w//2 < cursor[0] < cx+w//2 and cy-h//2 < cursor[1] < cy+h//2:
                colorR = 0, 255, 0
                cx, cy = cursor[0], cursor[1]
        else:
            colorR = 255, 0, 255

    # cv.rectangle(frame, (cx,cy), (w,h), colorR , -1)
    cv.rectangle(frame, (cx-w//2, cy-h//2), (cx+w//2, cy+h//2), colorR, -1)

    cv.imshow('Camera', frame)

    key = cv.waitKey(1)

    if key == ord('q'):
        print('Exiting...')
        break
