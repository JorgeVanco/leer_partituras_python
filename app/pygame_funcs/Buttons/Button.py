import pygame
from Classes.Errors import ImageNotSelected

class Button:
    def __init__(self, x:int, y:int, width:int, height:int, button_text: str, font, onclickFunction) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.button_surface = pygame.Surface((self.width, self.height))
        self.button_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.alreadyPressed = False
        self.button_text = button_text

        self.button_surf = font.render(self.button_text, True, (20, 20, 20))
        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }


    def process(self, screen) -> bool:
        running:bool = True
        mousePos = pygame.mouse.get_pos()
        self.button_surface.fill(self.fillColors['normal'])
        if self.button_rect.collidepoint(mousePos):
            self.button_surface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.button_surface.fill(self.fillColors['pressed'])
                try:
                    running = self.onclickFunction()
                except ImageNotSelected as e:
                    raise ImageNotSelected(e)


        self.button_surface.blit(self.button_surf, [
            self.button_rect.width/2 - self.button_surf.get_rect().width/2,
            self.button_rect.height/2 - self.button_surf.get_rect().height/2
        ])
        screen.blit(self.button_surface, self.button_rect)

        return running
