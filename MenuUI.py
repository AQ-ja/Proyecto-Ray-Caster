import pygame, pygame_gui, sys
from pygame.locals import *
from Level1 import Game
from Level2 import Game2
from Level3 import Game3


pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((1000, 500))


width = 600
height = 600


#background = pygame.image.load('Sources/fondo.jpg')
betaversion = pygame.image.load('Sources/beta.png')
background = pygame.image.load('Sources/fondoMenu.jpg')

class Menu(object):
    
    def __init__(self):
        super().__init__()

        self.mainClock = pygame.time.Clock()
        pygame.init()
        pygame.display.set_caption('STREETS')
        self.screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL)
        self.screen.set_alpha(None)

        self.titleFont = pygame.font.Font("Sources/pricedown.bl-regular.otf", 90)
        self.buttonFont = pygame.font.Font("Sources/arcadeclassic.regular.ttf", 35)

        self.click = False
        self.mouse_hover = False

        self.start()



    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)


    def draw_background(self):
        tex = pygame.transform.scale(background, (width, height))
        rect = tex.get_rect()
        self.screen.blit(tex, rect)


    def add_image(self):
        tex = pygame.transform.scale(betaversion, (100, 50))
        rect = tex.get_rect()
        self.screen.blit(tex, rect)


    def create_rect(self, width, height, border, color, border_color):
        surf = pygame.Surface((width+border*2, height+border*2), pygame.SRCALPHA)
        pygame.draw.rect(surf, color, (border, border, width, height), 0)
        for i in range(1, border):
            pygame.draw.rect(surf, border_color, (border-i, border-i, width+5, height+5), 1)
        return surf


    def start(self):

        while 1:

            self.screen.fill((0, 0, 0))
            self.draw_background()
            self.add_image()
            self.draw_text('STREETS', self.titleFont, (255, 185, 203), self.screen, 150, 50)

            mx, my = pygame.mouse.get_pos()

            # 1. X | 2. Y | 3. Largo | 4. Alto
            button_1 = pygame.Rect(225, 220, 140, 55) # Listo
            button_2 = pygame.Rect(225, 480, 140, 55) # El de Salida hasta abajo| Listo
            button_3 = pygame.Rect(120, 320, 140, 55) 
            button_4 = pygame.Rect(350, 320, 140, 55)
            



            button_1_is_hover = False
            button_2_is_hover = False
            button_3_is_hover = False
            button_4_is_hover = False


            if button_1.collidepoint((mx, my)):
                if self.click:
                    Game(self.screen, self.mainClock, width, height)

                elif self.mouse_hover:
                    button_1_is_hover = True

            if button_2.collidepoint((mx, my)):
                if self.click:
                    pygame.quit()
                    sys.exit()
                elif self.mouse_hover:
                    button_2_is_hover = True

            if button_3.collidepoint((mx, my)):
                if self.click:
                    Game3(self.screen, self.mainClock, width, height)
                elif self.mouse_hover:
                    button_3_is_hover = True

            if button_4.collidepoint((mx, my)):
                if self.click:
                    Game2(self.screen, self.mainClock, width, height)
                elif self.mouse_hover:
                    button_4_is_hover = True


            button_color = (218, 97, 36)
            button_color_hover = (205, 107, 107)

            button_1_color = button_color if button_1_is_hover else button_color_hover  
            button_2_color = button_color if button_2_is_hover else button_color_hover 
            button_3_color = button_color if button_3_is_hover else button_color_hover 
            button_4_color = button_color if button_4_is_hover else button_color_hover 

            # 1
            pygame.draw.rect(self.screen, button_1_color, button_1,  border_radius=10)
            self.draw_text('Nivel 1', self.buttonFont, (0, 0, 0), self.screen, 235, 230)

            # 2
            pygame.draw.rect(self.screen, button_2_color, button_2,  border_radius=10)
            self.draw_text('exit', self.buttonFont, (0, 0, 0), self.screen, 255, 490)

            #3
            pygame.draw.rect(self.screen, button_3_color, button_3,  border_radius=10)
            self.draw_text('Nivel 2', self.buttonFont, (0, 0, 0), self.screen, 125, 325)

            #4
            pygame.draw.rect(self.screen, button_4_color, button_4,  border_radius=10)
            self.draw_text('Nivel 3', self.buttonFont, (0, 0, 0), self.screen, 355, 325)


            self.click = False
            self.mouse_hover = False

            for event in pygame.event.get():

                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == button_1:
                    Game()

                elif event.type == button_3:
                    Game3()

                elif event.type == button_4:
                    Game2()

                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True

                elif event.type == MOUSEMOTION:
                    self.mouse_hover = True


            pygame.display.update()
            self.mainClock.tick(60)