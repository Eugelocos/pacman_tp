import pygame
import os
import sys
import math
import constantes as c 
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from data_structures.character.character_data_type import Personaje
from scripts.Utils.visual import AnimacionExplosion
from scripts.Fantasmas.phantom import decidir_movimiento


class Enemigo(Personaje):
    sprites_cache={}
    sprite_asustado=None
    sprite_blanco=None
    sprite_ojos=None
    def __init__(self, position, visibility, nombre_enemigo, tile_size, direction="derecha", state='scatter', pos_inicial=(0,0), target=(0,0)):
        ruta_inicial = f"pacman_tp/assets/imagenes/characters/enemies/{nombre_enemigo}/horizontal/{nombre_enemigo}_0.png"
        super().__init__(position, visibility, direction, tile_size, ruta_inicial, False)
        self.velocidad = c.VELOCIDAD_BASE * 0.75
        self.state=state
        self.pos_inicial=pos_inicial
        self.target=target
        self.nombre_enemigo=nombre_enemigo
        self.jugador_ref=None
        self.esta_en_casa=True
        self.ultima_celda=None
        if self.nombre_enemigo not in Enemigo.sprites_cache:
            self.cargar_frames()
        if Enemigo.sprite_asustado is None:
            Enemigo.sprite_asustado = pygame.transform.scale(cargar_con_transparencia("pacman_tp//assets//imagenes//characters//enemies//fantasma_asustado//fantasma_asustado_0.png"), (self.tile_size, self.tile_size))
        if Enemigo.sprite_blanco is None:
            Enemigo.sprite_blanco= pygame.transform.scale(cargar_con_transparencia("pacman_tp//assets//imagenes//characters//enemies//fantasma_asustado//fantasma_asustado_1.png"), (self.tile_size, self.tile_size))
        if Enemigo.sprite_ojos is None: 
            ruta_ojos_vert="pacman_tp//assets//imagenes//characters//enemies//ojos_fantasmas//ojos_vertical.png"
            ruta_ojos_hor="pacman_tp//assets//imagenes//characters//enemies//ojos_fantasmas//ojos_horizontal.png"
            ojos_arriba=pygame.transform.scale(cargar_con_transparencia(ruta_ojos_vert), (self.tile_size, self.tile_size))
            ojos_derecha=pygame.transform.scale(cargar_con_transparencia(ruta_ojos_hor), (self.tile_size, self.tile_size))
            ojos_abajo=pygame.transform.flip(ojos_arriba,False,True)
            ojos_izquierda=pygame.transform.flip(ojos_derecha,True,False)
            Enemigo.sprite_ojos={"arriba":ojos_arriba,
                                 "abajo":ojos_abajo,
                                 "derecha":ojos_derecha,
                                 "izquierda":ojos_izquierda}         

    def cargar_frames(self):
        for direccion in ["arriba", "abajo", "derecha", "izquierda"]:
            for i in range(2):
                if self.nombre_enemigo not in Enemigo.sprites_cache:
                    Enemigo.sprites_cache[self.nombre_enemigo]={}
                if direccion.lower() not in Enemigo.sprites_cache[self.nombre_enemigo]:
                    Enemigo.sprites_cache[self.nombre_enemigo][direccion.lower()]=[]
                if direccion == "izquierda" or direccion == "derecha":
                    ruta=f"pacman_tp/assets/imagenes/characters/enemies/{self.nombre_enemigo}/horizontal/{self.nombre_enemigo}_{i}.png"
                    if direccion == "izquierda":
                        Enemigo.sprites_cache[self.nombre_enemigo][direccion.lower()].append(pygame.transform.scale(cargar_con_transparencia(ruta), (self.tile_size, self.tile_size)))
                    else:
                        Enemigo.sprites_cache[self.nombre_enemigo][direccion.lower()].append(pygame.transform.scale(pygame.transform.flip(cargar_con_transparencia(ruta), True, False), (self.tile_size, self.tile_size)))
                else:
                    ruta=f"pacman_tp/assets/imagenes/characters/enemies/{self.nombre_enemigo}/{direccion.lower()}/{self.nombre_enemigo}_{i}.png"
                    Enemigo.sprites_cache[self.nombre_enemigo][direccion.lower()].append(pygame.transform.scale(cargar_con_transparencia(ruta), (self.tile_size, self.tile_size)))
        self.cambiar_sprite_por_direccion()


    def cambiar_sprite_por_direccion(self):
        if self.state=="muerto":
            if self.direction[0]==0 and self.direction[1]==-1:
                self.frames=[Enemigo.sprite_ojos["arriba"]]
            elif self.direction[0]==0 and self.direction[1]==1:
                self.frames=[Enemigo.sprite_ojos["abajo"]]
            elif self.direction[0]==1 and self.direction[1]==0:
                self.frames=[Enemigo.sprite_ojos["derecha"]]
            elif self.direction[0]==-1 and self.direction[1]==0:
                self.frames=[Enemigo.sprite_ojos["izquierda"]]    
            self.frame_actual = 0
            self.image = self.frames[self.frame_actual]
            return
        
        if self.direction[0]==0 and self.direction[1]==-1:
            self.frames=Enemigo.sprites_cache[self.nombre_enemigo]["arriba"]
        elif self.direction[0]==0 and self.direction[1]==1:
            self.frames=Enemigo.sprites_cache[self.nombre_enemigo]["abajo"]
        elif self.direction[0]==1 and self.direction[1]==0:
            self.frames=Enemigo.sprites_cache[self.nombre_enemigo]["derecha"]
        elif self.direction[0]==-1 and self.direction[1]==0:
            self.frames=Enemigo.sprites_cache[self.nombre_enemigo]["izquierda"]
            
        self.frame_actual=0
        self.image=self.frames[self.frame_actual]

    def actualizar_animacion(self, delta_time):
        
        if self.state=="asustado":
            self.image=Enemigo.sprite_asustado
        elif self.state=="asustado_parpadeando":
            tiempo=pygame.time.get_ticks()
            if (tiempo//250) % 2 == 0:
                self.image = Enemigo.sprite_asustado  # Azul
            else:
                self.image = Enemigo.sprite_blanco    # Blanco
        else:
            super().actualizar_animacion(delta_time)

    def update(self, pantalla, delta_time, escena, eventos=None):
        if not self.jugador_ref:
            self.jugador_ref = escena.jugador

        estados_validos=["asustado", "asustado_parpadeando", "muerto","explotando"]
        if self.state not in estados_validos:
            self.state = escena.game_manager.rutina_manager.get_modo_actual().lower()
            
        if self.state == "explotando":
            tiempo_actual = pygame.time.get_ticks()
            # Si pasaron 3000 milisegundos (3 segundos) desde que frenó:
            if tiempo_actual - getattr(self, "tiempo_inicio_explosion", tiempo_actual) >= 3000:
                self.detonar(escena)
            pass
        else:
            self.proxima_direccion=decidir_movimiento(self.jugador_ref, self, escena.game_manager)


        super().update(pantalla, delta_time, escena, eventos)

    def detonar(self, escena):

        centro_explosion = (self.rect.centerx, self.rect.centery)
        # Radio de 5 celdas exactas en formato circular
        radio_explosion = 5 * c.TAMAÑO_PARED 

        # Evaluamos a TODAS las entidades en pantalla
        for entity in escena.game_manager.entities:
            # Evitamos que el morado se evalúe a sí mismo antes de tiempo
            if entity == self:
                continue

            centro_entidad = (entity.rect.centerx, entity.rect.centery)
            
            # Calculamos la distancia euclidiana real (circular)
            distancia = math.hypot(centro_entidad[0] - centro_explosion[0], centro_entidad[1] - centro_explosion[1])

            # Si la entidad está dentro del radio de la explosión...
            if distancia <= radio_explosion:
                
                # 1. Si es el jugador
                if hasattr(entity, 'es_jugador') and entity.es_jugador:
                    entity.lives -= 1
                    # Opcional: si querés que suene la muerte
                    if hasattr(escena, 'muerte') and escena.muerte:
                         escena.muerte.play()
                
                # 2. Si es otro fantasma (Fuego amigo)
                elif hasattr(entity, 'nombre_enemigo'):
                    entity.state = "muerto"
                    entity.velocidad = c.VELOCIDAD_BASE * 1.5               # Vuelve rápido a la base
                    entity.cambiar_sprite_por_direccion()                   # Actualiza a sprite de ojos
                    if hasattr(entity, 'destino_kamikaze'):
                        del entity.destino_kamikaze
        animacion = AnimacionExplosion(centro_explosion[0], centro_explosion[1], radio_explosion)
        
        # Agregamos la animación al grupo general de sprites para que el GameManager la dibuje y actualice
        escena.game_manager.entities.add(animacion)
        # Finalmente, el morado "muere" tras explotar
        self.state = "muerto"
        self.velocidad = c.VELOCIDAD_BASE * 1.5                             # Vuelve rápido a la base
        self.cambiar_sprite_por_direccion()                                 # Actualiza a sprite de ojos
        if hasattr(self, 'destino_kamikaze'):
            del self.destino_kamikaze
        


def cargar_con_transparencia(ruta):
    img = pygame.image.load(ruta).convert()  
    img.set_colorkey((0, 0, 0))             
    return img.convert_alpha()  