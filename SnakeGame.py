"""The very famous Snake game built using Python
"""
from random import randint
from math import sqrt, pow
import pygame

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

def food_eaten(player, foodX, foodY):
    """[Checks if food has been eaten]

    Returns:
        [Bool]: [Returns True if food eaten else False]
    """
    if sqrt(pow(player.X - foodX, 2) + pow(player.Y-foodY, 2))<20:
        #The above is a math equation to find the distance between two coordinates
        #Link to study more about the equation - https://rb.gy/xe9zjt
        return True
    return False

class Player():
    def __init__(self):
        self.X = 364
        self.Y = 264
        self.size = 36
        self.velocityX = 0
        self.velocityY = 0
        self.snake_list = []
        self.snake_size = 1
        self.player_size = 36
    def display_player(self):
        """[DRAWS THE SNAKE]

        Args:
            snk_list (list): [description]
            snk_size (int): [description]
        """
        for x, y in self.snake_list:
            pygame.draw.rect(WINDOW, (0,0,0), (x, y, self.player_size, self.player_size))
        pygame.draw.rect(WINDOW, (255,0,0), (self.X, self.Y, self.player_size, self.player_size))
        """If you did not understand the snake increase logic, please read the
        snake increase logic.txt..."""

    def check_boundary(self):
        """[Checks if player hit the boundary]

        Returns:
            [bool]: [True if player hit boundary else False]
        """
        if self.X<=0:
            self.X = 0
            return True
        elif self.Y<=0:
            self.Y = 0
            return True
        if self.X>=768:
            self.X = 768
            return True
        elif self.Y>=568:
            self.Y = 568
            return True
        return False

    def check_hit(self):
        """[SEE IF SNAKE HIT ITS OWN BODY]

        Returns:
            [bool]: [True if hit its own body else false]
        """
        #below math equation same as food_eaten() func.
        for x,y in self.snake_list[:-6]:
            if sqrt(pow(self.X-x, 2)+pow(self.Y-y, 2))<25.9:
                return True
        return False
        """Why i gave index of -6 in for loop? because the snk_list[-1] is the
        head of the snake (the red square) and [-2] to [-6] are the tail but they are
        actually so close to the snake(they are inside the head almost) so if i try
        without the index of [:-6], it is gonna show i lose the first time i eat...
        Again, because they are so close to the head and the distance between them is less
        than 25"""
def change_player_position(player, set_velocity):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            want_to_play = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.velocityX = -set_velocity
                player.velocityY = 0
            elif event.key == pygame.K_RIGHT:
                player.velocityX = set_velocity
                player.velocityY = 0
            elif event.key == pygame.K_UP:
                player.velocityY = -set_velocity
                player.velocityX = 0
            elif event.key == pygame.K_DOWN:
                player.velocityY = set_velocity
                player.velocityX = 0
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.velocityX = -set_velocity
                player.velocityY = 0
            elif event.key == pygame.K_RIGHT:
                player.velocityX = set_velocity
                player.velocityY = 0
            elif event.key == pygame.K_UP:
                player.velocityY = -set_velocity
                player.velocityX = 0
            elif event.key == pygame.K_DOWN:
                player.velocityY = set_velocity
                player.velocityX = 0

def game():

    want_to_play = True
    lose = False
    set_velocity = 7
    score = 0
    foodX = randint(5,735)
    foodY = randint(5, 535)

    while want_to_play:
        change_player_position(player, set_velocity)
        WINDOW.blit(BACKGROUND, (0, 0))
        print_score(score)
        # display_player(snake_list, player_size)
        player.display_player()
        display_food(foodX, foodY)
        player.X += player.velocityX
        player.Y += player.velocityY
        head = []
        head.append(player.X) #Appending the current X position of snake to head
        head.append(player.Y) #Appending the current Y position of snake to head
        player.snake_list.append(head) #Appedning the current position of snake to snake_lis

        if len(player.snake_list)>player.snake_size:
            del player.snake_list[0] #deletes the old position of snake if the length of
                            #snake_list increases the snake_list
        if food_eaten(player, foodX, foodY):
            Food_sound = pygame.mixer.Sound("FoodEaten.wav")
            Food_sound.play()
            player.snake_size += 10
            score+=1
            foodX = randint(5, 735)
            foodY = randint(5, 535)

        if player.check_boundary() or player.check_hit():
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

player = Player()

#Below are the basic configurations of the game
pygame.init()

WINDOW = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Snake Game")

ICON = pygame.image.load("SnakeIcon.png")
pygame.display.set_icon(ICON)

BACKGROUND = pygame.image.load("SnakeBackground.png")

pygame.mixer.music.load("BackgroundMusic.wav")
pygame.mixer.music.play(-1)


game()