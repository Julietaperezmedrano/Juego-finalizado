import pygame
from random import randint
from settings import *
import time
from utils import *
from pygame.locals import *
from shared import fuente
from leer_json import *

clock = pygame.time.Clock()  # para manejar el tiempo

background = pygame.transform.scale(background, SCREEN_SIZE)
personaje_principal = pygame.transform.scale(personaje_principal, (100, 100))
personaje_pos = personaje_principal.get_rect(topleft=(80, 440))

def detectar_colision(elem1, elem2):
    return elem1.colliderect(elem2)


def create_enemie(imagen, tam):
    """Crear enemigo

    Args:
        imagen: imagen a cargar
        tam: tamaño de la img

    Returns:
        imagen escalada
    """
    enemie = pygame.image.load(imagen)
    return pygame.transform.scale(enemie, tam)

def create_enemies(num_enemies, imagen, tam):
    """Crear lista de enemigos

    Args:
        num_enemies: numeros de enemigos que quiero que se muestren en la pantalla
        imagen: La imagen recibida de la funcion create enemie
        tam: El tam recibido de la funcion create enemie

    Returns:
        retorna la lista de enemigos
    """
    enemies = []
    for _ in range(num_enemies):
        x = randint(0, WIDTH - 50)
        y = randint(-150, -50)  # Colocar enemigos fuera de la pantalla, en la parte superior
        speed = randint(2, 5)  # Asignar una velocidad aleatoria a cada enemigo
        enemy = create_enemie(imagen, tam)
        enemies.append((enemy, pygame.Rect(x, y, 50, 50), speed))  # Añadir la velocidad al tuple
    return enemies

def create_gift(imagen, tam):
    """crear regalo

    Args:
        imagen: imagen del regalo
        tam: tamaño que tiene el regalo

    Returns:
        _type_: _description_
    """
    gift = pygame.image.load(imagen)
    return pygame.transform.scale(gift, tam)

def create_gifts(num_gifts, imagen, tam):
    """Crear lista de regalos

    Args:
        num_gifts: numero de gifts que quiero
        imagen: imagen pasada a create gift
        tam: tam pasado a create gifts

    Returns:
        retorna una lista de regalos
    """
    gifts = []
    for _ in range(num_gifts):
        x = randint(0, WIDTH - 50)
        y = randint(-150, -50)  
        speed = randint(2, 5)  
        gift = create_gift(imagen, tam)
        gifts.append((gift, pygame.Rect(x, y, 50, 50), speed))  
    return gifts



def juego():
    global proyectil_imagen, gift_image, vida_imagen, food

    speed = 15
    move_left = False
    move_right = False
    move_up = False
    move_down = False
    is_running = True
    personaje_mirando_derecha = False

    pygame.mixer.music.load("./src/assets/sounds/juego.mp3")
    pygame.mixer.music.set_volume(0.15)
    pygame.mixer.music.play(-1)

    # Crear enemigos una vez al inicio del juego
    enemies = create_enemies(10, "./src/assets/img/rata.png", (50, 50))

    # Crear regalos
    gifts = []
    gift_timer = time.time()  # Temporizador para controlar la aparición de los regalos

    vidas = [(10, 10), (70, 10), (130, 10)]

    # Añadir una variable para gestionar el tiempo de invulnerabilidad
    ultimo_tiempo_colision = 0
    tiempo_invulnerabilidad = 1  # 2 segundos de invulnerabilidad después de una colisión

    proyectiles = []

    # Cargar la imagen del proyectil
    proyectil_imagen = pygame.transform.scale(proyectil_imagen, (20, 20))

    # Cargar la imagen del regalo
    gift_image = pygame.transform.scale(gift_image, (50, 50))

    food = pygame.transform.scale(food, (60, 60))
    foods = []
    food_timer = time.time()

    score = 0
    while is_running:
        clock.tick(FPS)

        texto_score = f"Score: {score}"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.KEYDOWN:  # apretar una tecla
                if event.key == K_a:
                    move_left = True
                    move_right = False
                    personaje_mirando_derecha = True
                if event.key == K_d:
                    move_right = True
                    move_left = False
                    personaje_mirando_derecha = False
                if event.key == K_w:
                    move_up = True
                    move_down = False
                if event.key == K_s:
                    move_down = True
                    move_up = False
                if event.key == K_ESCAPE:
                    quit_game()
                if event.key == K_t:
                    proyectil_rect = proyectil_imagen.get_rect(midtop=personaje_pos.midtop)
                    proyectiles.append(proyectil_rect)
                    sound_proyectil = pygame.mixer.Sound("./src/assets/sounds/disparo.mp3")
                    sound_proyectil.play()

            if event.type == pygame.KEYUP:  # soltar una tecla
                if event.key == K_a:
                    move_left = False
                if event.key == K_d:
                    move_right = False
                if event.key == K_w:
                    move_up = False
                if event.key == K_s:
                    move_down = False

        if move_left and personaje_pos.left > 0:
            personaje_pos.left -= speed
        if move_right and personaje_pos.right < WIDTH:
            personaje_pos.right += speed
        if move_up and personaje_pos.top > 0:
            personaje_pos.top -= speed
        if move_down and personaje_pos.bottom < HEIGHT:
            personaje_pos.bottom += speed

        vida_imagen = pygame.transform.scale(vida_imagen, (50, 50))


        SCREEN.blit(background, ORIGIN)
        crear_texto(texto_score, fuente, WHITE, (WIDTH - 240, 20))

        for pos in vidas:
            SCREEN.blit(vida_imagen, pos)

        tiempo_actual = time.time()  # obtiene el tiempo actual

        # Crear un nuevo regalo cada 10 segundos
        if tiempo_actual - gift_timer >= 10:
            gift_x = randint(0, WIDTH - 50)
            gift_y = randint(-150, -50)
            gift_speed = randint(2, 5)
            gift_rect = gift_image.get_rect(topleft=(gift_x, gift_y))
            gifts.append((gift_image, gift_rect, gift_speed))
            gift_timer = tiempo_actual


        if tiempo_actual - food_timer >= 20:
            food_x = randint(0, WIDTH - 50)
            food_y = randint(-150, -50)
            food_speed = randint(1, 8)
            food_rect = food.get_rect(topleft=(food_x, food_y))
            foods.append((food, food_rect, food_speed))
            food_timer = tiempo_actual

        for enemy, enemy_rect, speed in enemies[:]:
            enemy_rect.y += speed  # Mover enemigo hacia abajo
            if enemy_rect.top > HEIGHT:  # Si el enemigo sale de la pantalla por la parte inferior
                enemy_rect.x = randint(0, WIDTH - 50)  # Reposicionar en un lugar aleatorio en la parte superior
                enemy_rect.y = randint(-150, -50)

            SCREEN.blit(enemy, enemy_rect)

            if detectar_colision(personaje_pos, enemy_rect) and tiempo_actual - ultimo_tiempo_colision > tiempo_invulnerabilidad:
                punch_sound = pygame.mixer.Sound("./src/assets/sounds/golpe.mp3")
                punch_sound.play()
                if vidas:
                    vidas.pop()
                    ultimo_tiempo_colision = tiempo_actual  # actualizar tiempo de última colisión
                    if len(vidas) == 0:
                        pygame.mixer.music.stop()
                        punch_sound.stop()
                        game_over(score)
                        

        # Actualizar la posición de los proyectiles y detectar colisiones con los enemigos
        for proyectil in proyectiles[:]:
            proyectil.y -= 10  # Mueve el proyectil hacia arriba

            # Verificar colisión con cada enemigo
            for enemy, enemy_rect, speed in enemies[:]:
                if proyectil.colliderect(enemy_rect):
                    try: 
                        proyectiles.remove(proyectil)
                        enemies.remove((enemy, enemy_rect, speed))
                        score += 10
                        enemies.append((enemy, pygame.Rect(randint(0, WIDTH - 50), randint(-150, -50), 50, 50), speed))
                    except ValueError as e:
                        print("Error al eliminar enemigo", e)


        # Dibujar los proyectiles en la pantalla
        for proyectil in proyectiles:
            SCREEN.blit(proyectil_imagen, proyectil)

        # Actualizar y dibujar los regalos
        for gift, gift_rect, gift_speed in gifts[:]:
            gift_rect.y += gift_speed  # Mover el regalo hacia abajo
            if gift_rect.top > HEIGHT:  # Si el regalo sale de la pantalla por la parte inferior
                gifts.remove((gift, gift_rect, gift_speed))

            SCREEN.blit(gift, gift_rect)

            if detectar_colision(personaje_pos, gift_rect):
                gifts.remove((gift, gift_rect, gift_speed))
                if len(vidas) < 4:
                    vidas.append((len(vidas) * 60 + 10, 10))  # Añadir una vida
                    bonus = pygame.mixer.Sound("./src/assets/sounds/menuboton.mp3")
                    bonus.play()


        for food, food_rect, food_speed in foods[:]:
            food_rect.y += food_speed  # Mover el regalo hacia abajo
            if food_rect.top > HEIGHT:  # Si el regalo sale de la pantalla por la parte inferior
                foods.remove((food, food_rect, food_speed))

            SCREEN.blit(food, food_rect)

            if detectar_colision(personaje_pos, food_rect):
                foods.remove((food, food_rect, food_speed))
                score += 30
                
        #giro img
        if personaje_mirando_derecha:
            SCREEN.blit(personaje_principal, personaje_pos)
        else:
            personaje_principal_volteado = pygame.transform.flip(personaje_principal, True, False)
            SCREEN.blit(personaje_principal_volteado, personaje_pos)

        pygame.display.flip()  # actualizar pantalla

flag_space_2 = True
game_over_sound = pygame.mixer.Sound("./src/assets/sounds/game_over.wav")


def game_over(puntaje):
    archivo_cargado = cargar_archivo_csv("scores.csv") #leer
    for i in range(1, len(archivo_cargado)): 
        ultimo_id = archivo_cargado[i][0]
    id_actual = int(ultimo_id) + 1

    agregar_id_score("scores.csv", id_actual, puntaje) #escribir

    flag_sound_game_over = True
    max_puntaje = 0
    if int(ultimo_id) == 0:
        max_puntaje = puntaje
    else:
        for i in range(1, len(archivo_cargado)):
            if int(archivo_cargado[i][1]) > max_puntaje:
                max_puntaje = int(archivo_cargado[i][1])
    while True:
        SCREEN.fill(BLACK)
        if flag_sound_game_over:
            game_over_sound.play()
            flag_sound_game_over = False

        if puntaje > max_puntaje:
            max_puntaje = puntaje

        score = f"Score: {puntaje}"
        max_score = f"Max Score: {max_puntaje}"

        for event in pygame.event.get():
            if event.type == QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    juego()

        if flag_space_2:
            crear_texto("G A M E  O V E R", fuente, CUSTOM_1, (290, 70))
            crear_texto("G A M E  O V E R", fuente, CUSTOM_2, (290, 120))
            crear_texto("G A M E  O V E R", fuente, WHITE, (290, 170))
            crear_texto(score, fuente, PINK, (320 , 300))
            crear_texto(max_score, fuente, YELLOW_GREEN, (280, 360))
            crear_texto("Presione SPACE para continuar...", fuente, GREY, (110, 510))

        pygame.display.flip()