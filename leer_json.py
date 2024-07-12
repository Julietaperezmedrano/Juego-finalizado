import json
import pygame

def get_path_actual(nombre_archivo):
    """Me muestra el path del directorio actual que le pase

    Args:
        nombre_archivo: nombre del archivo el cual quiero el directorio

    Returns:
        Me retorna path
    """
    import os
    directorio_actual = os.path.dirname(__file__)
    return os.path.join(directorio_actual, nombre_archivo)

with open(get_path_actual("imagenes.json"), "r", encoding="utf-8") as archivo: #que lea el archivo
    datos = json.load(archivo) #que lo cargue a una lista de dict

imagenes = {}

for item in datos['imagenes']:
    nombre = item['nombre']
    ruta = item['ruta']
    imagenes[nombre] = pygame.image.load(ruta)


icono = imagenes['icono']
background = imagenes['background']
personaje_principal = imagenes['personaje_principal']    
proyectil_imagen = imagenes['proyectil_imagen']
gift_image = imagenes['gift_image']
food = imagenes['food']
vida_imagen = imagenes['vida_imagen']
menu_imagen = imagenes['menu_imagen']
background_options = imagenes['background_options']
vida_imagen = imagenes['vida_imagen']