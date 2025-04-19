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
    
    
    # Contar todos lo paquetes que hay en el mapa
    targets = []

    for row in range(len(matriz)):
        for col in range(len(matriz[row])):
            if matriz[row][col] == 4:
                targets.append((row, col))
    
    total_packages = len(targets)

    if (total_packages == 0):
        print("No hay objetivos en la matriz")
        return [start]

    print(f"Los objetivos son {targets}")

    #Denifimos la prioridad de movimientos que puede hacer el dron
    #Estos movimientos se pueden cambiar como quiera
    priority_movements = [(0, 1), (1, 0), (-1, 0), (0, -1)]

    # Iniciamos variables para el algoritmo BFS
    current_pos = start
    final_path =[start]
    visited = {start}
    package_collected = 0

    # Con este while vamos a continuar hasta encontrar todos los paquetes en el mapa
    while package_collected < total_packages:
        move_made = False

        # Vamos a probar los movimientos en orden de prioridad
        for dx, dy in priority_movements:
            next_x, next_y = current_pos[0] + dx, current_pos[1] + dy
            next_pos = (next_x, next_y)

            # Verificamos si el movimiento es valido y no visitado
            if(0 <= next_x < len(matriz) and
               0 <= next_y < len(matriz[0]) and
               matriz [next_x][next_y] != 1 and
               next_pos not in visited):
                
                #Realizando movimientos
                current_pos = next_pos
                final_path.append(current_pos)
                visited.add(current_pos)
                move_made = True

                #Verificamos si encontramos una trampa
                if matriz[next_x][next_y] == 3:
                    print(f"El dron cayo en una trampa :c en la posicion {next_x},{next_y}")
                
                elif matriz[next_x][next_y] == 4:
                    package_collected += 1
                    print(f"El dron encontro un paquete y lo recogio :D en la posicion {next_x},{next_y}")

                break

        # Si no se pudo realizar ningún movimiento, terminamos
        if not move_made:
            print("El dron no puede moverse más. No se pueden recoger todos los paquetes.")
            break  
                
    print(f"El dron ha recogido {package_collected} de {total_packages} paquetes")
    return final_path           