import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
import cvzone
import numpy as np

camera = cv.VideoCapture(0)
camera.set(3, 1280)
camera.set(4, 720)

detector = HandDetector(detectionCon=0.8)


class DragRect():
    def __init__(self, posCenter, size=[200, 200]):
        self.posCenter = posCenter
        self.size = size
        self.colorR = 255, 0, 255

    def Update(self, cursor):
        cx, cy = self.posCenter
        w, h = self.size
        if cx-w//2 < cursor[0] < cx+w//2 and cy-h//2 < cursor[1] < cy+h//2:
            self.colorR = 0, 255, 0
            self.posCenter = cursor[0:2]  # x and y are in this cursor

    def SetClickColor(self, color):
        self.colorR = color

    def GetRectColor(self):
        return self.colorR


rectList = []
for x in range(5):
    rectList.append(DragRect([x*250+150, 150]))

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
        # lmlist[8][0:2] means 8 is the tip of first finger and in it x,y total are x,y,z print this as a sample lmlist[8][:]
        l, _, _ = detector.findDistance(lmList[8][0:2], lmList[12][0:2], frame)
        if l < 40:
            for rect in rectList:
                rect.Update(cursor)
        else:
            for rect in rectList:
                rect.SetClickColor((255, 0, 255))
    
    ## For Draw Solid .....................            
    for rect in rectList:
        cx, cy = rect.posCenter
        w, h = rect.size
        cv.rectangle(frame, (cx-w//2, cy-h//2),
                    (cx+w//2, cy+h//2), rect.GetRectColor(), -1)
        cvzone.cornerRect(frame, (cx-w//2, cy-h//2, w, h), 20, rt=0)
    
    cv.imshow("Camera",frame)
    
    
    ## For Draw Transparency ......................
    # img_new = np.zeros_like(frame, np.uint8)
    # for rect in rectList:
    #     cx, cy = rect.posCenter
    #     w, h = rect.size
    #     cv.rectangle(img_new, (cx-w//2, cy-h//2),
    #                 (cx+w//2, cy+h//2), rect.GetRectColor(), -1)
    #     cvzone.cornerRect(img_new, (cx-w//2, cy-h//2, w, h), 20, rt=0)
    # out = frame.copy()
    # alpha = 0.5
    # mask = img_new.astype(bool)
    # # print(mask.shape)
    # out[mask] = cv.addWeighted(frame, alpha, img_new, 1 - alpha, 0)[mask]
    # cv.imshow('Camera', out)


    key = cv.waitKey(1)

    if key == ord('q'):
        print('Exiting...')
        break
