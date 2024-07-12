import pygame
from settings import *
from game import juego
import time
from pygame.locals import *
from shared import SCREEN, fuente
from utils import *
from leer_json import *

def menu_principal(SCREEN, fuente):
    pygame.mixer.music.load("./src/assets/sounds/musica_principal.mp3")
    pygame.mixer.music.set_volume(0.20)
    pygame.mixer.music.play(-1)  
    flag_space = True  #para alternar la visibilidad del texto
    temporizador_tiempo = 0
    temporizador_alternar_tiempo = 0.60
    menu = True
    hovered_start = False #para detectar si el ratón está sobre los botones
    hovered_options = False
    hovered_exit = False
    while menu:
        global menu_imagen
        menu_imagen = pygame.transform.scale(menu_imagen, SCREEN_SIZE)
        SCREEN.blit(menu_imagen, ORIGIN)
        # Detección y dibujo de botones
        is_hovered_start = dibujar_btn("Start", pygame.Rect(300, 210, 300, 70), GREY, DARK_GREY, juego)
        is_hovered_options = dibujar_btn("Options", pygame.Rect(300, 310, 300, 70), GREY, DARK_GREY, options)
        is_hovered_exit = dibujar_btn("Exit", pygame.Rect(300, 410, 300, 70), GREY, DARK_GREY, quit_game)
        sound_arriba_del_boton = pygame.mixer.Sound("./src/assets/sounds/menuboton.mp3")
        #Reproducir un sonido solo una vez cuando el ratón se mueve sobre un botón por primera vez, y no cada vez que se mantiene sobre él.
        if is_hovered_start and not hovered_start: #True / False
            sound_arriba_del_boton.play()
        if is_hovered_options and not hovered_options:
            sound_arriba_del_boton.play()
        if is_hovered_exit and not hovered_exit:
            sound_arriba_del_boton.play()
        # Actualizar el estado de "hovered"
        hovered_start = is_hovered_start
        hovered_options = is_hovered_options
        hovered_exit = is_hovered_exit
        tiempo_actual = time.time()  # obtiene el tiempo actual
        if tiempo_actual - temporizador_tiempo >= temporizador_alternar_tiempo:
            flag_space = not flag_space
            temporizador_tiempo = tiempo_actual

        if flag_space:
            crear_texto("Presione SPACE para continuar", fuente, GREY, (110, 510))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    sonido_space = pygame.mixer.Sound("./src/assets/sounds/space.mp3")
                    sonido_space.play()
                    juego()

        pygame.display.flip()


def options():
    global background_options
    music_on = True
    running = True
    background_options = pygame.transform.scale(background_options, SCREEN_SIZE)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        SCREEN.blit(background_options, ORIGIN)  # Dibujar la imagen de fondo en la pantalla

        if music_on:
            music_btn_text = "Music_on"
        else:
            music_btn_text = "Music_off"
        dibujar_btn(music_btn_text,  pygame.Rect(300, 270, 300, 70), GREY, CLEAR_BLUE)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Verificar si se hizo clic con el botón izquierdo del mouse
                mouse_pos = pygame.mouse.get_pos()
                music_btn_rect = pygame.Rect(300, 270, 300, 70)
                if music_btn_rect.collidepoint(mouse_pos):
                    pygame.time.delay(200)
                    music_on = not music_on
                    pygame.mixer.music.set_volume(0)
                if music_on:
                    pygame.mixer.music.set_volume(0.10)
                    
        dibujar_btn("Scores",  pygame.Rect(300, 370, 300, 70), GREY, CLEAR_BLUE, scores_screen)
        crear_texto("Press ESC to go back", fuente, WHITE, (220, 500))
        pygame.display.flip()  # Actualizar la pantalla



def scores_screen():
    running = True
    contador = 0
    archivo_cargado = cargar_archivo_csv("scores.csv")
    SCREEN.fill(VIOLET)

    while running:
        contador += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        dibujar_btn("Score", pygame.Rect(300, 50, 300, 70), GREY, CLEAR_BLUE)

        # Mostrar puntajes solo una vez al inicio
        if contador == 1:
            height_score = 150

            # Encontrar el puntaje más alto
            max_puntaje = 0
            max_jugador = ""
            for i in range(1, len(archivo_cargado)):
                puntaje = int(archivo_cargado[i][1])
                if puntaje >= max_puntaje:
                    max_puntaje = puntaje
                    max_jugador = archivo_cargado[i][0]

            # Obtener los últimos tres puntajes
            ultimos_tres = archivo_cargado[-3:] if len(archivo_cargado) >= 3 else archivo_cargado

            # Mostrar el puntaje más alto
            crear_texto(f"BEST: JUGADOR {max_jugador} SCORE {max_puntaje}", fuente, GREY, (160, height_score))
            height_score += 80

            # Mostrar los últimos tres puntajes
            for j in range(len(ultimos_tres)):
                crear_texto(f"JUGADOR {ultimos_tres[j][0]} SCORE: {ultimos_tres[j][1]}", fuente, WHITE, (220, height_score))
                height_score += 80
            pygame.display.flip()
