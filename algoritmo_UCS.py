import heapq

def obtener_costo_casilla(valor_celda):
    if valor_celda == 0 or valor_celda == 4:  
        return 1
    elif valor_celda == 3:  
        return 5
    else:
        return float('inf')  

def algoritmo_UCS(matriz):
    start = None

    # Encontramos el punto donde esta el dron
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

    current_pos = start
    final_path = [start]
    remaining_targets = targets.copy()

    while remaining_targets:
        heap = [(0, current_pos, [])]
        visited = {}

        found_path = None
        nearest_target = None

        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        while heap:
            cost, (x, y), path = heapq.heappop(heap)

            if (x, y) in visited and visited[(x, y)] <= cost:
                continue
            visited[(x, y)] = cost

            if (x, y) in remaining_targets:
                found_path = path + [(x, y)]
                nearest_target = (x, y)
                break

            for dx, dy in directions:
                next_x, next_y = x + dx, y + dy
                if 0 <= next_x < len(matriz) and 0 <= next_y < len(matriz[0]):
                    celda_valor = matriz[next_x][next_y]
                    if celda_valor != 1:  
                        move_cost = obtener_costo_casilla(celda_valor)
                        total_cost = cost + move_cost
                        next_pos = (next_x, next_y)
                        heapq.heappush(heap, (total_cost, next_pos, path + [next_pos]))

                        if celda_valor == 3:
                            print(f"Advertencia: Campo electromagnético en {next_pos}")

        if found_path:
            final_path.extend(found_path[1:])  # evitar repetir la posición actual
            current_pos = nearest_target
            remaining_targets.remove(nearest_target)
            print(f"Paquete recogido en {nearest_target}")
        else:
            print("No se encontró un camino a los paquetes restantes")
            return final_path

    print("Todos los paquetes han sido recogidos.")
    return final_path
