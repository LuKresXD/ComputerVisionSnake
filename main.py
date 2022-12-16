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
            cx, cy = bbox[0] + (bbox[2] // 2), bbox[1] + (bbox[3] // 2)

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
        self.imgFood = food[self.fruitSet][random.randint(0, 15)]
        self.hFood, self.wFood, _ = self.imgFood.shape
        self.foodPoint = random.randint(100, 1000), random.randint(100, 600)

        self.score = 0
        self.coins = 100
        self.record = 0
        self.skin = 0
        self.purchased = [0]
        self.gameOver = False
        self.gameStarted = False
        self.shopEnabled = False
        self.shopSection = 0

        self.cnt = 0

    def update(self, imgMain, currentHead):
        cx, cy = currentHead
        # print(cx, cy)
        if not self.gameStarted:
            text(imgMain, "Hello! In this game you", [75, 100], 3, (129, 129, 243), 5, 7)
            text(imgMain, "need to collect fruits", [125, 200], 3, (129, 129, 243), 5, 7)
            text(imgMain, "by your hand!", [300, 300], 3, (129, 129, 243), 5, 7)
            text(imgMain, "If you are ready hold", [105, 500], 3, (129, 129, 243), 5, 7)
            imgMain = pic(imgMain, play, (500, 550))
            if 525 < cx < 809 and 550 < cy < 683:
                self.cnt += 1
            else:
                self.cnt = 0
            if self.cnt == 25:
                self.cnt = 0
                self.gameStarted = True
        elif self.shopSection == 1:
            text(imgMain, "Skins", [10, 50], 2, (208, 255, 234), 5, 6)
            text(imgMain, f"{self.coins}", [1100, 50], 2, (211, 225, 149), 5, 6)
            imgMain = pic(imgMain, coin, (1225, 7))
            imgMain = pic(imgMain, back, (25, 560))
            if 1 not in self.purchased:
                imgMain = pic(imgMain, skin1, (204, 130))
            else:
                imgMain = pic(imgMain, purchased, (204, 130))
            if 2 not in self.purchased:
                imgMain = pic(imgMain, skin2, (562, 130))
            else:
                imgMain = pic(imgMain, purchased, (562, 130))
            if 3 not in self.purchased:
                imgMain = pic(imgMain, skin3, (920, 130))
            else:
                imgMain = pic(imgMain, purchased, (920, 130))
            if 4 not in self.purchased:
                imgMain = pic(imgMain, skin4, (204, 380))
            else:
                imgMain = pic(imgMain, purchased, (204, 380))
            if 5 not in self.purchased:
                imgMain = pic(imgMain, skin5, (562, 380))
            else:
                imgMain = pic(imgMain, purchased, (562, 380))
            if 6 not in self.purchased:
                imgMain = pic(imgMain, skin6, (920, 380))
            else:
                imgMain = pic(imgMain, purchased, (920, 380))
            if 25 < cx < 309 and 560 < cy < 693:  # back
                self.cnt += 1
                if self.cnt == 25:
                    self.cnt = 0
                    self.coins -= 10
                    self.shopSection = 0
            elif 204 < cx < 358 and 130 < cy < 294:  # skin1
                self.cnt += 1
                if self.cnt == 25 and self.coins >= 10:
                    self.cnt = 0
                    self.coins -= 10
                    self.purchased.append(1)
            elif 562 < cx < 716 and 130 < cy < 294:  # skin2
                self.cnt += 1
                if self.cnt == 25 and self.coins >= 10:
                    self.cnt = 0
                    self.coins -= 10
                    self.purchased.append(2)
            elif 920 < cx < 1074 and 130 < cy < 294:  # skin3
                self.cnt += 1
                if self.cnt == 25 and self.coins >= 10:
                    self.cnt = 0
                    self.coins -= 10
                    self.purchased.append(3)
            elif 204 < cx < 358 and 380 < cy < 544:  # skin4
                self.cnt += 1
                if self.cnt == 25 and self.coins >= 10:
                    self.cnt = 0
                    self.coins -= 10
                    self.purchased.append(4)
            elif 562 < cx < 716 and 380 < cy < 544:  # skin5
                self.cnt += 1
                if self.cnt == 25 and self.coins >= 10:
                    self.cnt = 0
                    self.coins -= 10
                    self.purchased.append(5)
            elif 920 < cx < 1074 and 380 < cy < 544:  # skin6
                self.cnt += 1
                if self.cnt == 25 and self.coins >= 10:
                    self.cnt = 0
                    self.coins -= 10
                    self.purchased.append(6)
            else:
                self.cnt = 0

        elif self.shopEnabled:
            text(imgMain, "Shop", [10, 50], 2, (208, 255, 234), 5, 6)
            text(imgMain, f"{self.coins}", [1100, 50], 2, (211, 225, 149), 5, 6)
            imgMain = pic(imgMain, coin, (1225, 7))
            imgMain = pic(imgMain, back, (25, 560))
            imgMain = pic(imgMain, skin, (226, 200))
            imgMain = pic(imgMain, foodi, (772, 200))
            if 25 < cx < 309 and 560 < cy < 693:  # back
                self.cnt += 1
                if self.cnt == 25:
                    self.cnt = 0
                    self.shopEnabled = False
            elif 226 < cx < 526 and 200 < cy < 520:  # skin
                self.cnt += 1
                if self.cnt == 25:
                    self.cnt = 0
                    self.shopSection = 1
            elif 752 < cx < 1052 and 200 < cy < 520:  # food
                self.cnt += 1
                if self.cnt == 25:
                    self.cnt = 0
                    self.shopSection = 2
            else:
                self.cnt = 0

        elif self.gameOver:
            text(imgMain, f"Score: {self.score}", [10, 50], 2, (208, 255, 234), 5, 6)
            text(imgMain, f"Record: {self.record}", [900, 50], 2, (211, 225, 149), 5, 6)
            imgMain = pic(imgMain, game_over, (220, 125))
            imgMain = pic(imgMain, shop, (500, 400))
            imgMain = pic(imgMain, restart, (500, 550))
            if 500 < cx < 784 and 400 < cy < 533:  # shop
                self.cnt += 1
                if self.cnt == 25:
                    self.cnt = 0
                    self.shopEnabled = True
            elif 500 < cx < 784 and 550 < cy < 683:  # restart
                self.cnt += 1
                if self.cnt == 25:
                    self.cnt = 0
                    game.skin = self.purchased[random.randint(0, len(self.purchased) - 1)]
                    self.gameOver = False
            else:
                self.cnt = 0
        else:
            text(imgMain, f"Score: {self.score}", [10, 50], 2, (208, 255, 234), 5, 6)
            text(imgMain, f"Record: {self.record}", [900, 50], 2, (211, 225, 149), 5, 6)
            px, py = self.previousHead

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
            if rx - self.wFood // 2 < cx < rx + self.wFood // 2 and \
                    ry - self.hFood // 2 < cy < ry + self.hFood // 2:
                self.imgFood = food[self.fruitSet][random.randint(0, 15)]
                self.allowedLength += 50
                self.score += 1
                self.coins += 1
                self.record = max(self.score, self.record)
                self.foodPoint = random.randint(100, 1000), random.randint(100, 600)
                print(self.score)

            # Draw Snake
            if self.points:
                size = len(self.points)
                colors = (np.linspace(skins[self.skin][0][0], skins[self.skin][1][0], size),
                          np.linspace(skins[self.skin][0][1], skins[self.skin][1][1], size),
                          np.linspace(skins[self.skin][0][2], skins[self.skin][1][2], size))
                for i, point in enumerate(self.points):
                    if i != 0:
                        cv2.line(imgMain, self.points[i - 1], self.points[i],
                                 (colors[0][i], colors[1][i], colors[2][i]), 20)
                cv2.circle(imgMain, self.points[-1], 20, skins[self.skin][1], cv2.FILLED)

            # Draw Food
            imgMain = pic(imgMain, self.imgFood, (rx - self.wFood // 2, ry - self.hFood // 2))

            # Check for Collision
            pts = np.array(self.points[:-2], int)
            pts = pts.reshape((-1, 1, 2))
            minDist = cv2.pointPolygonTest(pts, (cx, cy), True)

            if -1 <= minDist <= 1 and self.score > 0:
                print("Hit")
                self.gameOver = True
                self.score = 0
                self.points = []  # all points of the snake
                self.lengths = []  # distance between each point
                self.currentLength = 0  # total length of the snake
                self.allowedLength = 150  # total allowed Length
                self.previousHead = 0, 0  # previous head point
                self.foodPoint = random.randint(100, 1000), random.randint(100, 600)
        if self.gameOver or not self.gameStarted:
            try:
                imgMain = pic(imgMain, cursor, (cx, cy))
            except:
                pass
        return imgMain


food = [[cv2.imread("Pictures/Fruits/banana.png", cv2.IMREAD_UNCHANGED),
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

cursor = cv2.imread("Pictures/GUI/cursor.png", cv2.IMREAD_UNCHANGED)
play = cv2.imread("Pictures/GUI/play.png", cv2.IMREAD_UNCHANGED)
restart = cv2.imread("Pictures/GUI/restart.png", cv2.IMREAD_UNCHANGED)
game_over = cv2.imread("Pictures/GUI/game_over.png", cv2.IMREAD_UNCHANGED)
coin = cv2.imread("Pictures/GUI/coin.png", cv2.IMREAD_UNCHANGED)
back = cv2.imread("Pictures/GUI/back.png", cv2.IMREAD_UNCHANGED)
shop = cv2.imread("Pictures/GUI/shop.png", cv2.IMREAD_UNCHANGED)
skin = cv2.resize(cv2.imread("Pictures/GUI/skin.png", cv2.IMREAD_UNCHANGED), (300, 320))
foodi = cv2.resize(cv2.imread("Pictures/GUI/food.png", cv2.IMREAD_UNCHANGED), (300, 320))

skin1 = cv2.imread("Pictures/GUI/skins/first.png", cv2.IMREAD_UNCHANGED)
skin2 = cv2.imread("Pictures/GUI/skins/second.png", cv2.IMREAD_UNCHANGED)
skin3 = cv2.imread("Pictures/GUI/skins/third.png", cv2.IMREAD_UNCHANGED)
skin4 = cv2.imread("Pictures/GUI/skins/fourth.png", cv2.IMREAD_UNCHANGED)
skin5 = cv2.imread("Pictures/GUI/skins/fifth.png", cv2.IMREAD_UNCHANGED)
skin6 = cv2.imread("Pictures/GUI/skins/sixth.png", cv2.IMREAD_UNCHANGED)
purchased = cv2.imread("Pictures/GUI/skins/purchased.png", cv2.IMREAD_UNCHANGED)

skins = [[(200, 200, 200), (50, 50, 50)],
         [(31, 64, 55), (200, 242, 153)],
         [(199, 195, 189), (80, 62, 44)],
         [(199, 167, 217), (220, 252, 255)],
         [(195, 96, 131), (145, 191, 46)],
         [(125, 92, 252), (251, 130, 106)],
         [(142, 153, 17), (125, 239, 56)]]

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
    if key == ord('b') and game.gameOver and game.gameStarted:
        game.shopEnabled = True
    elif key == 27:  # esc
        break
    if game.shopEnabled:
        if game.shopSection == 0:
            if key == ord('1'):
                game.shopSection = 1
            elif key == ord('2'):
                game.shopSection = 2
            elif key == 127:  # backspace
                game.shopEnabled = False
        elif game.shopSection == 1:
            if key == 127:  # backspace
                game.shopEnabled = 0
        elif game.shopSection == 2:
            if key == 127:  # backspace
                game.shopEnabled = 0
