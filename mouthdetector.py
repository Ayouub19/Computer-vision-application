import cv2
from cvzone.FaceMeshModule import FaceMeshDetector
import cvzone
cap = cv2.VideoCapture(0)
cap.set(3,1000)
cap.set(4,800)
detector = FaceMeshDetector(maxFaces=1)
idlist=[0,17,78,292]
while True:
    success , img = cap.read()
    img , faces = detector.findFaceMesh(img,draw=False)
    if faces:
        face=faces[0]
        for id in idlist:
            cv2.circle(img,face[id],3,(0,255,0),5)
        cv2.line(img,face[idlist[0]],face[idlist[1]],(255,0,255),3)
        cv2.line(img,face[idlist[2]],face[idlist[3]],(255,0,255),3)
        updown, _  = detector.findDistance(face[idlist[0]],face[idlist[1]])
        leftright, _ = detector.findDistance(face[idlist[2]],face[idlist[3]])
        r=int((updown/leftright)*100)
        print(r)
        if r>60:
            mouth = "OPEN"
        else:
            mouth= "CLOSE"
        cv2.putText(img,mouth,(40,70),cv2.FONT_HERSHEY_TRIPLEX,2.5,(192,72,48),2)
    cv2.imshow("test2",img)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break
