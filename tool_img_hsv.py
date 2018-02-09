import cv2
import numpy as np

def nothing(x):
    pass

# Create a black image, a window
img = cv2.imread('img/1.png')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower = np.array([0, 0, 0])
upper = np.array([255, 255, 255])

cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('LowerH','image',0,255,nothing)
cv2.createTrackbar('LowerS','image',0,255,nothing)
cv2.createTrackbar('LowerV','image',0,255,nothing)
cv2.createTrackbar('UpperH','image',255,255,nothing)
cv2.createTrackbar('UpperS','image',255,255,nothing)
cv2.createTrackbar('UpperV','image',255,255,nothing)

# create switch for ON/OFF functionality
# switch = '0 : OFF \n1 : ON'
# cv2.createTrackbar(switch, 'image',0,1,nothing)

while(1):
    mask = cv2.inRange(hsv, lower, upper)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(img, img, mask=mask)
    cv2.imshow('image',res)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    lower_h =cv2.getTrackbarPos('LowerH','image')
    lower_s =cv2.getTrackbarPos('LowerS','image')
    lower_v =cv2.getTrackbarPos('LowerV','image')
    lower = np.array([lower_h,lower_s,lower_v])

    upper_h =cv2.getTrackbarPos('UpperH','image')
    upper_s =cv2.getTrackbarPos('UpperS','image')
    upper_v =cv2.getTrackbarPos('UpperV','image')
    upper = np.array([upper_h,upper_s,upper_v])
    # get current positions of four trackbars
    # r = cv2.getTrackbarPos('R','image')
    # g = cv2.getTrackbarPos('G','image')
    # b = cv2.getTrackbarPos('B','image')
    # s = cv2.getTrackbarPos(switch,'image')

    # if s == 0:
    #     img[:] = 0
    # else:
    #     img[:] = [b,g,r]

cv2.destroyAllWindows()