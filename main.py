import cv2
import pickle


width, height = 50, 22
try:
    with open('carParkingpos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList =[]

def mouseclick(events,x,y,flags,params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x,y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i,pos in enumerate(posList):
            x1,y1 = pos
            if x1<x<x1+width and y1<y<y1+height:
                posList.pop(i)
    with open('carParkingpos', 'wb') as f:
        pickle.dump(posList, f)


while True:
    #cv2.rectangle(image,(150,130),(100,108),(225,0,255),1)q

    image = cv2.imread("carparking1.jpg")
    image = cv2.resize(image, (1000, 550))
    for pos in posList:
        cv2.rectangle(image, pos,(pos[0] + width, pos[1] + height), (225, 0, 255), 1)
    cv2.imshow("Image",image)
    cv2.setMouseCallback("Image",mouseclick)
    if cv2.waitKey(1)==ord("q"):
        break
