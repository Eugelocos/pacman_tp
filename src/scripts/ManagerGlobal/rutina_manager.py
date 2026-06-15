"""
Módulo del Administrador de Rutinas (rutina_manager.py)

Este archivo es el "cerebro" global de los fantasmas. Controla las famosas "olas" 
de Pac-Man: alterna entre el modo SCATTER (cada fantasma va a su esquina) y el 
modo CHASE (persiguen a Pac-Man). También maneja el temporizador de cuando están 
asustados porque Pac-Man se comió una pastilla grande.
"""

import constantes as c

class RutinaManager():
    """
    Clase encargada de llevar el cronómetro interno de los modos de los fantasmas.
    """

    def __init__(self, game_manager):
        
        self.game_manager=game_manager
        self.rutina = self.inicializar_rutinas()
        self.indice_actual = 0
        self.modo = self.rutina[0][0]
        self.duracion_modo = self.rutina[0][1]
        self.contador_modo = 0
        self.asustado = False
        self.contador_asustado = 0
        self.duracion_asustado = 0
        self.cambio_modo_flag = False
        self.numero_destellos = 5
        self.pausa = True
    
    def inicializar_rutinas(self):
        """
        Lee de constantes.py la rutina de tiempos correspondiente al nivel actual.
        """
        nivel = self.game_manager.nivel
        print("nivel=", nivel)
        
        if nivel == 1:
            return c.RUTINA_NIVEL_1
        elif nivel <= 4:
            return c.RUTINA_NIVEL_2_A_4
        else:
            return c.RUTINA_NIVEL_5_MAS
            
    def update(self, delta_time):
        """
        El reloj interno del manager. Suma los milisegundos y decide si ya es hora 
        de cambiar de estado (de Scatter a Chase, o si se terminó el tiempo asustado).

        Args:
            delta_time (int): Tiempo en milisegundos desde el último frame.
        """
        if not self.pausa:
            delta_time = delta_time / 1000.0 # ms a seg
            self.cambio_modo_flag = False

            # Si están asustados, pausamos la rutina normal y corre el timer de susto
            if self.asustado:
                self.contador_asustado += delta_time
                if self.contador_asustado >= self.duracion_asustado:
                    #Se acabó el efecto de la pastilla
                    self.asustado = False
                    self.cambio_modo_flag = True
            else:
                #Si no están asustados, corre la rutina normal (Scatter/Chase)
                if self.duracion_modo > 0:
                    self.contador_modo+=delta_time

                    if int(self.contador_modo) > int(self.contador_modo - delta_time):
                        resto = self.duracion_modo - self.contador_modo
                        print(f"[RUTINA] {self.modo}: {self.contador_modo:.1f}/{self.duracion_modo}s restante: {resto:.1f}s")
                    
                    # Si llegamos al tiempo límite de esta ola, pasamos a la siguiente
                    if self.contador_modo >= self.duracion_modo:
                        self.avanzar_rutina()
        
    def avanzar_rutina(self):
        """
        Pasa al siguiente elemento en la lista de la rutina actual.
        Si ya estaba en el último (que suele ser infinito), se queda ahí.

        Returns:
            tuple: (Nuevo modo en string, True).
        """
        self.cambio_modo_flag = True
        self.indice_actual += 1

        #Tope para no salirnos de la lista
        if self.indice_actual >= len(self.rutina):
            self.indice_actual = len(self.rutina) - 1

        nuevo_modo, duracion = self.rutina[self.indice_actual]
        tiempo_texto = f"{duracion}s" if duracion > 0 else "infinito"
        print(f"[RUTINA] Cambio a {nuevo_modo} - Duración: {tiempo_texto}")
        print(f"         Indice: {self.indice_actual}/{len(self.rutina)-1}")
        self.modo = nuevo_modo
        self.duracion_modo = duracion
        self.contador_modo = 0
        
        return self.modo, True

    def get_modo_actual(self):
        """
        Devuelve en qué modo andan los fantasmas ahora mismo.

        Returns:
            str: 'asustado', 'SCATTER' o 'CHASE'.
        """
        if self.asustado:
            return 'asustado'
        return self.modo

    def activar_asustado(self):
        """
        Se llama desde el GameScene cuando Pac-Man se come un Power Pellet.
        Lee los datos del nivel actual para saber cuántos segundos tienen que huir.

        Returns:
            bool: True si efectivamente se asustaron (si el tiempo es > 0), False si no.
        """
        data = c.DATA_ASUSTADO.get(self.game_manager.nivel, {"time": 0, "flashes": 0})

        if data['time'] > 0:
            self.asustado=True
            self.duracion_asustado=data['time']
            self.contador_asustado=0
            self.numero_destellos = data["flashes"]
            self.cambio_modo_flag=True
            return True
        elif data["time"] == 0:
            # En niveles muy altos, los fantasmas ya no se asustan, solo pegan la vuelta
            self.cambio_modo_flag=True
            return True
        return False

    def debe_revertir_direccion(self):
        """
        Avisa si los fantasmas tienen que darse vuelta (media vuelta) en este frame.

        Returns:
            bool: True si hubo un cambio de modo y deben girar, False si siguen normal.
        """
        return self.cambio_modo_flag
    
    def pausar(self):
        """Congela el cronómetro (ideal para cuando muere Pac-Man o hay intermisión)."""
        self.pausa = True
    
    def reanudar(self):
        """Vuelve a correr el cronómetro de la rutina."""
        self.pausa = False

    def reiniciar(self):
        """
        Resetea todo el manager a cero. Se usa al pasar de nivel o cuando 
        se reinicia el juego por completo.
        """
        self.indice_actual = 0
        self.modo = self.rutina[0][0]
        self.duracion_modo = self.rutina[0][1]
        self.contador_modo = 0
        self.asustado = False
        self.contador_asustado = 0
        self.duracion_asustado = 0
        self.cambio_modo_flag = False