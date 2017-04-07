# camera type (only raspberry cam for now)
CAMERA_TYPE = 'picamera'

# actual photo resolution
CAMERA_RESOLUTION = 2592, 1944

# enter here your screen resolution (will be used for the camera preview images)
SCREEN_RESOLUTION = 640, 480

# in case you need to do some cropping on the camera's pictures
CAMERA_CROP = 0.0, 0.0, 1.0, 1.0

# configure the font used for text display
FONT_FILE = "square.ttf"
FONT_COLOR = 255, 255, 255
FONT_SIZE = 40

# time in secs before taking the picture
PHOTO_DELAY = 3

# duration in secs to display the new picture
PHOTO_DISPLAY_DURATION = 5

# duration in secs of the "printing" confirmation message
PRINT_DELAY = 3

# directory where images are stored
PHOTOS_DIR = "/opt/photobooth/photos/"

# keyboard inputs
import pygame
KEY_PHOTO = pygame.K_SPACE
KEY_PRINT = pygame.K_RETURN

# GPIO pins
ENABLE_GPIO = True
GPIO_PHOTO = 18
GPIO_PRINT = 16
GPIO_FLASH = 26

# text translations
TEXT_NO_LAST_PHOTO = "No photo found"
TEXT_PRINT_CONFIRM = "Print this photo ?"
TEXT_PRINT_WAIT = "Printing ! Please wait..."
