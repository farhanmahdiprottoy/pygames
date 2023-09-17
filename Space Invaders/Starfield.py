import pygame
import random

pygame.init()


width = 1200
height = 800

center_x = width/2
center_y = height/2

star_color = pygame.Color(255, 255, 255, 255)


class Star:

    def __init__(self):
        self.x = random.randint(-width, width)
        self.y = random.randint(-height, height)
        self.z = random.randint(center_y, width)
        self.pz = self.z

    def update(self):
        self.z -= 30
        if self.z < 1:
            self.x = random.randint(-width, width)
            self.y = random.randint(-height, height)
            self.z = random.randint(center_y, width)
            self.pz = self.z

    def draw(self):
        starX = self.x / self.z * center_y + center_x
        starY = self.y / self.z * center_y + center_y

        radius = maps(star.z, 0, width, 6, 0)

        pygame.draw.circle(screen, star_color, (starX, starY), radius)

        prevX = self.x / self.pz * center_y + center_x
        prevY = self.y / self.pz * center_y + center_y

        self.pz = self.z

        pygame.draw.line(screen, star_color, (prevX, prevY), (starX, starY), 2)


def maps(num, in_min, in_max, out_min, out_max):
    return out_min + (out_max - out_min) * (num - in_min) / (in_max - in_min)

def set_color(star):
    # The rgb values starts from 0 (black) and gradually increases to 255 (white)
    # Thus, causes the new stars to slowly fade onto the screen
    value = 255 - int((star.z * (255/width)))
    star_color.r, star_color.g, star_color.b = value, value, value


screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Starfield')
clock = pygame.time.Clock()

stars = []

for i in range(500):
    stars.append(Star())

running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    for star in stars:
        star.update()
        set_color(star)
        star.draw()

    pygame.display.update()
