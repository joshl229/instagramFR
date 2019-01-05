import os
import face_recognition
from Tkinter import *
from PIL import Image, ImageTk


print("Searching for person...")

# VARIABLES
matching = 0 # Counts the amount of matching images
position = 0 # Keeps track of which image we're on

# Process the person to be found
waldo = face_recognition.load_image_file('./graphics/compare.jpg') # Loads the image
waldoFV = face_recognition.face_encodings(waldo)[0] # Creates the feature vector for the image

# Find the matching images
instagramPics = os.listdir('./images') # Creates a list of all the images

for pic in instagramPics: # For loop to iterate over the instagram pictures
    # Process the image
    try: # Tries to create a feature vector for the image and compare it
        curr_pic = face_recognition.load_image_file('./images/' + pic) # Loads the image
        curr_pic_FV = face_recognition.face_encodings(curr_pic)[0] # Creates feature vector for image

        # Check for a match
        match = face_recognition.compare_faces([waldoFV], curr_pic_FV) # Returns a list of true/false values that tell if there was a match

        # If it was a match
        if match[0] == True:
            matching+=1 # Increment matching

        # If it wasn't a match
        else:
            os.remove('images/' + pic) # Delete the image

    except: # If it can't create a feature vector for the image, delete it
        os.remove('images/' + pic) # Deletes the file

print("Person found in " + str(matching) + " pictures.")

# METHODS
def nextPressed():
    # Allows the global variables to be accessed
    global position
    global matching

    if position < matching-1: # If you're able to increment the position, increment it
        position += 1 # Update position

        # Display the new image
        new_display_img = Image.open("./images/" + found_list[position])
        new_converted_img = ImageTk.PhotoImage(new_display_img)
        image_label.configure(image=new_converted_img)
        image_label.image = new_converted_img
        image_label.pack(fill=BOTH, expand=TRUE)

def prevPressed():
    # Allows the global variables to be accessed
    global position
    global matching

    if position > 0: # If you're able to decrement the position, decrement it
        position -= 1 # Update position

        # Display the new image
        new_display_img = Image.open("./images/" + found_list[position])
        new_converted_img = ImageTk.PhotoImage(new_display_img)
        image_label.configure(image=new_converted_img)
        image_label.image = new_converted_img
        image_label.pack(fill=BOTH, expand=TRUE)

# GUI DEVELOPMENT

# Run the GUI if there's a matching picture
if matching > 0:

    window = Tk()
    found_text = StringVar()

    # Creates GUI window
    window.title("Found Pictures")
    window.configure(background="black")
    window.geometry("480x600")
    window.resizable(width=False, height=False)

    # Creates frame for image
    image_frame = Frame(window)
    image_frame.pack(side=TOP, expand=TRUE, fill=BOTH)

    # Creates frame for buttons
    button_frame = Frame(window)
    button_frame.pack(side=BOTTOM,expand=TRUE,fill=BOTH)

    # Shows the image
    found_list = os.listdir("./images") # Creates a list of the images where the person is found
    display_img = Image.open("./images/" + found_list[0])
    converted_img = ImageTk.PhotoImage(display_img)
    image_label = Label(image_frame, image=converted_img) # Places image
    image_label.pack(fill=BOTH, expand=TRUE)



    # Creates next button
    next_btn = Button(button_frame, text="NEXT", bd=0, bg="black", fg="white", command=nextPressed)
    next_btn.pack(side=RIGHT, fill=BOTH, expand=TRUE)

    # Creates previous button
    prev_btn = Button(button_frame, text="PREV", bd=0, bg="black", fg="white", command=prevPressed)
    prev_btn.pack(side=LEFT, fill=BOTH, expand=TRUE)


    window.mainloop() # Runs the GUI window
    print("Cleaning up...")
