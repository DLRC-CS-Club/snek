#!/usr/bin/env python3

import random
import pygame
from pygame.math import Vector2
import sys

GAME_START = False

class Snake:

    def __init__(self, body: list[Vector2], color: str):
        # self.body = [[Vector2(7, 8), Vector2(7, 9), Vector2(7, 10)]]
        self.body = body
        self.direction = Vector2(0, 0)
        self.add_block = False
        self.speed = 150
        self.color = color

        def load_graphic(filename: str):
            path = rf"graphics\\{self.color}_{filename}.png"
            image = pygame.image.load(path)
            return image.convert_alpha()

        # Graphics
        self.head_up = load_graphic("head_up")
        self.head_down = load_graphic("head_down")
        self.head_right = load_graphic("head_right")
        self.head_left = load_graphic("head_left")

        self.tail_up = load_graphic("tail_up")
        self.tail_down = load_graphic("tail_down")
        self.tail_left = load_graphic("tail_left")
        self.tail_right = load_graphic("tail_right")

        self.body_vertical = load_graphic("body_vertical")
        self.body_horizontal = load_graphic("body_horizontal")

        self.turn_tr = load_graphic("turn_tr")
        self.turn_tl = load_graphic("turn_tl")
        self.turn_br = load_graphic("turn_br")
        self.turn_bl = load_graphic("turn_bl")

    def update_graphic_orientation(self):

        if not self.body: return
        head_relation = self.body[1] - self.body[0]
        match head_relation:
            case Vector2(x=1, y=0): self.head = self.head_left
            case Vector2(x=-1, y=0): self.head = self.head_right
            case Vector2(x=0, y=1): self.head = self.head_up
            case Vector2(x=0, y=-1): self.head = self.head_down

        tail_relation = self.body[-2] - self.body[-1]
        match tail_relation:
            case Vector2(x=1, y=0): self.tail = self.tail_left
            case Vector2(x=-1, y=0): self.tail = self.tail_right
            case Vector2(x=0, y=1): self.tail = self.tail_up
            case Vector2(x=0, y=-1): self.tail = self.tail_down

    def draw(self):
        self.update_graphic_orientation()
        
        for i, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if i == 0: screen.blit(self.head, block_rect)
            elif i == len(self.body) - 1: screen.blit(self.tail, block_rect)

            else:
                previous_block = self.body[i + 1] - block
                next_block = self.body[i - 1] - block
                if previous_block.x == next_block.x: screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y: screen.blit(self.body_horizontal, block_rect)
                else:
                    pos1 = (previous_block.x, next_block.y)
                    pos2 = (previous_block.y, next_block.x)

                    if pos1 == (-1, -1) or pos2 == (-1, -1): screen.blit(self.turn_br, block_rect)
                    elif pos1 == (-1, 1) or pos2 == (1, -1): screen.blit(self.turn_tr, block_rect)
                    elif pos1 == (1, -1) or pos2 == (-1, 1): screen.blit(self.turn_bl, block_rect)
                    elif pos1 == (1, 1) or pos2 == (1, 1): screen.blit(self.turn_tl, block_rect)

    def move(self):
        if self.add_block == True:
            _body = self.body[:]
            _body.insert(0, _body[0] + self.direction)
            self.body = _body
            self.add_block = False
        else:
            _body = self.body[:-1]
            _body.insert(0, _body[0] + self.direction)
            self.body = _body

    def grow(self):
        self.add_block = True


class Food:

    def __init__(self):
        self.randomize()

    def draw(self):
        fruit_rect = pygame.Rect(
            int(self.pos.x * cell_size),
            int(self.pos.y * cell_size),
            cell_size, cell_size)
        screen.blit(food, fruit_rect)
        #pygame.draw.rect(screen, "red", fruit_rect)

    def randomize(self):
        self.x = random.randint(1, cell_number - 2)
        self.y = random.randint(1, cell_number - 2)
        self.pos = Vector2(self.x, self.y)


class Main:

    def __init__(self):
        self.snake = Snake([Vector2(7, 6), Vector2(8, 6), Vector2(8, 7), Vector2(7, 7), Vector2(6, 7), Vector2(6, 8), Vector2(7, 8)], "blue")
        self.temp_snake = Snake([Vector2(9, 9), Vector2(8, 9), Vector2(8, 8), Vector2(9, 8), Vector2(10, 8), Vector2(10, 7), Vector2(9, 7)], "yellow")
        self.food = Food()
        self.background_music = pygame.mixer.Sound(".\\Sounds\\background.wav")
        self.point_sound = pygame.mixer.Sound(".\\Sounds\\point.wav")
        self.game_over_sound = pygame.mixer.Sound(".\\Sounds\\game_over.wav")

    def check_snack(self):
        if self.food.pos == self.snake.body[0]:
            self.food.randomize()
            self.snake.grow()
            self.point_sound.play()
            self.snake.speed = int(self.snake.speed//1.0125)
            pygame.time.set_timer(SCREEN_UPDATE, self.snake.speed)

        for block in self.snake.body[1:]:
            if block == self.food.pos:
                self.food.randomize()

    def check_collision(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:self.game_over()

    def game_over(self):
        global GAME_START
        GAME_START = False
        self.game_over_sound.play()
        # pygame.time.wait(1500)
        self.snake.__init__([Vector2(7, 6), Vector2(8, 6), Vector2(8, 7), Vector2(7, 7), Vector2(6, 7), Vector2(6, 8), Vector2(7, 8)], "blue")
        self.temp_snake.__init__([Vector2(9, 9), Vector2(8, 9), Vector2(8, 8), Vector2(9, 8), Vector2(10, 8), Vector2(10, 7), Vector2(9, 7)], "yellow")
        pygame.time.set_timer(SCREEN_UPDATE, self.snake.speed)

    def generate_grass(self):

        def draw_patch():
            grass_color = (162, 209, 73)
            grass_rect = pygame.Rect(tile*cell_size, row*cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, grass_color, grass_rect)

        for row in range(cell_number):
            if row % 2 == 0:
                for tile in range(cell_number):
                    if tile % 2 == 0: draw_patch()
            else:
                for tile in range(cell_number):
                    if tile % 2 != 0: draw_patch()

    def update(self):
        self.snake.move()
        self.check_snack()
        self.check_collision()

    def draw_elements(self):
        self.generate_grass()
        self.food.draw()
        self.snake.draw()
        self.temp_snake.draw()
        self.draw_score()

    def draw_score(self):
        score = str(len(self.snake.body) - 3)
        score_surface = font.render(score, True, (240,240, 240))
        score_x = int(cell_size*cell_number - 32)
        score_y = int(cell_size*cell_number - 32)
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        food_rect = food.get_rect(midright = (score_rect.left -8, score_rect.centery))
        bg_rect = pygame.Rect(food_rect.left -8/2, food_rect.top -8/2, food_rect.width + score_rect.width + 20, food_rect.height + 8)

        pygame.draw.rect(screen, (60, 64, 67), bg_rect)
        pygame.draw.rect(screen, (28, 28, 28), bg_rect, 2)
        screen.blit(score_surface, score_rect)
        screen.blit(food, food_rect)

pygame.init()
cell_size = 32
cell_number = 16
screen = pygame.display.set_mode((cell_number*cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
food = pygame.image.load(".\\Graphics\\food.png").convert_alpha()
game = Main()
font = pygame.font.Font(None, 25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, game.snake.speed)


while True:
    # game.background_music.play()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        elif event.type == SCREEN_UPDATE and GAME_START: game.update()

        if event.type == pygame.KEYDOWN:

            if not GAME_START:
                game.snake.__init__([Vector2(7, 6), Vector2(8, 6), Vector2(9, 6)], "blue")
                game.temp_snake.body = []
            GAME_START = True
            match event.key: # Direction Movements
                case pygame.K_UP | pygame.K_w:
                    if game.snake.direction.y != 1: game.snake.direction = Vector2(0, -1)
                case pygame.K_DOWN | pygame.K_s:
                    if game.snake.direction.y != -1:game.snake.direction = Vector2(0, 1)
                case pygame.K_LEFT | pygame.K_a:
                    if game.snake.direction.x != 1:game.snake.direction = Vector2(-1, 0)
                case pygame.K_RIGHT | pygame.K_d:
                    if game.snake.direction.x != -1:game.snake.direction = Vector2(1, 0)

    screen.fill(pygame.Color((170, 215, 81)))
    game.draw_elements()
    pygame.display.update()
    clock.tick(60)