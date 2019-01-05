import os
import face_recognition
from Tkinter import *

print("Searching for person...")

# VARIABLES
matching = 0 # Counts the amount of matching images

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

print(matching)

# METHODS



# GUI DEVELOPMENT
