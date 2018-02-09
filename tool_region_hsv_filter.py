# filter color by hsv in special region

import cv2
import numpy as np
import time

def nothing(x):
    pass


window_name_frame = "frame"
window_name_result = "result"
window_name_region = "region"
window_name_hsv = "hsv"

start = (0, 0)
end = (640, 480)
rect_color = (0, 0, 255)
rect_thickness = 3
lower = np.array([0, 90, 33])
upper = np.array([255, 255, 255])


def show_para_windows():
    # create trackbars for region set
    cv2.createTrackbar('startX', window_name_region, 0, 640, nothing)
    cv2.createTrackbar('startY', window_name_region, 0, 480, nothing)
    cv2.createTrackbar('endX', window_name_region, 640, 640, nothing)
    cv2.createTrackbar('endY', window_name_region, 480, 480, nothing)
    # create trackbars for color change
    cv2.createTrackbar('LowerH', window_name_hsv, 0, 255, nothing)
    cv2.createTrackbar('LowerS', window_name_hsv, 0, 255, nothing)
    cv2.createTrackbar('LowerV', window_name_hsv, 0, 255, nothing)
    cv2.createTrackbar('UpperH', window_name_hsv, 127, 255, nothing)
    cv2.createTrackbar('UpperS', window_name_hsv, 55, 255, nothing)
    cv2.createTrackbar('UpperV', window_name_hsv, 255, 255, nothing)
    cv2.imshow(window_name_region, np.zeros((50, 640, 3), np.uint8))
    cv2.imshow(window_name_hsv, np.zeros((10, 255 , 3), np.uint8))


def get_region_setting():
    global start, end
    start_x = cv2.getTrackbarPos('startX', window_name_region)
    start_y = cv2.getTrackbarPos('startY', window_name_region)
    start = (start_x, start_y)
    end_x = cv2.getTrackbarPos('endX', window_name_region)
    end_y = cv2.getTrackbarPos('endY', window_name_region)
    end = (end_x, end_y)


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
    region = src[start[1]:end[1], start[0]:end[0]]
    hsv = cv2.cvtColor(region, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(region, region, mask=mask)
    cv2.imshow(window_name_result, res)
    print("res.shape: ", res.shape)
    print("res.size: ", res.size)
    # cv2.imshow(window_name_result, region)


if __name__ == '__main__':
    cv2.namedWindow(window_name_frame)
    cv2.namedWindow(window_name_result)
    cv2.namedWindow(window_name_region)
    cv2.namedWindow(window_name_hsv)
    show_para_windows()
    cap = cv2.VideoCapture(0)
    while (1):
        time.sleep(0.1)
        _, frame = cap.read()
        show_filtered_img(frame)

        image = cv2.rectangle(frame, start, end, rect_color, rect_thickness)
        cv2.imshow(window_name_frame, image)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

        get_region_setting()
        get_hsv_setting()
        print("region: ", start, " -> ", end)
        print("hsv: ", lower, " -> ", upper)

    cv2.destroyAllWindows()
