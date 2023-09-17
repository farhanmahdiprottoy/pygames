import pygame
from pygame import mixer
from pygame.locals import *
import random


pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()


# FPS
clock = pygame.time.Clock()
FPS = 60


screen_width = 600
screen_height = 900

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Star War : Space Invaders (2D)')


# fonts
font30 = pygame.font.SysFont('Constantia', 30)
font60 = pygame.font.SysFont('Constantia', 60)


# sounds
explosion_fx = pygame.mixer.Sound("swsi/explosion.wav")
explosion_fx.set_volume(0.25)

explosion2_fx = pygame.mixer.Sound("swsi/explosion2.wav")
explosion2_fx.set_volume(0.25)

laser_fx = pygame.mixer.Sound("swsi/laser.wav")
laser_fx.set_volume(0.05)

mixer.music.load('swsi/bgmusic1.wav')
mixer.music.set_volume(0.5)
mixer.music.play(-1)


# game variables
rows = 4
cols = 5
alien_cooldown = 85      # bullet cooldown in mils
last_alien_shot = pygame.time.get_ticks()
countdown = 4
last_count = pygame.time.get_ticks()
game_over = 0            # 0 in-game, 1 means player has won, -1 means player has lost.

# colours used
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)


# loads image
bg = pygame.image.load("swsi/bg.png")
overlap = pygame.image.load("swsi/bg1.png")
pos = 0


def draw_bg():
    global pos
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))

    screen.blit(overlap, (0, pos))
    screen.blit(overlap, (0, overlap.get_height() + pos))
    pos += 1

    if pos+1800 > overlap.get_height():
        pos = 0


# defines function for creating text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# creates spaceship class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("swsi/spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.health_remaining = health
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        # sets movement speed
        speed = 10
        # sets a cooldown variable
        cooldown = 230  # in milliseconds
        game_over = 0


        # control keys
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += speed

        # ## if key[pygame.K_SPACE] and game_over != 0 :
        # ## game_over = 0
        # ## rows = 4
        # ## cols = 5
        # ## last_alien_shot = pygame.time.get_ticks()
        # ## countdown = 4
        # ## last_count = pygame.time.get_ticks()
        # ## self.spaceship.center = (int(screen_width / 2), screen_height - 70, 3)
        # ## alien_fleet.empty()


        # current time
        time_now = pygame.time.get_ticks()
        # shoots
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            laser_fx.play()
            bullet = Laser(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_shot = time_now

        # updates mask
        self.mask = pygame.mask.from_surface(self.image)

        # health bar
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 2), self.rect.width, 2))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 2), int(self.rect.width * (self.health_remaining / self.health_start)), 2))
        elif self.health_remaining <= 0:
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            explosion_group.add(explosion)
            self.kill()
            game_over = -1
        return game_over


# creates Laser class
class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("swsi/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, alien_fleet, True):
            self.kill()
            explosion_fx.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosion_group.add(explosion)


# creates Aliens class
class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        alien_num = random.randint(1, 4)
        self.image = pygame.image.load("swsi/alien" + str(alien_num) + ".png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        if (alien_num% 3 == 0):
            self.move_direction = 1
        if (alien_num% 2 == 0):
            self.move_direction = 1
        else:
            self.move_direction = -1

    def update(self):

        self.rect.x += self.move_direction
        self.move_counter += 1
        self.rect.y += 1

        if abs(self.move_counter) > 87:
            self.rect.y -= 3
            self.move_direction *= -1
            self.move_counter *= self.move_direction


# creates Alien Shockwaves class
class Alien_Shockwaves(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("swsi/alienshockwave" + str(random.randint(1, 3)) + ".png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += 2
        if self.rect.top > screen_height:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            self.kill()
            explosion2_fx.play()
            # reduces spaceship health
            spaceship.health_remaining -= 1
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            explosion_group.add(explosion)


# creates Explosion class
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f"swsi/exp{num}.png")
            if size == 1:
                img = pygame.transform.scale(img, (20, 20))
            if size == 2:
                img = pygame.transform.scale(img, (40, 40))
            if size == 3:
                img = pygame.transform.scale(img, (160, 160))
            # adds the image to the list
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 3
        # updates explosion animation
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        # if the animation is complete, deletes explosion
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()




# creates sprite groups
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_fleet = pygame.sprite.Group()
alien_shockwave_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()


def create_aliens():
    # generates aliens
    for row in range(rows):
        for item in range(cols):
            alien = Aliens(100 + item * 100, 100 + row * 70)
            alien_fleet.add(alien)


create_aliens()


# creates player
spaceship = Spaceship(int(screen_width / 2), screen_height - 70, 3)
spaceship_group.add(spaceship)


run = True
while run:

    clock.tick(FPS)

    # background
    draw_bg()

    if countdown == 0:
        # creates random alien shokwaves
        # records current time
        time_now = pygame.time.get_ticks()
        #shoot
        if time_now - last_alien_shot > alien_cooldown and len(alien_shockwave_group) < 25 and len(alien_fleet) > 0:
            attacking_alien = random.choice(alien_fleet.sprites())
            alien_shockwave = Alien_Shockwaves(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
            alien_shockwave_group.add(alien_shockwave)
            last_alien_shot = time_now

        # checks if all the aliens have been killed
        if len(alien_fleet) == 0:
            game_over = 1
        if time_now > 27000 and game_over != -1 and game_over != 1:
            game_over = -2

        if game_over == 0:
            # updates spaceship
            game_over = spaceship.update()

            # updates sprite groups
            bullet_group.update()
            alien_fleet.update()
            alien_shockwave_group.update()
        else:
            if game_over == -1:
                draw_text('KIA', font60, white, int(screen_width / 2 - 50), int(screen_height / 7 + 50))
                draw_text('please rerun to play again', font30, green, int(screen_width / 2 - 150), int(screen_height / 2 + 300))

            if game_over == 1:
                draw_text('Shabash !', font30, white, int(screen_width / 2 - 150), int(screen_height / 5 + 50))
                draw_text('All threats eliminated ', font30, white, int(screen_width / 2 - 150), int(screen_height / 4 + 50))
                draw_text('THE END ', font60, white, int(screen_width / 2 - 120), int(screen_height / 3 + 50))
                draw_text('please rerun to play again', font30, white, int(screen_width / 2 - 150), int(screen_height / 2 + 300))

            if game_over == -2:
                draw_text('GAME OVER', font30, red, int(screen_width / 2 - 150), int(screen_height / 5 + 50))
                draw_text('YOU FAILED', font60, white, int(screen_width / 2 - 170), int(screen_height / 4 + 50))
                draw_text('Humans Lost', font30, white, int(screen_width / 2 - 150), int(screen_height / 3 + 50))
                draw_text('please rerun to play again', font30, green, int(screen_width / 2 - 150), int(screen_height / 2 + 300))



    if countdown > 0:
        draw_text('Defend Humanity', font60, white, int(screen_width / 2 - 230), int(screen_height / 3 + 50))
        draw_text('And save yourself !', font30, white, int(screen_width / 2 - 60), int(screen_height / 2 + 20))
        draw_text(str(countdown), font60, white, int(screen_width / 2 - 10), int(screen_height / 2 + 100))
        count_timer = pygame.time.get_ticks()
        if count_timer - last_count > 1000:
            countdown -= 1
            last_count = count_timer


    # updates explosion group
    explosion_group.update()


    # sprite groups
    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    alien_fleet.draw(screen)
    alien_shockwave_group.draw(screen)
    explosion_group.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
