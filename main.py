import sys
import pygame

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

pygame.init()

BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
RED = [255, 0, 0]
GREEN = [0, 255, 0]
YELLOW = [255, 255, 0]

BLOCK_SIZE = 15
STEP = 15

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

play = False
pause = False
game_over = False

class Segment(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, color, direction):
        super().__init__()
        self.image = pygame.Surface([BLOCK_SIZE, BLOCK_SIZE])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.direction = direction
        self.rect.centerx = pos_x
        self.rect.centery = pos_y

    def move_up(self):
        self.rect.centery -= STEP

    def move_down(self):
        self.rect.centery += STEP

    def move_left(self):
        self.rect.centerx -= STEP
    
    def move_right(self):
        self.rect.centerx += STEP

class Apple():
    def __init__(self, pos_x, pos_y, exist):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.exist = exist

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

def check_out_of_bounds(snake_head:Segment):
    if snake_head.rect.centerx < EDGE_LEFT:
        return True
    if snake_head.rect.centerx > EDGE_RIGHT:
        return True
    if snake_head.rect.centery < EDGE_TOP:
        return True
    if snake_head.rect.centery > EDGE_BOTTOM:
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



running = True
UPDATE = pygame.USEREVENT
pygame.time.set_timer(UPDATE, 250)
clock = pygame.time.Clock()
input = RIGHT

snake = pygame.sprite.Group()
for i in range(0, 7):   
    segment = Segment(360- i*BLOCK_SIZE, 360, WHITE, RIGHT)
    snake.add(segment)
snake_length = 7



while running:
    viewport.fill(BLACK)
    font = pygame.font.SysFont('Bahnschrift', 54, False, False)
    text = font.render("S N A K E" , False, GREEN)
    viewport.blit(text, [EDGE_RIGHT / 2 - 55, 20])

    arena = pygame.draw.rect(viewport, WHITE, (EDGE_LEFT, EDGE_TOP, 480, 480), 1)
    
    snake.draw(viewport)

    snake_direction = snake.sprites()[0].direction

    key = pygame.key.get_pressed()
    
    if key[pygame.K_RETURN] and play == False:
        play = True
    
    if play:
        if key[pygame.K_UP] and snake_direction != DOWN:
            input = UP
        if key[pygame.K_DOWN] and snake_direction != UP:
            input = DOWN
        if key[pygame.K_LEFT] and snake_direction != RIGHT:
            input = LEFT
        if key[pygame.K_RIGHT] and snake_direction != LEFT:
            input = RIGHT

    snake.sprites()[0].direction = input

    for event in pygame.event.get():
        
        if event.type == UPDATE and play:
            move_snake(snake)
            if check_out_of_bounds(snake.sprites()[0]): game_over = True
            if check_self_collision(snake): game_over = True
        
        if event.type == pygame.QUIT or game_over:
            pygame.quit()
            sys.exit()

    pygame.display.flip()
    clock.tick(60)