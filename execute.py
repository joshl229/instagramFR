import os
import os.path
import shutil
import sys

# Run the image scraper
import image_scraper

# Run the facial recognition
import recognition

# Clean up

# Attempt to delete the images folder
try:
    shutil.rmtree('./images')
except:
    pass

# Attempt to delete the comparison photo in graphics folder
try:
    os.remove('./graphics/compare.jpg')
except:
    pass

# Attempt to delete the compiled python bytecode
try:
     os.remove('image_scraper.pyc')
except:
    pass

try:
    os.remove('recognition.pyc')
except:
    pass
