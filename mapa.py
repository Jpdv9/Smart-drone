import pygame
import sys

#Iniciamos el pygame
pygame.init();

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
title_size = 40
cols = len(matriz[0])
rows = len(matriz)
width = cols * title_size
height = rows * title_size

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Smart Drone')

# Aca configuramos los colores de cada elemento del mapa

COLOR_FREE = (255, 255, 255) #Blanco
COLOR_OBSTACLE = (128, 128, 128) #Gris

#Estos colores son mientras tanto, como referencia nada mas, mas adelante se remplaza con imagenes

COLOR_DRONE = (0, 0, 255) #Azul
COLOR_TRAP = (255, 0, 0) #Rojo
COLOR_PACKAGE = (255, 255, 0) #Amarillo

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,0,0)) #Aca es el color de fonde, si lo queremos cambiar si algo

    #Dibujamos el mapa
    for row in range(rows):
        for col in range(cols):

            title = matriz[row][col]
            
            x = col * title_size
            y = row * title_size

            if title == 0:
                color = COLOR_FREE
            elif title == 1:
                color = COLOR_OBSTACLE
            elif title == 2:
                color = COLOR_DRONE
            elif title == 3:
                color = COLOR_TRAP
            elif title == 4:
                color = COLOR_PACKAGE
            else:
                color = COLOR_FREE

            pygame.draw.rect(screen, color, (x, y, title_size, title_size))
            pygame.draw.rect(screen, (0, 0, 0), (x, y, title_size, title_size), 1)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()