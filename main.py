import pygame
from pygame.locals import *  
from menu import menu_principal
from leer_json import icono

from shared import SCREEN, fuente


pygame.init()  
fuente = pygame.font.Font("./src/assets/fonts/Gameplay.ttf", 35)


pygame.display.set_caption("CAT-GAME")  
pygame.display.set_icon(icono)

menu_principal(SCREEN, fuente)