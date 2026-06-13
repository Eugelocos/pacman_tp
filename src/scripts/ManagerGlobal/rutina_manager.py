




# MOVER A CONSTANTES

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

class RutinaManager():
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
        nivel = self.game_manager.nivel
        print("nivel=", nivel)
        if nivel == 1:
            # mover a constantes

            return [
                ('SCATTER', 7),
                ('CHASE', 20),
                ('SCATTER', 7),
                ('CHASE', 20),
                ('SCATTER', 5),
                ('CHASE', 20),
                ('SCATTER', 5),
                ('CHASE', -1),
            ]
        elif nivel <= 4:
            # mover a constantes

            return [
                ('SCATTER', 7),
                ('CHASE', 20),
                ('SCATTER', 7),
                ('CHASE', 20),
                ('SCATTER', 5),
                ('CHASE', 1033),
                ('SCATTER', 0.01),
                ('CHASE', -1),
            ]
        elif nivel > 4:
            # mover a constantes

            return [
                ('SCATTER', 5),
                ('CHASE', 20),
                ('SCATTER', 5),
                ('CHASE', 20),
                ('SCATTER', 5),
                ('CHASE', 1037),
                ('SCATTER', 0.01),
                ('CHASE', -1),
            ]
    
    def update(self, delta_time):
        if not self.pausa:
            delta_time = delta_time / 1000.0 # ms a seg
            self.cambio_modo_flag = False

            if self.asustado:
                self.contador_asustado += delta_time
                if self.contador_asustado >= self.duracion_asustado:
                    self.asustado = False
                    self.cambio_modo_flag = True
            else:
                if self.duracion_modo > 0:
                    self.contador_modo+=delta_time

                    if int(self.contador_modo) > int(self.contador_modo - delta_time):
                        resto = self.duracion_modo - self.contador_modo
                        print(f"[RUTINA] {self.modo}: {self.contador_modo:.1f}/{self.duracion_modo}s restante: {resto:.1f}s")
                    if self.contador_modo >= self.duracion_modo:
                        self.avanzar_rutina()
        
    def avanzar_rutina(self):
        self.cambio_modo_flag = True
        self.indice_actual += 1

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
        if self.asustado:
            return 'asustado'
        return self.modo

    def activar_asustado(self):
        data = DATA_ASUSTADO.get(self.game_manager.nivel, {"time": 0, "flashes": 0})

        if data['time'] > 0:
            self.asustado=True
            self.duracion_asustado=data['time']
            self.contador_asustado=0
            self.numero_destellos = data["flashes"]
            self.cambio_modo_flag=True
            return True
        elif data["time"] == 0:
            self.cambio_modo_flag=True
            return True
        return False

    def debe_revertir_direccion(self):
        return self.cambio_modo_flag
    
    def pausar(self):
        self.pausa = True
    
    def reanudar(self):
        self.pausa = False

    def reiniciar(self):
        self.indice_actual = 0
        self.modo = self.rutina[0][0]
        self.duracion_modo = self.rutina[0][1]
        self.contador_modo = 0
        self.asustado = False
        self.contador_asustado = 0
        self.duracion_asustado = 0
        self.cambio_modo_flag = False