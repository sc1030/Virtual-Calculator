import cv2
from cvzone.HandTrackingModule import HandDetector
import time

class Button:
    def __init__(self,pos,width,height,value):

        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self,img):
        cv2.rectangle(img,self.pos, (self.pos[0]+self.width,self.pos[1]+self.height),
                      (225, 225, 225), cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (50, 50, 50), 3)

        cv2.putText(img, self.value, (self.pos[0] + 40, self.pos[1] + 60), cv2.FONT_HERSHEY_PLAIN,
                    2, (50, 50, 50), 2)


    def checkClick(self,x,y):
        if self.pos[0]<x<self.pos[0] +self.width and \
                self.pos[1] < y < self.pos[1] +self.height:
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                          (255, 255, 255), cv2.FILLED)
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                          (50, 50, 50), 3)

            cv2.putText(img, self.value, (self.pos[0] + 40, self.pos[1] + 80), cv2.FONT_HERSHEY_PLAIN,
                        2, (0, 0, 0), 5)

            return True
        else:
            return False

cap  = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
detector = HandDetector(detectionCon=0.8, maxHands=1)

#Creating Button

# Buttons
buttonListValues = [['7', '8', '9', '*'],
                    ['4', '5', '6', '-'],
                    ['1', '2', '3', '+'],
                    ['0', '/', '.', '=']]

buttonList = []
for x in range(4):
    for y in range(4):
        xpos = x * 100 + 800
        ypos = y * 100 + 150
        buttonList.append(Button((xpos, ypos), 100, 100,
                                 buttonListValues[y][x]))

#variables
myEquation = ''
delayCounter = 0


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img, flipType=False)

     #Draw all Buttons
    cv2.rectangle(img, (800, 70), (800 + 400, 70 + 100),
                  (225, 225, 225), cv2.FILLED)

    cv2.rectangle(img, (800, 70), (800 + 400, 70 + 100),
                  (50, 50, 50), 3)

    for button in buttonList:
        button.draw(img)


# Check for hand
    # Check for hand
    if hands:
        lmList = hands[0]['lmList']

        # Unpack only the first two values (x, y) from lmList[8] and lmList[12]
        length, _, img = detector.findDistance(lmList[8][:2], lmList[12][:2], img)

        # Print the calculated distance
        #print(length)

        # Assign x and y values from lmList[8], ignoring any extra values
        x, y = lmList[8][:2]

        if length<50:
            for i, button in enumerate (buttonList):
                if button.checkClick(x,y) and  delayCounter == 0:
                    myValue = buttonListValues[int(i%4)][int(i/4)]
                    if myValue == "=":
                        myEquation =str(eval(myEquation))
                    else:
                      myEquation += myValue
                    delayCounter = 1

    # Avoid duplicates
    if delayCounter != 0:
        delayCounter += 1
        if delayCounter > 10:
            delayCounter = 0



    #Display the Equation
    cv2.putText(img, myEquation, (810, 130), cv2.FONT_HERSHEY_PLAIN,
                3, (50,50,50), 3)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('c'):
        myEquation = ''





