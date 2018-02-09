# filter color by hsv in special region

import cv2
import numpy as np
import time


def nothing(x):
    pass


window_name_frame = "frame"
window_name_result = "result"
window_name_hsv = "hsv"

lower = np.array([0, 90, 33])
upper = np.array([255, 255, 255])

click_x = -1
click_y = -1


def show_para_windows():
    # create trackbars for color change
    cv2.createTrackbar('LowerH', window_name_hsv, 0, 255, nothing)
    cv2.createTrackbar('LowerS', window_name_hsv, 0, 255, nothing)
    cv2.createTrackbar('LowerV', window_name_hsv, 0, 255, nothing)
    cv2.createTrackbar('UpperH', window_name_hsv, 127, 255, nothing)
    cv2.createTrackbar('UpperS', window_name_hsv, 55, 255, nothing)
    cv2.createTrackbar('UpperV', window_name_hsv, 255, 255, nothing)
    cv2.imshow(window_name_hsv, np.zeros((10, 255, 3), np.uint8))


def get_hsv_setting():
    global lower, upper
    lower_h = cv2.getTrackbarPos('LowerH', window_name_hsv)
    lower_s = cv2.getTrackbarPos('LowerS', window_name_hsv)
    lower_v = cv2.getTrackbarPos('LowerV', window_name_hsv)
    lower = np.array([lower_h, lower_s, lower_v])

    upper_h = cv2.getTrackbarPos('UpperH', window_name_hsv)
    upper_s = cv2.getTrackbarPos('UpperS', window_name_hsv)
    upper_v = cv2.getTrackbarPos('UpperV', window_name_hsv)
    upper = np.array([upper_h, upper_s, upper_v])


def show_filtered_img(src):
    # Convert BGR to HSV
    # region = src[start[0]:end[0], start[1]:end[1]]
    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(src, src, mask=mask)
    cv2.imshow(window_name_result, res)
    print("res.shape: ", res.shape)
    print("res.size: ", res.size)
    # cv2.imshow(window_name_result, region)


# mouse callback function
def show_pixinfo(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global click_y, click_x
        click_x = x
        click_y = y


if __name__ == '__main__':
    cv2.namedWindow(window_name_frame)
    cv2.namedWindow(window_name_result)
    cv2.namedWindow(window_name_hsv)
    show_para_windows()
    img = cv2.imread('img/demo1.png', -1)
    cv2.setMouseCallback(window_name_result, show_pixinfo)
    while (1):
        time.sleep(0.1)
        show_filtered_img(img)

        cv2.imshow(window_name_frame, img)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

        get_hsv_setting()
        print("hsv: ", lower, " -> ", upper)

    cv2.destroyAllWindows()
