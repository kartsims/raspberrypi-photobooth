import sys
import pygame
import pygame.camera
from pprint import pprint

pygame.init()
pygame.camera.init()

screen = pygame.display.set_mode((640,480),0)
cam_list = pygame.camera.list_cameras()
pprint(cam_list)
cam = pygame.camera.Camera(cam_list[0],(32,24))
cam.start()

while True:
   image1 = cam.get_image()
   image1 = pygame.transform.scale(image1,(640,480))
   screen.blit(image1,(0,0))
   pygame.display.update()

   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         cam.stop()
         pygame.quit()
         sys.exit()
