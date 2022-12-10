import math
import random
import cv2
import numpy as np
import mediapipe as mp

cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)


def text(img, text, pos, scale, color, thickness, stroke):
    cv2.putText(img, text, pos, cv2.FONT_HERSHEY_SIMPLEX, scale,
                (0, 0, 0), thickness + stroke)
    cv2.putText(img, text, pos, cv2.FONT_HERSHEY_SIMPLEX, scale,
                color, thickness)


def pic(imgBack, imgFront, pos):
    hf, wf, cf = imgFront.shape
    hb, wb, cb = imgBack.shape
    *_, mask = cv2.split(imgFront)
    maskBGRA = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGRA)
    maskBGR = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    imgRGBA = cv2.bitwise_and(imgFront, maskBGRA)
    imgRGB = cv2.cvtColor(imgRGBA, cv2.COLOR_BGRA2BGR)

    imgMaskFull = np.zeros((hb, wb, cb), np.uint8)
    imgMaskFull[pos[1]:hf + pos[1], pos[0]:wf + pos[0], :] = imgRGB
    imgMaskFull2 = np.ones((hb, wb, cb), np.uint8) * 255
    maskBGRInv = cv2.bitwise_not(maskBGR)
    imgMaskFull2[pos[1]:hf + pos[1], pos[0]:wf + pos[0], :] = maskBGRInv

    return cv2.bitwise_or(cv2.bitwise_and(imgBack, imgMaskFull2), imgMaskFull)


def findHands(img):
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = detector.process(imgRGB)
    allHands = []
    h, w, c = img.shape
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            myHand = {}
            ## lmList
            mylmList = []
            xList = []
            yList = []
            for id, lm in enumerate(handLms.landmark):
                px, py, pz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                mylmList.append([px, py, pz])
                xList.append(px)
                yList.append(py)
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            boxW, boxH = xmax - xmin, ymax - ymin
            bbox = xmin, ymin, boxW, boxH
            cx, cy = bbox[0] + (bbox[2] // 2), \
                     bbox[1] + (bbox[3] // 2)

            myHand["lmList"] = mylmList
            myHand["bbox"] = bbox
            myHand["center"] = (cx, cy)
            allHands.append(myHand)
    return allHands, img


detector = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=1,
                                    min_detection_confidence=0.8,
                                    min_tracking_confidence=0.5)


class SnakeGameClass:
    def __init__(self):
        self.points = []  # all points of the snake
        self.lengths = []  # distance between each point
        self.currentLength = 0  # total length of the snake
        self.allowedLength = 150  # total allowed Length
        self.previousHead = 0, 0  # previous head point

        self.fruitSet = 0
        self.imgFood = pics[self.fruitSet][random.randint(0, 15)]
        self.hFood, self.wFood, _ = self.imgFood.shape
        self.foodPoint = random.randint(100, 1000), random.randint(100, 600)

        self.score = 0
        self.record = 0
        self.gameOver = False
        self.gameStarted = False

    def update(self, imgMain, currentHead):
        if not self.gameStarted:
            text(imgMain, "Hello! In this game you", [75, 100], 3, (129, 129, 243), 5, 7)
            text(imgMain, "need to collect fruits", [125, 200], 3, (129, 129, 243), 5, 7)
            text(imgMain, "by your hand!", [300, 300], 3, (129, 129, 243), 5, 7)
            text(imgMain, "If you are ready press", [105, 500], 3, (129, 129, 243), 5, 7)
            text(imgMain, "Space", [500, 600], 3, (208, 255, 234), 5, 7)
        elif self.gameOver:
            text(imgMain, f"Score: {self.score}", [10, 50], 2, (208, 255, 234), 5, 6)
            text(imgMain, f"Record: {self.record}", [900, 50], 2, (211, 225, 149), 5, 6)
            text(imgMain, "Game Over", [200, 400], 5, (129, 129, 243), 10, 14)
        else:
            text(imgMain, f"Score: {self.score}", [10, 50], 2, (208, 255, 234), 5, 6)
            text(imgMain, f"Record: {self.record}", [900, 50], 2, (211, 225, 149), 5, 6)
            px, py = self.previousHead
            cx, cy = currentHead

            self.points.append([cx, cy])
            distance = math.hypot(cx - px, cy - py)
            self.lengths.append(distance)
            self.currentLength += distance
            self.previousHead = cx, cy

            # Length Reduction
            if self.currentLength > self.allowedLength:
                for i, length in enumerate(self.lengths):
                    self.currentLength -= length
                    self.lengths.pop(i)
                    self.points.pop(i)
                    if self.currentLength < self.allowedLength:
                        break

            # Check if snake ate the Food
            rx, ry = self.foodPoint
            if rx - self.wFood // 2 < cx < rx + self.wFood // 2 and ry - self.hFood // 2 < cy < ry + self.hFood // 2:
                self.imgFood = pics[self.fruitSet][random.randint(0, 15)]
                self.allowedLength += 50
                self.score += 1
                self.record = max(self.score, self.record)
                self.foodPoint = random.randint(100, 1000), random.randint(100, 600)
                print(self.score)

            # Draw Snake
            if self.points:
                for i, point in enumerate(self.points):
                    if i != 0:
                        cv2.line(imgMain, self.points[i - 1], self.points[i], (0, 0, 255), 20)
                cv2.circle(imgMain, self.points[-1], 20, (0, 255, 0), cv2.FILLED)

            # Draw Food
            imgMain = pic(imgMain, self.imgFood, (rx - self.wFood // 2, ry - self.hFood // 2))

            # Check for Collision
            pts = np.array(self.points[:-2], int)
            pts = pts.reshape((-1, 1, 2))
            minDist = cv2.pointPolygonTest(pts, (cx, cy), True)

            if -1 <= minDist <= 1:
                print("Hit")
                self.gameOver = True
                self.score = 0
                self.points = []  # all points of the snake
                self.lengths = []  # distance between each point
                self.currentLength = 0  # total length of the snake
                self.allowedLength = 150  # total allowed Length
                self.previousHead = 0, 0  # previous head point
                self.foodPoint = random.randint(100, 1000), random.randint(100, 600)
        return imgMain


pics = [[cv2.imread("Pictures/Fruits/banana.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Fruits/blueberries.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Fruits/cherries.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Fruits/grapes.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Fruits/green-apple.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Fruits/kiwi.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Fruits/lemon.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Fruits/mango.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Fruits/melon.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Fruits/peach.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Fruits/pear.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Fruits/pineapple.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Fruits/red-apple.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Fruits/strawberry.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Fruits/tangerine.png", cv2.IMREAD_UNCHANGED),
         cv2.imread("Pictures/Fruits/watermelon.png", cv2.IMREAD_UNCHANGED)]]
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
    if key == ord('r'):
        game.gameOver = False
    elif key == 32:
        game.gameStarted = True
    elif key == 27:
        break