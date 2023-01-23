import pygame
import time

# Initialize pygame and create window
pygame.init()
width = 500
height = 500
screen = pygame.display.set_mode((width, height))

# Set title and icon
pygame.display.set_caption("Snake Game")

# Set variables for snake position and movement
x1 = 250
y1 = 250
x1_change = 0
y1_change = 0

# Set snake block size
block_size = 10

snake_color = (255,0,0)

# Create a function to draw the snake
def snake(block_size, snake_list, color):
    for x,y in snake_list:
        pygame.draw.rect(screen, color, [x, y, block_size, block_size])

#...

# Create a loop to run the game
snake_list = [[250,250]]
score = 0
game_over = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            pygame.quit()
            quit()

    # Control snake movement using arrow keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x1_change = -block_size
        y1_change = 0
    elif keys[pygame.K_RIGHT]:
        x1_change = block_size
        y1_change = 0
    elif keys[pygame.K_UP]:
        y1_change = -block_size
        x1_change = 0
    elif keys[pygame.K_DOWN]:
        y1_change = block_size
        x1_change = 0

    # Fill the screen with black
    screen.fill((0,0,0))

    # Update snake position
    snake_list = update_snake(snake_list, x1, y1, x1_change, y1_change)
    snake_head = snake_list[0]
    if check_collision(snake_head):
        game_over = True
        pygame.quit()
        quit()
    else:
        score +=1
    # Draw snake
    snake(block_size, snake_list, snake_color)
    #display score
    display_score(score)
    # Update the display
    pygame.display.update()

    # Set the game speed
    clock = pygame.time.Clock()
    clock.tick(30)