import pygame
from PIL import Image

#initialize pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((1250,715)) #width & height

#title and icon
pygame.display.set_caption('TinyTails: Raise , Pet, Love')
icon = pygame.image.load('paw.png')
pygame.display.set_icon(icon)

#player
playerIMG = pygame.image.load('chop.png')
#position
playerX = 350
playerY = 350
playerX_change = 0
playerY_change = 0

#function
def player(x,y):
    screen.blit(playerIMG, (x, y))
    

#game loop 
running = True
while running:
    #screen color
    screen.fill((0,255,255))
  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
             
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.9
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.9
            if event.key == pygame.K_UP:
                playerY_change = -0.9
            if event.key == pygame.K_DOWN:
                playerY_change = 0.9

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0
        

    playerX += playerX_change
    if playerX <= -170:
        playerX = -170
    elif playerX >= 825:
        playerX = 825
    playerY += playerY_change
    if playerY <= -70:
        playerY = -70
    elif playerY >= 386:
        playerY = 386

    player(playerX, playerY) #calling function
     #and updating
    pygame.display.update()