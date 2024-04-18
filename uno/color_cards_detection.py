#importing all required libraries
import os #for interacting with operating system
import cv2 #for computer vision
import numpy as np #for numerical operations

def main():
    #setting the dir where the color cards are saved
    path = 'C:/Users/salma/Desktop/uno/dataset/colorcards'
    #creating ORB feature detector 
    orb = cv2.ORB_create(nfeatures=2000)

    #initializing empty lists to store images, class names and list of files
    images = []
    classNames = []
    myList = os.listdir(path)
    #looping through each in the dataset
    for cl in myList:
        #reading each image and adding to image list
        imgCur = cv2.imread(f'{path}/{cl}')
        images.append(imgCur)
        #remove the first word from the class name
        class_name = os.path.splitext(cl)[0]
        remaining_name = ' '.join(class_name.split()[1:])
        #adding remaining class name to the class name list
        classNames.append(remaining_name)

    #preprocessing of the images
    def preprocess_image(img):
        #converting to greyscale
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #blurring greyscale image
        img_smooth = cv2.blur(img_gray, (5, 5))
        #thresholding to create a binary image
        _, img_thresh = cv2.threshold(img_smooth, 110, 255, cv2.THRESH_BINARY_INV)
        #applying morphological operations(remove noise)
        kernel = np.ones((5, 5), np.uint8)
        img_morph = cv2.morphologyEx(img_thresh, cv2.MORPH_OPEN, kernel)
        contours, _ = cv2.findContours(img_morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        filtered_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            #filtering small contours
            if area > 1000:  
                filtered_contours.append(contour)
        #extracting largest contour as the card region of interest
        if filtered_contours:
            max_contour = max(filtered_contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(max_contour)
            card_roi = img[y:y+h, x:x+w]
            return card_roi
        else:
            return None

    #function to extract descriptors from each image in dataset
    def findDes(images):
        desList = []
        for img in images:
            img_processed = preprocess_image(img)
            if img_processed is not None:
                #detecting keypoints and computing descriptors using orb
                kp, des = orb.detectAndCompute(img_processed, None)
                desList.append(des)
        return desList

    #function to match descriptors of input image with dataset image
    def findID(img, desList, thres=25):
        kp2, des2 = orb.detectAndCompute(img, None)
        bf = cv2.BFMatcher()
        matchList = []

        try:
            for des in desList:
                #performs descriptor matching using brute force matcher
                matches = bf.knnMatch(des, des2, k=2)
                good = []
                for m, n in matches:
                    if m.distance < 0.75 * n.distance:
                        good.append([m])
                matchList.append(len(good))
        except Exception as e:
            print("Error:", e)

        #identifying the card class based on max number of matches
        if len(matchList) != 0:
            max_matches = max(matchList)
            if max(matchList) > thres:
                finalVal = matchList.index(max(matchList))
                return finalVal
        return -1

    #identifying the dominant color of card using color segmentation
    #ranges of each color was retrieved from dataset images using hsv color tracker
    def find_dominant_color_segmentation(img):
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        #red
        lower_red = np.array([0,130,129])
        upper_red = np.array([180,255,255])
        mask_red = cv2.inRange(img_hsv, lower_red, upper_red)
        #blue
        lower_blue = np.array([69,129,103])
        upper_blue = np.array([128,255,255])
        mask_blue = cv2.inRange(img_hsv, lower_blue, upper_blue)
        #green
        lower_green = np.array([73,159,0])
        upper_green = np.array([96,255,255])
        mask_green = cv2.inRange(img_hsv, lower_green, upper_green)
        #yellow
        lower_yellow = np.array([15,80,114])
        upper_yellow = np.array([40, 255, 255])
        mask_yellow = cv2.inRange(img_hsv, lower_yellow, upper_yellow)
        masks = [mask_red, mask_blue, mask_green, mask_yellow]
        color_names = ['red', 'blue', 'green', 'yellow']
        max_area = 0
        dominant_color = None
        for mask, color_name in zip(masks, color_names):
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if contours:
                contour_area = max([cv2.contourArea(contour) for contour in contours])
                if contour_area > max_area:
                    max_area = contour_area
                    dominant_color = color_name
        return dominant_color

    #extracting descriptors from dataset images
    desList = findDes(images)

    cap = cv2.VideoCapture(0)

    while True:
        success, img2 = cap.read()
        imgOrg = img2.copy()

        #finding id(class) of the detected card in frame
        id = findID(img2, desList)
        #checking if valid color card is identified
        if id != -1 and id < len(classNames):
            class_name = classNames[id]
            #finding dominant color of detected card
            dominant_color = find_dominant_color_segmentation(imgOrg)
            if dominant_color:
                #setting text color to display
                text_color = (0, 0, 255) if dominant_color == 'red' else (255, 0, 0) if dominant_color == 'blue' else (0, 255, 0) if dominant_color == 'green' else (0, 255, 255)
                #displaying detected class name along with dominant color found
                cv2.putText(imgOrg, f'{dominant_color} {class_name}', (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, text_color, 2)
        else:
            #displays if no card found
            cv2.putText(imgOrg, "No Card Detected!", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow('Color Cards Detection', imgOrg)

        #waiting for key (esc) press to exit loop
        k = cv2.waitKey(1)
        if k%256 == 27:
            print("Closing...")
            break
    #releasing frames and destroying all windows        
    cap.release()
    cv2.destroyAllWindows()

#calling main function when script is executed
if __name__ == "__main__":
    main()
