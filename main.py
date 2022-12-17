from SnakeGameClass import SnakeGameClass
from functions import *

cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)

game = SnakeGameClass()

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = findHands(img)

    if hands:
        pointIndex = hands[0]['lmList'][8][0:2]
        img = game.update(img, pointIndex)
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == 27:  # esc
        break
