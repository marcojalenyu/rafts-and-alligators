"""
    A simple game of Snakes and Ladders using Pygame
"""

# Importing the required libraries
import pygame
from pygame import mixer
import random
import time
import sys

# Initialize Pygame
pygame.init()

# Set the screen size
screen = pygame.display.set_mode((800, 600))
# Set the title and icon
pygame.display.set_caption("Rafts and Alligators")
icon = pygame.image.load('assets/img/icon.png')
pygame.display.set_icon(icon)

# Background (Credits to tahbikat: https://www.deviantart.com/tahbikat/art/Swamp-Background-440292485)
background = pygame.image.load('assets/img/background.png')

"""
Drawing the images
"""
player1Img = pygame.image.load('assets/img/player1.png')
player2Img = pygame.image.load('assets/img/player2.png')
boardImg = pygame.image.load('assets/img/board.png')
diceImgs = [pygame.image.load(f'assets/img/dices/dice{i}.png') for i in range(1, 7)]
fruitImg = pygame.image.load('assets/img/fruit.png')
exitImg = pygame.image.load('assets/img/exit.png')

"""
Player
"""
class Player:
    def __init__(self, number):
        self.number = number
        self.position = 0

    def draw(self, board):
        if self.number == 1:
            playerImg = player1Img
        else:
            playerImg = player2Img
        if self.position <= 99:
            # Face right if the player is on an even row
            if self.position // 10 % 2 == 0:
                screen.blit(playerImg, (board.tiles[self.position].x+7.5, board.tiles[self.position].y+7.5))
            # Otherwise, face left and should start from the right
            else:
                screen.blit(pygame.transform.flip(playerImg, True, False), (730-board.tiles[self.position].x, board.tiles[self.position].y+7.5))

    def move(self, steps, board, player2):
        # Move the player (with animation)
        for _ in range(steps):
            footstep_sound = mixer.Sound('assets/audio/footstep.mp3')
            footstep_sound.play()
            self.position += 1
            if self.position > board.end:
                self.position = 80
            board.draw()
            self.draw(board)
            player2.draw(board)
            pygame.display.flip()
            time.sleep(0.5)

        # Check if the player is on a raft
        if board.tiles[self.position].raft:
            raft_sound = mixer.Sound('assets/audio/raft.mp3')
            raft_sound.play()
            self.position = board.tiles[self.position].raft
        elif board.tiles[self.position].alligator:
            alligator_sound = mixer.Sound('assets/audio/alligator.mp3')
            alligator_sound.play()
            self.position = board.tiles[self.position].alligator

"""
Tile
"""
class Tile:
    def __init__(self, x, y, raft = None, alligator = None):
        self.x = x
        self.y = y
        self.raft = raft
        self.alligator = alligator

"""
Board
"""
class Board:
    def __init__(self):
        self.tiles = []
        self.create_tiles()
        self.set_rafts_and_alligators()
        self.end = 99

    def create_tiles(self):
        # Create the tiles
        for i in range(100):
            x = 60 * (i % 10) + 100
            y = 540 - 60 * (i // 10)
            self.tiles.append(Tile(x, y))
    
    # Manual setting of rafts and alligators
    def set_rafts_and_alligators(self):
        # Set the rafts
        self.tiles[3].raft = 14
        self.tiles[8].raft = 30
        self.tiles[19].raft = 37
        self.tiles[27].raft = 83
        self.tiles[39].raft = 58
        self.tiles[62].raft = 80
        self.tiles[70].raft = 90
        # Set the alligators
        self.tiles[16].alligator = 6
        self.tiles[53].alligator = 33
        self.tiles[61].alligator = 17
        self.tiles[63].alligator = 59
        self.tiles[86].alligator = 23
        self.tiles[92].alligator = 72
        self.tiles[94].alligator = 74
        self.tiles[98].alligator = 77

    def draw(self):
        screen.blit(boardImg, (100, 2.5))
        screen.blit(fruitImg, (108, 10))

"""
Dice
"""
class Dice:
    def __init__(self):
        self.x = 718
        self.y = 500
        self.face = 1

    def roll(self):
        self.face = random.randint(1, 6)
    
    def draw(self):
        screen.blit(diceImgs[self.face - 1], (self.x, self.y))

"""
Game Loop
"""
def display_score(player, player2):
    font = pygame.font.Font('freesansbold.ttf', 16)
    text = font.render(f"You: {player.position+1}", True, (255, 255, 255))
    screen.blit(text, (10, 10))
    text = font.render(f"Opp: {player2.position+1}", True, (255, 255, 255))
    screen.blit(text, (10, 30))

def checkWinner(player1, player2):
    if player1.position == 99:
        gameover(player1.number)
    elif player2.position == 99:
        gameover(player2.number)

def gameover(player):
    font = pygame.font.Font('freesansbold.ttf', 64)
    subfont = pygame.font.Font('freesansbold.ttf', 32)
    screen.blit(background, (0, 0))
    # Create the text
    main_text = font.render("Game Over", True, (255, 255, 255))
    sub_text = subfont.render(f"Player {player} won", True, (255, 255, 255))
    # Center the text
    text_rect = main_text.get_rect(center=(400, 250))
    screen.blit(main_text, text_rect)
    text_rect = sub_text.get_rect(center=(400, 350))
    screen.blit(sub_text, text_rect)
    screen.blit(exitImg, (18, 500))
    pygame.display.update()
    # Play winning sound
    trumpet_sound = mixer.Sound('assets/audio/trumpet.mp3')
    trumpet_sound.play()
    # Play winning sound
    mixer.music.load('assets/audio/win.mp3')
    mixer.music.play(-1)
    # Press any key to exit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 18 <= x <= 82 and 500 <= y <= 564:
                    mainmenu()

def game():
    player1 = Player(1)
    player2 = Player(2)
    board = Board()
    dice = Dice()
    running = True
    rolling = False
    while running:
        screen.fill((255, 255, 255))
        screen.blit(background, (0, 0))
        screen.blit(exitImg, (18, 500))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 18 <= x <= 82 and 500 <= y <= 564:
                    mainmenu()
                elif 718 <= x <= 782 and 500 <= y <= 564 and not rolling:
                    rolling = True

        if rolling:
            # Player 1
            dice_sound = mixer.Sound('assets/audio/dice_roll.mp3')
            dice_sound.play()
            display_score(player1, player2)
            for _ in range(10):
                dice.roll()
                dice.draw()
                board.draw()
                player1.draw(board)
                player2.draw(board)
                pygame.display.flip()
                time.sleep(0.1)

            player1.move(dice.face, board, player2)
            checkWinner(player1, player2)
            time.sleep(0.1)

            # Player 2
            dice_sound.play()
            for _ in range(10):
                dice.roll()
                dice.draw()
                board.draw()
                player1.draw(board)
                player2.draw(board)
                pygame.display.flip()
                time.sleep(0.1)

            player2.move(dice.face, board, player1)
            checkWinner(player1, player2)
            rolling = False      

        dice.draw()
        board.draw()
        player1.draw(board)
        player2.draw(board)
        display_score(player1, player2)

        pygame.display.update()

def mainmenu():
    # Background Music
    mixer.music.load('assets/audio/background.mp3')
    mixer.music.play(-1)
    font = pygame.font.Font('freesansbold.ttf', 64)
    screen.blit(background, (0, 0))
    # Create the text
    main_text = font.render("Rafts and Alligators", True, (255, 255, 255))
    # Center the text
    text_rect = main_text.get_rect(center=(400, 200))
    screen.blit(main_text, text_rect)
    # Buttons for Start and Exit
    pygame.draw.rect(screen, (255, 255, 255), (300, 350, 200, 50), 2)
    pygame.draw.rect(screen, (255, 255, 255), (300, 450, 200, 50), 2)
    # Create the text for the buttons
    font = pygame.font.Font('freesansbold.ttf', 32)
    start_text = font.render("Start", True, (255, 255, 255))
    exit_text = font.render("Exit", True, (255, 255, 255))
    # Center the text
    text_rect = start_text.get_rect(center=(400, 375))
    screen.blit(start_text, text_rect)
    text_rect = exit_text.get_rect(center=(400, 475))
    screen.blit(exit_text, text_rect)
    pygame.display.update()
    # Add credits
    font = pygame.font.Font('freesansbold.ttf', 12)
    developer_text = font.render("Developed by Maracoo", True, (255, 255, 255))
    screen.blit(developer_text, (10, 560))
    credit_text = font.render("Art and music belong to their respective owners.", True, (255, 255, 255))
    screen.blit(credit_text, (10, 580))
    # Press any key to start
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 300 <= x <= 500 and 350 <= y <= 400:
                    game()
                if 300 <= x <= 500 and 450 <= y <= 500:
                    sys.exit()
        
            # Check for hover effect
            mouse_pos = pygame.mouse.get_pos()
            if 300 <= mouse_pos[0] <= 500 and 350 <= mouse_pos[1] <= 400:
                pygame.draw.rect(screen, (200, 200, 200), (300, 350, 200, 50), 2)
            elif 300 <= mouse_pos[0] <= 500 and 450 <= mouse_pos[1] <= 500:
                pygame.draw.rect(screen, (200, 200, 200), (300, 450, 200, 50), 2)
            else:
                pygame.draw.rect(screen, (255, 255, 255), (300, 350, 200, 50), 2)
                pygame.draw.rect(screen, (255, 255, 255), (300, 450, 200, 50), 2)
        
        pygame.display.update()

# Start the game
mainmenu()