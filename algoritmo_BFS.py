def algoritmo_BFS(matriz):
    # Encontrar la posición inicial del dron
    start = None
    for row in range(len(matriz)):
        for col in range(len(matriz[row])):
            if matriz[row][col] == 2:
                start = (row, col)
                print(f"El dron está en la posición {row}, {col}")
                break
        if start:
            break
    
    if not start:
        print("No se encontró el dron en la matriz")
        return []
    
    # Identificar todos los paquetes  que estan en el mapa
    targets = []
    for row in range(len(matriz)):
        for col in range(len(matriz[row])):
            if matriz[row][col] == 4:
                targets.append((row, col))
    
    total_packages = len(targets)
    if total_packages == 0:
        print("No hay objetivos en la matriz")
        return [start]
    
    print(f"Los objetivos son {targets}")
    
    # Direcciones posibles de movimiento que puede hacer el dron (derecha, abajo, arriba, izquierda)
    directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
    
    # Variables para BFS 
    queue = [(start, [start])]  # (posición actual, camino recorrido)
    visited = {start}  # Conjunto de posiciones visitadas
    nodes_expanded = 0 # Los nodos expandidos
    packages_found = 0 # Paquetes encontrados
    final_path = [start] # El camino

    # BFS 
    while queue and packages_found < total_packages:
        current_pos, path = queue.pop(0)
        nodes_expanded += 1
        
        # Verificar si estamos en un paquete
        if current_pos in targets:
            packages_found += 1
            targets.remove(current_pos)  # Eliminamos el paquete de los objetivos
            print(f"El dron encontró un paquete y lo recogió :D en la posición {current_pos[0]},{current_pos[1]}")
            
            # Reiniciamos la búsqueda desde esta posición
            queue = [(current_pos, path)] 
            final_path = path
            visited = {pos for pos in visited if pos in path} 
            continue
        
        # Explorar movimientos en las cuatro direcciones, es decir, los vecinos
        for dx, dy in directions:
            next_x, next_y = current_pos[0] + dx, current_pos[1] + dy
            next_pos = (next_x, next_y)
            
            # Verificar si el movimiento es válido y no visitado
            if (0 <= next_x < len(matriz) and 
                0 <= next_y < len(matriz[0]) and 
                matriz[next_x][next_y] != 1 and 
                next_pos not in visited):
                
                # Si el dron cae en una trampa, lo reportamos pero seguimos avanzando
                if matriz[next_x][next_y] == 3:
                    print(f"El dron cayó en una trampa :c en la posición {next_x},{next_y}")
                
                # Añadir a la cola y marcar como visitado
                new_path = path + [next_pos]
                queue.append((next_pos, new_path))
                visited.add(next_pos)
    
    # Verificar si se recogieron todos los paquetes
    if packages_found == total_packages:
        print(f"El dron ha recogido todos los {total_packages} paquetes")
    else:
        print(f"El dron solo pudo recoger {packages_found} de {total_packages} paquetes")
    
    print(f"Nodos expandidos: {nodes_expanded}")
    print(f"Longitud del camino: {len(final_path)}")
    
    return final_path