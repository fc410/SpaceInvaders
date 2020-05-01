import math
import random
import os
import pygame
from pygame import mixer

from rules import *


highscore_File = "Highscore.txt"
from os import path


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

# Boss
bossImg = pygame.image.load('alienBoss.png')


# Enemy

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('bullet.png')

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# HighScore
high_score = 0
highTextX = 500
highTextY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def show_highscore(x, y):
    highscore = font.render("HighScore : " + str(contents), True, (255, 255, 255))
    screen.blit(highscore, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))

def alienBoss(x, y):
    screen.blit(bossImg, (x, y))



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

def load_data(self):
    # Load highscore
    self.dir = path.dirname(__file__)
    with open(path.join(self.dir, highscore_File), 'w') as f:
        try:
            self.highscore = int(f.read())
        except:
            self.highscore = 0

def highScore(score):
    if score >= int(contents):
        with open("Highscore.txt", "rb+") as filehandle:
            filehandle.seek(-1, os.SEEK_END)
            filehandle.truncate()
    f = open("Highscore.txt", "w")
    f.write(str(score))
    f.close()
# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
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

    bossX += bossX_change
    if bossX <= 0:
        bossX_change = 4
        bossY += bossY_change
    elif bossX >= 736:
        bossX_change = -4
        bossY += bossY_change

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()

        if bossY > 440 and bossY < 2000:
            bossY = 2000
            game_over_text()

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]\
        

        bossCollision = isCollision(bossX, bossY, bulletX, bulletY)
        if bossCollision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready" 
            score_value += 1
            if bossImg.get_width() > 16:
                bossImg = pygame.transform.scale(bossImg, (int(bossImg.get_width()/2), int(bossImg.get_height()/2)))
                alienBoss(bossX, bossY)
            if bossImg.get_width() <= 16:
                bossY = 2000
                bossX = 0
                bossY_change = 0
                bossX_change = 0
            if score_value >= high_score:
                high_score = score_value

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            if score_value >= int(contents):
                contents = str(score_value)
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
            if score_value >= high_score:
                high_score = score_value

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    if score_value >= 1:
        alienBoss(bossX, bossY)
    show_score(textX, testY)
    show_highscore(highTextX, highTextY)
    highScore(score_value)
    pygame.display.update()
