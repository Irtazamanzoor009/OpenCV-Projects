import cv2 as cv
import pickle

width , height = 107, 40

try:
    with open("CarParkingPositions","rb") as f:
        posList = pickle.load(f)
except:
    posList = []

# posList = []

def mouseClick(events, x, y, flags, params):
    if events == cv.EVENT_LBUTTONDOWN:
        posList.append((x,y))
    
    if events == cv.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1+width and y1 < y < y1 + height:
                posList.pop(i)

    with open("CarParkingPositions","wb") as f:
        pickle.dump(posList, f)

while True:
    img = cv.imread("carParkImg.png")
    img = cv.resize(img, (1050,650))
    for pos in posList:
        cv.rectangle(img, pos, (pos[0]+width, pos[1]+height) , (255,0,255), 2)

    cv.imshow("Image",img)

    cv.setMouseCallback("Image", mouseClick)


    key = cv.waitKey(1)

    if key == ord('q'):
        print("Exiting")
        break