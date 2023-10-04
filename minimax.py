import numpy as np
import random
import pygame
import sys
import math

##turnos
jugador = 0
IA = 1

##codigos de ficha en consola
vacio = 0
ficha_jugador = 1
ficha_IA = 2

def crear_tablero():	##dibujando tablero en matriz con 0s
    tablero = np.zeros((6, 7))	##dimensiones del tablero 6x7, 6 filas y 7 columnas
    return tablero

def soltar_ficha(tablero, fila, columna, ficha): ##soltar ficha requiere del tablero, fila, columna y codigo de ficha
    tablero[fila][columna] = ficha ##Se intercambia el valor del dato encontrado por el codigo de la ficha

def ubicacion_valida(tablero, columna): ## Se valida si la posicion donde el jugador pone su ficha es valida, 5=numero de filas, columna = la columna que el jugador escoja
    return tablero[5][columna] == 0

def obtener_proxima_fila_disponible(tablero, columna): ##Al haber seleccionado la columna, se evalua en que fila va a caer la ficha
    for fila in range(6):	##Evalua entre las filas
        if tablero[fila][columna] == 0: ##Si esa fila, en la determinada columna esta libre devuelve 0
            return fila				

def imprimir_tablero(tablero): ##Se voltea el tablero para que se vea correctamente
    print(np.flip(tablero, 0))

def movimiento_ganador(tablero, ficha):
    # Verificar ubicaciones horizontales para ganar
    for columna in range(7 - 3): ##cuando se verifica 4 en forma horizontal solo es posible comprobar hasta la columna 4 porque despues de esa el maximo que se podra es llegar a 3
        for fila in range(6): ## Todas las filas pueden ser validas
            ##Se verifica la ficha y que las 3 siguientes sean la misma ficha para ganar
            if tablero[fila][columna] == ficha and tablero[fila][columna + 1] == ficha and tablero[fila][columna + 2] == ficha and tablero[fila][columna + 3] == ficha: 
                return True

    # Verificar ubicaciones verticales para ganar
    for columna in range(7): ##Todas las columnas pueden ser validas
        for fila in range(6 - 3): ##cuando se verifica 4 en forma vertical solo es posible comprobar hasta la 3 fola porque despues el maximo no llegara a 4.
            ##Se verifica la ficha y que las 3 siguientes sean la misma ficha para ganar
            if tablero[fila][columna] == ficha and tablero[fila + 1][columna] == ficha and tablero[fila + 2][columna] == ficha and tablero[fila + 3][columna] == ficha:
                return True

    # Verificar diagonales inclinadas positivamente para ganar
    for columna in range(7 - 3): ##cuando se verifica 4 en forma horizontal solo es posible comprobar hasta la 4 columna porque despues el maximo no llegara a 4.
        for fila in range(6 - 3): ##cuando se verifica 4 en forma vertical solo es posible comprobar hasta la 3 fila porque despues el maximo no llegara a 4.
            if tablero[fila][columna] == ficha and tablero[fila + 1][columna + 1] == ficha and tablero[fila + 2][columna + 2] == ficha and tablero[fila + 3][columna + 3] == ficha:
                return True

    # Verificar diagonales inclinadas negativamente para ganar
    for columna in range(7 - 3):  ##cuando se verifica 4 en forma horizontal solo es posible comprobar hasta la 4 columna porque despues el maximo no llegara a 4.
        for fila in range(3, 6): ##cuando se verifica 4 en forma vertical solo es posible comprobar hasta la 3 fila porque despues el maximo no llegara a 4.
            if tablero[fila][columna] == ficha and tablero[fila - 1][columna + 1] == ficha and tablero[fila - 2][columna + 2] == ficha and tablero[fila - 3][columna + 3] == ficha:
                return True



def puntuar_posicion(tablero, ficha):
    puntaje = 0				##Se pone el contador de puntaje en 0

    # Puntuar columna central
    columna_central = [int(i) for i in list(tablero[:, 7 // 2])]
    conteo_central = columna_central.count(ficha)
    puntaje += conteo_central * 3

    # Puntuar horizontal
    for fila in range(6):		##Se recorre la fila
        fila_actual = [int(i) for i in list(tablero[fila, :])] ##Se crea un array para contar cuantas fichas del mismo color existen en la fila, se toma en cuenta todas las columnas
        for columna in range(7 - 3):	##Se eliminan las rondas que no podrian cumplir llegar a 4 fichas (similar a cuando se verifica movimiento ganador)
            potencial = fila_actual[columna:columna + 4] #un potencial es la posibilidad de llegar a 4 fichas, este valor selecciona la columna que puede obtener el 4
            puntaje += evaluar_potencial(potencial, ficha) ##Se usa la funcion evaluar potencial para designar el puntaje 

    # Puntuar vertical
    for columna in range(7): ##Se recorre columnas 
        columna_actual = [int(i) for i in list(tablero[:, columna])]  ##Se crea un array para contar cuantas fichas del mismo color existen en la columna, se toma en cuenta todas las filas
        for fila in range(6 - 3):	##Se eliminan las rondas que no podrian cumplir llegar a 4 fichas (similar a cuando se verifica movimiento ganador)
            potencial = columna_actual[fila:fila + 4] ##se halla el potencial, en este caso por fila
            puntaje += evaluar_potencial(potencial, ficha) ##Se usa la funcion evaluar potencial para designar el puntaje 

    # Puntuar diagonales inclinadas positivamente
    for fila in range(6 - 3):	##Se recorre las filas
        for columna in range(7 - 3): ## Se recorre columnas
            potencial = [tablero[fila + i][columna + i] for i in range(4)] ##Se calcula el potencial de la ficha en cuanto a diagonales
            puntaje += evaluar_potencial(potencial, ficha) ##Se usa la funcion evaluar potencial para designar el puntaje 

	 # Puntuar diagonales inclinadas negativamente
    for fila in range(6 - 3):##Se recorre las filas
        for columna in range(7 - 3):## Se recorre columnas
            potencial = [tablero[fila + 3 - i][columna + i] for i in range(4)] ##Se calcula el potencial de la ficha en cuanto a diagonales
            puntaje += evaluar_potencial(potencial, ficha) ##Se usa la funcion evaluar potencial para designar el puntaje 

    return puntaje

def evaluar_potencial(potencial, ficha): ##Calculara el puntaje
    puntaje = 0
    
    ficha_oponente = ficha_jugador ##Se hace intercambio de variables para poder variar el jugador
    if ficha == ficha_jugador:
        ficha_oponente = ficha_IA

    if potencial.count(ficha) == 4: ##Si la ficha puede cumplir 4, se puntua con 100
        puntaje += 100
    elif potencial.count(ficha) == 3 and potencial.count(vacio) == 1: ##Si la ficha puede cumplir 3, se puntua con 5 
        puntaje += 5
    elif potencial.count(ficha) == 2 and potencial.count(vacio) == 2: ##Si la ficha puede cumplir 2, se puntua con 2  
        puntaje += 2

    if potencial.count(ficha_oponente) == 3 and potencial.count(vacio) == 1: ##Si la ficha del oponente puede cumplir con 3, se puntua con -4
        puntaje -= 4

    return puntaje


##implementando minimax del pseudocodigo en wikipedia: https://en.wikipedia.org/wiki/Minimax#Pseudocode
def minimax(tablero, profundidad,maximizar_jugador): 
    columnas_validas = obtener_columnas_validas(tablero) ## Obteniendo las columnas validads
    es_terminal = es_nodo_terminal(tablero)	##definiendo si es la ultima jugada usando la funcion es nodo terminal
    
	##Si la profundidad es 0 o es el ultimo turno
    if profundidad == 0 or es_terminal:
        if es_terminal:	##Si es el ultimo turno
            if movimiento_ganador(tablero, ficha_IA): ##Si el movimiento final es de la IA mediante la funcion movimiento ganador (la que marca puntajes)
                return (None, 100000000000000)	##Se devolvera un puntaje muy grande si la AI puede terminar la partida, se pone None porque no interesa la columna en este caso
            elif movimiento_ganador(tablero, ficha_jugador): ##Si el movimiento final es del jugador mediante la funcion movimiento ganador (la que marca puntajes)
                return (None, -10000000000000) ##Se devolvera un puntaje muy pequeño si la AI no puede terminar la partida, se pone None porque no interesa la columna en este caso
            else:
                return (None, 0)	##Se devolvera 0 si la partida es un empate
        else: ##si la profundidad es 0, simplemente necesitamos ver el estado actual del tablero, por lo que se devuelve el puntaje actual de la IA
            return (None, puntuar_posicion(tablero, ficha_IA))
        
    if maximizar_jugador: ##MAX
        valor = -math.inf ##Segun el pseudocodigo se inicia un valor de menos infinito
        columna = random.choice(columnas_validas) ##Se escoje una columna al azar
        for col in columnas_validas:	#Se recorre los nodos hijos
            fila = obtener_proxima_fila_disponible(tablero, col) ##Posible fila a jugar
            copia_tablero = tablero.copy() ##Se copia el tablero para que la funcion recursiva no tenga errores.
            soltar_ficha(copia_tablero, fila, col, ficha_IA) ##Se ejecuta la funcion de soltar ficha (Se toma en cuenta la copia del tablero, la fila, la columnta y la ficha de IA)
            nuevo_puntaje = minimax(copia_tablero, profundidad - 1, False)[1] ## en la recursion se usa la copia del tablero, se sube la profundidad del arbol y se pone false para cambiar al otro jugador.
            if nuevo_puntaje > valor: ##Si el puntaje es mayor al anterior, se toma el puntaje mayor
                valor = nuevo_puntaje
                columna = col
        return columna, valor
    else:	##MIN
        valor = math.inf ## Se inicializa con un valor de mas infinito
        columna = random.choice(columnas_validas) ##Se escoje una columna al azar
        for col in columnas_validas:
            fila = obtener_proxima_fila_disponible(tablero, col)
            copia_tablero = tablero.copy()
            soltar_ficha(copia_tablero, fila, col, ficha_jugador)  ##Se ejecuta la funcion de soltar ficha (Se toma en cuenta la copia del tablero, la fila, la columnta y la ficha de del jugador)
            nuevo_puntaje = minimax(copia_tablero, profundidad - 1, True)[1] ## en la recursion se usa la copia del tablero, se sube la profundidad del arbol y se pone true para cambiar al otro jugador.
            if nuevo_puntaje < valor: ##Si el puntaje es menor al anterior se toma el puntaje menor
                valor = nuevo_puntaje
                columna = col
        return columna, valor

## Funcion que nos devuelve un array con las columnas disponibles para jugar
def obtener_columnas_validas(tablero):
    columnas_validas = []	##creacion del array
    for col in range(7):	##recorriendo columna
        if ubicacion_valida(tablero, col): ##Se usa la funcion ubicacion valida
            columnas_validas.append(col) ##Se agrega la columna a la lista
    return columnas_validas

def es_nodo_terminal(tablero): ## Comprueba mediante la funcion movimiento ganador si el arbol es el final
    return movimiento_ganador(tablero, ficha_jugador) or movimiento_ganador(tablero, ficha_IA) or len(obtener_columnas_validas(tablero)) == 0




def dibujar_tablero(tablero):	##dibujar tablero con pygame
    for col in range(7):
        for fila in range(6):
            pygame.draw.rect(screen, NEGRO, (col * SQUARESIZE, fila * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))	##dibujando rectangulo pide (surface,color,dimensiones)
            pygame.draw.circle(screen, GRIS, (int(col * SQUARESIZE + SQUARESIZE / 2), int(fila * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS) ##Dibujando circulos negros en cada cuadricula
    ##Dibujando las fichas de los participantes
    for col in range(7):
        for fila in range(6):       
            if tablero[fila][col] == ficha_jugador:
                pygame.draw.circle(screen, VERDE, (int(col * SQUARESIZE + SQUARESIZE / 2), height - int(fila * SQUARESIZE + SQUARESIZE / 2)), RADIUS) ##Se cambia al color del jugador, se usa height - para invertir el tablero
            elif tablero[fila][col] == ficha_IA: 
                pygame.draw.circle(screen, ROJO, (int(col * SQUARESIZE + SQUARESIZE / 2), height - int(fila * SQUARESIZE + SQUARESIZE / 2)), RADIUS) ##Se cambia al color de IA
    pygame.display.update() ##actualiza el tablero

tablero = crear_tablero()
imprimir_tablero(tablero)
juego_terminado = False

pygame.init()
##Colores para pygame
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)
VERDE = (0, 128, 0)
ROJO = (255, 0, 0)

SQUARESIZE = 100 ##Tamaño de cuadricula (se mide por diametro)

width = 7 * SQUARESIZE	##Largo de cuadricula
height = (6 + 1) * SQUARESIZE ##Altura de cuadricula (se añade uno para visualizar donde podria ir la ficha)

size = (width, height) ##tamaño del board

RADIUS = int(SQUARESIZE / 2 - 5) ## El radio es squaresize/2

screen = pygame.display.set_mode(size)
dibujar_tablero(tablero)
pygame.display.update()
myfont = pygame.font.SysFont("monospace", 75) ##fuente para el texto de victoria



turno = 0 ##turno 0 sera para el jugador, turno 1 para AI

while not juego_terminado:

    for event in pygame.event.get(): ##pygame funciona con eventos, por lo que toda accion se considera evento
        if event.type == pygame.QUIT: ## si se hace click en cerrar, el programa termina.
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, GRIS, (0, 0, width, SQUARESIZE)) ##se debe redibujar la parte negra cada vez que se mueve la ficha
            posx = event.pos[0]	##trackeando la posicion x del mouse
            if turno == jugador:
                pygame.draw.circle(screen, VERDE, (posx, int(SQUARESIZE / 2)), RADIUS) ##dibujando el circulo

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN: ##evento del click
            pygame.draw.rect(screen, GRIS, (0, 0, width, SQUARESIZE))
            if turno == jugador:
                posx = event.pos[0] ## Extrayendo la posicion x del click, solo nos interesa la posicion de la columna
                columna = int(math.floor(posx / SQUARESIZE)) ##determina la columna dividiendo entre el tamaño de la cuadricula, se usa math.floor para redondear.
                
				
				##Logica del juego
                if ubicacion_valida(tablero, columna): ##Se verifica que la columna sea valida
                    fila = obtener_proxima_fila_disponible(tablero, columna) ##Se obtiene la fila disponible en la columna escogida
                    soltar_ficha(tablero, fila, columna, ficha_jugador) ## se pone la ficha dle jugador en la matriz

                    if movimiento_ganador(tablero, ficha_jugador):
                        etiqueta = myfont.render("¡Jugador 1 gana!", 1, VERDE) ##imprime en pygame
                        screen.blit(etiqueta, (40, 10))						## imprime en pygame
                        juego_terminado = True								## el juego termina cambia a true para interrumpir el programa

                    turno += 1		##Se incrementa turno para que juegue la AI
                    turno = turno % 2 ## Se usa modulo para lograr que el turno solo varie entre 0 y 1

                    imprimir_tablero(tablero) ##imprimir el tablero corregido en consola
                    dibujar_tablero(tablero) ##imprime el tablero en pygame


    if turno == IA and not juego_terminado:				
		##Escoger columna mediante minimax parametros(tablero, profundidad, jugador que maximiza)
    
        columna, puntaje_minimax = minimax(tablero, 3, True)

        if ubicacion_valida(tablero, columna):		##Se verifica que la columna sea valida
            fila = obtener_proxima_fila_disponible(tablero, columna)	##Se obtiene la fila disponible en la columna escogida
            soltar_ficha(tablero, fila, columna, ficha_IA)	## se pone la ficha dle AI en la matriz

            if movimiento_ganador(tablero, ficha_IA):
                etiqueta = myfont.render("¡Jugador 2 gana!", 1, ROJO) ##imprime en pygame 
                screen.blit(etiqueta, (40, 10))								##imprime en pygame
                juego_terminado = True									## el juego termina cambia a true para interrumpir el programa

        
            turno += 1 ##Se incrementa turno para que juegue la AI
            turno = turno % 2 ## Se usa modulo para lograr que el turno solo varie entre 0 y 1
            
            imprimir_tablero(tablero) ##imprimir el tablero corregido en consola
            dibujar_tablero(tablero) ##imprime el tablero en pygame

    if juego_terminado:
        pygame.time.wait(1000)
