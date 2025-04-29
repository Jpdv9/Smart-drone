# Se importa la biblioteca heapq para usar colas de prioridad (min-heaps):
import heapq



# Se definen los movimientos posibles: arriba, abajo, izquierda, derecha; como variable global:
MOVIMIENTOS = [(-1, 0), (1, 0), (0, -1), (0, 1)]



# Se define una función para la heurística de Manhattan que calcula la distancia entre la posición actual del dron y los paquetes. Recibe la posición actual y la posición de los paquetes y retorna la menor de las distancias:
def heuristica_manhattan(pos, paquetes):
    
    # Se retorna la mínima distancia de Manhattan definida como |x1 - x2| + |y1 - y2|:
    return min(abs(pos[0] - p[0]) + abs(pos[1] - p[1]) for p in paquetes)



# Se define una función para obtener la posición inicial del dron y la de los paquetes. Recibe la matriz del tablero y retorna la lista con las posiciones:
def obtener_posicion_inicial_y_paquetes(matriz):
    
    # Se definen variables para guardar las posiciones:
    inicio = None
    paquetes = []

    # Se recorre la matriz para buscar las posiciones:
    for i, fila in enumerate(matriz):
        for j, valor in enumerate(fila):

            # Se guardan las posiciones:
            if valor == 2:
                inicio = (i, j)
            elif valor == 4:
                paquetes.append((i, j))

    # Se retornan las posiciones:
    return inicio, paquetes



# Se define una función para calcular el costo de moverse a una celda. Recibe la matriz y una posición. Retorna el costo correspondiente:
def costo_moverse(matriz, pos):
    
    # Si el valor en la celda es 3 (campo electromagnético), cuesta 8, sino cuesta 1:
    if matriz[pos[0]][pos[1]] == 3:
        return 8
    else:
        return 1



# Se define una función para desarrollar el algoritmo de búsqueda A*. La matriz recibe la matriz del tablero y retorna la lista de nodos que componen el recorrido a realizar:
def algoritmo_A_estrella(matriz):
    
    # Se crean variables para guardar la posición inicial y la de los paquetes:
    inicio, paquetes_restantes = obtener_posicion_inicial_y_paquetes(matriz)

    # Se crean variables para guardar el recorrido y la posición actual del dron:
    camino_completo = []
    posicion_actual = inicio

    # Se desarrolla el algoritmo:
    while paquetes_restantes:
        
        # Se crea un conjunto de estados visitados, para evitar ciclos:
        visitados = set()

        # Se define una cola (heap) de prioridad:
        heap = []

        # Se inserta la posición actual, el costo hasta ahora, el recorrido y su heurística en la cola:
        heapq.heappush(heap, (
            heuristica_manhattan(posicion_actual, paquetes_restantes),  # f(n) = g(n) + h(n)
            0,  # g(n) = costo acumulado
            posicion_actual,
            [posicion_actual]
        ))

        # Se extrae el nodo con menor valor de f(n):
        while heap:
            
            # Se extrae el nodo con menor valor de f(n):
            f, g, actual, camino = heapq.heappop(heap)

            # Se revisa si ya se visitó este estado:
            if actual in visitados:
                continue

            # Se marca como visitado:
            visitados.add(actual)

            # Se revisa si llegamos a un paquete para recogerlo:
            if actual in paquetes_restantes:
                paquetes_restantes.remove(actual)
                camino_completo.extend(camino[1:])
                posicion_actual = actual
                
                # Se reinicia la búsqueda para recoger el siguiente paquete:
                break

            # Se exploran los vecinos posibles:
            for dx, dy in MOVIMIENTOS:
                nx, ny = actual[0] + dx, actual[1] + dy

                # Se verifica si está dentro de los límites de la matriz o si es un muro:
                if 0 <= nx < len(matriz) and 0 <= ny < len(matriz[0]):
                    if matriz[nx][ny] != 1:  # No es muro
                        siguiente = (nx, ny)

                        # Se calcula el nuevo costo g(n):
                        costo = g + costo_moverse(matriz, siguiente)

                        # Se calcula la heurística h(n):
                        h = heuristica_manhattan(siguiente, paquetes_restantes)

                        # Se inserta el nuevo estado en la cola:
                        heapq.heappush(heap, (
                            costo + h,  # f(n) = g(n) + h(n)
                            costo,      # g(n)
                            siguiente,
                            camino + [siguiente]
                        ))
        else:
            # Se retorna None si salimos del bucle sin recoger un paquete o no hay solución posible:
            return None

    # Se retorna el camino total desde el inicio hasta recoger todos los paquetes:
    return [inicio] + camino_completo