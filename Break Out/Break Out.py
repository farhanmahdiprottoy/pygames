import pygame
import random

pygame.init()

WIDTH, HEIGHT = 1280, 700

WHITE = (255, 255, 255)
PRISON_BRICK = (56, 59, 57)
BRICK_RED = (203, 65, 84)
PRISON_ORANGE = (255, 102, 0)
BLUE = (0, 0, 200)
GREEN = (0, 200, 0)


BALL_SPEED = 5
PADDLE_SPEED = 10
BRICK_ROWS = 5
BRICK_COLS = 8
BRICK_WIDTH = WIDTH // BRICK_COLS
BRICK_HEIGHT = 20


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Break Out")

paddle = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 20, 100, 10)

ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, 10, 10)
ball_dx, ball_dy = BALL_SPEED, - BALL_SPEED

bricks = []
for row in range(BRICK_ROWS):
    for col in range(BRICK_COLS):
        brick = pygame.Rect(col * BRICK_WIDTH, row * BRICK_HEIGHT, BRICK_WIDTH - 2, BRICK_HEIGHT - 2)
        bricks.append(brick)

running = True
while running:
    screen.fill(RICH_BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= PADDLE_SPEED
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.x += PADDLE_SPEED

    ball.x += ball_dx
    ball.y += ball_dy

    if ball.left <= 0 or ball.right >= WIDTH:
        ball_dx = - ball_dx
    if ball.top <= 0:
        ball_dy = - ball_dy

    if ball.colliderect(paddle):
        ball_dy = - BALL_SPEED

    for brick in bricks[:]:
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball_dy = - ball_dy
            break

    if ball.bottom >= HEIGHT:
        running = False


    pygame.draw.rect(screen, WHITE, paddle, border_radius = 10)
    pygame.draw.ellipse(screen, WHITE, ball)
    for brick in bricks:
        # pygame.draw.rect(screen, BRICK_RED, brick)
        pygame.draw.rect(screen, PRISON_BRICK, brick)
    
    if not bricks:
        running = False    

    pygame.display.flip()
    pygame.time.delay(15)

pygame.quit()


