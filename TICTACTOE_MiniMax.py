import pygame
import numpy as np
import sys
import math
import time

size, offset, rad = 200, 55, 50
green = (55, 55, 200)
blue = (64, 224, 208)
red = (190, 66, 66)
board = np.zeros((3, 3))

dic = {1: 'Human', 2: 'AI'}


def checkwin(player):
    win_h = False
    win_v = False
    win_d = False
    for i in range(3):
        if board[0][i] == player and board[1][i] == player and board[2][i] == player:
            win_h = True


        elif board[i][0] == player and board[i][1] == player and board[i][2] == player:
            win_v = True


    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        win_d = True

    elif board[2][0] == player and board[1][1] == player and board[0][2] == player:
        win_d = True


    if win_d or win_h or win_v:
        return True
    else:
        return False


def fullboard():
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                return False
    return True


def mark(i, j, player):
    board[i][j] = player
    print(np.matrix(board))


def avail(i, j):
    return board[i][j] == 0


def drawfig(row, col, marked):
    i = int(size / 2 + size * row)
    j = int(size / 2 + size * col)
    if marked == 1:
        pygame.draw.circle(screen, blue, (j, i), rad, 4)

    elif marked == 2:
        pygame.draw.circle(screen, red, (j, i), rad, 4)


def choose_optimal():
    bscore = -100
    if fullboard():
        print("ALL POSITIONS FILLED")
        gameover = True
        return gameover
    for row in range(3):
        for col in range(3):
            if avail(row, col):
                board[row][col] = 2
                score = minimax(board, 0, False)
                board[row][col] = 0
                if score > bscore:
                    bscore = score
                    brow = row
                    bcol = col
                    print('Best move', (brow, bcol))

    try:
        mark(brow, bcol, 2)
    except:
        mark(row, col, 2)

    drawfig(brow, bcol, 2)


def minimax(board, depth, ismaximizing):
    if checkwin(1):
        return -10
    elif checkwin(2):
        return 10
    elif fullboard():
        return 0

    if ismaximizing:
        bscore = -2
        for row in range(3):
            for col in range(3):
                if board[row][col] == 0:
                    board[row][col] = 2
                    score = minimax(board, depth + 1, False)
                    board[row][col] = 0
                    bscore = max(bscore, score)

        return bscore

    else:
        bscore = 2
        for row in range(3):
            for col in range(3):
                if board[row][col] == 0:
                    board[row][col] = 1
                    score = minimax(board, depth + 1, True)
                    board[row][col] = 0
                    bscore = min(bscore, score)
        return bscore


def drawboard():
    pygame.draw.line(screen, green, (0, 200), (600, 200), 5)
    pygame.draw.line(screen, green, (0, 400), (600, 400), 5)
    pygame.draw.line(screen, green, (200, 0), (200, 600), 5)
    pygame.draw.line(screen, green, (400, 0), (400, 600), 5)


pygame.init()
pygame.display.set_caption('TicTacToe_MiniMax')
screen = pygame.display.set_mode((3 * size, 3 * size))
screen.fill((55, 55, 55))
drawboard()
pygame.display.update()

player = 0
gameover = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if checkwin(1):
            print('**___________________HUMAN WON__________________')
            time.sleep(1)
            sys.exit()
        elif checkwin(2):
            print('**________________AI WON__________________')
            time.sleep(.8)
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not gameover:
            ypos = event.pos[1]
            xpos = event.pos[0]
            row = int(math.floor(ypos / size))
            col = int(math.floor(xpos / size))
            print("Coordinates are ", end=':')
            print(row, col)

            if player % 2 == 0 and avail(row, col):
                print('Player : ', 'HUMAN')
                mark(row, col, 1)
                drawfig(row, col, 1)
                player += 1

        if player % 2 == 1:
            print('Computer')
            choose_optimal()
            player += 1

    if fullboard():
        print('________________TIE!!!!____________________')
        time.sleep(.5)
        sys.exit()
    pygame.display.update()
