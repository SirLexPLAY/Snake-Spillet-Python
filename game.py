import pygame
import random
import os
from user import User
from tools import Tools
pygame.font.init()
pygame.mixer.init()

# MAP
wall_boxes = []
wall_boxes, MAP_SIZE, START_POS = Tools.load_map(wall_boxes, "map.txt")

# BOX DIMENSIONS
BOX_SIZE = (16, 16)      # (Height, Width)
AMOUNT_BOXES = MAP_SIZE
BOX_SPACING = 1

# WINDOW OPTIONS (Depending on box dimensions!)
WIDTH = BOX_SIZE[0]*AMOUNT_BOXES[0] + BOX_SPACING*AMOUNT_BOXES[0] + BOX_SPACING
HEIGHT = BOX_SIZE[1]*AMOUNT_BOXES[1] + BOX_SPACING*AMOUNT_BOXES[1] + BOX_SPACING
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

# GAME OPTIONS
FPS = 60

# FONTS
SCORE_FONT = pygame.font.SysFont('comicsans', 40)
GAME_LOST_FONT = pygame.font.SysFont('comicsans', 100)

# SOUNDS
EAT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'eat.wav'))
OUCH_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'ouch.wav'))

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SNAKE_COLOR = (0, 100, 0)  # Dark green
RED = (255, 0, 0)  # Casual red
WALL_COLOR = (128, 128, 128) # Gray

# SNAKE OPTIONS
START_SIZE = 5
START_FACE_DIRECTION = "RIGHT"
START_SPEED = 10  # Every N'th tick, so if 4, so every  pygame.time.get_ticks() % 4 == 0

# DIRECTIONS
DIRECTIONS = {
    "RIGHT" : (1, 0),
    "LEFT" : (-1, 0),
    "UP" : (0, -1),
    "DOWN" : (0, 1)
}


def init_snake(start_size, start_pos):
    snake_boxes = [start_pos]

    for i in range(1, start_size):
        x = snake_boxes[i-1][0]
        y = snake_boxes[i-1][1]
        snake_boxes.append([x+1,y])
    
    return snake_boxes


def init_apple(snake_boxes, wall_boxes):
    pos = []

    allowed = False
    while not allowed:
        x_pos = random.randint(START_SIZE, AMOUNT_BOXES[0] - START_SIZE)
        y_pos = random.randint(1, AMOUNT_BOXES[1])

        if [x_pos, y_pos] not in snake_boxes and [x_pos, y_pos] not in wall_boxes:
            pos = Tools.get_pos([x_pos, y_pos], BOX_SPACING, BOX_SIZE)
            allowed = True
    
    apple = pygame.Rect(pos[0], pos[1], BOX_SIZE[0], BOX_SIZE[1])
    return apple


def draw_snake(boxes):
    for box in boxes:
        pos = Tools.get_pos([box[0], box[1]], BOX_SPACING, BOX_SIZE)
        box_rect = pygame.Rect(pos[0], pos[1], BOX_SIZE[0], BOX_SIZE[1])
        pygame.draw.rect(WIN, SNAKE_COLOR, box_rect)


def draw_walls(walls):
    for wall in walls:
        pos = Tools.get_pos(wall, BOX_SPACING, BOX_SIZE)
        box_rect = pygame.Rect(pos[0], pos[1], BOX_SIZE[0], BOX_SIZE[1])
        pygame.draw.rect(WIN, WALL_COLOR, box_rect)


def move_snake(boxes, facing):
    del boxes[0]
    x, y = boxes[-1][0], boxes[-1][1]
    pos = [x + 1*facing[0], y + 1*facing[1]]
    boxes.append(pos)

    return boxes


def draw_window(walls, snake, apple, score):
    WIN.fill(BLACK)
    draw_walls(walls)
    pygame.draw.rect(WIN, RED, apple)
    draw_snake(snake)
    draw_score(score)

    pygame.display.update()


def draw_score(score):
    draw_text = SCORE_FONT.render("SCORE: " + score, 1, WHITE)
    WIN.blit(draw_text, (WIDTH - draw_text.get_width() - 10, 10))



def draw_lose(text):
    draw_text = GAME_LOST_FONT.render(text, 1, RED)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()



def draw_try_again(text):
    draw_text = SCORE_FONT.render(text, 1, RED)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2 + 100))
    pygame.display.update()


def extend_snake(boxes, facing):
    last_box = boxes[-1]
    next_box = [last_box[0] + 1*facing[0], last_box[1] + 1*facing[1]]
    boxes.append(next_box)
    
    return boxes


def eat_self(boxes):
    for i in range(len(boxes)):
        for j in range(i+1, len(boxes)):
            if boxes[i] == boxes[j]:
                return True
    return False


def teleport_head(boxes):
    if boxes[-1][0] <= 0:
        boxes[-1] = [AMOUNT_BOXES[0], boxes[-1][1]]
    elif boxes[-1][0] > AMOUNT_BOXES[0]:
        boxes[-1] = [1, boxes[-1][1]]
    elif boxes[-1][1] <= 0:
        boxes[-1] = [boxes[-1][0], AMOUNT_BOXES[1]]
    elif boxes[-1][1] > AMOUNT_BOXES[1]:
        boxes[-1] = [boxes[-1][0], 1]

    return boxes


def main():
    clock = pygame.time.Clock()

    score = 0
    snake_boxes = init_snake(START_SIZE, START_POS)
    snake_speed = START_SPEED
    snake_facing = DIRECTIONS["RIGHT"]

    apple = init_apple(snake_boxes, wall_boxes)


    run = True
    count = 0
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_facing != (0, 1):
                    snake_facing = DIRECTIONS["UP"]
                if event.key == pygame.K_DOWN and snake_facing != (0, -1):
                    snake_facing = DIRECTIONS["DOWN"]
                if event.key == pygame.K_LEFT and snake_facing != (1, 0):
                    snake_facing = DIRECTIONS["LEFT"]
                if event.key == pygame.K_RIGHT and snake_facing != (-1, 0):
                    snake_facing = DIRECTIONS["RIGHT"]

        if (apple.x, apple.y) == Tools.get_pos(snake_boxes[-1], BOX_SPACING, BOX_SIZE):
            score += 1
            EAT_SOUND.play()
            if score % 5 == 0 and snake_speed > 0:
                snake_speed -=1

            apple = init_apple(snake_boxes, wall_boxes)
            snake_boxes = extend_snake(snake_boxes, snake_facing)

        if count % snake_speed == 0:
            snake_boxes = move_snake(snake_boxes, snake_facing)

        if eat_self(snake_boxes) or snake_boxes[-1] in wall_boxes:
            OUCH_SOUND.play()
            draw_lose("You Lose!")
            draw_try_again("Do you wanna try again? (y/n)")
            
            choosen = False
            to_break = False
            while not choosen:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_y:
                            choosen = True
                            to_break = True
                        if event.key == pygame.K_n:
                            run = False
                            choosen = True
                            pygame.quit()
                    if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()
            
            if to_break:
                break

        if Tools.check_outside(snake_boxes[-1], AMOUNT_BOXES):
            snake_boxes = teleport_head(snake_boxes)

        draw_window(wall_boxes, snake_boxes, apple, str(score))
        count += 1
    
    main()


if __name__ == "__main__":
    main()


