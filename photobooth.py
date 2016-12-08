#! /usr/bin/python

import picamera
import pygame
import RPIO
import atexit
import io
import os
import time
import multiprocessing
import threading
import sys
import re
import errno

IDLE_MODE, PHOTO_MODE, PRINT_MODE = range(3)

# buttons GPIOs
BUTTON_PHOTO = 4
BUTTON_PRINT = 5

# file directory where pictures will be stored
PHOTOS_DIR = "/media/XXX/photobooth_images/"

# time in secs before taking the picture
PHOTO_DELAY = 3

# duration in secs to display the new picture
PHOTO_DISPLAY_TIME = 5

# duration in secs to wait for print confirmation
PHOTO_PRINT_TIME = 5

# TODO whether or not to allow printing
# ENABLE_PRINT = 1

xSize, ySize = 640, 400
# global tmp array for low quality streaming
rgb = bytearray(xSize * ySize * 4)
# [ img resolution, size of output, field of view ]
sizeData =  [(1440, 1080), (xSize, ySize), (0.0, 0.0, 1.0, 1.0)]
OVERLAY_DIR = "images/"

# show camera preview on screen
def showPreview(camera, screen):
    stream = io.BytesIO() # Capture into in-memory stream
    camera.capture(stream, use_video_port=True, format='rgba')
    stream.seek(0)
    stream.readinto(rgb)
    stream.close()
    img = pygame.image.frombuffer(rgb[0: (xSize * ySize * 4)], sizeData[1], 'RGBA')
    screen.blit(img, ((xSize - img.get_width() ) / 2, (ySize - img.get_height()) / 2))
    pygame.display.update() # necessary?

# Save a jpeg to a file from picamera
def capturePhoto(camera):
    oldRes = camera.resolution
    filename = PHOTOS_DIR + '/image.jpg' # TODO add time info
    camera.resolution = (2592, 1944) # set to max resolution
    camera.capture(filename, use_video_port=False, format='jpeg', thumbnail=None)
    camera.resolution = oldRes
    return filename

# Show an image on screen
def overlayPicture(screen, filename):
    img = pygame.image.load(OVERLAY_DIR + filename, 'png')
    screen.blit(img, ((xSize - img.get_width() ) / 2, (ySize - img.get_height()) / 2))
    pygame.display.update() # necessary?

# infinite loop function
def photoboothLoop():
    state = IDLE_MODE

    # init camera
    camera = picamera.PiCamera()
    atexit.register(camera.close)
    camera.vflip = False
    camera.hflip = False
    camera.brightness = 60
    camera.resolution = sizeData[1]
    camera.crop = (0.0, 0.0, 1.0, 1.0) # can focus in for narrower field of view

    # build a screen
    os.environ["SDL_FBDEV"] = "/dev/fb0"
    pygame.init()
    pygame.mouse.set_visible(False)
    screen = pygame.display.set_mode((xSize,ySize))

    # variables used across the loop
    photoButtonTime = 0
    printButtonTime = 0
    lastPhoto = ''
    lastPhotoTime = 0

    # start an infinite loop
    while True:

        # idle mode : waiting for someone to press a button
        if state == IDLE_MODE:

            # show the camera preview
            showPreview(camera, screen)

            # pressed "photo" button
            if not RPIO.input(BUTTON_PHOTO):
                state = PHOTO_MODE
                photoButtonTime = time.clock()

            # pressed "print" button
            if not RPIO.input(BUTTON_PRINT):
                state = PRINT_MODE
                printButtonTime = time.clock()
                # show the last photo taken
                if not lastPhoto == '':
                    img = pygame.image.load(PHOTOS_DIR + lastPhoto, 'jpeg')
                    screen.blit(img, ((xSize - img.get_width() ) / 2, (ySize - img.get_height()) / 2))
                    pygame.display.update() # necessary?
                    # TODO display the print confirmation overlay

        # photo mode : we are in the process of taking a picture
        elif state == PHOTO_MODE:
            timeFromButton = time.clock() - photoButtonTime
            showPreview(camera, screen)
            if timeFromButton < PHOTO_DELAY:
                # show counter
                overlayPicture(screen, timeFromButton + '.png')
                sleep(1)
            else:
                # take photo
                lastPhoto = capturePhoto(camera)
                lastPhotoTime = time.clock()
                # display the photo
                state = DISPLAY_MODE
                img = pygame.image.load(PHOTOS_DIR + lastPhoto, 'jpeg')
                screen.blit(img, ((xSize - img.get_width() ) / 2, (ySize - img.get_height()) / 2))
                pygame.display.update() # necessary?

        # dislay mode : photo can be displayed for some time
        elif state == DISPLAY_MODE:
            timeFromPhoto = time.clock() - lastPhotoTime
            if timeFromPhoto > PHOTO_DISPLAY_TIME:
                showPreview(camera, screen)
                state = IDLE_MODE

        # print mode : photo is displayed for print confirmation
        elif state == PRINT_MODE:
            timeFromButton = time.clock() - printButtonTime
            if timeFromButton > PHOTO_PRINT_TIME:
                showPreview(camera, screen)
                state = IDLE_MODE

        else:
            print "UNKNOWN STATE! back to IDLE"
            state = IDLE_MODE


if __name__ == "__main__":

    # check that script is run as root user
    if os.getuid() != 0:
        print 'This must be run as root'
        sys.exit(1)

    # create pics directory if it does not exist
    try:
        os.makedirs(PHOTOS_DIR)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(PHOTOS_DIR):
            pass
        else: raise

    # bind the GPIOs
    RPIO.setup(BUTTON_PHOTO, RPIO.IN, pull_up_down=RPIO.PUD_UP)
    RPIO.setup(BUTTON_PRINT, RPIO.IN, pull_up_down=RPIO.PUD_UP)

    # start the infinite loop (kill process to stop the photobooth)
    photoboothLoop()
