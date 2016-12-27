import time
import picamera
from PIL import Image
from config import *

camera = picamera.PiCamera()
camera.resolution = CAM_RESOLUTION
camera.start_preview()
camera.annotate_text = 'Hello world!'

# Load the arbitrarily sized image
img = Image.open('./images/test.png')
# Create an image padded to the required size with
# mode 'RGB'
pad = Image.new('RGB', (
    ((img.size[0] + 31) // 32) * 32,
    ((img.size[1] + 15) // 16) * 16,
    ))
# Paste the original image into the padded one
pad.paste(img, (0, 0))

# Add the overlay with the padded image as the source,
# but the original image's dimensions
o = camera.add_overlay(pad.tostring(), size=img.size)
# By default, the overlay is in layer 0, beneath the
# preview (which defaults to layer 2). Here we make
# the new overlay semi-transparent, then move it above
# the preview
o.alpha = 128
o.layer = 3

time.sleep(10)
camera.stop_preview()

camera.close()
