from collections import deque

def algoritmo_BFS(matriz):

    start = None
    
    # Con este for encontramos la posicion del dron que es el numero 2 de la matriz
    for row in range(len(matriz)):
        for col in range(len(matriz[row])):
            element =  matriz[row][col]
            if element == 2:
                start = (row, col)
                print(f"El dron esta en la posicion {row}, {col}")
                break
        if start:
            break

    
    # Buscar todos los objetivos, es decir, los paquetes
    targets = []

    for row in range(len(matriz)):
        for col in range(len(matriz[row])):
            if matriz[row][col] == 4:
                targets.append((row, col))

    if not targets:
        print("No hay objetivos en la matriz")
        return None
    

    print(f"Los objetivos son {targets}")

    # Iniciamos variables para el algoritmo BFS
    current_pos = start
    final_path =[start]
    remaining_targets = targets.copy()

    # En este while vamos a buscar el camino a paquete
    while remaining_targets:
        # Iniciamos el BFS para el siguente objetivo
        tail = deque([(current_pos, [])])
        visited = {current_pos}
        found_path = None
        nearest_target = None

        # Movimientos del dron
        movements = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        # BFS para encontrar el camino mas corto
        while tail:
            (x, y), path = tail.popleft()

            # Verificar si la posicion que estamos actualmente no tiene un paquete
            if (x,y) in remaining_targets:
                found_path = path + [(x, y)]
                nearest_target = (x, y)
                break

            # Explorar movimientos adyacentes
            for dx, dy in movements:
                next_x, next_y = x + dx, y + dy
                next_pos = (next_x, next_y)

                if (0 <= next_x < len(matriz) and 
                    0 <= next_y < len(matriz[0]) and 
                    matriz[next_x][next_y] != 1 and 
                    next_pos not in visited):
                    
                    visited.add(next_pos)
                    tail.append((next_pos, path + [next_pos]))

                    # Verificar el movimiento del dron y si encontro algo
                    # Si el dron se mueve a una trampa
                    if matriz[next_x][next_y] == 3:
                        print(f"El dron cayo en una trampa en la posicion {next_x}, {next_y}")
                        #return final_path + path  + [next_pos]
        if found_path:
            #Actualizamos el camino  y la posicion actual
            final_path.extend(found_path[1:])
            current_pos = nearest_target
            remaining_targets.remove(nearest_target)
            print(f"El dron encontro un paquete en la posicion {nearest_target}")
        
        else:
            print("No se encontro un camino a los objetivos restantes")
            return final_path
                        

    print("El dron ha recogido todos los paquetes")
    return final_path           


