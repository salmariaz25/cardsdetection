import cv2 as cv
import argparse
import os


max_value = 255
max_value_H = 180  # Since OpenCV uses 0-179 for H values
low_H = 0
low_S = 0
low_V = 0
high_H = max_value_H
high_S = max_value
high_V = max_value
window_capture_name = 'Image Capture'
window_detection_name = 'Object Detection'
low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'

def on_low_H_thresh_trackbar(val):
    global low_H
    low_H = val
    cv.setTrackbarPos(low_H_name, window_detection_name, low_H)

def on_high_H_thresh_trackbar(val):
    global high_H
    high_H = val
    cv.setTrackbarPos(high_H_name, window_detection_name, high_H)

def on_low_S_thresh_trackbar(val):
    global low_S
    low_S = val
    cv.setTrackbarPos(low_S_name, window_detection_name, low_S)

def on_high_S_thresh_trackbar(val):
    global high_S
    high_S = val
    cv.setTrackbarPos(high_S_name, window_detection_name, high_S)

def on_low_V_thresh_trackbar(val):
    global low_V
    low_V = val
    cv.setTrackbarPos(low_V_name, window_detection_name, low_V)

def on_high_V_thresh_trackbar(val):
    global high_V
    high_V = val
    cv.setTrackbarPos(high_V_name, window_detection_name, high_V)

cv.namedWindow(window_capture_name)
cv.namedWindow(window_detection_name)

cv.createTrackbar(low_H_name, window_detection_name , low_H, max_value_H, on_low_H_thresh_trackbar)
cv.createTrackbar(high_H_name, window_detection_name , high_H, max_value_H, on_high_H_thresh_trackbar)
cv.createTrackbar(low_S_name, window_detection_name , low_S, max_value, on_low_S_thresh_trackbar)
cv.createTrackbar(high_S_name, window_detection_name , high_S, max_value, on_high_S_thresh_trackbar)
cv.createTrackbar(low_V_name, window_detection_name , low_V, max_value, on_low_V_thresh_trackbar)
cv.createTrackbar(high_V_name, window_detection_name , high_V, max_value, on_high_V_thresh_trackbar)

#dir where dataset of card images stored
directory_path = 'C:/Users/salma/Desktop/uno/dataset/colorcards/'

#user input for the name of the image required to track
while True:
    #name of the image
    image_name = input("Enter the name of the image: ")
    #combining mentioned path with input name and png
    image_path = os.path.join(directory_path, image_name + '.png')
    if os.path.exists(image_path):
        break
    else:
        print("Image not found.")

while True:
    #reading image from created path
    frame = cv.imread(image_path)
    frame_HSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    frame_threshold = cv.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))

    # Clean image
    bn_img = cv.erode(frame_threshold, cv.getStructuringElement(cv.MORPH_RECT, (3, 3)), iterations=1)
    bn_img = cv.dilate(bn_img, cv.getStructuringElement(cv.MORPH_RECT, (5, 5)), iterations=1)
    bn_img_inv = cv.bitwise_not(bn_img)

    # Find object in range
    M = cv.moments(bn_img_inv)
    if M['m00'] > 50000:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        # Circle the object
        cv.circle(frame, (cx, cy), 20, (255, 0, 0), 2)

    cv.imshow(window_capture_name, frame)
    cv.imshow(window_detection_name, frame_threshold)

    key = cv.waitKey(1)
    if key == 27:
        break

cv.destroyAllWindows()
