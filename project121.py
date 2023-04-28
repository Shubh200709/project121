import cv2
import time
import numpy as np
import keyboard

vid = cv2.VideoCapture(0)
out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'XVID'), 20, (640, 480), )

time.sleep(2)
bg = 0

for i in range(60):
    ret, bg = vid.read()

bg = np.flip(bg, axis = 1)

while vid.isOpened():
    ret,img = vid.read()
    if(not ret):
        break
    img = np.flip(img, axis=1)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    l_black = np.array([30,30,0])
    u_black = np.array([104,153,70])
    mask1 = cv2.inRange(hsv, l_black, u_black)

    l_black = np.array([170,30,0])
    u_black = np.array([180,153,70])
    mask2 = cv2.inRange(hsv, l_black, u_black)

    mask = mask1 + mask2

    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones([3,3],np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones([3,3], np.uint8))
    mask3 = cv2.bitwise_not(mask)

    b1 = cv2.bitwise_and(img, img, mask=mask)
    b2 = cv2.bitwise_and(bg, bg, mask=mask3)
    b = cv2.addWeighted(b1,1,b2,1,0)

    out.write(b)
    cv2.imshow('cloak',b)
    cv2.waitKey(1)
    if(keyboard.is_pressed('q') or keyboard.is_pressed('Esc')):
        break
        out.release()
        vid.release()
        cv2.destroyAllWindows()

out.release()
vid.release()
cv2.destroyAllWindows()