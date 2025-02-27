import numpy
import face_recognition
import cv2 as cv

imageElon = face_recognition.load_image_file("FaceRecognition/images/elon_train.jpeg")
imageElon = cv.cvtColor(imageElon,cv.COLOR_BGR2RGB)

faceLoc = face_recognition.face_locations(imageElon)[0]
faceEncode = face_recognition.face_encodings(imageElon)[0]
# print(faceEncode)
cv.rectangle(imageElon, (faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]), (255,0,255), 2)

imageElonTest = face_recognition.load_image_file("FaceRecognition/images/bill_test.jpeg")
imageElonTest = cv.cvtColor(imageElonTest, cv.COLOR_BGR2RGB)
faceLocTest = face_recognition.face_locations(imageElonTest)[0]
faceEncodeTest = face_recognition.face_encodings(imageElonTest)[0]
cv.rectangle(imageElonTest,(faceLocTest[3],faceLocTest[0]),(faceLocTest[1],faceLocTest[2]), (255,0,255), 2)

results = face_recognition.compare_faces([faceEncode],faceEncodeTest)
faceDist = face_recognition.face_distance([faceEncode],faceEncodeTest)
print(results, faceDist)


cv.imshow("elon",imageElon)
cv.imshow("elon test", imageElonTest)
cv.waitKey(0)