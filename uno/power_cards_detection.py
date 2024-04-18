#importing all required libraries
import os #for interacting with operating system
import cv2 #for computer vision
import numpy as np #for numerical operations

def main():
    #setting the dir where the power cards are saved
    path = 'C:/Users/salma/Desktop/uno/dataset/powercards'
    orb = cv2.ORB_create(nfeatures=2000)

    #initializing empty lists to store images, class names 
    images = []
    classNames = []
    myList = os.listdir(path)
    #looping through each in the dataset
    for cl in myList:
        #reading each image and adding to image list
        imgCur = cv2.imread(f'{path}/{cl}')
        images.append(imgCur)
        classNames.append(os.path.splitext(cl)[0])

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
            if area > 1000:  
                filtered_contours.append(contour)
        #extracting largest contour as the card region of interest
        if filtered_contours:
            max_contour = max(filtered_contours, key=cv2.contourArea)
            #boundry box of contour
            x, y, w, h = cv2.boundingRect(max_contour)
            #extracting region of interest (card)
            card_roi = img[y:y+h, x:x+w]
            #returning preprocessed card ROI
            return card_roi
        else:
            return None

    #function to extract ORB descriptors from preprocessed card images
    def findDes(images):
        #list to store descriptors of each image
        desList = []
        for img in images:
            img_processed = preprocess_image(img)
            if img_processed is not None:
                #detecting keypoints and computing descriptors using orb
                kp, des = orb.detectAndCompute(img_processed, None)
                desList.append(des)
        return desList

    #matching descriptors of input image with dataset image
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
                    #filtering out good matches
                    if m.distance < 0.75 * n.distance:
                        good.append([m])
                matchList.append(len(good))
            #print("Match List:", matchList)
        except Exception as e:
            print("Error:", e)

        #identifying the card class based on max number of matches
        if len(matchList) != 0:
            max_matches = max(matchList)
            if max(matchList) > thres:
                finalVal = matchList.index(max(matchList))
                return finalVal
        return -1

    #extracting descriptors from dataset images
    desList = findDes(images)

    cap = cv2.VideoCapture(0)

    while True:
        success, img2 = cap.read()
        imgOrg = img2.copy()
        #finding id(class) of the detected card in frame
        id = findID(img2, desList)
        #checking if valid power card is identified
        if id != -1 and id < len(classNames):
            #getting the class name of detected card
            class_name = classNames[id]
            #adding detected card text in frame    
            cv2.putText(imgOrg, class_name, (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
        else:
            #displays if no card found
            class_name = "No Card Detected!"
            cv2.putText(imgOrg, "No Card Detected!", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow('Power Cards Detection', imgOrg)

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


