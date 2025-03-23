import pygame
import pygame_gui
import sys
import os
import tkinter as tk
from tkinter import filedialog
import mapa

import pygame_gui.ui_manager

pygame.init()

# Configuracion de la pantalla de la interfaz
WINDOWS_WIDTH = 800
WINDOWS_HEIGHT = 600
screen = pygame.display.set_mode((WINDOWS_WIDTH, WINDOWS_HEIGHT))
pygame.display.set_caption('Smart Drone')

# Aca estan los colores
BACKGROUND_COLOR = (220, 220, 220)
PANEL_COLOR = (240, 240, 240)
TEXT_COLOR = (0, 0, 0)

# Fuentes que va utilizar la interfaz
pygame.font.init()
title_font = pygame.font.SysFont('Arial', 36)
normal_font = pygame.font.SysFont('Arial', 24)
small_font = pygame.font.SysFont('Arial', 18)

# Funciones
def open_file_selector():
    root = tk.Tk()
    root.withdraw()

    archive_path =filedialog.askopenfilename(
        title="Seleccionar archivo de mapa",
        filetypes=[("Archivo de texto", "*.txt"), ("Todos los archivos", "*.*")]
    )

    root.destroy()
    return archive_path if archive_path else None

# leer achivo
def read_file(route_file):
    try:
        with open(route_file, 'r') as file:
            content = file.read()
        return content
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None
    
def convert_to_array(content):
    try:
        lines = content.strip().split('\n')
        matriz = []

        for line in lines:
            row = [int(value) for value in line.strip().split()]
            matriz.append(row)
        return matriz
    
    except Exception as e:
        print(f"Error al convertir el contenido a matriz: {e}")
        return None
    
# Variables
selected_file = None
file_content = None
matriz_result = None
current_mode = "No se ha seleccionado un archivo"


# GUI Manager
manager = pygame_gui.UIManager((WINDOWS_WIDTH, WINDOWS_HEIGHT))



# Elemento GUI para pantalla de carga
load_panel = pygame.Rect((WINDOWS_WIDTH // 2 - 300, WINDOWS_HEIGHT // 2 - 200, 600, 400))

# Boton que abre el selector de archivos
load_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((WINDOWS_WIDTH // 2 - 150, WINDOWS_HEIGHT // 2 - 75, 300,  50)),
    text= 'SELECCIONAR ARCHIVO TXT',
    manager=manager
) 

# Boton para continuar
continue_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((WINDOWS_WIDTH // 2 - 100, WINDOWS_HEIGHT // 2 + 100, 200, 50)), 
    text='Continuar', 
    manager=manager
)

continue_button.disable()

# Panel de vista previa del contenido
panel_preview = pygame.Rect((WINDOWS_WIDTH//2 - 250, WINDOWS_HEIGHT//2, 500, 80))
text_preview = small_font.render("Sin contenido para mostrar", True, TEXT_COLOR)

# Etiqueta que muestra el archivo seleccionado
file_tag = small_font.render("Ningun archivo seleccionado", True, TEXT_COLOR)
current_tag = small_font.render(current_mode, True, TEXT_COLOR)

# Funcion para cargar el mapa y pasar a la pantalla del mapa
def load_main_map():
    if matriz_result:
        print('Continuando con la matriz: ')
        for row  in matriz_result:
            print(row)

        print("Saliendo de la pantalla")

        mapa.run_map_screen(matriz_result)

        pygame.quit()
        sys.exit()


clock = pygame.time.Clock()
running = True

while running:
    
    time_delta = clock.tick(60)/1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # En esta parte procesamos los eventos de la GUI
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == load_button:

                    route_file = open_file_selector()

                    if route_file:
                        selected_file = route_file
                        current_mode = "Archivo seleccionado, leyendo el contenido..."
                        file_tag = small_font.render(f"Archivo: {os.path.basename(selected_file)}", True, TEXT_COLOR)

                        # leer el contenido del archivo
                        file_content = read_file(selected_file)

                        if file_content:
                            # Damos una vista previa del contenido
                            lines = file_content.split('\n')
                            preview_view = '\n'.join(lines[:3]) + ('...' if len(lines) > 3 else '')
                            preview_text = small_font.render(preview_view[:70] + ('...' if len(preview_view) > 70 else ''), True, TEXT_COLOR)

                            matriz_result = convert_to_array(file_content)

                            if matriz_result:
                                current_mode = "Archivo cargado correctamente :D"
                                current_tag = small_font.render(current_mode, True, (0, 128, 0))
                                continue_button.enable()
                            
                            else:
                                current_mode = "Error al procesar el archivo :c"
                                current_tag = small_font.render(current_mode, True, (255, 0, 0))
                        
                        else: 
                            current_mode = "Error a leer el archivo :c"
                            current_tag = small_font.render(current_mode, True, (255, 0, 0))

                    else:
                        current_mode = "No se selecciono ningun archivo pendejo"
                        current_tag = small_font.render(current_mode, True, TEXT_COLOR)
                
                elif event.ui_element == continue_button and matriz_result:
                    load_main_map()

        manager.process_events(event)
    
    manager.update(time_delta)

    # Renderizando
    screen.fill(BACKGROUND_COLOR)

    # Panel de carga
    pygame.draw.rect(screen, PANEL_COLOR, load_panel)
    pygame.draw.rect(screen, (100, 100, 100), load_panel, 2)

    # Titulo
    title_text =  title_font.render('SMART DRONE', True, TEXT_COLOR)
    screen.blit(title_text, (WINDOWS_WIDTH // 2 - title_text.get_width() // 2, load_panel.y + 30))

    # Subtitulos
    subtitle_text =  normal_font.render('Cargar Mapa', True, TEXT_COLOR)
    screen.blit(subtitle_text, (WINDOWS_WIDTH // 2 - subtitle_text.get_width() // 2, load_panel.y + 80 ))

    # Informacion del archivo
    screen.blit(file_tag, (WINDOWS_WIDTH // 2 - file_tag.get_width() // 2, WINDOWS_HEIGHT // 2))
    screen.blit(current_tag, (WINDOWS_WIDTH//2 - current_tag.get_width()//2, WINDOWS_HEIGHT//2 - 20))


    if file_content:
        pygame.draw.rect(screen, (230, 230, 230), panel_preview)
        pygame.draw.rect(screen, (180, 180, 180), panel_preview, 1)
        screen.blit(text_preview, (panel_preview.x + 10, panel_preview.y + 10))

        if matriz_result:
            rows = len(matriz_result)
            columns = len(matriz_result[0]) if rows > 0 else 0
            text_dimensions = small_font.render(f"Dimensiones: {rows}x{columns}", True, TEXT_COLOR)
            screen.blit(text_dimensions, (panel_preview.x +10, panel_preview.y + 40))

    
    manager.draw_ui(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()