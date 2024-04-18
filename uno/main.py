#importing each module to this main file
import capture_card
import color_cards_detection
import color_image_detection
import power_cards_detection
import power_image_detection

def main():
    #welcome message
    print("Welcome to the UNO card detection program!")
    print("Please select an option:")
    print("1. Capture Card")
    print("2. Color Card Detection")
    print("3. Power Card Detection")
    
    #user input for opening desired program
    option = input("Enter your choice (1-3): ")

    if option == "1":
        capture_card.main()  
    elif option == "2":
        color_card_det_menu()
    elif option == "3":
        power_card_det_menu()  
    else:
        print("Invalid option. Please enter a number between 1 and 4.")

#color card contains 2 options.. detecting from camera and detecting the image in dataset
def color_card_det_menu():
    print("Color Card Detection Menu:")
    print("1. Color Card detection from camera")
    print("2. Color Image Detection")

    option = input("Enter your choice (1-2): ")

    if option == "1":
        color_cards_detection.main()  
    elif option == "2":
        color_image_detection.main()  
    else:
        print("Invalid option. Please enter 1 or 2.")
#color card contains 2 options.. detecting from camera and detecting the image in dataset
def power_card_det_menu():
    print("Power Card Detection Menu:")
    print("1. Power Card detection from camera")
    print("2. Power Image Detection")

    option = input("Enter your choice (1-2): ")

    if option == "1":
        power_cards_detection.main()  
    elif option == "2":
        power_image_detection.main()
    else:
        print("Invalid option. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
