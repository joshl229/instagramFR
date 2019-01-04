import json
import requests
from bs4 import BeautifulSoup
import sys
import os
import os.path
import shutil
from Tkinter import *
from PIL import Image, ImageTk
import Tkinter, tkFileDialog
import time

# VARIABLES:

window = Tk() # Creates Tkinter instance
statusMsg = StringVar() # Holds String Variable
show_browse = 0 # Tells when to show the browse button

# FUNCTIONS:

# Creates the images folder
def create_folder():
    try : # Tries to create a folder called images
        os.mkdir('images')

    except: # If the image folder already exists it deletes the folder and creates a new one to get rid of residual images
        shutil.rmtree('./images') # Deletes the folder
        os.mkdir('images') # Creates a new folder

# Downloads the image with the filename being the number image it is
def download_image(url, number): # Creates the function and sets its parameters
    image_browser = requests.get(url) # Creates a requests object to go to the image url
    image_file = open("./images/" + str(number) + '.jpg', "w") # Creates a jpg images in the images folder
    image_file.write(image_browser.content) # Writes the content to the image by scraping the image data from the url
    image_file.close() # Closes the file

# Handles what to do if there's an invalid instagram profile
def err_Msg(number):
    statusLabel.configure(fg="red")
    # If it's invalid username error
    if number == 1:
        statusMsg.set("\n\n\n\n\nInvalid Instagram Username. Please Enter a New User.")

    # If it's a private user
    if number == 2:
        statusMsg.set("\n\n\n\n\nUser Private Or Has No Photos. Please Enter A New User.")

    # Clears textbox
    textBox.delete(0,END)

# Handles what to do when submit button is pressed
def submitPressed():
    create_folder() # Creates a folder
    profile = textBox.get() # Stores the profile entered into the profile variable
    private_tester = 0
    while private_tester == 0: # Checks to make sure a valid user is entered

        completed = 0 # Value to check when a valid instagram username is entered

        # If it's an invalid instagram username, it prompts you to enter a valid one
        while completed != 200: # While invalid profiles are entered
            link = 'https://www.instagram.com/' + profile # Gets the Instagram profile link
            pagefile = requests.get(link) # Creates an object for the instagram user's information
            completed = pagefile.status_code # Checks if a valid Instagram link was entered. If it was, value should be 200.

            if completed != 200: # If it's an invalid username
                err_Msg(1) # Sends out error message
                return

        parser = BeautifulSoup(pagefile.text, 'lxml') # Parses the instagram website using lxml

        ig_json = parser.find('script', text=lambda t: t.startswith('window._sharedData')).text.split(' = ', 1)[1].rstrip(';') # Strips the useless information and just leaves the image data and stores it in a JSON for easy manipulation
        url_file = json.loads(ig_json) # Opens the JSON file and creates an object that we can find the urls from

        for count in url_file['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']: # Goes through each instagram post and finds the link to the 480 x 600 image
            photo_link = count['node']['thumbnail_resources'][3]['src'] # Creates a string with the image link
            private_tester += 1 # If it has a post, increment it
            download_image(photo_link, private_tester) # Passes the link and number to the image download function

        if private_tester == 0:
            err_Msg(2) # Sends out error message
            return

        # Images successfully downloaded
        statusLabel.configure(fg="green")
        statusMsg.set("\tFind image of person to recognize.")

        # Displays the Browse Button
        browseBtn.grid(row=5, column=1,columnspan=2)

# Copies the browsed for image into graphics folder
def browsePressed():
    new_img = open("./graphics/" + "compare" + '.jpg', "w") # Creates the new file
    og_img = tkFileDialog.askopenfile(filetypes = [("Image File", ("*.jpg","*.jpeg"))]) # Search for file

    # Copies the image into a new file
    for text in og_img:
        new_img.write(text)

    # Closes the files
    new_img.close()
    og_img.close()

    # Updates status update and then closes app
    statusMsg.set("\tImage Successfully Imported.") # Changes the status message
    window.update() # Updates the window
    time.sleep(3) # Waits three seconds before closing app
    quit()

# GUI DEVELOPMENT:

# Creates GUI window
window.title("Image Downloader")
window.geometry("500x500")
window.resizable(width=False, height=False)
convert_img = Image.open("graphics/instaLogo.png")
logo = ImageTk.PhotoImage(convert_img)
Label(window, image=logo).grid(row=0, column=2,sticky="W") # Places Logo

# Creates Instgram Profile Label
Label(window, text="\n        Enter Instagram Profile", font="arial 12 bold").grid(row=1, column=0, columnspan=3)

# Creates Textbox
textBox = Entry(window,width=20)
textBox.grid(row=2, column=1, columnspan=3, sticky="W")

# Creates status label
statusLabel = Label(window, textvariable=statusMsg, font="arial 7 bold")
statusLabel.grid(row=4,column=0,columnspan=4)

# Creates Submit Button
submitBtn = Button(window, text="Submit",command=submitPressed)
submitBtn.grid(row=3, column=1,columnspan=2)

# Creates Browse Button and initially hides it
browseBtn = Button(window, text="Browse",command=browsePressed)
browseBtn.grid_remove() # Hides the button

window.mainloop() # Runs the window
