import cv2 as cv
import time
import mediapipe as mp


class handDetector():
    def __init__(self, mode=False, maxHands=1, detectionConfidence=0.5, trackingConfidence=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionConfidence = detectionConfidence
        self.trackingConfidence = trackingConfidence

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode,max_num_hands=self.maxHands, min_detection_confidence=self.detectionConfidence, min_tracking_confidence=self.trackingConfidence)
        self.mpDraw = mp.solutions.drawing_utils
        
    def findHands(self, img, draw = True):
        resize_img = cv.resize(img, (640, 480))
        imageRGB = cv.cvtColor(resize_img, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)

        if self.results.multi_hand_landmarks:
            for handLandMark in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(resize_img,handLandMark, self.mpHands.HAND_CONNECTIONS)
        
        return resize_img
                
    def findPosition(self, img, handNo=0):
        landMarkList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                landMarkList.append([id,cx,cy])
        return landMarkList

def main():
    image = cv.VideoCapture(0)
    prevTime = 0
    currTime = 0
    detect = handDetector()
    while True:
        isTrue, frame = image.read() 
              
        if not isTrue:
            print("Frame not loaded correctly")
            break
        
        img = detect.findHands(frame,draw=True)
        lmlist = detect.findPosition(img)
        if len(lmlist) != 0:
            print(lmlist[4])
        
        currTime = time.time()
        fps = 1/(currTime-prevTime)
        prevTime = currTime

        cv.putText(img, str(int(fps)), (10, 70), cv.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)    

        cv.imshow('Camera', img)
        key = cv.waitKey(1)

        if key == ord('q'):
            print("Exiting...")
            break

if __name__ == "__main__":
    main()
