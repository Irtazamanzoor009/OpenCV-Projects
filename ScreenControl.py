import cv2 as cv
import time
import HandTrackingModule as htm
import math
# import pyautogui
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import keyboard

camWidth = 640
camHeight = 480

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
# print("volume is................",volume.GetMasterVolumeLevelScalar())

camera = cv.VideoCapture(0)
camera.set(3, camWidth)
camera.set(4, camHeight)

prev_x, prev_y = 0,0
detector = htm.handDetector()

while True:
    isTrue, frame = camera.read()
    
    if not isTrue:
        print("Error loading frame...")
        break
    frame = cv.flip(frame,1)
    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame)
    
    if len(lmList) != 0:        
        x,y = lmList[8][1], lmList[8][2]        
        diff_x = x - prev_x
        diff_y = y - prev_y
        
        if abs(diff_x) > abs(diff_y):  # ...............horizontal...............
            
            if diff_x > 20: # ...........right..............
                
                cv.putText(frame, "Right", (20, 60), cv.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
                keyboard.press_and_release("win+ctrl+right")
                
            elif diff_x < -20: # .............left.............
                
                cv.putText(frame, "Left", (20, 60), cv.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
                keyboard.press_and_release("win+ctrl+left")
                
        else:  # .................vertical..............
            
            if diff_y > 20: # ..............downward.................
                
                cv.putText(frame, "Down", (20, 60), cv.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
                current_volume = volume.GetMasterVolumeLevelScalar()
                new_volume = max(min(current_volume - 0.1, 1.0), 0.0)  # Ensure it's between 0.0 and 1.0
                volume.SetMasterVolumeLevelScalar(new_volume, None)
                
            elif diff_y < -20: # ................upward.................
                
                cv.putText(frame, "Up", (20, 60), cv.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
                volume.SetMasterVolumeLevelScalar(min(volume.GetMasterVolumeLevelScalar() + 0.1, 1.0), None)
                
        prev_x = x
        prev_y = y
        
    cv.imshow('Camera',frame)
    
    key = cv.waitKey(1)
    
    if key == ord('q'):
        print('Exiting...')
        break
