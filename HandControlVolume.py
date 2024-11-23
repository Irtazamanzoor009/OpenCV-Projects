import numpy as np
import cv2 as cv
import time
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

camWidth = 640
camHeight = 480

camera = cv.VideoCapture(0)
camera.set(3, camWidth)
camera.set(4, camHeight)

currTime = 0
prevTime = 0

detector = htm.handDetector()

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volumeRange = volume.GetVolumeRange()
minVol = volumeRange[0]
maxVol = volumeRange[1]
# volume.SetMasterVolumeLevel(-74.0,None)

while True:
    isTrue, frame = camera.read()
    frame = cv.flip(frame,1)
    if not isTrue:
        print("Error Frame Loading...")
        break

    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame)
    if len(lmList) != 0:
        # print(lmList[4], lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2)//2, (y1 + y2)//2

        cv.circle(frame, (x1, y1), 10, (0, 255, 0), -1)
        cv.circle(frame, (x2, y2), 10, (0, 255, 0), -1)
        cv.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv.circle(frame, (cx, cy), 10, (0, 255, 0), -1)
        
        length = math.hypot(x2-x1, y2-y1)
        # print(length)
        
        # Hand Range 20 - 240
        # Volume Range -74 0
        
        vol = np.interp(length, [20,180], [minVol, maxVol])
        # print(vol)
        volume.SetMasterVolumeLevel(vol,None)
        
        if length < 20:
            cv.circle(frame, (cx, cy), 10, (0, 0, 255), -1)


    currTime = time.time()
    fps = 1/(currTime-prevTime)
    prevTime = currTime

    cv.putText(frame, f'FPS: {int(fps)}', (20, 60),
               cv.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

    cv.imshow('Camera', frame)

    key = cv.waitKey(1)

    if key == ord('q'):
        print('Exiting...')
        break
