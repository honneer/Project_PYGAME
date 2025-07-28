#ERRORS SO FAR - image.load & diplay.set_mode
#pygame.event.get()
#screen.blit
#event.key (not type as we r letting uder press key and checking that) & forgot to add_change - playerX_change  
#didn't create the variable palerX_change


import pygame

#initialization 
pygame.init()

#screen width and height
screen = pygame.display.set_mode((800, 600))

#playerimg and x and y
playerImg = pygame.image.load('bear.png')
playerX = 370
playerY = 470
playerX_change = 0
playerY_change = 0

def player(x, y):
    screen.blit(playerImg, (x, y))

#caption and icon
icon = pygame.image.load('paw.png')
pygame.display.set_icon(icon)

#game loop
running = True
while running: 

    screen.fill((200, 255, 255))
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3 
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_UP:
                playerY_change = -0.3
            if event.key == pygame.K_DOWN:
                playerY_change = 0.3
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    playerX += playerX_change
    playerY += playerY_change

    player(playerX, playerY)
    pygame.display.update()