"""The very famous Snake game built using Python
"""
#Importing all the necessary dependencies
from random import randint
from math import sqrt, pow
from buttons import Button
from sys import exit
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
    """A class for the Player (i.e. the snake)
    """
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
def change_player_position(event, player, set_velocity):
    """[Change the position of the player based on the key pressed]

    Args:
        event (event): It is the event log.. (event means everything which happens in a game,
        from key press to mouse , etc.)
        player (Player): The object (The main player.. i.e The Snake)
        set_velocity (int): velocity of the player
    """
    if event.type == pygame.KEYDOWN: #If we pressed down any key
        if event.key == pygame.K_LEFT: #If key pressed is left, its all the same for the rest
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

def is_over_play_button(pos, x, y, width, height):
    #Pos is the mouse position or a tuple of (x,y) coordinates
    if pos[0] > x and pos[0] < x + width:
        if pos[1] > y and pos[1] < y + height:
            return True

    return False

def button_maker(Food_sound,*args):
    """Makes buttons in the menus

    Returns:
        bool: True if we press any key, else False
    """
    sound_playing = True
    while True:
        WINDOW.blit(BACKGROUND, (0,0))
        if sound_playing:
            WINDOW.blit(PLAY_BUTTON, (720, 520))
        else:
            WINDOW.blit(PAUSE_BUTTON, (720,520))
        args[0].draw(WINDOW, (0,0,0))
        args[1].draw(WINDOW, (0,0,0))
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEMOTION:
                if args[0].isOver(pos):
                    args[0].color = (0,255,255)
                elif args[1].isOver(pos):
                    args[1].color = (0,255,255)
                else:
                    args[0].color = (220,220,220)
                    args[1].color = (220,220,220)


            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if args[0].isOver(pos):
                    args[0].color = (0,128,255)
                elif args[1].isOver(pos):
                    args[1].color = (0,128,255)
            if event.type == pygame.MOUSEBUTTONUP:
                if args[0].isOver(pos):
                    return True
                elif args[1].isOver(pos):
                    exit()

                if is_over_play_button(pos, 720,520,64,64):
                    if sound_playing:
                        sound_playing = False
                        pygame.mixer.music.pause()
                        Food_sound.set_volume(0.0)
                    else:
                        sound_playing = True
                        pygame.mixer.music.unpause()
            if event.type == pygame.QUIT:
                exit()
        pygame.display.update()
def player_chose_play(Food_Sound):
    """The Start menu

    Returns:
        bool: True if hit Play
    """
    start = Button((220,220,220), 300, 100+50, 200, 70, "START")
    end = Button((220,220,220), 300, 300+50,200,70,"END")
    if button_maker(Food_Sound,start, end):
        return True

def game():
    WINDOW.blit(BACKGROUND, (0,0))
    player = Player()
    lose = False
    set_velocity = 8
    score = 0
    foodX = randint(5,735)
    foodY = randint(5, 535)


    while True:
        if player_chose_play(Food_sound):
            want_to_play = True
            break

    while want_to_play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                want_to_play = False

            change_player_position(event, player, set_velocity)

        WINDOW.blit(BACKGROUND, (0, 0))
        print_score(score)
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
            Food_sound.play()
            player.snake_size += 10
            score+=1

            foodX = randint(5,735)
            foodY = randint(5,535)
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game()
        pygame.display.update()
        clock.tick(35) #This will set the max fps of the game to 35

#Below are the basic configurations of the game
pygame.init()

WINDOW = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Snake Game")

ICON = pygame.image.load("SnakeIcon.png")
pygame.display.set_icon(ICON)

BACKGROUND = pygame.image.load("SnakeBackground.png")

pygame.mixer.music.load("BackgroundMusic.wav")
pygame.mixer.music.play(-1)

PLAY_BUTTON = pygame.image.load("play.png")
PAUSE_BUTTON = pygame.image.load("pause.png")

Food_sound = pygame.mixer.Sound("FoodEaten.wav")

clock = pygame.time.Clock()
game()
