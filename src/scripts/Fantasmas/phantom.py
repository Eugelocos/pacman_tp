from funciones_aux import nombres_carpetas,escalar_img,contar_elementos
import pacman_tp.src.constantes as c 
import pygame


def decidir_movimiento(jugador, fantasma, game_manager, ):
    # Lógica para decidir la dirección del fantasma

    # se llamaria a:
    # self.cambiar_direccion(nueva_direccion)
    # donde nueva_direccion es una de las siguientes: "arriba", "abajo", "izquierda", "derecha"
    # la logica de decision dependera del tipo de fantasma ( self.nombre_enemigo ) y del estado del juego ( self.state )

    target=decidir_target(jugador, fantasma, game_manager)
    direccion=decidir_direccion(fantasma, target, game_manager)
    pass

def decidir_target(jugador, fantasma, game_manager):
    target=None
    if fantasma.state=="scatter":
        target=fantasma.pos_inicial
    elif fantasma.state=="chase":
        if fantasma.name=="fantasma_rojo":
            target=(jugador.rect.centerx, jugador.rect.centery)
        ...
    elif fantasma.state=="muerto":
        target=(13, 11)

    return target

def decidir_direccion(fantasma, target, game_manager):
    
    pass


