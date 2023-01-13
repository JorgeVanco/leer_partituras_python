import pygame
from lectura_partituras.functions.functions import find_complete_path
from pygame_funcs.Buttons.Button import Button


def blit_long_text(text:str, screen, font_name, size, x_start, x_end, y_start, colour:tuple = (255,255,255)) -> None:
    y = y_start
    x = x_start

    font = pygame.font.SysFont(font_name, size)

    frases:list = text.split("\n")
    for frase in frases:
        words:list = frase.split(" ")
        
        for word in words:

            word_t = font.render(word, True, colour)
            if word_t.get_width() + x <= x_end:
                screen.blit(word_t, (x, y))
                x += word_t.get_width() + size//3
            else:
                y += word_t.get_height() + size//3
                x = x_start
                screen.blit(word_t, (x, y))
                x += word_t.get_width() + 6
        x = x_start
        y += size * 3 // 2

def main_instrucciones(buttons_width:int, height:int, font) -> bool:
    pygame.init()

    instrucciones:str = "Seleccione la imagen que quiere leer.\nPuede editarla seleccionando una nota particular. Ya sea mediante las flechas del teclado o el ratón y presionando 'Enter' o click derecho en el ratón.\nEn 'Tocar música' sonará la partitura que acabas de editar.\nEn ajustes tienes todos los parámetros más relevantes para modificar el resultado de la lectura de la partirura, así como la velocidad a la que quieres que suene la partitura."
    

    running = True
    w = 1024
    h = 768
    
    complete_path = find_complete_path(__file__)
    bg = pygame.image.load(complete_path + "app/pygame_funcs/imagenes_menu/escenario.png")
    screen = pygame.display.set_mode((w, h))
    pygame.display.set_caption("Instrucciones")

    x:int = w // 2 - buttons_width//2
    button_return:Button = Button(x, 550, buttons_width, height, 'RETURN', font, lambda: False)

    to_return = True

    while running:
        
        screen.blit(bg, (0, 0))
        blit_long_text(instrucciones, screen, 'microsoftjhengheimicrosoftjhengheiuibold', 40, 100, w-100, 100)
        running = button_return.process(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                to_return = False
        
        
        pygame.display.update()

    return to_return