from State import State
import numpy as np
from Logic import Logic
import time
import pygame
import sys

pygame.init()

WIDTH = 500
HEIGHT = 600
LINE_WIDTH = 3
BOARDS_CELL = 5
CIRCLE_CENTER = 35
SPACE = 20
game_finished = False
who_plays = " "

BG_COLOR = (65, 185, 122)
LINE_COLOR = (85, 200, 140)
FONT_COLOR = (64, 132, 93)
FONT2_COLOR = (204, 50, 50)
BUILLDING_COLOR = (50, 50, 50)
TRUK_COLOR = (150, 150, 250, 50)

RED = (200, 20, 20)
X_COLOR = (49, 86, 66)
O_COLOR = (200, 230, 202)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("King of the Road")
screen.fill(BG_COLOR)

state: State
state = State()

cell_size = max(np.shape(state.cells)[0], np.shape(state.cells)[1])
cell_size = 500/cell_size
row_number = np.shape(state.cells)[0]
col_number = np.shape(state.cells)[1]

font = pygame.font.SysFont("Paladins Straight", 22)
font2 = pygame.font.SysFont("cocon", 25)
font3 = pygame.font.SysFont("cocon", 13)

rBox = pygame.image.load('images/rBox.png')
rBox = pygame.transform.scale(rBox, (cell_size-10, cell_size - 10))
drop = pygame.image.load('images/drop.png')
drop = pygame.transform.scale(drop, (cell_size-10, cell_size - 10))
buillding = pygame.image.load('images/buillding.png')
buillding = pygame.transform.scale(buillding, (cell_size-10, cell_size - 10))


def draw_lines():

    temp = np.shape(state.cells)[1]*cell_size
    for i in range(row_number+1):
        pygame.draw.line(screen, LINE_COLOR, (0, i*cell_size),
                         (temp, i*cell_size), LINE_WIDTH)
    temp = np.shape(state.cells)[0]*cell_size
    for i in range(col_number+1):
        pygame.draw.line(screen, LINE_COLOR, (i*cell_size, 0),
                         (i*cell_size, temp), LINE_WIDTH)
        # (left line ,up line ,width , height)
    pygame.draw.rect(screen, LINE_COLOR, (20, 530, 90, 40), 0, 5)
    ucs = font.render("UCS", True, FONT_COLOR)
    screen.blit(ucs, (32, 538))
    pygame.draw.rect(screen, LINE_COLOR, (135, 530, 90, 40), 0, 5)
    ucs = font.render("A* 1", True, FONT_COLOR)
    screen.blit(ucs, (147, 538))
    pygame.draw.rect(screen, LINE_COLOR, (250, 530, 90, 40), 0, 5)
    ucs = font.render("A* 2", True, FONT_COLOR)
    screen.blit(ucs, (262, 538))
    pygame.draw.rect(screen, LINE_COLOR, (365, 530, 90, 40), 0, 5)
    ucs = font.render("A* 3", True, FONT_COLOR)
    screen.blit(ucs, (377, 538))


draw_lines()


def LoadDrop(sstate):
    c = cell_size/2
    c -= 5
    for i in sstate.loadPlaces.items():
        screen.blit(rBox, (i[0][1]*cell_size+5, i[0][0]*cell_size+5))
        text = font3.render('Load Place', True, FONT2_COLOR)
        screen.blit(text, (i[0][1]*cell_size+c/2, i[0][0]*cell_size+c-5))
        text = font2.render(f'{i[1]}', True, FONT2_COLOR)
        screen.blit(text, (i[0][1]*cell_size+c, i[0][0]*cell_size+c+5))

    for i in sstate.dropPlaces.items():
        screen.blit(drop, (i[0][1]*cell_size, i[0][0]*cell_size))
        text = font2.render(f'{i[1]}', True, FONT_COLOR)
        screen.blit(text, (i[0][1]*cell_size+5, i[0][0]*cell_size+5))


def putBuillding():
    for i in range(row_number):
        for j in range(col_number):
            if(state.cells[i][j] == '#'):
                # pygame.draw.rect(screen,BUILLDING_COLOR,(j*cell_size+5,i*cell_size+5,cell_size-10,cell_size-10))
                screen.blit(buillding, (j*cell_size+5, i*cell_size+5))

    LoadDrop(state)
    truckPosition = state.getTruckPosition()
    pygame.draw.rect(screen, TRUK_COLOR, (
        truckPosition[1]*cell_size+5, truckPosition[0]*cell_size+5, cell_size-10, cell_size-10))


putBuillding()


def ucs():
    logic = Logic(state)
    start = time.time()
    logic.UniformCostSearch()
    end = time.time()
    print(f'time is: {end - start}')

####################


logic = Logic(state)

# start = time.time()
# #logic.UniformCostSearch()

# logic.aStareOrdinary(2)
# end = time.time()

# print(f'time is: {end - start}')
##############################


def restart():
    screen.fill(BG_COLOR)
    putBuillding()
    draw_lines()


clock = pygame.time.Clock()

x = 0
counter = 0
done = False
is_restart = False

color2 = 50
color3 = 50


running = True
# main loop
while running:
    counter += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Buttons
            if 570 > event.pos[1] > 530:
                # First Button   UCS
                if 110 > event.pos[0] > 20:
                    start = time.time()
                    logic.UniformCostSearch()
                    end = time.time()
                    print(f'time is: {end - start}')
                    x = len(logic.path)-1
                    done = True
                    color2 = 250
                    color3 = 10
                    is_restart = False
                    # second Button   A* (1)
                if 325 > event.pos[0] > 135:
                    start = time.time()
                    logic.aStareOrdinary(1)
                    end = time.time()
                    print(f'time is: {end - start}')
                    x = len(logic.path)-1
                    done = True
                    color2 = 100
                    color3 = 210
                    is_restart = False
                   # Third Button   A* (2)
                if 340 > event.pos[0] > 210:
                    print("////////// A* 2 ///////////")
                    start = time.time()
                    logic.aStareOrdinary(2)
                    end = time.time()
                    print(f'time is: {end - start}')
                    x = len(logic.path)-1
                    done = True
                    color2 = 50
                    color3 = 50
                    is_restart = False
                    # Fourth Button   A* (3)
                if 455 > event.pos[0] > 365:
                    print("////////// A* 3 ///////////")
                    start = time.time()
                    logic.aStareOrdinary(3)
                    end = time.time()
                    print(f'time is: {end - start}')
                    x = len(logic.path)-1
                    done = True
                    color2 = 200
                    color3 = 200
                    is_restart = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                is_restart = True

    if x == -1 or is_restart:
        done = False
    if done and counter >= 10:
        counter = 0
        truckPosition = logic.path[x].getTruckPosition()
        # print(logic.path[x].printState())
        color = x*30
        while color > 255:
            color -= 255
        pygame.draw.rect(screen, (color, color2, color3), ((
            truckPosition[1]*cell_size)+5, (truckPosition[0]*cell_size)+5, cell_size-10, cell_size-10))
        LoadDrop(logic.path[x])
        x -= 1

    pygame.display.update()
    clock.tick(60)

pygame.quit()


# state = state.nextState()[0]
# state = state.nextState()[1]
# state.printState()
# print('_________')

# i: State
# for i in state.nextState():
#     i.printState()
#     print('..........................')
