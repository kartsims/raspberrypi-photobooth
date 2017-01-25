# actual photo resolution
CAM_RESOLUTION = 2592, 1944

# enter here your actual screen resolution
# SCREEN_RESOLUTION = 1280, 1024
SCREEN_RESOLUTION = 640, 512
# SCREEN_RESOLUTION = 320, 256

# in case you need to do some cropping on top of the cam cropping
CROP_WINDOW = 0.0, 0.0, 1.0, 1.0

# configure the font used for text display
FONT_FILE = "dizzyedge.otf"
FONT_COLOR = 255, 255, 255
FONT_SIZE = 20

# time in secs before taking the picture
PHOTO_DELAY = 3

# duration in secs to display the new picture
PHOTO_DISPLAY_DURATION = 7

# duration in secs of the "printing" confirmation message
PRINT_DELAY = 3

# directory where images are stored
PHOTOS_DIR = "./photos/"

# keyboard inputs
import pygame
KEY_PHOTO = pygame.K_SPACE
KEY_PRINT = pygame.K_RETURN

# GPIO inputs
ENABLE_GPIO = True
GPIO_PHOTO = 18
GPIO_PRINT = 16

# text translations
TEXT_PRINT_CONFIRM = "Print this photo ?"
TEXT_PRINT_WAIT = "Printing ! Please wait..."
