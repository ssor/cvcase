import cv2
import numpy as np

cap = cv2.VideoCapture(0)


def nothing(x):
    pass


window_name_frame = "frame"
window_name_paras = "paras"
cv2.namedWindow(window_name_frame)
cv2.namedWindow(window_name_paras)

start = (0, 0)
end = (640, 480)
rect_color = (0, 0, 255)
rect_thickness = 3

# create trackbars for color change
cv2.createTrackbar('startX', window_name_paras, 0, 640, nothing)
cv2.createTrackbar('startY', window_name_paras, 0, 480, nothing)
cv2.createTrackbar('endX', window_name_paras, 640, 640, nothing)
cv2.createTrackbar('endY', window_name_paras, 480, 480, nothing)

cv2.imshow(window_name_paras, np.zeros((1,512,3), np.uint8))

while (1):

    # Take each frame
    _, frame = cap.read()
    image = cv2.rectangle(frame, start, end, rect_color, rect_thickness)
    cv2.imshow(window_name_frame, image)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
    start_x = cv2.getTrackbarPos('startX', window_name_paras)
    start_y = cv2.getTrackbarPos('startY', window_name_paras)
    start = (start_x, start_y)
    end_x = cv2.getTrackbarPos('endX', window_name_paras)
    end_y = cv2.getTrackbarPos('endY', window_name_paras)
    end = (end_x, end_y)
    print("start: ", start)
    print("end: ", end)

cv2.destroyAllWindows()
