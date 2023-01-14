import pygame
from Classes.Errors import ImageNotSelected, ErrorPentagramas, ErrorPath

class Button:
    def __init__(self, x:int, y:int, width:int, height:int, button_text: str, font, onclickFunction) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.button_surface = pygame.Surface((self.width, self.height))
        self.button_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.button_text = button_text

        self.button_surf = font.render(self.button_text, True, (20, 20, 20))
        self.fill_colors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

    def render(self, screen) -> None:
        """
        Dibuja el botón en la pantalla

        Args:
            screen: La superficie de pygame sobre la que dibujar el botón
        """
        self.button_surface.blit(self.button_surf, [
            self.button_rect.width/2 - self.button_surf.get_rect().width/2,
            self.button_rect.height/2 - self.button_surf.get_rect().height/2
        ])
        screen.blit(self.button_surface, self.button_rect)

    
    def process(self, screen) -> bool:
        """
        Comprueba si el cursor está sobre el botón y si ha sido pulsado. 
        Ejecuta la función asignada al botón.

        Args:
            screen: La superficie de pygame sobre la que dibujar el botón
        
        Returns: 
            running: Si el código debe seguir corriendo o no
        """
        running:bool = True
        mousePos = pygame.mouse.get_pos()
        
        self.button_surface.fill(self.fill_colors['normal'])
        
        if self.button_rect.collidepoint(mousePos):
            self.button_surface.fill(self.fill_colors['hover'])
            
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.button_surface.fill(self.fill_colors['pressed'])
                try:
                    running = self.onclickFunction()
                except ImageNotSelected as e:
                    raise ImageNotSelected(e)
                except pygame.error as e:
                    raise pygame.error(e)
                except ErrorPentagramas as e:
                    raise ErrorPentagramas(e)
                except FileNotFoundError as e:
                    raise FileNotFoundError(e)
                except ErrorPath as e:
                    raise ErrorPath(e)
        
        self.render(screen)
        
        return running
