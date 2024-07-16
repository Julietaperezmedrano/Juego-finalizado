import pygame
import sys
from settings import *
from shared import fuente, SCREEN


def quit_game():
    """Cierro con la x el juego
    """
    pygame.quit()
    sys.exit()

def crear_texto(texto, font, color, coordenadas):
    """Creo un texto y lo bliteo en la pantalla

    Args:
        texto: Texto que quiero que se muestre en pantalla
        font: el tipo de fuente que quiero que se me muestre en pantalla
        color: Color del texto
        coordenadas: Coordenadas width y height

    Returns:
        el bliteo del texto en las coordenadas que le pase
    """
    text_superficie = font.render(texto, True, color)
    return SCREEN.blit(text_superficie, coordenadas)

# Función para dibujar un botón
def dibujar_btn(text, rect, color, hover_color, action=None):
    """Me dibuja un botón

    Args:
        text: El texto que quiero que tenga el botón
        rect: El rectangulo que va a contener el texto
        color: Color del rectangulo
        hover_color: Color del rectangulo cuando paso el mouse encima
        action (optional): La accion a la que quiero que me rediriga cuando haga click 
    Returns:
        El hover
    """
    mouse_pos = pygame.mouse.get_pos() 
    click = pygame.mouse.get_pressed()  
    hover = rect.collidepoint(mouse_pos)  

    if hover:
        pygame.draw.rect(SCREEN, hover_color, rect) 
        if click[0] == 1 and action: 
            pygame.time.delay(200) 
            action()  
    else:
        pygame.draw.rect(SCREEN, color, rect)  
    
    text_surf = fuente.render(text, True, BLACK)
    SCREEN.blit(text_surf, (rect.x + (rect.width - text_surf.get_width()) // 2, rect.y + (rect.height - text_surf.get_height()) // 2))
    
    return hover  

def get_path_actual(nombre_archivo):
    import os
    directorio_actual = os.path.dirname(__file__)
    return os.path.join(directorio_actual, nombre_archivo)

def cargar_archivo_csv(nombre_archivo):
    """Lee el archivo csv
    Args:
        nombre_archivo: El nombre del archivo que quiero leer

    Returns:
        La lista datos con el id y el score
    """
    datos = []
    with open(get_path_actual(nombre_archivo), "r", encoding="utf-8") as archivo:
        for linea in archivo:
            id, score = linea.strip().split(',') 
            datos.append((id, score))
    return datos

def agregar_id_score(nombre_archivo, id_nuevo, score_nuevo):
    """Escribe el nuevo id y score que se genere

    Args:
        nombre_archivo: Nombre del archivo en el que quiero escribir
        id_nuevo: Id nuevo que se genera
        score_nuevo: Score nuevo que se genera
    """
    with open(get_path_actual(nombre_archivo), "a", encoding="utf-8") as archivo:
        archivo.write("\n" + f"{id_nuevo},{score_nuevo}")
