class EscenaBase():
    """Clase base abstracta para todas las escenas del juego.

    Define la interfaz que deben implementar todas las escenas (menu, juego,
    game over, etc.). Utiliza el patron Template Method para que las escenas
    hijas sobrescriban los metodos necesarios.

    Metodos principales:
        update(delta_time, eventos): Actualiza la logica de la escena.
        render(): Dibuja los elementos de la escena en pantalla.
        on_enter(): Se ejecuta al entrar a la escena (inicializacion).
        on_exit(): Se ejecuta al salir de la escena (limpieza).

    Attributes:
        game_manager (GameManager): Referencia al administrador principal del juego.
    """
    def __init__(self, game_manager):
        """Guarda la referencia al GameManager.

        Args:
            game_manager: Instancia del GameManager.
        """
        self.game_manager = game_manager

    def update(self, delta_time, eventos):
        """Actualiza la logica de la escena (movimientos, colisiones, etc.)."""
        pass
    
    def render(self):
        """Dibuja todos los elementos de la escena en pantalla."""
        pass
    
    def on_exit(self):
        """Se ejecuta al salir de la escena (detener sonidos, pausar rutinas)."""
        pass

    def on_enter(self):
        """Se ejecuta al entrar a la escena (reanudar rutinas, inicializar)."""
        pass

