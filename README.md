Readme – Report

Running the ‘ main.py ’  file can be used to call all other files.

The uno card detection program created contains 7 python files namely main.py, capture_card.py, color_cards_detection.py, color_image_detection.py, power_cards_detection.py, power_image_detection.py, hsvrange_tracking.py .
Once the main.py file is run the user is prompted to enter any of the 3 options which are:
1.	Capture card if he requires to input an image to the dataset
2.	Color cards detections menu which consists of reading card from the camera and detecting it or detecting image from the dataset
3.	Power cards detections menu which also consists of reading card from the camera and detecting it or detecting image from the dataset

How this program is carried out :
The uno card detection scripts uses computer vision technique to identify and classify the uno cards based on their color and patterns. It solely relies on OpenCV, Numpy, ORB.
The program is carried out with the use of ORB to detect features, extract descriptors as well as preprocess images and determine the dominant color using hsv ranges.
The program first goes through the images in the dataset, preprocesses them by applying blur and threshold as well as performing morphological operations to remove noise. After preprocessing the images, ORB is applied, and descriptors are extracted and stored. Each descriptor represents a key point feature in the images.
When the input image from the camera frame is received. Its descriptors are compared with the descriptors in the dataset images. Brute-force matcher (BFMatcher) performs this comparison.
The matches are filtered based on a threshold value provided. Then the number of good matches for each dataset image is recorded.
The dataset image with the highest number of good matches above the threshold value provided is considered to be the best match, which indicates the detected uno cards class.
Images are also converted to HSV color space. The ranges used in the program are defined with the help of hsvrange_tracking.py. Once this python file is run, the user can enter the name of color card he wants to find the range of and it can be used to detect the color in the program.
This method was applied as the ORB alone was not effective enough to find the colors accurately. Hence finding the range of a single card in every color and rounding it made the process easier as all the images in the dataset were under the same lighting condition and position.

Conclusion: 
The uno card detection uses computer vision techniques, includes image preprocessing, features extraction, and matching to identify and classify uno cards. By combining these techniques, the program enables real-time detection of UNO cards.
