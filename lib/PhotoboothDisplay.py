import pygame
from config import *

class PhotoboothDisplay:
    def __init__(self):
        # init pygame and screen
        pygame.init()
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        # disable full screen (might be useful when accessed through "ssh -X")
        # self.screen = pygame.display.set_mode(SCREEN_RESOLUTION)

        # init font file
        self.font = pygame.font.Font("/opt/photobooth/fonts/" + FONT_FILE, FONT_SIZE)

    def text(self, text):
        label = self.font.render(text, 1, FONT_COLOR)
        size = self.font.size(text)
        self.screen.blit(label, ((SCREEN_RESOLUTION[0] - size[0]) / 2, (SCREEN_RESOLUTION[1] - size[1]) / 2))

    def image(self, img):
        self.screen.blit(img, ((SCREEN_RESOLUTION[0] - img.get_width() ) / 2, (SCREEN_RESOLUTION[1] - img.get_height()) / 2))

    def imageScaled(self, filepath):
        fullSize = pygame.image.load(filepath)
        img = pygame.transform.scale(fullSize, SCREEN_RESOLUTION)
        self.image(img)

    def imageBuffer(self, imgBuffer):
        img = pygame.image.frombuffer(imgBuffer, SCREEN_RESOLUTION, 'RGB')
        self.image(img)

    def update(self):
        pygame.display.update()
