import pygame

class Entity(pygame.sprite.Sprite):
    """Clase base abstracta para todas las entidades del juego.

    Hereda de pygame.sprite.Sprite para poder agrupar entidades en grupos
    y usar metodos nativos de pygame como colisiones y actualizacion en masa.
    Toda entidad (jugador, fantasmas, tiles) hereda de esta clase.

    Attributes:
        visibility (bool): True si la entidad debe ser visible, False si no.
        image (pygame.Surface | None): Imagen de la entidad escalada al tile_size.
        rect (pygame.Rect): Rectangulo de posicion y tamaño (centro para ubicacion).
        tile_size (int | float): Tamano de celda para escalado de imagenes.
    """

    def __init__(self, position: tuple, visibility: bool, tile_size: int|float, sprite=None):
        """Inicializacion de la entidad

        Args:
            position (tuple): Representa el centro de la entidad en pixeles
            visibility (bool): Si se dibuja o no se dibuja
            tile_size (int | float): EL tamano de celda por el que se escalara la imagen, caulquier entidad lo tiene
            sprite (str, optional): Ruta de la imagen que utilizara, si es None se utiliza un pygame.rect simple. Defaults to None.
        """
        super().__init__()

        self.visibility=visibility
        if sprite:
            self.image=pygame.transform.scale(pygame.image.load(sprite).convert_alpha(), (tile_size, tile_size))
        else:
            self.image=None
        if self.image:
            self.rect = self.image.get_rect()
        else:
            self.rect = pygame.Rect(0, 0, tile_size, tile_size)
        self.tile_size=tile_size
        x,y=position
        x, y = position
        self.rect.centerx = x
        self.rect.centery = y
    def draw(self, pantalla):
        """Metodo para renderizar la entidad en la ventana

        Args:
            pantalla (pygame.Surface): Superficie en la que se dibujara la entidad
        """
        pantalla.blit(self.image, (self.rect.x, self.rect.y))
    def update(self, ventana,  delta_time: int|float, escena=None, eventos=None):
        """Metodo para actualizar a la entidad

        Args:
            ventana (pygame.Surface): Superficie en la que se dibujara la entidad
            delta_time (float|int): Tiempo que tarda el ordenador en procesar y mostrar un único fotograma (o frame) en pantalla
            escena (object, optional): Objeto de la escena. Defaults to None.
            eventos (_type_, optional): Eventos de pygame. Defaults to None.
        """
        self.actualizar_animacion(delta_time) 
    def actualizar_animacion(self, delta_time: int|float):
        """Place holder, se utiliza para actualizar la animacion y el frame

        Args:
            delta_time (float|int): Tiempo que tarda el ordenador en procesar y mostrar un único fotograma (o frame) en pantalla
        """
        pass


