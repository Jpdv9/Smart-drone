import heapq

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

# Heurística por defecto: distancia de Manhattan al paquete más cercano
def heuristica_manhattan(pos, objetivos):
    return min(abs(pos[0] - x) + abs(pos[1] - y) for (x, y) in objetivos)

def algoritmo_GBFS(matriz, heuristica=heuristica_manhattan):
    inicio, paquetes = encontrar_inicio_y_paquetes(matriz)
    paquetes_set = set(paquetes)

    visitados = set()
    cola = []
    heapq.heappush(cola, (heuristica(inicio, paquetes), inicio, [inicio], set()))

    while cola:
        _, actual, camino, recogidos = heapq.heappop(cola)

        if actual in paquetes_set:
            recogidos = recogidos | {actual}

        if len(recogidos) == len(paquetes_set):
            return camino

        clave = (actual, tuple(sorted(recogidos)))
        if clave in visitados:
            continue
        visitados.add(clave)

        for vecino in obtener_vecinos(actual, matriz):
            nueva_ruta = camino + [vecino]
            heapq.heappush(
                cola,
                (heuristica(vecino, list(paquetes_set - recogidos)), vecino, nueva_ruta, recogidos)
            )

    return None  # Si no se encuentra camino