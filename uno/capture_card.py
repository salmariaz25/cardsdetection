#importing opencv library
import cv2

#setting directory where captured images are saved
save_directory = "C:/Users/salma/Desktop/uno/dataset/colorcards/"

#defining main function where image capture takes place 
def main():
    #default camera opened
    cam = cv2.VideoCapture(0)
    #window for displaying captured frames
    cv2.namedWindow("Dataset Capture")

    #loop for capturing frames begins 
    while True:
        #reading frame from camera
        ret, frame = cam.read()
        if not ret:
            print("Failed to capture")
            break
        #gaussian blur applied to reduce noice 
        frameblur = cv2.GaussianBlur(frame, (5, 5), 0)
        #displaying the blurred frame
        cv2.imshow("Creating Dataset", frameblur)

        #waiting for key press
        k = cv2.waitKey(1)

        #if esc key is pressed then the loop exits and program is closed
        if k % 256 == 27:
            print("Closing the window...")
            break
        
        #if space key is pressed then image is saved
        elif k % 256 == 32:
            #user input for image name saving
            img_name = input("Enter name of the card: ")
            #checking if input name is empty
            if img_name.strip() == "":
                print("Image not saved.")
            else:
                #constructing file name 
                img_name = "{}{}.png".format(save_directory, img_name)
                
                cv2.imwrite(img_name, frame)
                print("Image saved as:", img_name)
    #releasing camera
    cam.release()
    #destroying all opencv windows
    cv2.destroyAllWindows()
#calling main function when script is executed
if __name__ == "__main__":
    main()
