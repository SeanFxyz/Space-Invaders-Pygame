import math
import random

import pygame
from pygame import mixer

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

enemy_freq = 2000

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 0

def add_enemy():
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(10)
    enemyY.append(40)
    enemyX_change.append(4)
    enemyY_change.append(40)
    global num_of_enemies
    num_of_enemies += 1

def rm_enemy(i):
    del enemyImg[i]
    del enemyX[i]
    del enemyY[i]
    del enemyX_change[i]
    del enemyY_change[i]
    global num_of_enemies
    num_of_enemies -= 1

add_enemy()

# Enemy spawn portal
portalImg = pygame.image.load('portal.png')
portalX = 0
portalY = 80

# Time since last enemy spawned
last_enemy_spawn = pygame.time.get_ticks()

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    # Enemy spawn portal
    screen.blit(portalImg, (portalX, portalY))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    # Get the current x cordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Spawning enemies
    if pygame.time.get_ticks() - last_enemy_spawn > enemy_freq:
        add_enemy()
        last_enemy_spawn = pygame.time.get_ticks()

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()

            try:
                with open('score.txt') as score_file:
                    stored_score = int(score_file.readline())
                    if score_value > stored_score:
                        highscore = font.render("High Score!!!", True, (255, 255, 255))
                        screen.blit(highscore, (200, 300))
                        score_file.close()
                        write_score = True
            except IOError:
                write_score = True
            if write_score:
                with open('score.txt', 'w') as score_file:
                    score_file.writelines(str(score_value) + '\n')
                    score_file.close()

            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            if enemy_freq > 200:
                enemy_freq -= 50
            enemyX[i] = -100
            enemyY[i] = -100
            enemyX_change[i] = 0
            enemyY_change[i] = 0
        else:
            enemy(enemyX[i], enemyY[i], i)

    # Removing enemies
    i = 0
    while i < num_of_enemies:
        if enemyX[i] < -50 and enemyX_change[i] == 0:
            rm_enemy(i)
        i += 1

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()
