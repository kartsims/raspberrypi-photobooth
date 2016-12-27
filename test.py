import time
import pygame
import atexit
import io
import picamera
from config import *


# init pygame and screen
pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

# init camera
camera = picamera.PiCamera()
atexit.register(camera.close)
camera.resolution = SCREEN_RESOLUTION
camera.crop = CROP_WINDOW

# def showCamPreview():
    # stream = io.BytesIO() # Capture into in-memory stream
    # camera.capture(stream, use_video_port=True, format='jpeg')
    # stream.seek(0)
    # stream.readinto(yuv)  # stream -> YUV buffer
    # stream.close()
    # yuv2rgb.convert(yuv, rgb, SCREEN_RESOLUTION[0], SCREEN_RESOLUTION[1])
    # img = pygame.image.frombuffer(stream, SCREEN_RESOLUTION, 'RGB')
    # displayImage(img)

def displayImage(img):
    screen.blit(img, ((SCREEN_RESOLUTION[0] - img.get_width() ) / 2, (SCREEN_RESOLUTION[1] - img.get_height()) / 2))


screen.fill((255, 0, 0))
pygame.display.update()
time.sleep(2)
screen.fill((0, 255, 0))
pygame.display.update()
time.sleep(2)

# main loop
# while True:
#
#     showCamPreview()
#     pygame.display.update()
