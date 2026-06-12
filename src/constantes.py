#VENTANA
ANCHO_VENTANA=800
ALTO_VENTANA=750
COLOR_BG=(0,0,20)
TAMAÑO_PARED=25
MAPA_ANCHO = 28  # columnas
MAPA_ALTO = 31   # filas

FPS=60
#direcciones
DIRECCIONES = {
    "UP":    (0, -1),
    "DOWN":  (0,  1),
    "LEFT":  (-1, 0),
    "RIGHT": (1,  0),
    "IDLE":  (0,  0)
}

#COLORES
AZUL=(0,0,255)
BLANCO=(255,255,255)
AMARILLO = (255, 255, 0)
VERDE=(50, 205, 50)
ROJO=(255, 0, 0)
ROSA=(255, 182, 193)
CIAN=(0, 255, 255)
NARANJA=(255, 165, 0)
VERDE=(0, 255, 0)
VIOLETA=(148, 0, 211)
GRIS=(128, 128, 128)

#JUGADOR
VELOCIDAD_BASE=7.5*TAMAÑO_PARED

#PARPADEO PRINCIPAL
PARPADEO=150

#FANTASMAS 
FANTASMAS = [
    ("fantasma_rojo", "Blinky", "Rojo - El perseguidor.", ROJO,),
    ("fantasma_rosa", "Pinky", "Rosa - El emboscador.", ROSA),
    ("fantasma_cian", "Inky", "Celeste - El flanqueador.", CIAN),
    ("fantasma_amarillo", "Clyde", "Naranja - El tímido.", NARANJA),
    ("fantasma_verde", "Artola", "Verde - El traidor.", VERDE),
    ("fantasma_violeta", "Michae", "Violeta - El kamikaze.", VIOLETA),
]

#SONIDOS Y RUTAS: 

MUSICA = {
    "welcome": "pacman_tp//assets//sonidos//inicio.mp3",
    "select_fantasmas": "pacman_tp//assets//sonidos//menu_elegir_fantasmas.mp3",
    "select_esquinas": "pacman_tp//assets//sonidos//menu_elegir_fantasmas.mp3",    
}

EFECTOS = {
    "punto" : "pacman_tp//assets//sonidos//waka_waka.wav",
    "power_pellet" : "pacman_tp//assets//sonidos//power_pellet.wav",
    "mov_fantasmas" : "pacman_tp//assets//sonidos//sirena_fantasmas_1.wav",
    "fantasma_comido" : "pacman_tp//assets//sonidos//pacman_come_fantasma.wav",
    "ojos" : "pacman_tp//assets//sonidos//sirena_ojos.wav",
    "vida_perdida" : "pacman_tp//assets//sonidos//vida_perdida.wav"
}