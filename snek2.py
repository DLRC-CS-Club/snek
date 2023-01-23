import pygame

WINDOW_X, WINDOW_Y = 720, 480
# colors
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED =  pygame.Color(255,0,0)
GREEN =  pygame.Color(0,255,0)
BLUE =  pygame.Color(0,0,255)

pygame.init()

pygame.display.set_caption("snek")
game_window = pygame.display.set_mode((WINDOW_X, WINDOW_Y))
fps = pygame.time.Clock()

snake_position = [100,50]
snake_body = [[100,50], [90,50], [80,50], [70,50]]

