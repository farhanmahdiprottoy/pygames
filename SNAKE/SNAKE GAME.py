import pygame
import time
import random

pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 50)
RED = (200, 50, 50)
GREEN = (0, 140, 0)
BLACK = (0, 0, 0)
ORANGE = (255, 140, 0)
PINK = (255, 105, 180)
BRIGHT_MAROON = (200, 25, 69)
GREY = (169, 169, 169)

# Screen dimensions
WIDTH, HEIGHT = 600, 600
SNAKE_SIZE = 20
SPEED = 10
DASH_SPEED = 20

# Dash mechanics
dashing = False
last_dash_time = 0
dash_cooldown = 4  # Cooldown period of 4 seconds

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SNAKE GAME")

clock = pygame.time.Clock()
font = pygame.font.Font(pygame.font.match_font('pressstart2p'), 24)

# Snake and food properties
snake = [(WIDTH // 2, HEIGHT // 2)]
direction = "STOP"
food = (
    random.randint(0, (WIDTH // SNAKE_SIZE) - 1) * SNAKE_SIZE,
    random.randint(0, (HEIGHT // SNAKE_SIZE) - 1) * SNAKE_SIZE)
score = 0
high_score = 0
paused = False
marry_me_shown = False


def draw_border():
    pygame.draw.rect(screen, PINK, pygame.Rect(0, 0, WIDTH, HEIGHT), 3)


def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))
        # pygame.draw.rect(screen, BRIGHT_MAROON, pygame.Rect(segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))
        pygame.draw.rect(screen, BLACK, pygame.Rect(segment[0] + 2, segment[1] + 2, SNAKE_SIZE - 4, SNAKE_SIZE - 4))


def draw_food(food):
    pygame.draw.rect(screen, BLACK, pygame.Rect(food[0], food[1], SNAKE_SIZE, SNAKE_SIZE))
    pygame.draw.rect(screen, BRIGHT_MAROON, pygame.Rect(food[0] + 2, food[1] + 2, SNAKE_SIZE - 4, SNAKE_SIZE - 4))
    # pygame.draw.rect(screen, RED, pygame.Rect(food[0] + 2, food[1] + 2, SNAKE_SIZE - 4, SNAKE_SIZE - 4))


def display_score(score, high_score):
    score_text = font.render(f"SCORE: {score} HIGH SCORE: {high_score}", True, WHITE)
    # score_text = font.render(f"SCORE: {score} HIGH SCORE: {high_score}", True, GREY)
    screen.blit(score_text, [10, 10])


def display_message(message, duration=5):
    screen.fill(BLACK)
    draw_border()
    text = font.render(message, True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    time.sleep(duration)


def move_snake(snake, direction):
    x, y = snake[0]
    if direction == "UP":
        y -= SNAKE_SIZE
    elif direction == "DOWN":
        y += SNAKE_SIZE
    elif direction == "LEFT":
        x -= SNAKE_SIZE
    elif direction == "RIGHT":
        x += SNAKE_SIZE

    new_head = (x, y)
    return [new_head] + snake[:-1]


def check_collision(snake):
    x, y = snake[0]
    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        return True
    if snake[0] in snake[1:]:
        return True
    return False


def main():
    global direction, food, score, high_score, snake, dashing, last_dash_time, paused, marry_me_shown
    running = True
    while running:
        screen.fill(BLACK)
        draw_border()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if paused:
                    paused = False
                else:
                    if event.key == pygame.K_w and direction != "DOWN":
                        direction = "UP"
                    elif event.key == pygame.K_s and direction != "UP":
                        direction = "DOWN"
                    elif event.key == pygame.K_a and direction != "RIGHT":
                        direction = "LEFT"
                    elif event.key == pygame.K_d and direction != "LEFT":
                        direction = "RIGHT"
                    elif event.key == pygame.K_SPACE and not dashing and (time.time() - last_dash_time > dash_cooldown):
                        dashing = True
                        last_dash_time = time.time()

        if score == 700 and not marry_me_shown:
            marry_me_shown = True
            display_message("Marry Me?", 5)

        if dashing and time.time() - last_dash_time > 1:
            dashing = False

        if direction != "STOP":
            snake = move_snake(snake, direction)

        if check_collision(snake):
            time.sleep(1)
            snake = [(WIDTH // 2, HEIGHT // 2)]
            direction = "STOP"
            score = 0

        if snake[0] == food:
            score += 10
            if score > high_score:
                high_score = score
            food = (random.randint(0, (WIDTH // SNAKE_SIZE) - 1) * SNAKE_SIZE,
                    random.randint(0, (HEIGHT // SNAKE_SIZE) - 1) * SNAKE_SIZE)
            snake.append(snake[-1])

        draw_food(food)
        draw_snake(snake)
        display_score(score, high_score)
        pygame.display.update()
        clock.tick(DASH_SPEED if dashing else SPEED)

    pygame.quit()


if __name__ == "__main__":
    main()
