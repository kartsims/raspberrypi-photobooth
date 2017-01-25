# access libraries from lib/
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], 'lib'))

# import required libraries
import math
import pygame
import time
import atexit
import io
import picamera
from config import *
import yuv2rgb

# TODO : remove this (debug only)
from pprint import pprint

# Buffers for viewfinder data
rgb = bytearray(SCREEN_RESOLUTION[0] * SCREEN_RESOLUTION[1] * 3)
yuv = bytearray(SCREEN_RESOLUTION[0] * SCREEN_RESOLUTION[1] * 3 / 2)

# init pygame and screen
pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
# disable full screen (might be useful when accessed through "ssh -X")
# screen = pygame.display.set_mode(SCREEN_RESOLUTION)

# init font file
font = pygame.font.Font("./fonts/" + FONT_FILE, FONT_SIZE)

# init camera
camera = picamera.PiCamera()
atexit.register(camera.close)
camera.resolution = SCREEN_RESOLUTION
camera.crop = CROP_WINDOW

# init GPIO pins
if ENABLE_GPIO:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_PHOTO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(GPIO_PRINT, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def displayText(text):
    label = font.render(text, 1, FONT_COLOR)
    size = font.size(text)
    screen.blit(label, ((SCREEN_RESOLUTION[0] - size[0]) / 2, (SCREEN_RESOLUTION[1] - size[1]) / 2))

def displayImage(img):
    screen.blit(img, ((SCREEN_RESOLUTION[0] - img.get_width() ) / 2, (SCREEN_RESOLUTION[1] - img.get_height()) / 2))

def showCamPreview():
    stream = io.BytesIO()
    camera.capture(stream, use_video_port=True, format='raw')
    stream.seek(0)
    stream.readinto(yuv)
    stream.close()
    yuv2rgb.convert(yuv, rgb, SCREEN_RESOLUTION[0],
    SCREEN_RESOLUTION[1])
    img = pygame.image.frombuffer(rgb[0: (SCREEN_RESOLUTION[0] * SCREEN_RESOLUTION[1] * 3)], SCREEN_RESOLUTION, 'RGB')
    displayImage(img)

def takePicture():
	filepath = PHOTOS_DIR + "PHOTOBOOTH-" + time.strftime("%Y%m%d-%H%M%S") + ".jpg"
	scaled = None
	camera.resolution = CAM_RESOLUTION
	camera.crop = CROP_WINDOW
	try:
		camera.capture(filepath, use_video_port=False, format='jpeg',
		thumbnail=None)

	finally:
		# TODO add error handling/indicator (disk full, etc.)
		camera.resolution = SCREEN_RESOLUTION
		camera.crop = CROP_WINDOW

	return filepath


# TODO fetch last photo in the system directly instead of saving it to a variable
lastPhoto = None
def getLastPhoto():
    global lastPhoto
    return lastPhoto

def showLastPhoto():
    lastPhoto = getLastPhoto()
    if not lastPhoto:
        return
    fullSize = pygame.image.load(lastPhoto)
    img = pygame.transform.scale(fullSize, SCREEN_RESOLUTION)
    displayImage(img)
    displayText(TEXT_PRINT_CONFIRM)
    pygame.display.update()
    pygame.event.clear()
    buttonTime = time.clock()
    while True:
        timeFromButton = int(math.ceil(time.clock() - buttonTime))
        if timeFromButton > PHOTO_DISPLAY_DURATION:
            return
        # listen for keyboard inputs
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == KEY_PHOTO:
                    return
                elif event.key == KEY_PRINT:
                    printLastPhoto()
                    return
        # listen for GPIO inputs
        if ENABLE_GPIO:
            if GPIO.input(GPIO_PHOTO) == False:
                time.sleep(.3)
                return
            if GPIO.input(GPIO_PRINT) == False:
                printLastPhoto()
                return

def printLastPhoto():
    lastPhoto = getLastPhoto()
    fullSize = pygame.image.load(lastPhoto)
    img = pygame.transform.scale(fullSize, SCREEN_RESOLUTION)
    displayImage(img)
    displayText(TEXT_PRINT_WAIT)
    pygame.display.update()
    # TODO start printing
    time.sleep(PRINT_DELAY)

def startCountdown():
    buttonTime = time.clock()
    while True:
        timeFromButton = int(math.ceil(time.clock() - buttonTime))
        if timeFromButton <= PHOTO_DELAY:
            # show counter
            showCamPreview()
            displayText(str(timeFromButton))
            pygame.display.update()
        else:
            # save the image as a file
            global lastPhoto
            lastPhoto = takePicture()
            showLastPhoto()
            return

        # listen for keyboard inputs
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == KEY_PHOTO:
                    return
        # listen for GPIO inputs
        if ENABLE_GPIO:
            if GPIO.input(GPIO_PHOTO) == False:
                time.sleep(.3)
                return



# main loop
while True:

    # listen to keyboard events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.key == KEY_PHOTO:
                startCountdown()
            elif event.key == KEY_PRINT:
                showLastPhoto()

    # listen for GPIO inputs
    if ENABLE_GPIO:
        if GPIO.input(GPIO_PHOTO) == False:
            time.sleep(.3)
            startCountdown()
        if GPIO.input(GPIO_PRINT) == False:
            showLastPhoto()

    # show camera preview
    showCamPreview()
    pygame.display.update()
