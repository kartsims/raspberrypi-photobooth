import sys
import os
import glob
import time

print "\n--- %s\n" % time.strftime("%d/%m/%Y %H:%M:%S")

# access libraries from lib/
sys.path.insert(1, os.path.join(sys.path[0], 'lib'))

# import required libraries
import math
import pygame
import RPi.GPIO as GPIO
from config import *
from PhotoboothCamera import *
from PhotoboothDisplay import *
from PhotoboothPrinter import *

# TODO : remove this (debug only)
from pprint import pprint

camera = PhotoboothCamera()
display = PhotoboothDisplay()
printer = PhotoboothPrinter()

# init GPIO inputs
if ENABLE_GPIO:
    print "\nInitializing GPIO pins..."
    print "Board revision : %s" % GPIO.RPI_REVISION
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_PHOTO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    print "Photo on pin %d" % GPIO_PHOTO
    GPIO.setup(GPIO_PRINT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    print "Print on pin %d" % GPIO_PRINT

# setup flash GPIO
if GPIO_FLASH:
    GPIO.setup(GPIO_FLASH, GPIO.OUT)
    print "Flash on pin %d" % GPIO_FLASH
    # print 'HIGH'
    # GPIO.output(GPIO_FLASH, GPIO.HIGH)
    # time.sleep(3)
    # print 'LOW'
    # GPIO.output(GPIO_FLASH, GPIO.LOW)
    # time.sleep(3)
    # print 'HIGH'
    # GPIO.output(GPIO_FLASH, GPIO.HIGH)
    # time.sleep(3)
    # GPIO.cleanup()
    # sys.exit()

# whenever program is exited
def doAtExit():
    GPIO.cleanup()
import atexit
atexit.register(doAtExit)

# display the last photo taken
def showLastPhoto():
    if not camera.lastPhoto:
        display.text(TEXT_NO_LAST_PHOTO)
        display.update()
        time.sleep(1)
        return
    display.imageScaled(camera.lastPhoto)
    display.update()
    pygame.event.clear()
    counter = PHOTO_DISPLAY_DURATION
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    while True:
        # listen for keyboard inputs and timer
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if counter == 0:
                    return
                counter -= 1
            if event.type == pygame.KEYDOWN:
                if event.key == KEY_PHOTO:
                    return
                elif event.key == KEY_PRINT:
                    browseToPhoto(loadPhotosList(), 0)
                    return
        # listen for GPIO inputs
        if ENABLE_GPIO:
            if GPIO.input(GPIO_PHOTO) == False:
                time.sleep(.3)
                return
            if GPIO.input(GPIO_PRINT) == False:
                browseToPhoto(loadPhotosList(), 0)
                return


# the "photo" button has been clicked !
def startCountdown():
    print "Countdown for %d seconds..." % PHOTO_DELAY
    counter = PHOTO_DELAY
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    # flash ON
    GPIO.output(GPIO_FLASH, GPIO.HIGH)
    while True:
        # listen for keyboard inputs and timer
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if counter == 0:
                    print "0!"
                    # save the image as a file
                    camera.takePicture()
                    # flash OFF
                    GPIO.output(GPIO_FLASH, GPIO.LOW)
                    # show photo on screen
                    showLastPhoto()
                    return
                sys.stdout.write(str(counter) + "...")
                sys.stdout.flush()
                counter -= 1
            if event.type == pygame.KEYDOWN:
                if event.key == KEY_PHOTO:
                    return
        # listen for GPIO inputs
        if ENABLE_GPIO:
            if GPIO.input(GPIO_PHOTO) == False:
                time.sleep(.3)
                return

        # show counter
        imgBuffer = camera.preview()
        display.imageBuffer(imgBuffer)
        if counter > 0:
            display.text(str(counter))
        display.update()

# photos browser
def loadPhotosList():
    photos = glob.glob(PHOTOS_DIR + "*.jpg")
    photos.sort(key=os.path.getmtime, reverse=True)
    photos = filter(lambda x:os.path.getsize(x) > 2000L, photos)
    return photos

# show a specific photo
def browseToPhoto(photos, index):
    if len(photos) <= index:
        return
    display.imageScaled(photos[index])
    display.update()
    pygame.event.clear()
    counter = PHOTO_BROWSER_TIMEOUT
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    while True:
        # listen for keyboard inputs and timer
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if counter == 0:
                    return
                counter -= 1
            if event.type == pygame.KEYDOWN:
                if event.key == KEY_PHOTO:
                    return
                elif event.key == KEY_PRINT:
                    browseToPhoto(photos, index + 1)
                    return
        # listen for GPIO inputs
        if ENABLE_GPIO:
            if GPIO.input(GPIO_PHOTO) == False:
                time.sleep(.3)
                return
            if GPIO.input(GPIO_PRINT) == False:
                browseToPhoto(photos, index + 1)
                return

# main loop
while True:

    # listen to keyboard events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print "Clean exit"
                sys.exit()
            elif event.key == KEY_PHOTO:
                startCountdown()
            elif event.key == KEY_PRINT:
                browseToPhoto(loadPhotosList(), 0)

    # listen for GPIO inputs
    if ENABLE_GPIO:
        if GPIO.input(GPIO_PHOTO) == False:
            time.sleep(.3)
            startCountdown()
        if GPIO.input(GPIO_PRINT) == False:
            browseToPhoto(loadPhotosList(), 0)

    # show camera preview
    imgBuffer = camera.preview()
    display.imageBuffer(imgBuffer)
    display.update()
