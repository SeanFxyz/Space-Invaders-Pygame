import math
import random

import pygame
from pygame import mixer
from pygame import math

# List of all active and not-yet deleted GameObjects
game_objects = []

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background Music
#mixer.music.load("background.wav")
#mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Text Objects
## Score
score = 0
score_font = pygame.font.Font('freesansbold.ttf', 32)
## Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Cached sprites
playerImg = pygame.image.load('player.png')
bulletImg = pygame.image.load('bullet.png')
enemyImg = pygame.image.load('enemy.png')
portalImg = pygame.image.load('portal.png')
background = pygame.image.load('background.png')


# Game management
game_clock = pygame.time.Clock()
## Time since last enemy spawned
last_enemy_spawn = 0
## Enemy spawn frequency
enemy_freq = 2000

def add_score(enemyObj):
    global score
    score += enemyObj.score_value

def show_score(x, y):
    score_text = score_font.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def is_collision(obj1, obj2):
    for hb1 in obj1.hitboxes:
        for hb2 in obj2.hitboxes:
            if hb1.colliderect(hb2):
                return True
    return False

class GameObject():

    def __init__(self, x=0, y=0, sprite=None):

        self.enabled = True
        self.deleted = False
        self.x = x
        self.y = y
        self.sprite = sprite
        self.tags = []
        self.hitboxes = [pygame.Rect(0, 0, 0, 0)]

        # Whether the update function will take a list of events as a parameter.
        self.is_event_handler = False

    def update(self, delta):
        pass

    def on_collision(self, collider):
        pass

class Enemy(GameObject):
    def __init__(self, x=0, y=0, sprite=pygame.image.load('enemy.png'), speed=1):
        super().__init__()

        self.x, self.y = x, y
        self.sprite = sprite
        self.hitboxes = [
                pygame.Rect(
                    self.x, self.y,
                    self.sprite.get_width(), self.sprite.get_height())
                ]

        self.tags = ['enemy']

        self.velocity = math.Vector2()
        self.velocity.x = speed
        self.changeY = 40

        self.score_value = 1

    def update(self, delta):

        self.velocity.normalize
        self.x += self.velocity.x * delta
        self.y += self.velocity.y * delta

        if self.x <= 0:
            self.velocity.x *= -1
            self.x = 1
            self.y += self.changeY
        elif self.x >= 736:
            self.velocity.x *= -1
            self.x = 735
            self.y += self.changeY

        self.hitboxes = [
                pygame.Rect(
                    self.x, self.y,
                    self.sprite.get_width(), self.sprite.get_height())
                ]

    def on_collision(self, collider):
        if 'bullet' in collider.tags:
            self.deleted = True
            add_score(self)

class Player(GameObject):

    def __init__(self, x=0, y=0, sprite=pygame.image.load('player.png'),
            bullet_sprite=pygame.image.load('bullet.png'),
            score_tracker=None):

        super().__init__()
        
        selfx, self.y = x, y
        self.sprite = sprite
        self.bullet_sprite = bullet_sprite
        self.bullet_xoffset = (
                self.sprite.get_width() / 2 - bullet_sprite.get_width() / 2)

        self.tags = ['player']

        self.velocity = math.Vector2()

        self.is_event_handler = True

        inputs = [
                pygame.K_LEFT,
                pygame.K_RIGHT,
                pygame.K_UP,
                pygame.K_DOWN,
                pygame.K_SPACE
                ]

        self.input_state = {}
        for i in inputs:
            self.input_state[i] = False

        self.attack_ready = True
        self.attack_time = 0
        # Attack cooldown in ms.
        self.attack_cooldown = 1000

        self.bullet_dmg = 10

    
    def update(self, delta, events):

        # Get Player Input
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in self.input_state.keys():
                    self.input_state[event.key] = True
            elif event.type == pygame.KEYUP:
                if event.key in self.input_state.keys():
                    self.input_state[event.key] = False

        # Translate pressed keys to a movement direction.
        self.velocity = math.Vector2()
        if self.input_state[pygame.K_LEFT]:
            self.velocity.x -= 1
        if self.input_state[pygame.K_RIGHT]:
            self.velocity.x += 1
#        if self.input_state[pygame.K_UP]:
#            self.velocity.y -= 1
#        if self.input_state[pygame.K_DOWN:
#            self.velocity.y += 1
        if self.input_state[pygame.K_SPACE]:
            self.shoot()

        # Apply movement
        if self.velocity.length() != 0:
            self.velocity.normalize()
            self.x += self.velocity.x * delta
            self.y += self.velocity.y * delta

        self.hitboxes = [
                pygame.Rect(
                    self.x + 5, self.y + 5,
                    self.sprite.get_width() - 5, self.sprite.get_height() - 5)
                ]
        
        # If attack is on cooldown, check if cooldown is expired.
        if(self.attack_ready == False and
                pygame.time.get_ticks() - self.attack_time > self.attack_cooldown):

            self.attack_ready = True

    def shoot(self):
        if self.attack_ready:
            self.attack_ready = False
            self.attack_time = pygame.time.get_ticks()
            bulletSound = mixer.Sound("laser.wav")
            bulletSound.play()
            game_objects.append(Bullet(self.x + self.bullet_xoffset, self.y,
                sprite=self.bullet_sprite, dmg=self.bullet_dmg))

    def on_collision(self, collider):
        if 'enemy' in collider.tags:
            self.deleted = True
            game_objects.append(
                    GameObject(200, 250, 
                        over_font.render("GAME OVER", True, (255, 255, 255))))

class Bullet(GameObject):
    def __init__(self, x=0, y=0, sprite=pygame.image.load('bullet.png'),
            speed=1, dmg=10):

        super().__init__()

        self.x = x
        self.y = y
        self.tags = ['bullet']
        self.sprite = sprite
        self.speed = speed
        self.hitboxes = [
                pygame.Rect(
                    self.x, self.y,
                    self.sprite.get_width(), self.sprite.get_height())
                ]

        self.dmg = dmg

    def update(self, delta):
        self.y -= self.speed * delta
        if self.y < -10:
            self.deleted = True
        self.hitboxes = [
                pygame.Rect(
                    self.x, self.y,
                    self.sprite.get_width(), self.sprite.get_height())
                ]

class EnemySpawner(GameObject):

    def __init__(self, x=0, y=0, sprite=pygame.image.load('portal.png'),
            cooldown=1000, speed=1):

        super().__init__()

        self.x, self.y = x, y
        self.sprite = sprite
        self.tags = ['enemySpawner']
        self.hitboxes = [
                pygame.Rect(
                    self.x, self.y,
                    self.sprite.get_width(), self.sprite.get_height())
                ]

        self.cooldown = cooldown
        self.hp = 100
        self.last_spawn = pygame.time.get_ticks()
        self.speed = speed

    def update(self, delta):
        time = pygame.time.get_ticks()
        if time - self.last_spawn >= self.cooldown:
            game_objects.append(Enemy(self.x, self.y + 30,
                        sprite=enemyImg, speed=self.speed))
            self.last_spawn = time

    def on_collision(self, collider):
        if 'bullet' in collider.tags:
            self.hp -= collider.dmg
            collider.deleted = True
            if self.hp <= 0:
                self.deleted = True

# Initial positions
## Player
playerX = 370
playerY = 480
## Enemy spawn portal
portalX = 0
portalY = 80

# Initial GameObjects
game_objects.append(
        Player(playerX, playerY, playerImg, bulletImg))
game_objects.append(
        EnemySpawner(0, 80, sprite=portalImg,
            cooldown=1000, speed=1))

# Game Loop
running = True
while running:

    delta = game_clock.tick()
    events = pygame.event.get()

    # Initialize screen
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    i = 0
    while i < len(game_objects):
        if game_objects[i].deleted:
            del game_objects[i]
        else:
            i += 1

    for obj in game_objects:
        if obj.enabled:
            if obj.is_event_handler:
                obj.update(delta, events)
            else:
                obj.update(delta)
            screen.blit(obj.sprite, (obj.x, obj.y))

        for collider in game_objects:
            if obj != collider and is_collision(obj, collider):
                obj.on_collision(collider)


    show_score(0, 0)
            
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

exit(0)
