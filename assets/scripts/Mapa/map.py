#abrir el mapa 

with open("pacman_tp/assets/scripts/Mapa/mapa.txt","r") as mapa:
    matriz_mapa=[]
    caracteres_validos=["X",".","P","o"," ","G","-","T"]
    for linea in mapa:
        l=linea.strip()
        for letra in l:
            if letra not in caracteres_validos:
                print("mapa invalido")
                break    
        matriz_mapa.append(l)

#funcion de crear el mapa
def crear_mapa(matriz,ventana):
    for x in range(31):
        for y in range(28):
            if matriz[x][y]=="X":
                pared=pygame.Rect(y*c.TAMAÑO_PARED,x*c.TAMAÑO_PARED,c.TAMAÑO_PARED,c.TAMAÑO_PARED)
                pygame.draw.rect(ventana,c.AZUL,pared)
            elif matriz[x][y]==".":
                pun_peq=Item(y*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,x*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,1,[punto_pequeño])
                grupo_items.add(pun_peq)
            elif matriz[x][y]=="o":
                pun_gran=Item(y*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,x*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,2,[punto_grande])
                grupo_items.add(pun_gran)
            elif matriz[x][y]=="P":
                #crear jugador 
                jugador=Personaje(y*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,x*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,c.COLOR_PERSONAJE,animaciones) 
            elif matriz[x][y]=="G":
                #crear enemigo
                for i in range(4):
                    fantasma_amarillo=Personaje(y*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,x*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,c.COLOR_PAREDES,animaciones_enemigos[0])
                    fantasma_cian=Personaje(y*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,x*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,c.COLOR_PAREDES,animaciones_enemigos[1])
                    fantasma_rojo=Personaje(y*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,x*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,c.COLOR_PAREDES,animaciones_enemigos[2])
                    fantasma_rosa=Personaje(y*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,x*c.TAMAÑO_PARED+c.TAMAÑO_PARED//2,c.COLOR_PAREDES,animaciones_enemigos[3])

                #crear lista de enemigos
                lista_enemigos=[]
                lista_enemigos.append(fantasma_amarillo)
                lista_enemigos.append(fantasma_cian)
                lista_enemigos.append(fantasma_rojo)
                lista_enemigos.append(fantasma_rosa)

    return jugador,lista_enemigos

