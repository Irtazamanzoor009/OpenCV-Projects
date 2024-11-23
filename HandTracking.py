import cv2 as cv
import time
import mediapipe as mp

image = cv.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

prevTime = 0
currTime = 0

while True:
    isTrue, frame = image.read()
    frame_resized = cv.resize(frame, (640, 480)) # this is done to maintain 30fps
    imageRGB = cv.cvtColor(frame_resized, cv.COLOR_BGR2RGB)
    results = hands.process(imageRGB)
    # print(results.multi_hand_landmarks)
    
    if results.multi_hand_landmarks:
        for handLandMark in results.multi_hand_landmarks:
            for id, lm in enumerate(handLandMark.landmark):
                h, w, c = frame_resized.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id,cx,cy)
                # if id == 0 or id == 12:
                    # cv.circle(frame_resized, (cx,cy), 25, (0,255,0), -1)
                
            mpDraw.draw_landmarks(frame_resized, handLandMark, mpHands.HAND_CONNECTIONS)
            
    currTime = time.time()
    fps = 1/(currTime-prevTime)
    prevTime = currTime
    
    cv.putText(frame_resized, str(int(fps)), (10,70), cv.FONT_HERSHEY_PLAIN, 3, (0,255,0), 3)
            
    
    if not isTrue:
        print("Frame not loaded correctly")
        break
    
    cv.imshow('Camera',frame_resized)
    key = cv.waitKey(1)
    
    if key == ord('q'):
        print("Exiting...")
        break
    
image.release()
cv.destroyAllWindows()
    