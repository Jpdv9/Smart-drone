import heapq

#Definimos la heuristica a usar
def heuristica_manhattan(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def obtener_costo_casilla(valor_celda):
    if valor_celda == 0 or valor_celda == 4:
        return 1
    elif valor_celda == 3:
        return 5
    else:
        return float('inf')

def algoritmo_A_estrella(matriz):
    start = None
    for row in range(len(matriz)):
        for col in range(len(matriz[row])):
            if matriz[row][col] == 2:
                start = (row, col)
                print(f"El dron está en la posición {start}") #obtenermos la posicion del dron
                break
        if start:
            break

    targets = []
    for row in range(len(matriz)):
        for col in range(len(matriz[row])):
            if matriz[row][col] == 4:
                targets.append((row, col))#obtenemos la poscion de los paquetes

    if not targets:
        print("No hay objetivos en la matriz")
        return None

    print(f"Los objetivos son {targets}")

    current_pos = start
    final_path = [start]
    remaining_targets = targets.copy()

    while remaining_targets:
        objetivo_actual = min(remaining_targets, key=lambda t: heuristica_manhattan(current_pos, t))
        cola_prioridad = []
        heapq.heappush(cola_prioridad, (0, current_pos, []))
        visitados = {}

        movimientos = [(-1,0),(0,1),(1,0),(0,-1)]

        while cola_prioridad:
            costo_total, actual, camino = heapq.heappop(cola_prioridad)
            if actual in visitados and visitados[actual] <= costo_total:
                continue
            visitados[actual] = costo_total

            if actual == objetivo_actual:
                found_path = camino + [actual]
                break

            for dx, dy in movimientos:
                nx, ny = actual[0] + dx, actual[1] + dy
                if 0 <= nx < len(matriz) and 0 <= ny < len(matriz[0]):
                    valor = matriz[nx][ny]
                    if valor != 1:
                        next_pos = (nx, ny)
                        g = costo_total + obtener_costo_casilla(valor)
                        h = heuristica_manhattan(next_pos, objetivo_actual)
                        f = g + h
                        heapq.heappush(cola_prioridad, (f, next_pos, camino + [actual]))

        if found_path:
            final_path.extend(found_path[1:])
            current_pos = objetivo_actual
            remaining_targets.remove(objetivo_actual)
            print(f"Paquete recogido en {objetivo_actual}")
        else:
            print("No se encontró camino a todos los objetivos")
            return final_path

    print("El dron ha recogido todos los paquetes")
    return final_path
