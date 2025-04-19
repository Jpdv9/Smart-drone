def encontrar_inicio_y_paquetes(matriz):
    inicio = None
    paquetes = []
    for i, fila in enumerate(matriz):
        for j, valor in enumerate(fila):
            if valor == 2:
                inicio = (i, j)
            elif valor == 4:
                paquetes.append((i, j))
    return inicio, paquetes

def encontrar_inicio_y_paquetes(matriz):
    inicio = None
    paquetes = []
    for i, fila in enumerate(matriz):
        for j, valor in enumerate(fila):
            if valor == 2:
                inicio = (i, j)
            elif valor == 4:
                paquetes.append((i, j))
    return inicio, paquetes

def obtener_vecinos(pos, matriz):
    filas, columnas = len(matriz), len(matriz[0])
    i, j = pos
    vecinos = []
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ni, nj = i + di, j + dj
        if 0 <= ni < filas and 0 <= nj < columnas and matriz[ni][nj] != 1:
            vecinos.append((ni, nj))
    return vecinos

def algoritmo_DFS(matriz):
    inicio, paquetes = encontrar_inicio_y_paquetes(matriz)
    paquetes_set = set(paquetes)

    stack = [(inicio, [inicio], set())]  # posición, camino, recogidos
    visitados = set()

    while stack:
        actual, camino, recogidos = stack.pop()
        if actual in paquetes_set:
            recogidos = recogidos | {actual}

        if len(recogidos) == len(paquetes_set):
            return camino

        if (actual, tuple(sorted(recogidos))) in visitados:
            continue
        visitados.add((actual, tuple(sorted(recogidos))))

        for vecino in obtener_vecinos(actual, matriz):
            if (vecino, tuple(sorted(recogidos))) not in visitados:
                stack.append((vecino, camino + [vecino], recogidos))

    return None
