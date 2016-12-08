import sys
import math
import pygame
import pygame.camera
import time
import atexit
import io

SCREEN_RESOLUTION = 640, 480
CAM_RESOLUTION = 640, 480
# TODO how to use small size preview ?..
# CAM_RESOLUTION = 1280, 720

# font file used for text display
FONT_FILE = "dizzyedge.otf"

# time in secs before taking the picture
PHOTO_DELAY = 3

# duration in secs to display the new picture
PHOTO_DISPLAY_DURATION = 7

# duration in secs of the "printing" confirmation message
PRINT_DELAY = 3

# directory where images are stored
PHOTOS_DIR = "./photos/"

# init pygame
pygame.init()
pygame.mouse.set_visible(False)
SCREEN = pygame.display.set_mode(SCREEN_RESOLUTION)
FONT = pygame.font.Font("./fonts/" + FONT_FILE, 46)

# init camera
pygame.camera.init()
camlist = pygame.camera.list_cameras()
if not camlist:
    raise ValueError("Sorry, no cameras detected.")
CAM_FILEPATH = camlist[0]
CAM = pygame.camera.Camera(CAM_FILEPATH, CAM_RESOLUTION)
CAM.start()
# os.system('v4l2-ctl -d 0 -c focus_auto=0')          #set auto focus to 0 to not interfere with focus
# os.system('v4l2-ctl -d 0 -c focus_absolute=250')    #set focus of camera to max

def centerPosition(itemSize, containerSize):
    positionX = (containerSize[0] - itemSize[0]) / 2
    positionY = (containerSize[1] - itemSize[1]) / 2
    return positionX, positionY

def addText(text):
    label = FONT.render(text, 1, (255,255,255))
    size = FONT.size(text)
    labelPosition = centerPosition(size, SCREEN_RESOLUTION)
    SCREEN.blit(label, labelPosition)

def displayLastPhoto():
    SCREEN.blit(lastPhoto, (0, 0))
    addText("Print this photo ?")
    pygame.display.update()

# variables that will be updated during the loop
currentMode = 'IDLE'
photoButtonTime = 0
lastPhoto = ''

while 1:
    SCREEN.fill((0, 0, 0))

    # idle mode : waiting for user action
    if currentMode == 'IDLE':
        IMAGE = CAM.get_image()
        SCREEN.blit(IMAGE, (0, 0))
        pygame.display.update()
        # listen to keyboard events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    photoButtonTime = time.clock()
                    currentMode = 'PHOTO_COUNTDOWN'
                elif event.key == pygame.K_RETURN:
                    # TODO check if lastPhoto exists
                    displayLastPhoto()
                    photoDisplayTime = time.clock()
                    currentMode = 'PHOTO_DISPLAY'

    # countdown until photo is actually taken
    elif currentMode == 'PHOTO_COUNTDOWN':
        timeFromButton = int(math.ceil(time.clock() - photoButtonTime))
        if timeFromButton <= PHOTO_DELAY:
            # show counter
            IMAGE = CAM.get_image()
            SCREEN.blit(IMAGE, (0, 0))
            addText(str(timeFromButton))
            pygame.display.update()
        else:
            # take photo
            lastPhoto = CAM.get_image()
            # save the image as a file
            filename = "PHOTOBOOTH-" + time.strftime("%Y%m%d-%H%M%S") + ".jpg"
            pygame.image.save(lastPhoto, PHOTOS_DIR + filename)
            # switch mode to wait for print
            displayLastPhoto()
            photoDisplayTime = time.clock()
            currentMode = 'PHOTO_DISPLAY'

    # show the last photo for sometime
    elif currentMode == 'PHOTO_DISPLAY':
        timeFromButton = int(math.ceil(time.clock() - photoDisplayTime))
        if timeFromButton > PHOTO_DISPLAY_DURATION:
            currentMode = 'IDLE'
        # listen to keyboard events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    currentMode = 'PRINT_CONFIRM'

    # show print confirmation message
    elif currentMode == 'PRINT_CONFIRM':
        SCREEN.blit(lastPhoto, (0, 0))
        addText("Printing ! Please wait...")
        pygame.display.update()
        time.sleep(PRINT_DELAY)
        currentMode = 'IDLE'
