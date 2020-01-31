import os
from random import randrange as rand
from collections import deque
from typing import *
import pygame
import sys

# -*- coding: utf-8 -*-
#
# Control keys:
# Down - Drop stone faster
# Left/Right - Move stone
# Up - Rotate Stone clockwise
# Escape - Quit game
# P - Pause game
#
# Have fun!

# Copyright (c) 2020 "Anatolii Trofimov & Bogban Popovich" <a3.trofimov@gmail.com popovbogdan21@yandex.ru>
#
# Permission is hereby granted, free of charge, to any person.


# The configuration
settings = {
    'cell_size': 26,
    'cols': 10,
    'rows': 24,
    'delay': 10,
    'maxfps': 6000,
    'score': 0
}

speed_levels = {
    10000: (75, 100),
    9000: (100, 100),
    8000: (125, 100),
    7000: (150, 100),
    6000: (200, 175),
    5000: (250, 175),
    4000: (350, 175),
    3000: (450, 175),
    2000: (550, 200),
    1000: (650, 225),
    500: (700, 250)
}
# Define the colors of the single shapes
colors = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 150, 0),
    (0, 0, 255),
    (255, 120, 0),
    (255, 255, 0),
    (180, 0, 255),
    (0, 220, 220)
]

# Define the shapes of the single parts
tetris_shapes = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3, 0],
     [0, 3, 3]],

    [[4, 0, 0],
     [4, 4, 4]],

    [[0, 0, 5],
     [5, 5, 5]],

    [[6, 6, 6, 6]],

    [[7, 7],
     [7, 7]]
]

# Initialization of pygame.
pygame.init()
# Creating gaming window 1000 * 725.

screen_size = width, height = (600, 674)
window = pygame.display.set_mode(screen_size)
# Creating window's title.
pygame.display.set_caption('TETRIS')
# icon of game.
icon = pygame.image.load('data/tetris1.jpg')
pygame.display.set_icon(icon)
FPS = 50
clock = pygame.time.Clock()
cycle = True
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()

gameover_sound = pygame.mixer.Sound('data/gameover.wav')
line_sound = pygame.mixer.Sound('data/line.wav')

def load_image(name, colorkey=None):
    # adding the folder name to the image name.
    fullname = os.path.join('data', name)
    # loading the picture.
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load:', name)
        raise SystemExit(message)
    image = image.convert()
    # If second parameter =-1: doing transparent.
    # color from point 0,0.
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def terminate():
    pygame.quit()
    quit()


def start_screen():
    # loading background.
    fon = load_image('tetris1.jpg')
    # loading music.
    pygame.mixer.music.load('data/zvuk-vstuplenija-v-tetrise-na-dendi.mp3')
    pygame.mixer.music.set_volume(0.3)  # 1 -100%  громкости звука.
    pygame.mixer.music.play(-1)  # играть бесконечно -1.

    # Creation the button 'Play'.
    play_button = Button(280, 70, window)
    # Creation the button 'Rules'.
    rules_button = Button(280, 70, window)
    # Creating the button 'Quit'.
    quit_btn = Button(280, 70, window)
    menu = True

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                check_play_button(play_button, mouse_x, mouse_y)
                check_rules_button(rules_button, mouse_x, mouse_y)
                check_quit_button(quit_btn, mouse_x, mouse_y)

        window.blit(fon, (0, 0))
        play_button.draw_button(160, 200, "Play")
        rules_button.draw_button(160, 300, "Rules")
        quit_btn.draw_button(160, 400, 'Quit')
        pygame.display.flip()
        clock.tick(FPS)


def check_play_button(button, mouse_x, mouse_y):
    """Launch a new game by pressing the button 'Play'."""
    if button.rect.collidepoint(mouse_x, mouse_y):
        pass
        start_game()


def check_rules_button(button, mouse_x, mouse_y):
    """displaying the screen with the game's rules."""
    if button.rect.collidepoint(mouse_x, mouse_y):
        rules_show()


def rules_show():
    """Screen with the game's rules."""
    intro_text = ["The aim: stay in the game as long as possible.", "",
                  "Collect so many points as possible.", "",
                  "The rate of appearance of 'tetramino' cubes increases", "",
                  "With each level.", "",
                  "Do all your best to fill the row.", "",
                  "You can turn the figures.", "",
                  "You can personally increase the speed of falling figures.", "",
                  "To pause the game press ESC."]

    fon = load_image('black.jpg')
    window.blit(fon, (0, 0))
    font = pygame.font.Font('data/PingPong.ttf', 21)
    text_coord = 20
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(165, 155, 168))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        window.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def check_quit_button(button, mouse_x, mouse_y):
    """Leave the game."""
    button_clicked = button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked:
        terminate()


def start_game() -> None:
    """
    Starting the game.
    :return: None
    """
    app = TetrisGame()
    app.run()
    # Adding the music - only mp3.



def print_text(x: int, y: int, msg: str, font_color: Tuple[int, int, int] = (0, 0, 0),
               font_type='data/PingPong.ttf', font_size: int = 50) -> None:
    """
    Output the text from the button.
    :param x:  coordinate of starting the message on х.
    :param y: coordinate of starting the message on у.
    :param msg:
    :param font_color: font color.
    :param font_type: font type.
    :param font_size: font size.
    :return:
    """
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(msg, True, font_color)
    window.blit(text, (x, y))


class Button:
    def __init__(self, w: int, h: int, screen) -> None:
        """
        Initialization of the buttons's attributes.
        :param w: buttons's width
        :param h: button's height
        :param screen: screen where it should be placed
        :return: None
        """
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Purpose of sizes and functions of the buttons.
        self.width, self.height = w, h
        self.button_color = (0, 219, 106)

        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        self.rect = None

    def draw_button(self, x: int, y: int, msg: str) -> None:
        """
        Displaying the buttons with the given text.
        :param x: coordinate x
        :param y: coordinate y
        :param msg: message to be shown on the button
        :return: None
        """
        self.rect = pygame.Rect(x, y, self.width, self.height)
        pygame.draw.rect(self.screen, self.button_color, self.rect)
        print_text(x + 90, y + 10, msg)


class Board:
    def __init__(self, w: int, h: int) -> None:
        """
        Initializing new board with diven number of cols(w) and rows(h).
        :param w: width (nuber of cols)
        :param h: height (number of rows)
        :return: None
        """
        self.width = w
        self.height = h
        self.board_ = None
        self.left = 0
        self.top = 0

    def new_board(self) -> List[List[int]]:
        """
        Creating empty board for the new game.
        :return: new empty board
        """
        self.board_ = [[0 for _ in range(settings['cols'])]
                       for _ in range(settings['rows'])] + \
                      [[1 for _ in range(settings['cols'])]]
        return self.board_

    def remove_row(self, row: int) -> None:
        """
        - Removing row which is full of blocks.
        - Adding empty row to the top of the board.
        :param row: row number
        :return: None
        """
        del self.board_[row]
        self.board_ = [[0 for _ in range(settings['cols'])]] + self.board_

    def draw_board(self) -> None:
        """
        Drawing tetris board.
        :return: None
        """
        for y, row in enumerate(self.board_):
            for x, val in enumerate(row):
                # going through every cell and paint it
                pygame.draw.rect(
                    window,
                    colors[val],  # colors of different shapes
                    pygame.Rect(
                        (x * (settings['cell_size'] + 2)) + 2,
                        (y * (settings['cell_size'] + 2)) + 2,
                        settings['cell_size'],
                        settings['cell_size']), 0)

    @staticmethod
    def draw_shape(shape: List[List[int]], offset: Tuple[int, int] = (0, 0)) -> None:
        """
        Drawing the falling stone on the board.
        :param shape: Current falling stone
        :param offset: x and y coordinates of the stone
        :return:
        """
        off_x, off_y = offset
        for y, row in enumerate(shape):
            for x, val in enumerate(row):
                # going through every cell and paint it
                if val:
                    pygame.draw.rect(
                        window,
                        colors[val],
                        pygame.Rect(
                            ((off_x + x) *
                             (settings['cell_size'] + 2)) + 2,
                            ((off_y + y) *
                             (settings['cell_size'] + 2)) + 2,
                            settings['cell_size'],
                            settings['cell_size']), 0)

    @staticmethod
    def join_matrixes(matrix_1: List[List[int]],
                      matrix_2: List[List[int]],
                      matrix_2_off: Tuple[int, int]) -> List[List[int]]:
        """
        Inserting one small matrix into the big matrix according to the given coordinates.
        :param matrix_1: big matrix
        :param matrix_2: small matrix
        :param matrix_2_off: small matrix's coordinates
        :return: big matrix including small one
        """
        off_x, off_y = matrix_2_off
        for cy, row in enumerate(matrix_2):
            for cx, val in enumerate(row):
                matrix_1[cy + off_y - 1][cx + off_x] += val
        return matrix_1

    @staticmethod
    def check_collision(board: List[List], shape: List[List], offset: Tuple) -> bool:
        """
        Checking whether shape doesn't hit borders.
        :param board: current playing board
        :param shape: falling shape
        :param offset: x and y coordinates of the falling shape
        :return: if shape hits border: True else: False
        """
        off_x, off_y = offset
        for cy, row in enumerate(shape):
            for cx, cell in enumerate(row):
                try:
                    if cell and board[cy + off_y][cx + off_x]:
                        return True
                except IndexError:
                    return True
        return False


class TetrisGame:
    def __init__(self) -> None:
        """
        Initializing our game:
        - setting width and height
        - disabling mouse
        - initializing useful variables(self.paused: bool, self.gameover: bool, self.board: List[List[int]], etc.)
        - starting the game
        :return: None
        """
        pygame.init()
        pygame.key.set_repeat(250, 25)
        pygame.mouse.set_visible(False)  # We do not need mouse movement
        pygame.event.set_blocked(pygame.MOUSEMOTION)  # events, so we block them.

        self.width = settings['cell_size'] * settings['cols']
        self.height = settings['cell_size'] * settings['rows']

        self.stones = deque([tetris_shapes[rand(len(tetris_shapes))]], maxlen=2)
        self.stone = None
        self.next_stone = None
        self.stone_x = None
        self.stone_y = None
        self.board = Board(10, 24)
        self.gameover = False
        self.paused = False
        self.init_game()
        self.speed = speed_levels.copy()
        self.run_b = True

    def new_stone(self) -> None:
        """
        Preparing next random stone for the game.
        :return: None
        """
        self.stones.append(tetris_shapes[rand(len(tetris_shapes))])

        self.stone = self.stones.popleft()
        self.stone_x = int(settings['cols'] / 2 - len(self.stone[0]) / 2)
        self.stone_y = 0

        self.next_stone = self.stones[-1]

        if self.board.check_collision(self.board.board_,
                                      self.stone,
                                      (self.stone_x, self.stone_y)):
            self.gameover = True
            gameover_sound.play()
            pygame.mixer.music.pause()

    def init_game(self) -> None:
        """
        Resetting game (updating score and speed, making new board and new stones)
        :return: None
        """
        settings['score'] = 0
        settings['delay'] = 750
        self.speed = speed_levels.copy()
        self.board.new_board()
        self.new_stone()
        self.run_b = True
        pygame.key.set_repeat(250, 25)
        pygame.mixer.music.unpause()

    @staticmethod
    def center_msg(msg: str) -> None:
        """
        Displays given message in the center of the screen.
        :param msg: message
        :return: None
        """
        for i, line in enumerate(msg.splitlines()):  # displaying every line
            msg_image = pygame.font.Font(
                pygame.font.get_default_font(), 20).render(
                line, False, (255, 255, 255), (0, 0, 0))

            msgim_center_x, msgim_center_y = msg_image.get_size()
            msgim_center_x //= 2
            msgim_center_y //= 2

            window.blit(msg_image, (
                width // 2 - msgim_center_x,
                height // 2 - msgim_center_y + i * 22))

    def move(self, delta_x: int) -> None:
        """
        Moving current falling shape.
        :param delta_x: x offset to move shape
        :return: None
        """
        if not self.gameover and not self.paused:  # checking whether game is paused or finished
            new_x = min(max(0, self.stone_x + delta_x), settings['cols'] - len(self.stone[0]))
            if not self.board.check_collision(self.board.board_,
                                              self.stone,
                                              (new_x, self.stone_y)):
                self.stone_x = new_x

    def quit(self) -> None:
        """
        Quitting the app.
        :return: None
        """
        self.center_msg("Exiting...")
        pygame.display.update()
        self.run_b = False
        pygame.mouse.set_visible(True)
        # loading music.
        pygame.mixer.music.load('data/zvuk-vstuplenija-v-tetrise-na-dendi.mp3')
        pygame.mixer.music.set_volume(0.3)  # 1 -100%  громкости звука.
        pygame.mixer.music.play(-1)  # играть бесконечно -1.

    def drop(self) -> None:
        """
        - Dropping current stone down.
        - Counting score and giving bonuses for extra speed and destroyed rows
        :return: None
        """
        if not self.gameover and not self.paused:
            settings['score'] += 1
            for x, (s, d) in self.speed.items():
                if settings['score'] >= x:
                    pygame.time.set_timer(pygame.USEREVENT + 1, 0)
                    pygame.time.set_timer(pygame.USEREVENT + 1, s)
                    pygame.key.set_repeat(d, 25)
                    del self.speed[x]
                    break

            self.stone_y += 1
            if self.board.check_collision(self.board.board_, self.stone,
                                          (self.stone_x, self.stone_y)):  # checking if we can move stone
                self.board.join_matrixes(self.board.board_, self.stone,  # and join it if possible
                                         (self.stone_x, self.stone_y))
                self.new_stone()
                c = 0  # row destroyed counter
                while True:

                    for i, row in enumerate(self.board.board_[:-1]):
                        if 0 not in row:
                            self.board.remove_row(i)
                            line_sound.play()
                            c += 1
                            break
                    else:

                        # counting scores and giving bonuses
                        settings['score'] += c * 100
                        if c == 2:
                            settings['score'] += 50
                        elif c == 3:
                            settings['score'] += 100
                        elif c == 4:
                            settings['score'] += 200

                        break

    def rotate_stone(self) -> None:
        """
        Rotating falling stone clockwise.
        :return: None
        """
        if not self.gameover and not self.paused:
            new_stone = [[self.stone[y][x]
                          for y in range(len(self.stone))]
                         for x in range(len(self.stone[0]) - 1, -1, -1)]  # rotating stone

            if not self.board.check_collision(self.board.board_,
                                              new_stone,
                                              (self.stone_x, self.stone_y)):  # checking if everything is okay
                self.stone = new_stone

    def toggle_pause(self) -> None:
        """
        Turning pause on and off.
        :return: None
        """
        self.paused = not self.paused

    def start_game(self) -> None:
        """
        Starting our game by initializing it.
        :return: None
        """
        if self.gameover:
            self.init_game()
            self.gameover = False
            self.run_b = True

    def show_info(self) -> None:
        """
        Showing important game information such as score and next stone.
        :return: None
        """
        text_score = pygame.font.Font(pygame.font.get_default_font(), 24) \
            .render(f"SCORE: {settings['score']}", False, (255, 255, 255))
        window.blit(text_score, (380, 10))
        text_shape = pygame.font.Font(pygame.font.get_default_font(), 24) \
            .render(f"NEXT SHAPE:", False, (255, 255, 255))
        window.blit(text_shape, (370, 100))

        for y, row in enumerate(self.next_stone):
            for x, val in enumerate(row):
                # going through every cell and paint it
                if val:
                    pygame.draw.rect(
                        window,
                        colors[val],
                        pygame.Rect(
                            x * (settings['cell_size'] + 2) + 420,
                            y * (settings['cell_size'] + 2) + 150,
                            settings['cell_size'],
                            settings['cell_size']), 0)

    def run(self) -> None:
        """
        The main game processor.
        :return: None
        """
        key_actions = {  # control key fuctions
            'ESCAPE': self.quit,
            'LEFT': lambda: self.move(-1),
            'RIGHT': lambda: self.move(+1),
            'DOWN': self.drop,
            'UP': self.rotate_stone,
            'p': self.toggle_pause,
            'SPACE': self.start_game
        }

        pygame.mixer.music.load('data/zvuk-tetrisa-na-konsoli.mp3')
        pygame.mixer.music.set_volume(0.3)  # 1 -100% sound
        pygame.mixer.music.play(-1)  # play unlimited -1, either a number indicates the amount of payback cycles.

        dont_burn_my_cpu = pygame.time.Clock()
        pygame.time.set_timer(pygame.USEREVENT + 1, settings['delay'])
        while self.run_b:
            # prepapring board
            window.fill((0, 0, 0))

            # must have conditions, checking the game process
            if self.gameover:
                fon = pygame.transform.scale(load_image('black1.jpg'), screen_size)
                window.blit(fon, (0, 0))
                self.center_msg(f"Game Over!\nYou scored: {settings['score']}!\nPress space to continue...")
            elif self.paused:
                fon = pygame.transform.scale(load_image('black1.jpg'), screen_size)
                window.blit(fon, (0, 0))
                self.center_msg("Paused")
            else:  # if not paused and not finished the board will draw
                pygame.draw.rect(window, pygame.Color('white'), pygame.Rect(0, 0, 282, 1000))
                self.board.draw_board()
                self.board.draw_shape(self.stone, (self.stone_x,
                                                   self.stone_y))
                self.show_info()

            pygame.display.update()

            # checking pressed buttons and calling key controls functions
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT + 1:
                    self.drop()
                elif event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    for key in key_actions:
                        if event.key == eval("pygame.K_" + key):
                            key_actions[key]()

            dont_burn_my_cpu.tick(settings['maxfps'])


def main():
    start_screen()


main()
