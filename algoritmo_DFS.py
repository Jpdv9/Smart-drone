# DESARROLLO DEL ALGORITMO DE BÚSQUEDA PREFERENTE POR PROFUNDIDAD:



# Se define una función que reciba la matriz o tablero de juego y retorne la posición inicial del dron y las posiciones de los paquetes:
def encontrar_inicio_y_paquetes(matriz):

    # Se crean variables para guardar las posiciones:
    inicio = None  
    paquetes = set()

    # Se recorre la matriz buscando la posición inicial y los paquetes:  
    for i, fila in enumerate(matriz):
        for j, valor in enumerate(fila):

            # Se guardan las posiciones:
            if valor == 2:
                inicio = (i, j)
            elif valor == 4:
                paquetes.add((i, j))

    # Se retornan las posiciones:
    return inicio, paquetes



# Se define una función que recibe la posición actual del dron, la matriz o tablero y la prioridad definida de los movimientos, para retornar las posiciones de los vecinos disponibles:
def obtener_vecinos(pos, matriz, prioridad):

    # Se inicializan variables relacionadas a las dimenciones del tablero y a la posición actual del dron:
    filas, columnas = len(matriz), len(matriz[0]) 
    i, j = pos

    # Se crea una variable para guardar las posiciones de los vecinos de acuerdo a la prioridad dada:
    vecinos = []

    # Se calculan las posiciones y se verifican que estén disponibles (Que no sean muros):
    for di, dj in prioridad:
        ni, nj = i + di, j + dj 
        if 0 <= ni < filas and 0 <= nj < columnas and matriz[ni][nj] != 1:
            vecinos.append((ni, nj))

    # Se retorna la lista de posiciones con los vecinos:
    return vecinos



# Se define una función para desarrollar el algoritmo de búsqueda preferente por profundidad (DFS). La función recibe la matriz del tablero y retorna la lista de nodos que componen el recorrido a realizar:
def algoritmo_DFS(matriz):

    # Se crean variables para guardar la posición inicial y la de los paquetes:
    inicio, paquetes = encontrar_inicio_y_paquetes(matriz)

    # Se define el caso en que no se encuentre la posición inicial dentro del tablero:
    if not inicio:
        print("No se encontró la posición inicial del dron.")
        return None

    # Se define la prioridad con la que se escogerán los movimientos: arriba, derecha, abajo, izquierda (Como es una pila, la prioridad es al revés):
    prioridad = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    # Se define la pila (stack) con la que se realizará la búsqueda preferente por profundidad. Cada elemento es una lista con información de la posición actual, el camino recorrido, los paquetes recogidos y la disponibilidad de regresarse:
    stack = [(inicio, [inicio], set(), False)]

    # Se crea un conjunto de estados visitados, para evitar los ciclos:
    visitados = set()

    # Se desarrolla el algoritmo:
    while stack:

        # Se saca el nodo más reciente de la pila:
        actual, camino, recogidos, se_puede_regresar = stack.pop()

        # Se crea un estado único considerando la posición y los paquetes recogidos:
        estado_actual = (actual, frozenset(recogidos))

        # Se revisa si ya se visitó este estado y si la cantidad de paquetes es la misma:
        if estado_actual in visitados and not se_puede_regresar:
            continue
        visitados.add(estado_actual)

        # Se verifica si el dron ha llegado a una posición con paquete y si ya lo ha recogido:
        nuevo_recogidos = set(recogidos)
        if actual in paquetes and actual not in recogidos:
            nuevo_recogidos.add(actual)
            se_puede_regresar = True  # Permitimos retroceso justo después de recoger

        # Se revisa si se han recogido todos los paquetes para finalizar el algoritmo:
        if nuevo_recogidos == paquetes:
            return camino

        # Se recorren los vecinos válidos en orden de prioridad (Movimiento):
        for vecino in obtener_vecinos(actual, matriz, prioridad):

            # Se revisa si el vecino o nuevo nodo disponible para avanzar no se ha recorrido antes o si se tomó un paquete para poder regresarse:
            if vecino not in camino or se_puede_regresar:

                # Se extiene el recorrido con el nuevo vecino y se agrega el estado a la pila:
                nuevo_camino = camino + [vecino] 
                stack.append((vecino, nuevo_camino, nuevo_recogidos, False))

    # Se imprime en caso que se exploren todos los caminos posibles y no se logre recoger todos los paquetes:
    print("No se encontró solución completa.")
    return None