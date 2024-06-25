import random
import cv2
from cvzone.FaceMeshModule import FaceMeshDetector
import cvzone
import os
 
cap = cv2.VideoCapture(0)
cap.set(3, 1200)
cap.set(4, 800)
 
detector = FaceMeshDetector(maxFaces=2)
idList = [0, 17, 78, 292]
 
# import images
folderEatable = r"eatable"
listEatable = os.listdir(folderEatable)
eatables = []
for object in listEatable:
    eatables.append(cv2.imread(f'{folderEatable}/{object}', cv2.IMREAD_UNCHANGED))
 
folderNonEatable = r"oneatable"
listNonEatable = os.listdir(folderNonEatable)
nonEatables = []
for object in listNonEatable:
    nonEatables.append(cv2.imread(f'{folderNonEatable}/{object}', cv2.IMREAD_UNCHANGED))
 
currentObject = eatables[0]
pos = [300, 0]
speed = 15
count = 0
global isEatable
isEatable = True
gameOver = False
 
 
def resetObject():
    global isEatable
    pos[0] = random.randint(100, 700)
    pos[1] = 0
    randNo = random.randint(0, 2)  # change the ratio of eatables/ non-eatables
    if randNo == 0:
        currentObject = nonEatables[random.randint(0, 3)]
        isEatable = False
    else:
        currentObject = eatables[random.randint(0, 3)]
        isEatable = True
 
    return currentObject
 
 
while True:
    success, img = cap.read()
 
    if gameOver is False:
        img, faces = detector.findFaceMesh(img, draw=False)
        img = cvzone.overlayPNG(img, currentObject, pos)
        pos[1] += speed
 
        if pos[1] < 350 and pos[1] > 300 :
            currentObject = resetObject()
 
        if faces:
            face = faces[0]
            # for idNo,point in enumerate(face):
            #     cv2.putText(img,str(idNo),point,cv2.FONT_HERSHEY_COMPLEX,0.7,(255,0,255),1)
 
            up = face[idList[0]]
            down = face[idList[1]]
 
            for id in idList:
                cv2.circle(img, face[id], 3, (0, 0, 0), 1)
            cv2.line(img, up, down, (192, 192, 192), 1)
            cv2.line(img, face[idList[2]], face[idList[3]], (192, 192, 192), 1)
 
            upDown, _ = detector.findDistance(face[idList[0]], face[idList[1]])
            leftRight, _ = detector.findDistance(face[idList[2]], face[idList[3]])
 
            ## Distance of the Object
            cx, cy = (up[0] + down[0]) // 2, (up[1] + down[1]) // 2
            cv2.line(img, (cx, cy), (pos[0] + 50, pos[1] + 50), (192, 192, 192), 1)
            distMouthObject, _ = detector.findDistance((cx, cy), (pos[0] + 50, pos[1] + 50))
            print(distMouthObject)
 
            # Lip opened or closed
            ratio = int((upDown / leftRight) * 100)
            # print(ratio)
            if ratio > 60:
                mouth = "Open"
            else:
                mouth = "Close"
            cv2.putText(img, mouth, (50, 90), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 0, 0), 5)
 
            if distMouthObject < 100 and ratio > 60:
                if isEatable:
                    currentObject = resetObject()
                    count += 1
                else:
                    gameOver = True
        cv2.putText(img, str(count), (850, 90), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0), 5)
    else:
        cv2.putText(img, "Game Over", (200, 300), cv2.FONT_HERSHEY_PLAIN, 7, (255, 0, 0), 10)
        cv2.putText(img, str(count), (500, 600), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0), 5)
    cv2.imshow("test3", img)
    key = cv2.waitKey(1)
 
    if key == ord('r'):
        resetObject()
        gameOver = False
        count = 0
        currentObject = eatables[0]
        isEatable = True
    key1= cv2.waitKey(1)
    if key1 == ord('c'):
        break
