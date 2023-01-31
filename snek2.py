import pygame
import random

WINDOW_X, WINDOW_Y = 480, 480
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

def fruit_position():
    pos = ((random.randint(0, WINDOW_X)//24)*24, (random.randint(0, WINDOW_X)//24)*24)
    return pos

FRUIT_SPAWN = True

direction = 'RIGHT'
change_to = direction

while True:

    # handling key events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_UP | pygame.K_w: change_to = 'UP'
                case pygame.K_DOWN | pygame.K_s: change_to = 'DOWN'
                case pygame.K_LEFT | pygame.K_a: change_to = 'LEFT'
                case pygame.K_RIGHT | pygame.K_d: change_to = 'RIGHT'

    # If two keys pressed simultaneously
    # we don't want snake to move into two directions
    # simultaneously
    
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snake_position[1] -= 24
    if direction == 'DOWN':
        snake_position[1] += 24
    if direction == 'LEFT':
        snake_position[0] -= 24
    if direction == 'RIGHT':
        snake_position[0] += 24

    # Snake body growing mechanism
    # if fruits and snakes collide then scores will be
    # incremented by 10
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += 10
        fruit_spawn = False
    else:
        snake_body.pop()
        
    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x//10)) * 10,
                        random.randrange(1, (window_y//10)) * 10]
        
    fruit_spawn = True
    game_window.fill(black)
    
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(
        pos[0], pos[1], 10, 10))
        
    pygame.draw.rect(game_window, white, pygame.Rect(
    fruit_position[0], fruit_position[1], 10, 10))

    # Game Over conditions
    if snake_position[0] < 0 or snake_position[0] > window_x-10:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > window_y-10:
        game_over()
    
    # Touching the snake body
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()
    
    # displaying score countinuously
    show_score(1, white, 'times new roman', 20)
    
    # Refresh game screen
    pygame.display.update()

    # Frame Per Second /Refresh Rate
    fps.tick(snake_speed)
