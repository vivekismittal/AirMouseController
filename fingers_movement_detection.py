import math
import hand_tracking as ht
import cv2
import numpy as np
import pyautogui as gui

                        ###################
                        #### VARIABLES ####
                        ###################

scrnWidth,scrnHeight=gui.size()
oldPoint,newPoint=[0,0],[0,0]
screenResolutionRatio=2
frmWidth,frmHeight=(640,480)
draw=1
click=1
first=1
smoothening=7
mouseControlRange=[frmWidth-50,frmHeight-80]
printStatement=''

cap = cv2.VideoCapture(0)
handDetect=ht.handDetector(maxHands=1)

x1,y1,x2,y2,x3,y3=0,0,0,0,0,0

while True:
    _,img=cap.read()
    img=cv2.flip(img, 1)

    img=handDetect.findHands(img,draw)
    points=handDetect.findPosition(img)

    if len(points)!=0:
        fingers=handDetect.fingersUp()
        
                            ##############
                            #### MOVE ####
                            ##############
        if fingers[1]==1 and fingers[2]==0 and fingers[3]==0 and fingers[4]==0:
            first=1
            draw=0
            x1,y1=points[8]
            

            x3=np.interp(x1,(50,mouseControlRange[0]),(0,scrnWidth))
            y3=np.interp(y1,(10,mouseControlRange[1]-90),(0,scrnHeight))

            cv2.circle(img, (x1,y1),5,(255,255,0),-1)
            cv2.rectangle(img,(50,10),(mouseControlRange[0],mouseControlRange[1]-90),(0,255,0),3)

            newPoint[0]=oldPoint[0]+(x3-oldPoint[0])/smoothening
            newPoint[1]=oldPoint[1]+(y3-oldPoint[1])/smoothening

            if int(newPoint[0])!=0 or int(newPoint[1])!=0 or int(newPoint[0])<scrnWidth or int(newPoint[1])<scrnHeight:
                gui.moveTo(newPoint[0],newPoint[1])
                printStatement='Moving'
            

                            ####################
                            #### LEFT CLICK ####
                            ####################

        elif fingers[0]==1 and fingers[1]==1 and fingers[2]==1 and fingers[3]==0 and fingers[4]==0:
            draw=0
            first=1


            distance,img,fngInfo=handDetect.findDistance(img,8,12,draw=0)

            if distance<30:
                cv2.circle(img,(fngInfo[4],fngInfo[5]),7,(255,85,58),-1)
                if click:
                    gui.click(newPoint[0], newPoint[1])
                    printStatement='Left Click'
                    click=0
            else:
                click=1
                printStatement=''


                            #####################
                            #### RIGHT CLICK ####
                            #####################

        elif fingers[0]==0 and fingers[1]==1 and fingers[2]==1 and fingers[3]==0 and fingers[4]==0:
            draw=0
            first=1


            distance,img,fngInfo=handDetect.findDistance(img,8,12,draw=0)

            if distance<30:
                cv2.circle(img,(fngInfo[4],fngInfo[5]),7,(0,185,158),-1)
                if click:
                    gui.rightClick(newPoint[0], newPoint[1])
                    printStatement='Right Click'
                    click=0
            else:
                click=1
                printStatement=''

                            ################
                            #### SCROLL ####
                            ################

        elif fingers[1]==1 and fingers[2]==1 and fingers[3]==1 and fingers[4]==0:
            x2,y2=points[12]
            if first:
                x4,y4 = x2,y2
                first=0
            cv2.circle(img,(x2,y2),7,(200,200,0),-1)
            scrollAmount= 20 if y4>y2 else -20

            gui.scroll(scrollAmount)
            printStatement='Scrolling'

        
        else:
            draw=1
            click=1
            printStatement=''

    oldPoint=newPoint
    print(printStatement)
    cv2.imshow('frame',img)

    key=cv2.waitKey(1) 
    if key==27:
        print('Stop')
        break

cap.release()
cv2.destroyAllWindows()
    