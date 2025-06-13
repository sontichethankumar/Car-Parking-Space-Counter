import cv2
import pickle
import cvzone
import numpy as np

    #video feed
cap = cv2.VideoCapture("Carparking.mp4")

with open('carParkingpos', 'rb') as f:
    posList = pickle.load(f)

width, height = 50, 19

def checkParkingSpace(imgpro):
    spaceCounter = 0



    for pos in posList:
        x,y = pos

        imgCrop = imgpro[y:y+height,x:x+width]
        #cv2.imshow(str(x*y),imgCrop)
        count = cv2.countNonZero(imgCrop)

        if count < 170:
            color = (0,255,0)
            thickness= 2
            spaceCounter +=1
        else:
            color = (0,0,255)
            thickness =1
        cv2.rectangle(image, pos, (pos[0] + width, pos[1] + height), color, thickness)
        cvzone.putTextRect(image, str(count), (x, y + height - 10), scale=0.7,
                           thickness=1, offset=0, colorR=color)


    cvzone.putTextRect(image, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=3,
                       thickness=5, offset=10, colorR=(0, 200, 0))
while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
         cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    success, image = cap.read()
    image = cv2.resize(image, (1000, 550))
    imgGray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    imageBlur = cv2.GaussianBlur(imgGray,(3, 3),1)
    imgThreshold = cv2.adaptiveThreshold(imageBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold,5)
    kernel = np.ones((3,3), np.int8)
    imgDIlate = cv2.dilate(imgMedian, kernel, iterations=1)
    checkParkingSpace(imgDIlate)
    #for pos in posList:
    cv2.imshow("Image",image)
    #cv2.imshow("ImageBlur", imageBlur)
    #cv2.imshow("ImageThreshold", imgMedian)
    if cv2.waitKey(50)==ord("q"):
        break