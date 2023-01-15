import pygame
import pygame_funcs.Buttons.Button as b
from pygame_funcs.main_edicion_partituras import main_edicion_partituras
from lectura_partituras.main_lectura_partituras import main_lectura_partituras
from pygame_funcs.ajustes import main_ajustes
from pygame_funcs.instrucciones import main_instrucciones
from musica.musica import main_musica
from pygame_funcs.menu import get_title, show_error_msg
from lectura_partituras.functions.functions import find_complete_path
import time
from Classes.Errors import ImageNotSelected, ErrorPentagramas, ErrorPath, ErrorGuardado

if __name__ == "__main__":
    pygame.init()

    complete_path = find_complete_path(__file__)
    bg = pygame.image.load(complete_path + "app/pygame_funcs/imagenes_menu/escenario.png")

    running = True
    w = 1024
    h = 768
    screen = pygame.display.set_mode((w, h))

    buttons_width: int = 400
    buttons_height:int = 70
    
    x1:int = w // 4 - buttons_width//2 + 50  # La posición en el eje x de los botones de la izquierda
    x2: int = 3 * w//4 - buttons_width//2 - 50  # La posición en el eje x de los botones de la derecha

    clock = pygame.time.Clock()

    title_text = "LECTURA PARTITURAS"

    title, pos_title, title_shadow, pos_title_shadow = get_title(title_text, w)

    font_name:str = 'microsoftjhengheimicrosoftjhengheiuibold'
    font = pygame.font.SysFont(font_name, 40)
    
    button_lectura:b.Button = b.Button(x1, 270, buttons_width, buttons_height, 'LEER PARTITURA', font, main_lectura_partituras)
    button_edit:b.Button = b.Button(x2, 270, buttons_width, buttons_height, "EDITAR PARTITURA", font, main_edicion_partituras)
    button_music:b.Button = b.Button(x1, 350, buttons_width, buttons_height, "TOCAR MÚSICA", font, main_musica)
    button_options:b.Button = b.Button(x2, 350, buttons_width, buttons_height, 'AJUSTES', font, main_ajustes)
    button_instructions:b.Button = b.Button(x1, 430, buttons_width, buttons_height, 'INSTRUCCIONES', font, lambda: main_instrucciones(buttons_width, buttons_height, font))
    button_quit:b.Button = b.Button(x2, 430, buttons_width, buttons_height, 'QUIT', font, lambda: False)
    
    buttons = [button_options, button_lectura, button_music, button_edit, button_instructions, button_quit]
    
    while running:
        error_happened:bool = False
        pygame.display.set_caption("Menú Lectura Partituras")
        clock.tick(60)/1000.0
        
        
        screen = pygame.display.set_mode((w, h))
        screen.blit(bg, (0, 0))
        screen.blit(title_shadow, pos_title_shadow)
        screen.blit(title, pos_title)
        
        # for button in buttons:
        i:int = 0
        while i < len(buttons) and running:
            button = buttons[i]
            try:
                running = button.process(screen)
                
            except ImageNotSelected as e:
                error_happened = True
                error_msg = str(e)
            except pygame.error as e:
                error_happened = True
                error_msg = str(e)
            except ErrorPentagramas as e:
                error_happened = True
                error_msg = str(e)
            except FileNotFoundError as e:
                error_happened = True
                error_msg = str(e)
            except ErrorPath as e:
                error_happened = True
                error_msg = str(e)
            except ErrorGuardado as e:
                error_happened = True
                error_msg = str(e)
            
            i += 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        pygame.display.update()
        if error_happened:
            screen = pygame.display.set_mode((w, h))
            screen.blit(bg, (0, 0))
            screen.blit(title_shadow, pos_title_shadow)
            screen.blit(title, pos_title)
            for button in buttons:
                button.render(screen)
            show_error_msg(screen, error_msg, w, font_name)
            pygame.display.update()
            time.sleep(1)
    pygame.quit()
