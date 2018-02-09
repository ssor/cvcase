import cv2
import numpy as np

cap = cv2.VideoCapture(0)


def nothing(x):
    pass


lower = np.array([0, 90, 33])
upper = np.array([255, 255, 255])
cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('LowerH', 'image', 0, 255, nothing)
cv2.createTrackbar('LowerS', 'image', 0, 255, nothing)
cv2.createTrackbar('LowerV', 'image', 0, 255, nothing)
cv2.createTrackbar('UpperH', 'image', 127, 255, nothing)
cv2.createTrackbar('UpperS', 'image', 55, 255, nothing)
cv2.createTrackbar('UpperV', 'image', 255, 255, nothing)

while (1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV


    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower, upper)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('res', res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
    lower_h = cv2.getTrackbarPos('LowerH', 'image')
    lower_s = cv2.getTrackbarPos('LowerS', 'image')
    lower_v = cv2.getTrackbarPos('LowerV', 'image')
    lower = np.array([lower_h, lower_s, lower_v])

    upper_h = cv2.getTrackbarPos('UpperH', 'image')
    upper_s = cv2.getTrackbarPos('UpperS', 'image')
    upper_v = cv2.getTrackbarPos('UpperV', 'image')
    upper = np.array([upper_h, upper_s, upper_v])

cv2.destroyAllWindows()
