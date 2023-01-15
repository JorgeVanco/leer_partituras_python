import pygame

def get_title(text:str, w:int, size:int = 100, font_name:str = 'microsoftjhengheimicrosoftjhengheiuibold',):
    """
    Genera el texto del título con una sombra para que se vea mejor

    Args:
        text (str): El texto para escribir
        w (int): La anchura de la pantalla
        size (int): El tamaño de la letra
        font_name (str): El nombre de la fuente

    Returns:
        title (any): El título renderizado
        pos_title (tuple[int, int]): La posición del centro del titulo
        title_shadow (any): La sombra del título renderizada
        pos_title_shadow (title[int, int]): La posición del centro de la sombra del titulo
    """
    font_title:pygame.Surface = pygame.font.SysFont(font_name, size)
    title = font_title.render(text, True, (255,255,255))
    title_shadow = font_title.render(text, True, (0,0,0))
    title_rect = title.get_rect()
    pos_title = (w//2 - title_rect.width//2, 160)

    shadow_offset = 1 + (size // 30)
    pos_title_shadow = (pos_title[0] + shadow_offset, pos_title[1] + shadow_offset) 

    return title, pos_title, title_shadow, pos_title_shadow

def show_error_msg(screen, error:str, width:int, font_name:str) -> None:
    """
    Muestra un mensaje de error en la parte de arriba de la pantalla

    Args:
        screen: La pantalla de pygame
        error (str): El mensaje de error
        width (int): La anchura de la pantalla
        font_name (str): El nombre de la fuente
    """
    font = pygame.font.SysFont(font_name, 40)
    pygame.draw.rect(screen, (255, 0, 0, 0.4), pygame.Rect(0, 0, width, 60))

    error_text = font.render(error, True, (0,0,0))
    screen.blit(error_text, (width//2 - error_text.get_width()//2, 60//2 - error_text.get_height()//2))