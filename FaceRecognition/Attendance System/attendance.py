import numpy as np
import face_recognition
import cv2 as cv
import os

path = "Attendance System/images"
images = []
classNames = []

myList = os.listdir(path)

for img in myList:
    currImg = cv.imread(f"{path}/{img}")
    images.append(currImg)
    classNames.append(os.path.splitext(img)[0])

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnown = findEncodings(images)
print("Encoding Completed")

camera = cv.VideoCapture(0)

while True:
    isTrue, frame = camera.read()
    if not isTrue:
        print("Frame Not Loaded Successfully...")
        break

    frameS = cv.resize(frame, (0,0), None, 0.25,0.25)
    frameS = cv.cvtColor(frameS, cv.COLOR_BGR2RGB)

    facesLoc = face_recognition.face_locations(frameS)
    encode = face_recognition.face_encodings(frameS,facesLoc)

    for currEncode, currFaceLoc in zip(encode, facesLoc):
        matches = face_recognition.compare_faces(encodeListKnown, currEncode)
        faceDis = face_recognition.face_distance(encodeListKnown,currEncode)

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            
            y1,x2, y2,x1 = currFaceLoc
            y1,x2, y2,x1 = y1*4, x2*4, y2*4, x1*4
            cv.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
            cv.rectangle(frame, (x1, y2-35), (x2,y2), (0,255,0), cv.FILLED)
            cv.putText(frame, name, (x1+6, y2-6), cv.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)

    cv.imshow("Camera", frame)

    key = cv.waitKey(1)
    if key == ord('q'):
        print("Exiting...")
        break

camera.release()
cv.destroyAllWindows()