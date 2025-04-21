import heapq

def heuristica_manhattan(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

# Costo según el tipo de celda
def obtener_costo_casilla(valor_celda):
    if valor_celda == 0 or valor_celda == 4:
        return 1
    elif valor_celda == 3:
        return 8  # campo electromagnetico
    else:
        return float('inf')  

def algoritmo_A_estrella(matriz):
    # Buscar la ubicacion del dron
    inicio = None
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            if matriz[i][j] == 2:
                inicio = (i, j)
                print(f"Inicio encontrado en {inicio}")
                break
        if inicio:
            break

    # Busca la ubicacion de todos los paquetes
    objetivos = []
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            if matriz[i][j] == 4:
                objetivos.append((i, j))

    if not inicio or not objetivos:
        print("No se encontró el inicio o los paquetes.")
        return None

    # Se definen los movimientos
    movimientos = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    #definimos las variables a usar
    current_pos = inicio
    final_path = [inicio]
    remaining_targets = objetivos.copy()
    costo_total = 0
    profundidad_acumulada = 0

    while remaining_targets:
        objetivo_actual = remaining_targets[0]
        visitados = {}
        cola_prioridad = [(0, 0, 0, current_pos, [])]  # (f, g, profundidad, nodo, camino)
        profundidad_maxima_explorada = 0
        encontrado = False

        while cola_prioridad:
            f, g_actual, profundidad, actual, camino = heapq.heappop(cola_prioridad)
            profundidad_maxima_explorada = max(profundidad_maxima_explorada, profundidad)

            if actual in visitados and visitados[actual] <= g_actual:
                continue
            visitados[actual] = g_actual

            # revisamos los costos y profundidadades
            if actual == objetivo_actual:
                camino_completo = camino + [actual]
                final_path.extend(camino_completo[1:])  # Evitamos duplicar la posición actual
                costo_total += g_actual
                profundidad_acumulada += profundidad_maxima_explorada
                print(f"Paquete recogido en {actual}")
                current_pos = actual
                remaining_targets.remove(actual)
                encontrado = True
                break
            
            #aplicamos el movimiento
            for dx, dy in movimientos:
                nx, ny = actual[0] + dx, actual[1] + dy
                if 0 <= nx < len(matriz) and 0 <= ny < len(matriz[0]):
                    valor = matriz[nx][ny]
                    if valor != 1:
                        costo = obtener_costo_casilla(valor)
                        if costo == float('inf'):
                            continue
                        siguiente = (nx, ny)
                        nuevo_g = g_actual + costo
                        h = heuristica_manhattan(siguiente, objetivo_actual)
                        nuevo_f = nuevo_g + h
                        heapq.heappush(cola_prioridad, (nuevo_f, nuevo_g, profundidad + 1, siguiente, camino + [actual]))

# Imprimimos los resultados
        if not encontrado:
            print("No se pudo encontrar un camino a uno de los objetivos.")
            return None

    print("Todos los paquetes han sido recogidos.")
    print(f"Costo total del camino: {costo_total}")
    print(f"Profundidad acumulada del árbol explorado: {profundidad_acumulada}")
    return final_path
