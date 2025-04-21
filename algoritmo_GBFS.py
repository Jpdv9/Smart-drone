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



# Se define una función para desarrollar el algoritmo de búsqueda avara. La matriz recibe la matriz del tablero y retorna la lista de nodos que componen el recorrido a realizar:
def algoritmo_GBFS(matriz):

    # Se crean variables para guardar la posición inicial y la de los paquetes:
    inicio, paquetes_restantes = obtener_posicion_inicial_y_paquetes(matriz)

    # Se crean variables para guardar el recorrido, la posición actual del dron y si se puede devolver: 
    camino_completo = []          
    posicion_actual = inicio      
    se_puede_devolver = False     

    # Se desarrolla el algoritmo:
    while paquetes_restantes:

        # Se crea un conjunto de estados visitados, para evitar los ciclos:
        visitados = set()     

        # Se define una cola (heap) de prioridad:    
        heap = []                 

        # Se inserta la posición actual con su heurística en la cola:
        heapq.heappush(heap, (
            heuristica_manhattan(posicion_actual, paquetes_restantes),  
            posicion_actual,                                            
            [posicion_actual]                                           
        ))

        while heap:

            # Se extrae el nodo con menor valor en la heurística:
            heur, actual, camino = heapq.heappop(heap) 

            # Se revisa si ya se visitó este estado y si la cantidad de paquetes es la misma:
            if actual in visitados and not se_puede_devolver:
                continue

            # Se marca como visitado:
            visitados.add(actual)

            # Se revisa si llegamos a un paquete para recogerlo:
            if actual in paquetes_restantes:
                paquetes_restantes.remove(actual)             
                camino_completo.extend(camino[1:])            
                posicion_actual = actual                      
                se_puede_devolver = True                      
                break  

            # Se exploran los vecinos posibles:
            for dx, dy in MOVIMIENTOS:
                nx, ny = actual[0] + dx, actual[1] + dy

                # Se verifica si está dentro de los límites de la matriz o si es un muro:
                if 0 <= nx < len(matriz) and 0 <= ny < len(matriz[0]):
                    if matriz[nx][ny] != 1:  
                        siguiente = (nx, ny)

                        # Se verifica que se pueda acceder al nodo si no ha sido recorrido antes o si se puede devolver a él:
                        if siguiente not in visitados or se_puede_devolver:
                            nueva_heur = heuristica_manhattan(siguiente, paquetes_restantes)

                            # Se inserta el nuevo estado con su heurística en la cola:
                            heapq.heappush(heap, (
                                nueva_heur,
                                siguiente,
                                camino + [siguiente]
                            ))

        else:
            # Se retorna None si salimos del bucle sin recoger un paquete, o no hay solución posible:
            return None

        # Se desactiva el permiso de retroceso después de planear la siguiente ruta:
        se_puede_devolver = False

    # Se retorna el camino total desde el inicio hasta recoger todos los paquetes:
    return [inicio] + camino_completo