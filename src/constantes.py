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


#JUGADOR
VELOCIDAD_BASE=7.5*TAMAÑO_PARED

#PARPADEO PRINCIPAL
PARPADEO=100

#FANTASMAS 
FANTASMAS = [
    ("fantasma_rojo", "Blinky", "Rojo - El perseguidor.", ROJO),
    ("fantasma_rosa", "Pinky", "Rosa - El emboscador.", ROSA),
    ("fantasma_cian", "Inky", "Celeste - El flanqueador.", CIAN),
    ("fantasma_naranja", "Clyde", "Naranja - El tímido.", NARANJA),
    ("fantasma_verde", "Artola", "Verde - El traidor.", VERDE),
    ("fantasma_violeta", "Michae", "Violeta - El kamikaze.", VIOLETA),
]

