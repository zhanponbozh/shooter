import pygame
from pygame import mixer, key
from random import randint

pygame.font.init()
pygame.init()
mixer.init()

font = pygame.font.Font(None, 80)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((700, 500))
mixer.music.load('space.ogg')
shoot_sound = pygame.mixer.Sound("fire.ogg")

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y, w, h):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load(image_path), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def __init__(self, image_path, x, y, w, h):
        super().__init__(image_path, x, y, w, h)
        self.speed = 5

    def update(self):
        keys = key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x >= 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x <= 640:
            self.rect.x += self.speed

    def fire(self):
        pass


class Enemy(GameSprite):
    def __init__(self, image_path, x, y, w, h):
        super().__init__(image_path, x, y, w, h)
        self.speed = 3

    def update(self):
        bullets_collided = pygame.sprite.spritecollide(self, bullets, False)
        if bullets_collided:
            for bullet in bullets_collided:
                bullet.kill()
            self.rect.x = randint(0, 600)
            self.rect.y = randint(-200, 0)
            points_label.score += 1
            
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.x = randint(0, 600)
            self.rect.y = randint(-100, 0)
            lost_label.score += 1


class Label:
    def __init__(self, text, score, color, x, y):
        self.text = text
        self.score = score
        self.color = color
        self.x = x
        self.y = y
        self.font = pygame.font.Font(None, 36)

    def draw(self):
        image = self.font.render(self.text + str(self.score), True, self.color)
        screen.blit(image, (self.x, self.y))


class Bullet(GameSprite):
    def __init__(self, image_path, x, y, w, h):
        super().__init__(image_path, x, y, w, h)
        self.speed = 5

    def update(self):
        self.rect.y -= self.speed

win_text = font.render('WIN!', True, (0, 255, 0))
lose_text = font.render('LOSE!', True, (255, 0, 0))
points_label = Label('Очки: ', 0, (255, 255, 255), 20, 10)
lost_label = Label('Пропущено: ', 0, (255, 255, 255), 20, 40)
bg = GameSprite('galaxy.jpg', 0, 0, 700, 500)
player = Player('rocket.png', 325, 400, 60, 90)
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
for i in range(5):
    x = randint(0, 600)
    y = randint(0, 200)
    enemy = Enemy('ufo.png', x, y, 100, 70)
    enemies.add(enemy)

cooldown = 0
run = True
mixer.music.play()
state = 'game'
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and cooldown <= 0:
                pygame.mixer.Sound.play(shoot_sound)
                bullet = Bullet('bullet.png', player.rect.x+23, player.rect.y, 10, 20)
                bullets.add(bullet)
                cooldown = 15
    
    if state == 'game':            
        cooldown -= 1
        player.update()
        bullets.update()
        enemies.update()
    
    if points_label.score == 10:
        state = 'win'

    if lost_label.score >= 3:
        state = 'lose'

        
    bg.draw()
    bullets.draw(screen)
    enemies.draw(screen)
    player.draw()
    points_label.draw()
    lost_label.draw()
    if state == 'lose':
        screen.blit(lose_text, (300, 200))

    if state == 'win':
        screen.blit(win_text, (300, 200))
    pygame.display.update()
    clock.tick(30)