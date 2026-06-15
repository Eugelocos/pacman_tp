"""
MODULO DE CONSTANTES GLOBALES

este archivo centraliza todas las configuraciones "fijas" del juego.
Contiene las dimensiones de la ventana, definiciones de grilla, paleta de colores, 
velocidades, atributos de los enemigos y rutas a los recursos (assets) de audio.
Modificar los valores aquí afectará globalmente el comportamiento y la estética del juego.

"""



#CONFIGURACION DE VENTANA
ANCHO_VENTANA = 476
ALTO_VENTANA = 612
COLOR_BG = (0,0,20) #Color del fondo
TAMAÑO_PARED = (612//36) #Tamaño en pixeles de cada tile (aprox 17px)
MAPA_ANCHO = 28  # columnas
MAPA_ALTO = 31   # filas
FPS=60 #taza de fotogramas por segundo a la que corre el juego


#MOVIMIENTO Y DIRECCIONES
DIRECCIONES = {
    "UP":    (0, -1),
    "DOWN":  (0,  1),
    "LEFT":  (-1, 0),
    "RIGHT": (1,  0),
    "IDLE":  (0,  0)    #estado de reposo
}

#COLORES (EN RGB)
AZUL=(33, 33, 222)
BLANCO=(255,255,255)
AMARILLO = (255, 231, 55)
VERDE=(50, 205, 50)
ROJO=(253, 0, 0)
ROSA=(255, 182, 193)
CIAN=(0, 255, 255)
NARANJA=(255, 165, 0)
VERDE=(0, 255, 0)
VIOLETA=(148, 0, 211)
GRIS=(128, 128, 128)

#JUGADOR
VELOCIDAD_BASE=7.5*TAMAÑO_PARED #velocidad de movimiento base de todo el juego, todas las entidades utlizan esta velocidad como guia

#PARPADEO PRINCIPAL
PARPADEO=150 #intervalo en milisegundos para las animaciones de parpadeo (como los textos en pantalla)

#FANTASMAS 
#Lista que define cada fantasma.
#Formato: (Identificador interno, Nombre propio, Descripción, Color en RGB)
FANTASMAS = [
    ("fantasma_rojo", "Blinky", "Rojo - El perseguidor.", ROJO,),
    ("fantasma_rosa", "Pinky", "Rosa - El emboscador.", ROSA),
    ("fantasma_cian", "Inky", "Celeste - El flanqueador.", CIAN),
    ("fantasma_amarillo", "Clyde", "Naranja - El tímido.", NARANJA),
    ("fantasma_verde", "Artola", "Verde - El traidor.", VERDE),
    ("fantasma_violeta", "Artur", "Violeta - El kamikaze.", VIOLETA),
]

#multiplicadores de velocidad para alterar el movimiento base según que enemigo es
MULTIPLICADOR_VELOCIDAD_ENEMIGOS = {
    "fantasma_rojo": 1.0,
    "fantasma_rosa": 1.0,
    "fantasma_cian": 1.0,
    "fantasma_amarillo": 1.0,
    "fantasma_verde": 1.5, #el fantasma artola es mas rapido 
    "fantasma_violeta": 1.0
}



#SONIDOS Y RUTAS: 
#Diccionario con las rutas a los archivos de música de fondo por escena
MUSICA = {
    "welcome": "pacman_tp//assets//sonidos//inicio.mp3",
    "select_fantasmas": "pacman_tp//assets//sonidos//menu_elegir_fantasmas.mp3",
    "select_esquinas": "pacman_tp//assets//sonidos//menu_elegir_fantasmas.mp3",   
    "intermision": "pacman_tp//assets//sonidos//menu_elegir_fantasmas.mp3",
    "game_over":"pacman_tp//assets//sonidos//game_over.mp3"
}

#Diccionario con las rutas a los efectos de sonido puntuales.
EFECTOS = {
    "punto" : "pacman_tp//assets//sonidos//waka_waka.wav",
    "power_pellet" : "pacman_tp//assets//sonidos//power_pellet.wav",
    "mov_fantasmas" : "pacman_tp//assets//sonidos//sirena_fantasmas_1.wav",
    "fantasma_comido" : "pacman_tp//assets//sonidos//pacman_come_fantasma.wav",
    "ojos" : "pacman_tp//assets//sonidos//sirena_ojos.wav",
    "vida_perdida" : "pacman_tp//assets//sonidos//vida_perdida.wav",
    "click" : "pacman_tp//assets//sonidos//click.mp3",
    "error" : "pacman_tp//assets//sonidos//error.mp3",
    "jugar" : "pacman_tp//assets//sonidos//jugar.mp3",
    "explosion" : "pacman_tp//assets//sonidos//explosion.wav",
    "pre_explosion":"pacman_tp//assets//sonidos//pre_explosion.wav"
}



# RUTINAS Y TIEMPOS DE LOS FANTASMAS

#Tiempos del modo "Asustado" según el nivel
DATA_ASUSTADO = {
    1: {"time": 6, "flashes": 5}, 2: {"time": 5, "flashes": 5},
    3: {"time": 4, "flashes": 5}, 4: {"time": 3, "flashes": 5},
    5: {"time": 2, "flashes": 5}, 6: {"time": 5, "flashes": 5},
    7: {"time": 2, "flashes": 5}, 8: {"time": 2, "flashes": 5},
    9: {"time": 1, "flashes": 3}, 10: {"time": 5, "flashes": 5},
    11: {"time": 2, "flashes": 5}, 12: {"time": 1, "flashes": 3},
    13: {"time": 1, "flashes": 3}, 14: {"time": 3, "flashes": 5},
    15: {"time": 1, "flashes": 3}, 16: {"time": 1, "flashes": 3},
    17: {"time": 0, "flashes": 0}, 18: {"time": 1, "flashes": 3},
    19: {"time": 0, "flashes": 0}, 20: {"time": 0, "flashes": 0},
}

#Modos (Estado, Segundos)
RUTINA_NIVEL_1 = [
    ('SCATTER', 7), ('CHASE', 20), ('SCATTER', 7), ('CHASE', 20),
    ('SCATTER', 5), ('CHASE', 20), ('SCATTER', 5), ('CHASE', -1),
]

RUTINA_NIVEL_2_A_4 = [
    ('SCATTER', 7), ('CHASE', 20), ('SCATTER', 7), ('CHASE', 20),
    ('SCATTER', 5), ('CHASE', 1033), ('SCATTER', 0.01), ('CHASE', -1),
]

RUTINA_NIVEL_5_MAS = [
    ('SCATTER', 5), ('CHASE', 20), ('SCATTER', 5), ('CHASE', 20),
    ('SCATTER', 5), ('CHASE', 1037), ('SCATTER', 0.01), ('CHASE', -1),
]