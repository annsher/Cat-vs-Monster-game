import time
import pygame
import random
from os import path
import sys

img_dir = path.join(path.dirname(__file__), 'img')
font_name = pygame.font.match_font('helvetica')

WIDTH = 600
HEIGHT = 480
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cat vs Monster")
clock = pygame.time.Clock()

walk_cat = False
walk_monster = False
shoot_cat = False
shoot_monster = False

def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "CAT VS MONSTER", 64, WIDTH / 2, HEIGHT / 5)
    draw_text(screen, "CAT: W - вверх, S - вниз, D - выстрел", 22, WIDTH / 2, 2.5 * HEIGHT / 5)
    draw_text(screen, "MONSTER: клавиша вверх, клавиша вниз, пробел - выстрел ", 22, WIDTH / 2, 3 * HEIGHT / 5)
    draw_text(screen, "Нажмите X, чтобы начать", 18, WIDTH / 2, HEIGHT * 4 / 5)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    waiting = False

def draw_lives(surf, x, y, lives, img, name):
    for i in range(lives):
        img_rect = img.get_rect()
        if name == 'cat':
           img_rect.x = x + 30 * i
           img_rect.y = y
        else:
            img_rect.x = x + 210 - 30 * i
            img_rect.y = y
        surf.blit(img, img_rect)

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

class Cat(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.images.append(pygame.image.load(path.join(img_dir, "walkingcat1.png")).convert())
        self.images.append(pygame.image.load(path.join(img_dir, "walkingcat2.png")).convert())
        self.images.append(pygame.image.load(path.join(img_dir, "walkingcat3.png")).convert())
        self.images.append(pygame.image.load(path.join(img_dir, "walkingcat4.png")).convert())
        self.images.append(pygame.image.load(path.join(img_dir, "walkingcat5.png")).convert())
        self.images.append(pygame.image.load(path.join(img_dir, "walkingcat6.png")).convert())
        self.images.append(pygame.image.load(path.join(img_dir, "walkingcat7.png")).convert())
        self.images.append(pygame.image.load(path.join(img_dir, "walkingcat8.png")).convert())
        self.images.append(pygame.image.load(path.join(img_dir, "shootcat0.png")).convert())
        self.index = 0
        self.image = self.images[self.index]
        for i in range(9):
            self.images[i] = pygame.transform.scale(self.images[i], (90, 90))
            self.images[i].set_colorkey(BLACK)
            self.rect = self.images[i].get_rect()
        self.rect.centery = HEIGHT / 2
        self.rect.left = 0
        self.speedy = 0

    def update(self):
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_w]:
            self.speedy = -3
        elif keystate[pygame.K_s]:
            self.speedy = 3
        else:
            self.index = 0
        self.rect.y += self.speedy
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

    def shoot(self):
        self.index = 8
        cat_bullet = CatShoot(self.rect.centerx, self.rect.top)
        all_sprites.add(cat_bullet)
        cat_bullets.add(cat_bullet)

class Monster(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.images.append(pygame.image.load(path.join(img_dir, "walkingmon1.png")).convert())
        self.images.append(pygame.image.load(path.join(img_dir, "walkingmon2.png")).convert())
        self.images.append(pygame.image.load(path.join(img_dir, "walkingmon3.png")).convert())
        self.images.append(pygame.image.load(path.join(img_dir, "walkingmon4.png")).convert())
        self.images.append(pygame.image.load(path.join(img_dir, "walkingmon5.png")).convert())
        self.images.append(pygame.image.load(path.join(img_dir, "shootmon0.png")).convert())
        self.index = 0
        self.image = self.images[self.index]
        for i in range(6):
            self.images[i] = pygame.transform.scale(self.images[i], (80, 80))
            self.images[i].set_colorkey(BLACK)
            self.rect = self.images[i].get_rect()
        self.rect.centery = HEIGHT / 2
        self.rect.right = WIDTH
        self.speedy = 0

    def update(self):
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_UP]:
            self.speedy = -3
        elif keystate[pygame.K_DOWN]:
            self.speedy = 3
        else:
            self.index = 0
        self.rect.y += self.speedy
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

    def shoot(self):
        monster_bullet = MonsterShoot(self.rect.centerx, self.rect.top)
        all_sprites.add(monster_bullet)
        monster_bullets.add(monster_bullet)

class CatShoot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = cat_fire
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y + 70
        self.rect.centerx = x + 25
        self.speedx = 5

    def update(self):
        self.rect.x += self.speedx
        if self.rect.right < 0:
            self.kill()

class MonsterShoot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = monster_fire
        self.image = pygame.transform.scale(monster_fire, (30, 30))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y + 65
        self.rect.centerx = x - 15
        self.speedx = -7

    def update(self):
        self.rect.x += self.speedx
        if self.rect.left < 0:
            self.kill()


background = pygame.image.load(path.join(img_dir, "bg.jpg")).convert()
background_rect = background.get_rect()
cat_fire = pygame.image.load(path.join(img_dir, "cat_shoot.png")).convert()
monster_fire = pygame.image.load(path.join(img_dir, "monsterball.png")).convert()
all_sprites = pygame.sprite.Group()
monster = Monster()
cat = Cat()
cat_mini_img = pygame.transform.scale(cat.images[0], (25, 25))
cat.lives = 8
monster_mini_img = pygame.transform.scale(monster.images[0], (25, 25))
monster.lives = 8
all_sprites.add(cat)
all_sprites.add(monster)
cat_bullets = pygame.sprite.Group()
monster_bullets = pygame.sprite.Group()
running = True
game_over = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        cat_bullets = pygame.sprite.Group()
        monster_bullets = pygame.sprite.Group()
        cat = Cat()
        monster = Monster()
        all_sprites.add(cat)
        all_sprites.add(monster)
        cat.lives = 8
        monster.lives = 8
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                shoot_cat = True
                walk_cat = False
                cat.shoot()
            if event.key == pygame.K_SPACE:
                walk_monster = False
                shoot_monster = True
                monster.shoot()
            if event.key == pygame.K_w:
                walk_cat = True
                shoot_cat = False
            if event.key == pygame.K_s:
                walk_cat = True
                shoot_cat = False
            if event.key == pygame.K_UP:
                walk_monster = True
            if event.key == pygame.K_DOWN:
                walk_monster = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                shoot_cat = False
            if event.key == pygame.K_SPACE:
                shoot_monster = False

    if walk_cat:
        cat.index += 1
        if cat.index >= len(cat.images):
            cat.index = 0
        cat.image = cat.images[cat.index]
    elif shoot_cat:
        cat.image = cat.images[8]
    else:
        cat.index = 0
        cat.image = cat.images[cat.index]

    if walk_monster:
        monster.index += 1
        if monster.index >= len(monster.images):
            monster.index = 0
        monster.image = monster.images[monster.index]
    elif shoot_monster:
        monster.image = monster.images[5]
    else:
        monster.image = monster.images[0]
        monster.index = 0
    if monster.lives == 0:
        draw_text(screen, 'Cat wins!', 48, WIDTH / 2, HEIGHT / 2)
        pygame.display.flip()
        time.sleep(2)
        game_over = True
    if cat.lives == 0:
        draw_text(screen, 'Monster wins!', 48, WIDTH / 2, HEIGHT / 2)
        pygame.display.flip()
        time.sleep(2)
        game_over = True
    cat_hits = pygame.sprite.spritecollide(cat, monster_bullets, True)
    for hit in cat_hits:
        cat.lives -= 1
    monster_hits = pygame.sprite.spritecollide(monster, cat_bullets, True)
    for hit in monster_hits:
        monster.lives -= 1


    all_sprites.update()

    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_lives(screen, 0, 5, cat.lives, cat_mini_img, 'cat')
    draw_lives(screen, WIDTH - 25*10 + 10, 5, monster.lives, monster_mini_img, 'monster')
    pygame.display.flip()

pygame.quit()
sys.exit()