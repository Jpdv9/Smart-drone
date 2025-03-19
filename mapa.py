import pygame
import sys

#Iniciamos el pygame
pygame.init()

#Matriz el cual sera utilizada para dibujar el mapa

matriz = [
    [1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 1, 0, 1, 0, 1, 0, 1, 1, 1],
    [0, 2, 0, 3, 4, 4, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [3, 3, 0, 1, 0, 1, 1, 1, 1, 1],
    [1, 1, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 0, 0, 0, 0, 4, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Configuracion de la vista
MARGIN = 200
title_size = 50
cols = len(matriz[0])
rows = len(matriz)
map_width = cols * title_size
map_height = rows * title_size

# ventana
window_width = map_width + (MARGIN * 2)
window_height = map_height + (MARGIN * 2)

screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Smart Drone')

# Aca configuramos los colores de cada elemento del mapa

COLOR_FREE = (255, 255, 255) #Blanco
COLOR_OBSTACLE = (128, 128, 128) #Gris

## Elemento del mapa con imagenes

# Estilos
PADDING = 2
image_size = title_size - (PADDING * 2)

# Dron
IMAGEN_DRONE = pygame.image.load('./Imagenes/Dron.png')
IMAGEN_DRONE = pygame.transform.scale(IMAGEN_DRONE, (image_size, image_size))

# Trampas
IMAGEN_TRAP = pygame.image.load('./Imagenes/advertencia-electrica.png')
IMAGEN_TRAP = pygame.transform.scale(IMAGEN_TRAP, (image_size, image_size))

# Paquetes
IMAGEN_PACKAGE = pygame.image.load('./Imagenes/paquete.png')
IMAGEN_PACKAGE = pygame.transform.scale(IMAGEN_PACKAGE, (image_size, image_size))

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((200, 200, 200)) #Aca es el color de fonde, si lo queremos cambiar si algo

    map_border = pygame.Rect(
        MARGIN - 2,
        MARGIN - 2,
        map_width + 4, 
        map_height + 4
    )

    pygame.draw.rect(screen, (0, 0, 0), map_border, 2)

    #Dibujamos el mapa
    for row in range(rows):
        for col in range(cols):

            title = matriz[row][col]
            
            x = col * title_size + MARGIN
            y = row * title_size + MARGIN

            if title == 0:
                color = COLOR_FREE
            elif title == 1:
                color = COLOR_OBSTACLE
            elif title == 2:
                pygame.draw.rect(screen, COLOR_FREE, (x, y, title_size, title_size))
                screen.blit(IMAGEN_DRONE, (x + PADDING, y + PADDING))
                pygame.draw.rect(screen, (0, 0, 0), (x, y, title_size, title_size), 1)
                continue
            elif title == 3:
                pygame.draw.rect(screen, COLOR_FREE, (x, y, title_size, title_size))
                screen.blit(IMAGEN_TRAP, (x + PADDING, y + PADDING))
                pygame.draw.rect(screen, (0, 0, 0), (x, y, title_size, title_size), 1)
                continue
            elif title == 4:
                pygame.draw.rect(screen, COLOR_FREE, (x, y, title_size, title_size))
                screen.blit(IMAGEN_PACKAGE,  (x + PADDING, y + PADDING))
                pygame.draw.rect(screen, (0, 0, 0), (x, y, title_size, title_size), 1)
                continue
            else:
                color = COLOR_FREE

            pygame.draw.rect(screen, color, (x, y, title_size, title_size))
            pygame.draw.rect(screen, (0, 0, 0), (x, y, title_size, title_size), 1)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()