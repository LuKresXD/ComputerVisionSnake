import math
import random
from functions import *


class SnakeGameClass:
    def __init__(self):
        self.points = []  # all points of the snake
        self.lengths = []  # distance between each point
        self.currentLength = 0  # total length of the snake
        self.allowedLength = 150  # total allowed Length
        self.previousHead = 0, 0  # previous head point

        self.fruitSet = 0
        self.imgFood = food[self.fruitSet][random.randint(0, len(food[self.fruitSet]) - 1)]
        self.hFood, self.wFood, _ = self.imgFood.shape
        self.foodPoint = random.randint(100, 1000), random.randint(100, 600)

        self.score = 0
        self.coins = 0
        self.record = 0
        self.skin = 0
        self.purchased = [0]
        self.sets = [0]
        self.gameOver = False
        self.gameStarted = False
        self.shopEnabled = False
        self.shopSection = 0

        self.cnt = 0

    def update(self, imgMain, currentHead):
        cx, cy = currentHead
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
                    self.shopSection = 0
            elif 204 < cx < 358 and 130 < cy < 294:  # skin1
                self.cnt += 1
                if self.cnt == 25 and self.coins >= 10 and 1 not in self.purchased:
                    self.cnt = 0
                    self.coins -= 10
                    self.purchased.append(1)
            elif 562 < cx < 716 and 130 < cy < 294:  # skin2
                self.cnt += 1
                if self.cnt == 25 and self.coins >= 10 and 2 not in self.purchased:
                    self.cnt = 0
                    self.coins -= 10
                    self.purchased.append(2)
            elif 920 < cx < 1074 and 130 < cy < 294:  # skin3
                self.cnt += 1
                if self.cnt == 25 and self.coins >= 10 and 3 not in self.purchased:
                    self.cnt = 0
                    self.coins -= 10
                    self.purchased.append(3)
            elif 204 < cx < 358 and 380 < cy < 544:  # skin4
                self.cnt += 1
                if self.cnt == 25 and self.coins >= 10 and 4 not in self.purchased:
                    self.cnt = 0
                    self.coins -= 10
                    self.purchased.append(4)
            elif 562 < cx < 716 and 380 < cy < 544:  # skin5
                self.cnt += 1
                if self.cnt == 25 and self.coins >= 10 and 5 not in self.purchased:
                    self.cnt = 0
                    self.coins -= 10
                    self.purchased.append(5)
            elif 920 < cx < 1074 and 380 < cy < 544:  # skin6
                self.cnt += 1
                if self.cnt == 25 and self.coins >= 10 and 6 not in self.purchased:
                    self.cnt = 0
                    self.coins -= 10
                    self.purchased.append(6)
            else:
                self.cnt = 0
        elif self.shopSection == 2:
            text(imgMain, "Food sets", [10, 50], 2, (208, 255, 234), 5, 6)
            text(imgMain, f"{self.coins}", [1100, 50], 2, (211, 225, 149), 5, 6)
            imgMain = pic(imgMain, coin, (1225, 7))
            imgMain = pic(imgMain, back, (25, 560))
            if 1 not in self.sets:
                imgMain = pic(imgMain, food1, (221, 100))
            else:
                imgMain = pic(imgMain, food_purchased, (221, 100))
            if 2 not in self.sets:
                imgMain = pic(imgMain, food2, (750, 100))
            else:
                imgMain = pic(imgMain, food_purchased, (750, 100))
            if 25 < cx < 309 and 560 < cy < 693:  # back
                self.cnt += 1
                if self.cnt == 25:
                    self.cnt = 0
                    self.shopSection = 0
            elif 221 < cx < 529 and 100 < cy < 624:  # set1
                self.cnt += 1
                if self.cnt == 25 and self.coins >= 50 and 1 not in self.sets:
                    self.cnt = 0
                    self.coins -= 50
                    self.sets.append(1)
            elif 750 < cx < 1058 and 100 < cy < 624:  # set2
                self.cnt += 1
                if self.cnt == 25 and self.coins >= 50 and 2 not in self.sets:
                    self.cnt = 0
                    self.coins -= 50
                    self.sets.append(2)
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
                    self.skin = self.purchased[random.randint(0, len(self.purchased) - 1)]
                    self.fruitSet = random.randint(0, len(self.sets) - 1)
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
                self.imgFood = food[self.fruitSet][random.randint(0, len(food[self.fruitSet]) - 1)]
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
