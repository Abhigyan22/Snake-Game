"""The very famous Snake game built using Python
"""
import pygame
from random import randint
from math import sqrt, pow

def display_player(snk_list: list, snk_size: int):
    """[DRAWS THE SNAKE]

    Args:
        snk_list (list): [description]
        snk_size (int): [description]
    """
    for x, y in snk_list:
        pygame.draw.rect(WINDOW, (0,0,0), (x, y, player_size, player_size))
    pygame.draw.rect(WINDOW, (255,0,0), (playerX, playerY, player_size, player_size))
    """If you did not understand the snake increase logic, please read the
    snake increase logic.txt..."""
def check_boundary():
    """[Checks if player hit the boundary]

    Returns:
        [bool]: [True if player hit boundary else False]
    """
    global playerY, playerX
    if playerX<=0:
        playerX = 0
        return True
    elif playerY<=0:
        playerY = 0
        return True
    if playerX>=768:
        playerX = 768
        return True
    elif playerY>=568:
        playerY = 568
        return True
    return False

def lose_message(scr:int):
    """[PRINTS THE LOSE MESSAGE]

    Args:
        scr (means score) -(int): [Prints the score (After player loses)]
    """

    msg = pygame.font.Font("BAARS___.TTF", 100)
    msg = msg.render(f"YOUR SCORE: {scr}", True, (0,0, 0))
    WINDOW.blit(msg, (90, 230))

def print_score(score):
    """[Prints the score in game]

    Args:
        score ([int]): [Player score]
    """
    msg = pygame.font.Font("BAARS___.TTF", 70)
    msg = msg.render(f"{score}", True, (0,0,0,100))
    WINDOW.blit(msg, (30, 30))

def display_food(x:int, y:int):
    """[Display the food in its position ]

    Args:
        x (int): [Position of food in X axis]
        y (int): [Position of food in Y axis]
    """

    pygame.draw.rect(WINDOW, (255,255,0), (x,y,36,36))

def food_eaten():
    """[Checks if food has been eaten]

    Returns:
        [Bool]: [Returns True if food eaten else False]
    """
    if sqrt(pow(playerX - foodX, 2) + pow(playerY-foodY, 2))<20:
        #The above is a math equation to find the distance between two coordinates
        #Link to study more about the equation - https://rb.gy/xe9zjt
        return True
    return False

def check_hit(snk_list):
    """[SEE IF SNAKE HIT ITS OWN BODY]

    Args:
        snk_list ([list]): [The snake_list]

    Returns:
        [bool]: [True if hit its own body else false]
    """
    #below math equation same as food_eaten() func.
    for x,y in snk_list[:-6]:
        if sqrt(pow(playerX-x, 2)+pow(playerY-y, 2))<25.9:
            return True
    return False
    """Why i gave index of -6 in for loop? because the snk_list[-1] is the
    head of the snake (the red square) and [-2] to [-6] are the tail but they are
    actually so close to the snake(they are inside the head almost) so if i try
    without the index of [:-6], it is gonna show i lose the first time i eat...
    Again, because they are so close to the head and the distance between them is less
    than 25"""

#Below are the basic configurations of the game
pygame.init()

WINDOW = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Snake Game")

ICON = pygame.image.load("SnakeIcon.png")
pygame.display.set_icon(ICON)

BACKGROUND = pygame.image.load("SnakeBackground.png")

pygame.mixer.music.load("BackgroundMusic.wav")
pygame.mixer.music.play(-1)

#Below are the variables used in the game
want_to_play = True

playerX = 364 #position of player in X axis
playerY = 264 #position of player in Y axis

lose = False

foodX = randint(5, 735) #position of food in X axis
foodY = randint(5, 535) #position of food in Y axis

player_size = 36 #Size of the player
score = 0

velocityX = 0
velocityY = 0
set_velocity = 7
snake_list = []
snake_size = 1

#The main loop of the game -
while want_to_play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            want_to_play = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                velocityX = -set_velocity
                velocityY = 0
            elif event.key == pygame.K_RIGHT:
                velocityX = set_velocity
                velocityY = 0
            elif event.key == pygame.K_UP:
                velocityY = -set_velocity
                velocityX = 0
            elif event.key == pygame.K_DOWN:
                velocityY = set_velocity
                velocityX = 0
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                velocityX = -set_velocity
                velocityY = 0
            elif event.key == pygame.K_RIGHT:
                velocityX = set_velocity
                velocityY = 0
            elif event.key == pygame.K_UP:
                velocityY = -set_velocity
                velocityX = 0
            elif event.key == pygame.K_DOWN:
                velocityY = set_velocity
                velocityX = 0
    WINDOW.blit(BACKGROUND, (0, 0))
    print_score(score)
    display_player(snake_list, player_size)
    display_food(foodX, foodY)
    playerX += velocityX
    playerY += velocityY
    head = []
    head.append(playerX) #Appending the current X position of snake to head
    head.append(playerY) #Appending the current Y position of snake to head
    snake_list.append(head) #Appedning the current position of snake to snake_lis

    if len(snake_list)>snake_size:
        del snake_list[0] #deletes the old position of snake if the length of
                          #snake_list increases the snake_list
    if food_eaten():
        Food_sound = pygame.mixer.Sound("FoodEaten.wav")
        Food_sound.play()
        snake_size += 10
        score+=1
        foodX = randint(5, 735)
        foodY = randint(5, 535)

    if check_boundary() or check_hit(snake_list):
        lose = True
        want_to_play = False

    pygame.display.update()

while lose:
    WINDOW.blit(BACKGROUND, (0, 0))
    lose_message(score)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lose = False
    pygame.display.update()
