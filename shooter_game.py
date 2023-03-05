#Створи власний Шутер!
import pygame as pg
from random import randint, uniform, shuffle
import time

pg.mixer.init()
pg.font.init()

pg.mixer.music.load('space.ogg')
pg.mixer.music.play()
fire_sound = pg.mixer.Sound('fire.ogg')

DISPLAY = WIN_W, WIN_H = 800, 600
FPS = 60

mw = pg.display.set_mode(DISPLAY)
bg = pg.transform.scale(pg.image.load('galaxy.jpg'), DISPLAY)
clock = pg.time.Clock()

class GameSprite(pg.sprite.Sprite):
    def __init__(self, image, speed, x_cor, y_cor, width, height):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(pg.image.load(image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x_cor
        self.rect.y = y_cor
        self.speed = speed

    def reset(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        key_pressed = pg.key.get_pressed()
        if key_pressed[pg.K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if key_pressed[pg.K_d] and self.rect.x < WIN_W - self.rect.width:
            self.rect.x += self.speed
        # if key_pressed[pg.K_SPACE]:
        #     self.shoot()
        #     fire_sound.play()

    def shoot(self):
        b = Bullet('bullet.png', 9, self.rect.centerx - 5, self.rect.top, 10, 15)
        bullets.add(b)

class UFO(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > WIN_H + 5:
            if type(self) == UFO:
                lost += 1
            self.speed = uniform(1.5, 3.5)
            self.rect.y = -self.rect.height - 10
            self.rect.x = randint(0, WIN_W - self.rect.width)

class Asteroid(UFO):
    pass

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < -self.rect.height:
            self.kill()

bullets = pg.sprite.Group()            
ufos = pg.sprite.Group()
asteroids = pg.sprite.Group()

for i in range(3):
    a = Asteroid('asteroid.png', uniform(1.3, 2.3), randint(0, WIN_W - 50), -60, 50,50)
    asteroids.add(a)

for i in range(5):
    u = UFO('ufo.png', uniform(1.5, 3.5), randint(0, WIN_W - 80), -60, 80, 50)
    ufos.add(u)

player = Player('rocket.png', 7, WIN_W/2, WIN_H-80, 50, 80)

score = 0
lost = 0
health = 3

num_fire = 0
rel_time = False

game = True

while game:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                if num_fire < 7 and not rel_time:
                    fire_sound.play()
                    player.shoot()
                    num_fire += 1
                # Дз
                # Условие работает не правильно, при нажатии на пробел
                # если идёт перезарядка, счётчик обнуляется.
                # ТАК БЫТЬ НЕ ДОЛЖНО. ИСПРАВИТЬ!
                if num_fire >= 7: 
                    rel_time = True
                    start_reload = time.time()
     
    if len(ufos) < 5:
        u = UFO('ufo.png', uniform(1.5, 3.5), randint(0, WIN_W - 80), -60, 80, 50)
        ufos.add(u)
    
    if len(asteroids) < 3:
        a = Asteroid('asteroid.png', uniform(1.3, 2.3), randint(0, WIN_W - 50), -60, 50,50)
        asteroids.add(a) 

    mw.blit(bg, (0,0))
    player.update()
    ufos.update()
    bullets.update()
    asteroids.update()

    player.reset()
    for u in ufos:
        u.reset()
    for b in bullets:
        b.reset()
    for a in asteroids:
        a.reset()

    if rel_time:
        if time.time() - start_reload < 3:
            rel = pg.font.Font(None, 30).render('Reload...', True, (200, 0, 0))
            mw.blit(rel, (player.rect.topright)) 
        else:
            num_fire = 0
            rel_time = False

    pg.sprite.groupcollide(bullets, asteroids, True, False)
    if pg.sprite.groupcollide(bullets, ufos, True, True):
        score += 1
    colisions = pg.sprite.spritecollide(player, ufos, True)
    if len(colisions) > 0:
        health -= len(colisions)
        score += len(colisions)
        print('Colisions ->', len(colisions))
    colisions = pg.sprite.spritecollide(player, asteroids, True)
    if len(colisions) > 0:
        health -= len(colisions)
        
    lost_font = pg.font.Font(None, 40).render(f'Lost: {str(lost)}', True, (255,255,255))
    score_font = pg.font.Font(None, 40).render(f'Score: {str(score)}', True, (255,255,255))
    health_font = pg.font.Font(None, 30).render(str(health), True, (255,255,255))
    mw.blit(health_font, (player.rect.topleft))
    mw.blit(lost_font, (10,10))
    mw.blit(score_font, (10,35))

    if health <= 0:
        end = pg.font.Font(None, 40).render(f'YOU LOSE...', True, (255,0,0))
        mw.blit(end, (WIN_W/2, WIN_H/2))
        pg.display.update()
        pg.time.wait(3000)
        game = False

    if score >= 70:
        end = pg.font.Font(None, 40).render(f'YOU WIN !!!', True, (0,255,0))
        mw.blit(end, (WIN_W/2, WIN_H/2))
        pg.display.update()
        pg.time.wait(3000)
        game = False
    

    pg.display.update()
    clock.tick(FPS)