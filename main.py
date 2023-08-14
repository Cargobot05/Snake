import sys
import pygame
import random
import time

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

pygame.init()

BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
RED = [255, 0, 0]
GREEN = [0, 255, 0]
YELLOW = [255, 255, 0]

BLOCK_SIZE = 30
STEP = BLOCK_SIZE

EDGE_RIGHT = 600
EDGE_LEFT = 120
EDGE_TOP = 120
EDGE_BOTTOM = 600

UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"

VIEWPORT_SIZE = 720

viewport = pygame.display.set_mode([VIEWPORT_SIZE, VIEWPORT_SIZE])
pygame.display.set_caption("SNAKE")

score = 0
high_score = 0
snake_length = 3

play = False
pause = False

class Segment(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direction):
        super().__init__()
        self.image = pygame.Surface([BLOCK_SIZE, BLOCK_SIZE])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.direction = direction
        self.rect.x = pos_x
        self.rect.y = pos_y

    def move_up(self):
        self.rect.y -= STEP

    def move_down(self):
        self.rect.y += STEP

    def move_left(self):
        self.rect.x -= STEP
    
    def move_right(self):
        self.rect.x += STEP

class Apple():
    def __init__(self):
        super().__init__()
        self.exist = False
        self.image = pygame.Surface([BLOCK_SIZE, BLOCK_SIZE])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
    
    def generate(self):
        while self.exist == False:
            self.rect.x = random.randint(EDGE_LEFT // BLOCK_SIZE, EDGE_RIGHT // BLOCK_SIZE) * BLOCK_SIZE
            self.rect.y = random.randint(EDGE_TOP // BLOCK_SIZE, EDGE_BOTTOM // BLOCK_SIZE) * BLOCK_SIZE

            for segment in snake:
                if self.rect.center != segment.rect.center and check_out_of_bounds(self) == False:
                    self.exist = True



def move_snake(snake):
    next_dir = ""
    last_dir = ""

    for segment in snake:

        next_dir = last_dir
        
        if segment.direction == UP:
            segment.move_up()
        
        if segment.direction == DOWN:
            segment.move_down()
        
        if segment.direction == LEFT:
            segment.move_left()

        if segment.direction == RIGHT:
            segment.move_right()

        last_dir = segment.direction
        
        if (next_dir != ""):
            segment.direction = next_dir

def snake_add(snake:pygame.sprite.Group):
    snake_tail:Segment = snake.sprites()[snake_length-1]

    if snake_tail.direction == UP:
        new_segment = Segment(snake_tail.rect.x, snake_tail.rect.y + BLOCK_SIZE, UP)
    if snake_tail.direction == DOWN:
        new_segment = Segment(snake_tail.rect.x, snake_tail.rect.y - BLOCK_SIZE, DOWN)
    if snake_tail.direction == LEFT:
        new_segment = Segment(snake_tail.rect.x + BLOCK_SIZE, snake_tail.rect.y, LEFT)
    if snake_tail.direction == RIGHT:
        new_segment = Segment(snake_tail.rect.x - BLOCK_SIZE, snake_tail.rect.y, RIGHT)

    snake.add(new_segment)

def check_out_of_bounds(object):
    if object.rect.x < EDGE_LEFT:
        return True
    if object.rect.x > EDGE_RIGHT - BLOCK_SIZE:
        return True
    if object.rect.y < EDGE_TOP:
        return True
    if object.rect.y > EDGE_BOTTOM - BLOCK_SIZE:
        return True
    return False
    
def check_self_collision(snake:pygame.sprite.Group):
    snake_head = snake.sprites()[0]
    skip_snake_head = True
    for segment in snake:
        if skip_snake_head == False:
            if snake_head.rect.center == segment.rect.center:
                return True
        skip_snake_head = False
    return False

def check_snake_apple_collision(snake:pygame.sprite.Group, apple:Apple):
    for segment in snake:
        if apple.rect.center == segment.rect.center:
            return True
    return False

def game_over():
    global snake, score, high_score, snake_length, play

    play = False

    if score > high_score: high_score = score
    score = 0

    snake_length = 3

    time.sleep(0.5)

    font = pygame.font.SysFont('Bahnschrift', 32, False, False)
    text = font.render("GAME OVER", True, RED)
    viewport.blit(text, [EDGE_RIGHT / 2 - 20, EDGE_BOTTOM / 2 - 20])

    pygame.display.flip()

    time.sleep(2)

    snake.empty()
    for i in range(0, snake_length):   
        new_segment = Segment(360- i*BLOCK_SIZE, 360, RIGHT)
        snake.add(new_segment)


running = True
UPDATE = pygame.USEREVENT
pygame.time.set_timer(UPDATE, 250)
clock = pygame.time.Clock()

snake = pygame.sprite.Group()
for i in range(0, snake_length):   
    new_segment = Segment(360- i*BLOCK_SIZE, 360, RIGHT)
    snake.add(new_segment)

apple = Apple()

input = RIGHT


while running:
    viewport.fill(BLACK)
    font = pygame.font.SysFont('Bahnschrift', 54, False, False)
    text = font.render("S N A K E" , False, GREEN)
    viewport.blit(text, [EDGE_RIGHT / 2 - 55, 20])

    font = pygame.font.SysFont('Bahnschrift', 24, False, False)
    text = font.render(f"SCORE: {score}" , False, WHITE)
    viewport.blit(text, [EDGE_LEFT, EDGE_TOP - 25])
    
    text = font.render(f"HIGH: {high_score}" , False, WHITE)
    viewport.blit(text, [EDGE_RIGHT - 85, EDGE_TOP - 25])

    font = pygame.font.SysFont('Bahnschrift', 20, False, False)
    text = font.render("press SPACE to pause" , False, WHITE)
    viewport.blit(text, [EDGE_RIGHT / 2 - 30, EDGE_BOTTOM + 20])

    arena = pygame.draw.rect(viewport, WHITE, (EDGE_LEFT, EDGE_TOP, 480, 480), 1)

    snake_direction = snake.sprites()[0].direction

    key = pygame.key.get_pressed()
    
    if key[pygame.K_RETURN] and play == False:
        play = True
    
    if key[pygame.K_SPACE]:
        if play:
            play = False
        else:
            play = True

        if pause:
            pause = False
        else:
            pause = True
    
    if play:
        if key[pygame.K_UP] and snake_direction != DOWN:
            input = UP
        if key[pygame.K_DOWN] and snake_direction != UP:
            input = DOWN
        if key[pygame.K_LEFT] and snake_direction != RIGHT:
            input = LEFT
        if key[pygame.K_RIGHT] and snake_direction != LEFT:
            input = RIGHT

        snake.draw(viewport)

        if check_snake_apple_collision(snake, apple) == True:
            apple.exist = False
            score += 1
            snake_add(snake)
            snake_length += 1

        if apple.exist == False:
            apple.generate()
            
        viewport.blit(apple.image, [apple.rect.x, apple.rect.y])

    elif (pause):
        font = pygame.font.SysFont('Bahnschrift', 32, False, False)
        text = font.render("PAUSED", True, YELLOW)
        viewport.blit(text, [EDGE_RIGHT / 2 + 5, EDGE_BOTTOM / 2 - 20])

    else:
        font = pygame.font.SysFont('Bahnschrift', 20, False, False)
        text = font.render("press ENTER to start" , False, WHITE)
        viewport.blit(text, [EDGE_RIGHT / 2 - 30, EDGE_BOTTOM / 2 + 20])

    snake.sprites()[0].direction = input

    for event in pygame.event.get():
        
        if event.type == UPDATE and play:
            move_snake(snake)
            if check_out_of_bounds(snake.sprites()[0]): game_over()
            if check_self_collision(snake): game_over()
        
        if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

    pygame.display.flip()
    clock.tick(60)