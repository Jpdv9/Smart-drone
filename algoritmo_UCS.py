import heapq


#Damos valores de costo a las casillas
def obtener_costo_casilla(valor_celda):
    if valor_celda == 0 or valor_celda == 4:  
        return 1
    elif valor_celda == 3:  
        return 8
    else:
        return float('inf')  

def algoritmo_UCS(matriz):
    start = None

    # Encontramos el punto donde está el dron
    for row in range(len(matriz)):
        for col in range(len(matriz[row])):
            if matriz[row][col] == 2:
                start = (row, col)
                print(f"El dron está en la posición {row}, {col}")
                break
        if start:
            break

    # Buscamos los paquetes
    targets = []
    for row in range(len(matriz)):
        for col in range(len(matriz[row])):
            if matriz[row][col] == 4:
                targets.append((row, col))

    if not targets:
        print("No hay objetivos en la matriz")
        return None

    print(f"Los objetivos son {targets}")


    #creamos nuestras variables que acumularn nuestros resultados
    current_pos = start
    final_path = [start]
    remaining_targets = targets.copy()
    costo_total = 0
    profundidad_acumulada = 0  

    while remaining_targets:
        heap = [(0, 0, current_pos, [])]  # (costo, profundidad, posición, camino)
        visited = {}
        profundidad_maxima_explorada = 0
        found_path = None
        nearest_target = None
        
        #declaramos sus movimientos
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        while heap:
            cost, profundidad, (x, y), path = heapq.heappop(heap)

            profundidad_maxima_explorada = max(profundidad_maxima_explorada, profundidad)

            if (x, y) in visited and visited[(x, y)] <= cost:
                continue
            visited[(x, y)] = cost

            if (x, y) in remaining_targets:
                found_path = path + [(x, y)]
                nearest_target = (x, y)
                costo_total += cost
                break
            #si hay paquetes que puedan ser alcanzables empezamos a movernos por el mapa teniendo en cuenta sus costos
            for dx, dy in directions:
                next_x, next_y = x + dx, y + dy
                if 0 <= next_x < len(matriz) and 0 <= next_y < len(matriz[0]):
                    celda_valor = matriz[next_x][next_y]
                    if celda_valor != 1:
                        if abs(next_x - x) + abs(next_y - y) == 1:
                            move_cost = obtener_costo_casilla(celda_valor)
                            total_cost = cost + move_cost
                            next_pos = (next_x, next_y)
                            heapq.heappush(heap, (total_cost, profundidad + 1, next_pos, path + [(x, y)]))

#Finalmente guardamos en nuestras variables los resultados obtenidos y los imprimimos
        if found_path:
            final_path.extend(found_path[1:])
            current_pos = nearest_target
            remaining_targets.remove(nearest_target)
            profundidad_acumulada += profundidad_maxima_explorada  
            print(f"Paquete recogido en {nearest_target}")
        else:
            print("No se encontró camino a todos los objetivos")
            return None

    print("Todos los paquetes han sido recogidos.")
    print(f"Costo total del camino: {costo_total}")
    print(f"Profundidad acumulada del árbol explorado: {profundidad_acumulada}")
    return final_path
