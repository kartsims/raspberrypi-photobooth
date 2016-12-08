import sys
import pygame
import time

# TODO TIME ???
print (time.strftime("%Y-%m-%d"))

SCREEN_RESOLUTION = 640, 480

# init pygame
pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode(SCREEN_RESOLUTION)

IMAGE = pygame.image.load("images/test.png")
IMAGE_POSITION = 0, 0

FONT = pygame.font.Font("./fonts/dizzyedge.otf", 46)

def showText(text):
    size = FONT.size(text)
    positionX = (SCREEN_RESOLUTION[0] - size[0]) / 2
    positionY = (SCREEN_RESOLUTION[1] - size[1]) / 2
    labelPosition = positionX, positionY
    label = FONT.render(text, 1, (255,255,255))
    screen.fill((0, 0, 0))
    screen.blit(IMAGE, IMAGE_POSITION)
    screen.blit(label, labelPosition)
    pygame.display.update()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.key == pygame.K_SPACE:
                for x in range(0, 3):
                    count = str(3 - x)
                    showText(count)
                    time.sleep(1)
            elif event.key == pygame.K_LEFT:
                IMAGE_POSITION = IMAGE_POSITION[0] - 10, IMAGE_POSITION[1]
            elif event.key == pygame.K_RIGHT:
                IMAGE_POSITION = IMAGE_POSITION[0] + 10, IMAGE_POSITION[1]
                # showText("LEFT")
                # time.sleep(1)
            elif event.key == pygame.K_DOWN:
                IMAGE_POSITION = IMAGE_POSITION[0], IMAGE_POSITION[1] + 10
            elif event.key == pygame.K_UP:
                IMAGE_POSITION = IMAGE_POSITION[0], IMAGE_POSITION[1] - 10

    screen.fill((0, 0, 0))
    screen.blit(IMAGE, IMAGE_POSITION)
    pygame.display.update()
