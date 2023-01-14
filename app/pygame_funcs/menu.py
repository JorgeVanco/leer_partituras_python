import pygame
import pygame_funcs.Buttons.Button as b
from pygame_funcs.main_pygame import main_pygame
from lectura_partituras.main_lectura_partituras import main_lectura_partituras
from pygame_funcs.ajustes import main_ajustes
from pygame_funcs.instrucciones import main_instrucciones
from musica.musica import main_musica
from lectura_partituras.functions.functions import find_complete_path
import time

from Classes.Errors import ImageNotSelected, ErrorPentagramas, ErrorPath, ErrorGuardado

def get_title(text:str, w:int, size:int = 100, font_name:str = 'microsoftjhengheimicrosoftjhengheiuibold',):
    size = 100
    font_title = pygame.font.SysFont(font_name, size)
    title = font_title.render(text, True, (255,255,255))
    title_shadow = font_title.render(text, True, (0,0,0))
    title_rect = title.get_rect()
    pos_title = (w//2 - title_rect.width//2, 160)

    shadow_offset = 1 + (size // 30)
    pos_title_shadow = (pos_title[0] + shadow_offset, pos_title[1] + shadow_offset) 

    return title, pos_title, title_shadow, pos_title_shadow

def show_error_msg(screen, error:str, width:int, font_name:str) -> None:
    font = pygame.font.SysFont(font_name, 40)
    pygame.draw.rect(screen, (255, 0, 0, 0.4), pygame.Rect(0, 0, width, 60))
    print(error)
    error_text = font.render(error, True, (0,0,0))
    screen.blit(error_text, (width//2 - error_text.get_width()//2, 60//2 - error_text.get_height()//2))

def main_menu():
    pygame.init()

    complete_path = find_complete_path(__file__)
    bg = pygame.image.load(complete_path + "app/pygame_funcs/imagenes_menu/escenario.png")

    running = True
    w = 1024
    h = 768
    screen = pygame.display.set_mode((w, h))

    buttons_width: int = 400
    buttons_height:int = 70
    
    x1:int = w // 4 - buttons_width//2 + 50
    x2: int = 3 * w//4 - buttons_width//2 - 50

    clock = pygame.time.Clock()

    title_text = "LECTURA PARTITURAS"

    title, pos_title, title_shadow, pos_title_shadow = get_title(title_text, w)

    font_name:str = 'microsoftjhengheimicrosoftjhengheiuibold'
    font = pygame.font.SysFont(font_name, 40)

    while running:
        error_happened:bool = False
        pygame.display.set_caption("Menú Lectura Partituras")
        clock.tick(60)/1000.0
        
        button_lectura:b.Button = b.Button(x1, 270, buttons_width, buttons_height, 'LEER PARTITURA', font, main_lectura_partituras)
        button_edit:b.Button = b.Button(x2, 270, buttons_width, buttons_height, "EDITAR PARTITURA", font, main_pygame)
        button_music:b.Button = b.Button(x1, 350, buttons_width, buttons_height, "TOCAR MÚSICA", font, main_musica)
        button_options:b.Button = b.Button(x2, 350, buttons_width, buttons_height, 'AJUSTES', font, main_ajustes)
        button_instructions:b.Button = b.Button(x1, 430, buttons_width, buttons_height, 'INSTRUCCIONES', font, lambda: main_instrucciones(buttons_width, buttons_height, font))
        button_quit:b.Button = b.Button(x2, 430, buttons_width, buttons_height, 'QUIT', font, lambda: False)
        
        buttons = [button_options, button_lectura, button_music, button_edit, button_instructions, button_quit]
        
        
        screen = pygame.display.set_mode((w, h))
        screen.blit(bg, (0, 0))
        screen.blit(title_shadow, pos_title_shadow)
        screen.blit(title, pos_title)
        
        for button in buttons:
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
                pygame.display.update()
            except FileNotFoundError as e:
                error_happened = True
                error_msg = str(e)
            except ErrorPath as e:
                error_happened = True
                error_msg = str(e)
            except ErrorGuardado as e:
                error_happened = True
                error_msg = str(e)
        
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
