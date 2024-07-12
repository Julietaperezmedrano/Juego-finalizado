import pygame
from pygame.locals import *  # para las teclas
from menu import menu_principal
from leer_json import icono

from shared import SCREEN, fuente


pygame.init()  # inicio pygame
fuente = pygame.font.Font("./src/assets/fonts/Gameplay.ttf", 35)

# ------------------- icono ----------------------
pygame.display.set_caption("CAT-GAME")  # titulo pantalla pygame
pygame.display.set_icon(icono)

menu_principal(SCREEN, fuente)