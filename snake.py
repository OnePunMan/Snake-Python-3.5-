# Author: Jackie Xu
# Date: 11/14/2016
# Purpose: First game using pygame in Python (snake)

import pygame
import random
import math
import time

#S = Skeleton code/requirements
#E = Examples

#S This initializes the module
pygame.init()

# colours: RGB
white = (255, 255, 255)
black = (0, 0, 0)
cyan = (20, 220, 220)
red = (255, 0, 0)
green = (0, 155, 0)
blue = (0, 0, 255)

WIDTH = 800
HEIGHT  = 600

# sound effects
point_sound = pygame.mixer.Sound("pick_up.wav")
crash_sound = pygame.mixer.Sound("crash.wav")
pygame.mixer.music.load("bg.wav")

#S Surface (Display of the game)
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake')

# Sprites
img = pygame.image.load('Head.png')


# Same functions pretty much
# flip: flipbook analogy - updates entire surface
#S update: only updates certain parts, unless parameters empty
#E pygame.display.flip()
#E pygame.display.update()

# Variables
block_size = 20
snakeSpeed = 20
FPS = 15
score = 0

direction = "right"

# game fonts
font = pygame.font.SysFont(None, 25)

# FPS control object
clock = pygame.time.Clock()

# Functions
def snake(block_size, snakelist):

    # Rotations
    if direction == "right":
        head = pygame.transform.rotate (img, 270)
    elif direction == "left":
        head = pygame.transform.rotate (img, 90)
    elif direction == "up":
        head = img
    elif direction == "down":
        head = pygame.transform.rotate (img, 180)
        
    
    gameDisplay.blit(head, (snakelist[-1][0], snakelist[-1][1]))
    for XnY in snakelist[:-1]:
        pygame.draw.rect(gameDisplay, green, [XnY[0], XnY[1], block_size, block_size])

def text_objects(text, colour):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()
    
def msg_to_screen (msg, colour, posX, posY):
    textSurf, textRect = text_objects(msg, colour)

    textRect.center = posX, posY
    gameDisplay.blit (textSurf, textRect)
    
   # screen_text = font.render(msg, True, colour)

    # placing font
    # gameDisplay.blit(screen_text, [math.floor(WIDTH / 2), math.floor(HEIGHT / 2)])

#S Gameloop/mainloop
def gameLoop():
    global direction
    global score
    gameExit = False
    gameOver = False
    pause = False

    lead_x = math.floor(WIDTH / 2)
    lead_y = math.floor(HEIGHT / 2)
    
    lead_dx = 0
    lead_dy = 0

    snakeList = []
    snakeLength = 1

    randAppleX = block_size * random.randrange(0, math.ceil((WIDTH/block_size)))
    randAppleY = block_size * random.randrange(0, math.ceil((HEIGHT/block_size)))

    pygame.mixer.music.play(-1)
    while not gameExit:

        while gameOver:
            gameDisplay.fill(white)
            msg_to_screen("Game over, press C to play again or Q to quit.", red, WIDTH / 2, HEIGHT / 2)
            msg_to_screen("Your score is: " + str(score), blue, WIDTH / 2, HEIGHT / 2 + 40)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        score = 0
                        gameLoop()

        #S Event handling
        for event in pygame.event.get():            
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                pygame.mixer.music.unpause()
                if event.key == pygame.K_LEFT:
                    if lead_dx <= 0 :
                        lead_dx = -snakeSpeed
                        lead_dy = 0
                        direction = "left"
                elif event.key == pygame.K_RIGHT:
                    if lead_dx >= 0 :
                        lead_dx = snakeSpeed
                        lead_dy = 0
                        direction = "right"
                elif event.key == pygame.K_UP:
                    if lead_dy <= 0 :
                        lead_dy = -snakeSpeed
                        lead_dx = 0
                        direction = "up"
                elif event.key == pygame.K_DOWN:
                    if lead_dy >= 0 :    
                        lead_dy = snakeSpeed
                        lead_dx = 0
                        direction = "down"
                elif event.key == pygame.K_SPACE:
                    pause = not pause
                    pygame.mixer.music.pause()
                    msg_to_screen("Paused, press 'Space' to continue" , black, WIDTH / 2, HEIGHT / 2 + 40)

        # Dead            
        if lead_x >= WIDTH or lead_x < 0 or lead_y >= HEIGHT or lead_y < 0:
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(crash_sound)
            gameOver = True

        if not pause:
            lead_x = lead_x + lead_dx
            lead_y = lead_y + lead_dy
        
            #E    print(event)
            gameDisplay.fill(cyan)
            #E pygame.draw.rect(where, colour, [x , y, w, h])

            appleSize = 20
            pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, appleSize, appleSize])
            
            snakeHead = []
            snakeHead.append(lead_x)
            snakeHead.append(lead_y)
            snakeList.append(snakeHead)

            if len(snakeList) > snakeLength:
                del snakeList [0]
            snake(block_size, snakeList)

            for eachSeg in snakeList[:-1]:
                if eachSeg == snakeHead:
                    pygame.mixer.music.stop()
                    pygame.mixer.Sound.play(crash_sound)
                    gameOver = True
        
            #E [Draw using fill] gameDisplay.fill(colour, shape = [x, y, w, h]) (faster)
            #E gameDisplay.fill(red, rect = [200, 200, 50, 50])
            
            

            # Full Object collision (eat apple)
            if lead_x >= randAppleX and lead_x < randAppleX + appleSize or lead_x + block_size > randAppleX and lead_x + block_size <= randAppleX + appleSize:
                if lead_y >= randAppleY and lead_y < randAppleY + appleSize or lead_y + block_size > randAppleY and lead_y + block_size <= randAppleY + appleSize:                  
                    pygame.mixer.Sound.play(point_sound)
                    score = score + 1
                    print ("Score: ", score)
                    randAppleX = block_size * random.randrange(0, math.ceil((WIDTH/block_size)))
                    randAppleY = block_size * random.randrange(0, math.ceil((HEIGHT/block_size)))
                    snakeLength = snakeLength + 1

                
            #S FPS control
        pygame.display.update()
        clock.tick(FPS)
        
    #S Exiting/uninitialize

    pygame.quit()
    #quit()

gameLoop()
