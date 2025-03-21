import pygame
import pygame_gui
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

# GUI manager
manager  = pygame_gui.UIManager((window_width, window_height))

#variables para la apliacion
movements = 0
points = 0
start_time = None
elapsed_time = 0
selected_algorithm = "BFS"
game_started = False

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

# Fuente para el texto
pygame.font.init()
font_title =pygame.font.SysFont('Arial', 36)
font_normal = pygame.font.SysFont('Arial', 24)

# Aca colocamos los elemento del GUI

# Titulo de la aplicacion
title_rect = pygame.Rect((window_width // 2 - 150, 30, 300, 50))
title_text = font_title.render('SMART DRONE', True, (0, 0, 0))

# Panel de informacion
panel_info = pygame.Rect((window_width - MARGIN + 10, MARGIN + 50, MARGIN - 20, 200))

# Boton para iniciar
start_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((window_width - MARGIN + 20, MARGIN + 330, MARGIN - 40, 50)),
    text='Iniciar',
    manager=manager
)

#Selector de algoritmo
algorithm = ['BFS', 'DFS', 'A*']
algorithm_select =pygame_gui.elements.UIDropDownMenu(
    options_list=algorithm,
    starting_option=selected_algorithm,
    relative_rect=pygame.Rect((window_width - MARGIN + 20, MARGIN + 400, MARGIN - 40, 50)),
    manager=manager
)

clock = pygame.time.Clock()
running = True

while running:

    time_delta = clock.tick(60)/1000.0

    # Aca actualizamos el tiempo si la aplicacion esta iniciada
    if game_started and start_time is not None:
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time) // 1000 #Segundo


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Procesamos los eventos GUI
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_button:
                    game_started = True
                    start_time = pygame.time.get_ticks()
                    movements = 0
                    points = 0
                    # Aqui iniciamos la logica
                    print(f"SMART DRONE iniciado con el algoritmo:  {selected_algorithm}")

            elif event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == algorithm_select:
                    selected_algorithm = event.text
                    print(f"Algoritmo seleccionado: {selected_algorithm}")

        manager.process_events(event)
    
    manager.update(time_delta)

    screen.fill((200, 200, 200)) #Aca es el color de fondo, si lo queremos cambiar si algo

    # Title
    screen.blit(title_text, (title_rect.x, title_rect.y))

    # Panel
    pygame.draw.rect(screen, (255, 255, 255), panel_info)
    pygame.draw.rect(screen, (0, 0, 0), panel_info, 2)

    # Informacion de estado
    algorithm_text = font_normal.render(f"Algoritmo: {selected_algorithm}", True, (0, 0, 0))
    movements_text = font_normal.render(f"Movimientos: {movements}", True, (0, 0, 0))
    time_text =  font_normal.render(f"Tiempo: {elapsed_time}", True, (0, 0, 0))
    points_text = font_normal.render(f"Puntos: {points}", True, (0, 0, 0))

    screen.blit(algorithm_text, (panel_info.x + 10, panel_info.y + 20))
    screen.blit(movements_text, (panel_info.x + 10, panel_info.y + 60))
    screen.blit(time_text, (panel_info.x + 10, panel_info.y + 100))
    screen.blit(points_text, (panel_info.x +10, panel_info.y + 140))

    #Borde del mapa
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

    manager.draw_ui(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()