import pygame
import math
import random
import sys
from pygame import mixer

pygame.init()

# Screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("TinyTails Game")

# Background
bg = pygame.image.load('bg.jpg')

# Music
mixer.music.load('cupid.mp3')
mixer.music.play(-1)

# Icon
icon = pygame.image.load('paw.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('deer.png')
playerX = 370
playerY = 470
playerX_change = 0
playerY_change = 0

# Bowl
bowlImg = pygame.image.load('bowl.png')
bowlX = 0
bowlY = 470
bowlY_change = 0.5
bowl_state = "ready"

# Candy
cotcanImg, cotcanX, cotcanY, cotcanX_change, cotcanY_change = [], [], [], [], []
num_of_candy = 6
for i in range(num_of_candy):
    cotcanImg.append(pygame.image.load('cotcan2.png'))
    cotcanX.append(random.randint(0, 750))
    cotcanY.append(random.randint(20, 160))
    cotcanX_change.append(0.2)
    cotcanY_change.append(50)

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 30)
over_font = pygame.font.Font('freesansbold.ttf', 64)
game_over = False

# Draw functions
def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def player(x, y):
    screen.blit(playerImg, (x, y))

def cotcan(x, y, i):
    screen.blit(cotcanImg[i], (x, y))

def fire_bowl(x, y):
    global bowl_state
    bowl_state = "fire"
    screen.blit(bowlImg, (x + 16, y + 10))

def isCollision(cX, cY, bX, bY):
    distance = math.sqrt((cX - bX)**2 + (cY - bY)**2)
    return distance < 40

def game_over_text():
    sad_Sound = mixer.Sound('ohh.mp3')
    sad_Sound.play()
    over_text = over_font.render("GAME OVER!", True, (30,144,255))
    screen.blit(over_text, (200, 200))
    play_again_font = pygame.font.Font('freesansbold.ttf', 40)
    play_again_text = play_again_font.render("Press ENTER to Play Again", True, (30,144,255))
    screen.blit(play_again_text, (120, 300))

def reset_game():
    global playerX, playerY, bowlX, bowlY, bowl_state, score_value, cotcanX, cotcanY, game_over
    playerX = 370
    playerY = 470
    bowlX = 0
    bowlY = 470
    bowl_state = "ready"
    score_value = 0
    for i in range(num_of_candy):
        cotcanX[i] = random.randint(0, 750)
        cotcanY[i] = random.randint(20, 160)
    game_over = False

# Return button setup
return_font = pygame.font.Font('freesansbold.ttf', 24)
return_text = return_font.render("Press ESC to Return to Main Menu", True, (255, 255, 255))

# Game Loop
running = True
while running:
    screen.blit(bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_LEFT:
                    playerX_change = -0.22
                if event.key == pygame.K_RIGHT:
                    playerX_change = 0.22
                if event.key == pygame.K_SPACE and bowl_state == "ready":
                    bowl_Sound = mixer.Sound('pew.mp3')
                    bowl_Sound.play()
                    bowlX = playerX
                    fire_bowl(bowlX, bowlY)
            else:
                if event.key == pygame.K_RETURN:
                    reset_game()
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                import subprocess
                subprocess.Popen(["python", "main_page.py"])
                sys.exit()
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                playerX_change = 0

    if not game_over:
        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        for i in range(num_of_candy):
            if cotcanY[i] > 440:
                for j in range(num_of_candy):
                    cotcanY[j] = 2000
                game_over = True
                break

            cotcanX[i] += cotcanX_change[i]
            if cotcanX[i] <= 0:
                cotcanX_change[i] = 0.20
                cotcanY[i] += cotcanY_change[i]
            elif cotcanX[i] >= 736:
                cotcanX_change[i] = -0.20
                cotcanY[i] += cotcanY_change[i]

            if isCollision(cotcanX[i], cotcanY[i], bowlX, bowlY):
                touch_Sound = mixer.Sound('yum.mp3')
                touch_Sound.play()
                bowlY = 470
                bowl_state = "ready"
                score_value += 1
                cotcanX[i] = random.randint(0, 750)
                cotcanY[i] = random.randint(20, 160)

            cotcan(cotcanX[i], cotcanY[i], i)

        if bowlY <= 0:
            bowlY = 470
            bowl_state = "ready"
        if bowl_state == "fire":
            fire_bowl(bowlX, bowlY)
            bowlY -= bowlY_change

        player(playerX, playerY)
        show_score(10, 10)
    else:
        game_over_text()

    screen.blit(return_text, (200, 550))
    pygame.display.update()
