import numpy as np
import mediapipe as mp
from config import *

detector = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=1,
                                    min_detection_confidence=0.8,
                                    min_tracking_confidence=0.5)


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
    mylmList = []
    h, w, c = img.shape
    if results.multi_hand_landmarks:
        mylmList = []
        for id, lm in enumerate(results.multi_hand_landmarks[0].landmark):
            px, py, pz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
            mylmList.append([px, py, pz])
    return mylmList, img
