import pygame
import math
import random
from pygame import mixer

#initialization 
pygame.init()

#screen width and height
screen = pygame.display.set_mode((800, 600))

#background
bg = pygame.image.load('bg.jpg')

# bg sound 
mixer.music.load('cupid.mp3')
mixer.music.play(-1) #the music will be played continuously on loop

#window's name
pygame.display.set_caption("TinyTails Game")

#-----------------PLAYER-----------------------
#playerimg and x and y
playerImg = pygame.image.load('deer.png')
playerX = 370
playerY = 470
playerX_change = 0
playerY_change = 0

#bowl image + positioning
bowlImg = pygame.image.load('bowl.png')
bowlX = 0
bowlY = 470
bowlX_change = 0
bowlY_change = 0.5
#ready = can't see the bullet moving and 
#fire = the bullet is currently moving
bowl_state = "ready"

#SCORE & FONT
score_value = 0
font = pygame.font.Font('freesansbold.ttf' , 30)
textX = 10
textY = 10

# GAME OVER
over_font = pygame.font.Font('freesansbold.ttf' , 64)

def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    sad_Sound = mixer.Sound('ohh.mp3')
    sad_Sound.play()
    over_text = over_font.render("GAME OVER!", True, (30,144,255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))

#creating list and using for loop
cotcanImg = []
cotcanX = []
cotcanY = []
cotcanX_change = []
cotcanY_change = []
num_of_candy = 6

for i in range(num_of_candy):
    #-----------------COTTON CANDY IMAGE 1------------------
    cotcanImg.append(pygame.image.load('cotcan2.png'))
    #position
    cotcanX.append(random.randint(0 , 750))
    cotcanY.append(random.randint(20, 160))
    cotcanX_change.append(0.2)
    cotcanY_change.append(50)

def cotcan(x, y, i):
    screen.blit(cotcanImg[i], (x, y))

def fire_bowl(x,y):
    global bowl_state
    bowl_state = "fire"
    screen.blit(bowlImg, (x + 16, y + 10))

#defining collision
def isCollision(cotcanX, cotcanY, bowlX, bowlY):
    distance = math.sqrt((math.pow(cotcanX - bowlX, 2)) + (math.pow(cotcanY - bowlY, 2)))
    if distance < 40: 
        return True
    else:
        return False

#caption and icon
icon = pygame.image.load('paw.png')
pygame.display.set_icon(icon)

#game loop
running = True
while running: 

    screen.fill((200, 255, 255))
    #bg image
    screen.blit(bg, (0,0))
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # keystrokes - right left down up
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.22
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.22
            if event.key == pygame.K_SPACE:
                if bowl_state is "ready":
                    bowl_Sound = mixer.Sound('pew.mp3')
                    bowl_Sound.play()
                    #get the current x'x coordinate of the player
                    bowlX = playerX #stores the player's x coordinate in bowlX 
                    fire_bowl(bowlX, bowlY) # and then fires it, this prevents our bowl from moving along with our player
           
            if event.key == pygame.K_UP:
                playerY_change = -0.22
            if event.key == pygame.K_DOWN:
                playerY_change = 0.22
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0
        


#checking for boundaries
    playerX += playerX_change
    if playerX <= 0: 
        playerX = 0 
    elif playerX >= 736: #800-64
        playerX = 736

    for i in range(num_of_candy):

        #game over
        if cotcanY[i] > 440: 
            for j in range(num_of_candy):
                cotcanY[j] = 2000
            game_over_text()
            break

        cotcanX[i] += cotcanX_change[i]
        if cotcanX[i] <= 0: 
            cotcanX_change[i] = 0.25
            cotcanY[i] += cotcanY_change[i]
        elif cotcanX[i] >= 736: #800-64
            cotcanX_change[i] = -0.25
            cotcanY[i] += cotcanY_change[i]

        #collision
        collision = isCollision(cotcanX[i], cotcanY[i], bowlX, bowlY)
        if collision:
            touch_Sound = mixer.Sound('yum.mp3')
            touch_Sound.play()
            bowlY = 470
            bowl_state = "ready"
            score_value += 1
            cotcanX[i] = random.randint(0 , 750)
            cotcanY[i] = random.randint(20, 160)

        cotcan(cotcanX[i], cotcanY[i], i)    


    #bullet Movement
    if bowlY <= 0:
        bowlY = 470
        bowl_state = "ready"

    if bowl_state is "fire":
        fire_bowl(bowlX, bowlY)
        bowlY -= bowlY_change

    player(playerX, playerY)
    show_score(textX, textY)
    # cotcan2(cotcan2X,cotcan2Y)
    pygame.display.update()