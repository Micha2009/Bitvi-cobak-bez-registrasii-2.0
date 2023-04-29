#Создай собственный Шутер!

from random import randint
from pygame import *


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, w, h):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w, h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, -15, 50, 50)
        bullets.add(bullet)

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 50:
            self.rect.x -=10
        if keys_pressed[K_d] and self.rect.x < 650:
            self.rect.x +=10

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0 :
            self.kill()

lost = 0
max_lost = 4
goal = 20
score = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(500, 630)
            lost = lost+1

bullets = sprite.Group()

monsters = sprite.Group()
for i in range(8):
    m = Enemy('ufo.png', randint(5, 630), 0 , randint(1, 5), 100, 80)
    monsters.add(m)

font.init()
font1 = font.SysFont('Arial', 57)
text_lose = font1.render("Пропущено: " + str(lost), 1, (234, 54, 193))
lose = font1.render("Проиграл" + str(), 1, (200, 35, 106))
win = font1.render("Ура победа" + str(), 1,  (200, 35, 106))

win_width = 800
win_height = 600
window = display.set_mode((win_width, win_height))
display.set_caption("Maze")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')

game = True
clock = time.Clock()
FPS = 600

rocket = Player('rocket.png', 350, 500, 1, 100, 80)

finish = False

while game:
    if not finish:
        window.blit(background,(0, 0))
        text_lose = font1.render("Пропущено: " + str(lost), 1, (234, 54, 193))
        window.blit(text_lose,(0, 0))
        rocket.reset()
        rocket.update()
        bullets.update()
        monsters.draw(window)
        bullets.draw(window)
        monsters.update()
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire.play()
                rocket.fire()
    
    collides = sprite.groupcollide(monsters, bullets, True, True)
    for c in collides:
        score = score + 1
        monster = Enemy('ufo.png', randint(5, 630), 0 , randint(1, 5), 100, 80)
        monsters.add(monster)

    if sprite.spritecollide(rocket, monsters, False) or lost >= max_lost:
        finish = True
        window.blit(lose, (200, 200))

    if score >= goal:
        finish = True
        window.blit(win, (200, 200))

    display.update()
    clock.tick(FPS)

