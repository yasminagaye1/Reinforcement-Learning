# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 12:41:27 2018
"""
from Tkinter import *
import numpy as np
import time
from copy import copy, deepcopy
import time
master = Tk()

triangle_size = 0.1
cell_score_min = -0.2
cell_score_max = 0.2
Width = 20
(x, y) = (25, 25)
x1=0
y1=0
actions = ["up", "down", "left", "right"]
start_time = time.time()
red_blocks = 3
green_blocks = 2

#creating the display
board = Canvas(master, width=x*Width, height=(y+5)*Width)

#create label and entry to get the data
labelX = Label(text='Enter X')
labelX.configure(width = 10)
labelX_window = board.create_window(1*Width, 26*Width, anchor=NW, window=labelX)

labelY = Label(text='Enter Y')
labelY.configure(width = 10)
labelY_window = board.create_window(10*Width, 26*Width, anchor=NW, window=labelY)

entryX = Entry()
entryX.configure(width = 10)
entryX_window = board.create_window(1*Width, 27*Width, anchor=NW, window=entryX)

entryY = Entry()
entryY.configure(width = 10)
entryY_window = board.create_window(10*Width, 27*Width, anchor=NW, window=entryY)

def ok():
    global x1, y1, orig_player, player, me, map_grid 
    x1 = entryX.get()
    y1 = entryY.get()
    player = (int(x1), int(y1))
    if map_grid[player[0]][player[1]] == 1:  #Chech if the square is a wall if yes keep start at a random place untile
        #getting input from GUI
        labelERROR = Label(text='Please choose a different coordinate')
        labelERROR.configure(width = 50, fg = "red")
        labelERROR_window = board.create_window(1*Width, 25*Width, anchor=NW, window=labelERROR)
        time.sleep(5)
        return None
    orig_player = deepcopy(player)
    print ("X=", x1, "Y=", y1)
    me = board.create_rectangle(player[0]*Width+Width*2/10, player[1]*Width+Width*2/10,
                            player[0]*Width+Width*8/10, player[1]*Width+Width*8/10, fill="orange", width=1, tag="me")

#CReating a button on 
#start button
buttonS = Button(board, text = "Start", command = ok, anchor = W)
buttonS.configure(width = 10, activebackground = "#D4D6D3",fg = "blue", relief = FLAT)
buttonS_window = board.create_window(5*Width, 28.5*Width, anchor=NW, window=buttonS)
#add quit button
buttonQ = Button(board, text = "Quit", command = quit, anchor = W)
buttonQ.configure(width = 10, activebackground = "#D2D2D2",fg = "red", relief = FLAT)
buttonQ_window = board.create_window(20*Width, 28.5*Width, anchor=NW, window=buttonQ)


score = 1
restart = False
walk_reward = -0.04

# Perform cellular automata to generate a random grid layout
iter_max = 7

map_grid = []
for i in range(x):
    map_row = []
    for j in range(y):
        map_row.append(0)
    map_grid.append(map_row)

for i in range(1,x-1):
    for j in range(1,y-1):
        map_grid[i][j] = np.random.choice([0,1], p=[0.38, 0.62])

for iter_t in range(iter_max):
    new_map_grid = deepcopy(map_grid)
    for i in range(1,x-1):
        for j in range(1,y-1):
            neighbour_score = 0
            for i1 in range(-1,2):
                for j1 in range(-1,2):
                    if (i1 != 0 or j1 != 0) and map_grid[i+i1][j+j1] == 1:
                        neighbour_score += 1
            # print neighbour_score
            if neighbour_score > 4:
                new_map_grid[i][j] = 1
            else:
                new_map_grid[i][j] = 0
    map_grid = deepcopy(new_map_grid)

#create a wall
walls = []
for i in range(0,x):
    for j in range(0,y):
        if map_grid[i][j] == 1:
            walls.append((i,j))

# Randomly initilaize player where there is no wall
'''player = (np.random.randint(x), np.random.randint(y)) #Start at a random square
while map_grid[player[0]][player[1]] == 1:  #Chech if the square is a wall if yes keep start at a random place untile
    player = (np.random.randint(x), np.random.randint(y))  #you find a square that is not a wall'''

#Inicialize Player to 00
player = (int(x1), int(y1)) #Start at coordinate indicate by user

#place the red and green box somewhere without wall
specials = []
specialGren = []
for i in range(red_blocks):
    gen_pos = (np.random.randint(x), np.random.randint(y))
    while map_grid[gen_pos[0]][gen_pos[1]] == 1: #chech to see if it is a wall
        gen_pos = (np.random.randint(x), np.random.randint(y))
    specials.append((gen_pos[0], gen_pos[1], "red", -1)) #red blocks have -1 reward
for i in range(green_blocks):
    gen_pos = (np.random.randint(x), np.random.randint(y))
    while map_grid[gen_pos[0]][gen_pos[1]] == 1:
         gen_pos = (np.random.randint(x), np.random.randint(y))
    specials.append((gen_pos[0], gen_pos[1], "green", 1))  #green blocks have 1 reward
    #specialGren.append((gen_pos[0], gen_pos[1], "green", 1))  #green blocks have 1 reward

cell_scores = {}


def create_triangle(i, j, action):
    if action == actions[0]:
        return board.create_polygon((i+0.5-triangle_size)*Width, (j+triangle_size)*Width,
                                    (i+0.5+triangle_size)*Width, (j+triangle_size)*Width,
                                    (i+0.5)*Width, j*Width,
                                    fill="white", width=1)
    elif action == actions[1]:
        return board.create_polygon((i+0.5-triangle_size)*Width, (j+1-triangle_size)*Width,
                                    (i+0.5+triangle_size)*Width, (j+1-triangle_size)*Width,
                                    (i+0.5)*Width, (j+1)*Width,
                                    fill="white", width=1)
    elif action == actions[2]:
        return board.create_polygon((i+triangle_size)*Width, (j+0.5-triangle_size)*Width,
                                    (i+triangle_size)*Width, (j+0.5+triangle_size)*Width,
                                    i*Width, (j+0.5)*Width,
                                    fill="white", width=1)
    elif action == actions[3]:
        return board.create_polygon((i+1-triangle_size)*Width, (j+0.5-triangle_size)*Width,
                                    (i+1-triangle_size)*Width, (j+0.5+triangle_size)*Width,
                                    (i+1)*Width, (j+0.5)*Width,
                                    fill="white", width=1)


def render_grid():
    global specials, walls, Width, x, y, player
    for i in range(x):
        for j in range(y):
            board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="cyan", width=1)
            temp = {}
            for action in actions:  #actions = ["up", "down", "left", "right"]
                temp[action] = create_triangle(i, j, action)
            cell_scores[(i,j)] = temp
    for (i, j, c, w) in specials:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill=c, width=1) # specials.append((gen_pos[0], gen_pos[1], "green", 1)) 
    for (i, j) in walls:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="black", width=1)
        #walls.append((i,j))
render_grid()


def set_cell_score(state, action, val):
    global cell_score_min, cell_score_max
    triangle = cell_scores[state][action]
    green_dec = int(min(255, max(0, (val - cell_score_min) * 255.0 / (cell_score_max - cell_score_min))))
    green = hex(green_dec)[2:]
    red = hex(255-green_dec)[2:]
    if len(red) == 1:
        red += "0"
    if len(green) == 1:
        green += "0"
    color = "#" + red + green + "00"
    board.itemconfigure(triangle, fill=color)


def try_move(dx, dy):
    global player, x, y, score, walk_reward, me, restart, start_time 
    if restart == True:
        restart_game()
    new_x = player[0] + dx
    new_y = player[1] + dy
    score += walk_reward
    if (new_x >= 0) and (new_x < x) and (new_y >= 0) and (new_y < y) and not ((new_x, new_y) in walls):
        board.coords(me, new_x*Width+Width*2/10, new_y*Width+Width*2/10, new_x*Width+Width*8/10, new_y*Width+Width*8/10)
        player = (new_x, new_y)
    for (i, j, c, w) in specials:
        if new_x == i and new_y == j:
            #Time****************
            end_time = time.time()
            time1 = end_time - start_time 
            score -= walk_reward
            score += w
            if score > 0:
                print "Success! score: ", score
                print "Time: ", time1
            else:
                print "Fail! score: ", score            
                print "Time: ", time1
            restart = True
            return
    #print "score: ", score


def call_up(event):
    try_move(0, -1)


def call_down(event):
    try_move(0, 1)


def call_left(event):
    try_move(-1, 0)


def call_right(event):
    try_move(1, 0)


def restart_game():
    global player, score, me, restart, start_time
    #start the time
    start_time = time.time()
    player =  deepcopy(orig_player)
    score = 1
    restart = False
    board.coords(me, player[0]*Width+Width*2/10, player[1]*Width+Width*2/10, player[0]*Width+Width*8/10, player[1]*Width+Width*8/10)

def has_restarted():
    return restart

master.bind("<Up>", call_up)
master.bind("<Down>", call_down)
master.bind("<Right>", call_right)
master.bind("<Left>", call_left)

board.grid(row=0, column=0)


def start_game():
    global x1, y1
    global start_time
    start_time = time.time()
    master.mainloop()