import os
import random
import sys
import time
import threading

import pygame
import readchar
from colorist import BgColor, Color, bg_blue, red, yellow

from classes import (
    Armor,
    Entity,
    Player,
    Trap,
    Weapon,
)
from display import display_maze, gameover, print_statusline, start, game_won
from generation import (
    arena,
    arena_start_col,
    arena_width,
    deletewalls,
    dfs_algorithm,
    gen_item,
    rooms,
    spawn_mobs,
    wall,
    gen_item_coords,
)
from logic import check_fight, move_mobs, playsong, check_upgrade, check_trap, handle_fight
from player2 import player2_move

# clean terminal and collect terminal infos + recursion for the maze to work (first if checks if Posix or windows :) neat thing!)
if os.name == "posix":
    os.system("clear")
else:
    os.system("cls")

terminal = os.get_terminal_size()
term_cols = terminal.columns
term_rows = terminal.lines
sys.setrecursionlimit(2000)

# print beautiful ascii stuff and arks for name and simulate loading
pygame.mixer.init()
pygame.mixer.music.set_volume(0.1)
start("frodo")

time.sleep(0.1)  # 0.5

# create classes and generate the random values for this round
atkvalue = random.randrange(1, 4)
defvalue = random.randrange(1, 3)

weapon = Weapon("(", "Anduril - Flame of the West", "weapon", atkvalue)
armor = Armor("[", "Bilbos Mihtril Armor", "armor", defvalue)

# if the terminal size is not even, i need to set it to even
wall_col = term_cols // 2
if wall_col % 2 == 0:
    wall_col -= 1

#ue = uneven
col_ue = term_cols
if col_ue % 2 == 0:
    col_ue -= 1

#-3 because of the status line and stuff
rows_ue = term_rows - 3
if rows_ue % 2 == 0:
    rows_ue-= 1

# fill maze with walls completly for size of the terminal
maze = [["█" for i in range(col_ue)] for j in range( rows_ue)]

# set player start positions
player_row = 1
player_col = 1


anti_row = len(maze) - 3
anti_col = len(maze[0]) - 3

player = Player("@","frodo", 10, 1, 1, 1, 1, 0,  player_row, player_col,)
player2 = Player("*", "Mouth of Sauron", 10, 1, 1, 1, 1, 0,  anti_row, anti_col)

dragon = Entity("D", "Smaug", 30, 20, 10, 10)
gremlin = Entity("G", "gremlin", 6, 2, 1, 6)
jelly = Entity("J", "jelly", 8, 3, 0, 8)
gnome = Entity("N", "gnome", 5, 1, 2, 6)
bobklin = Entity("B", "bobklin", 3, 4, 2, 5)
ruffy = Entity("R", "ruffy", 3, 10, 20, 10)
franky = Entity("F", "Franko", 1, 1, 1, 1)

enemy_list = [dragon, gremlin, jelly, gnome, bobklin, ruffy, franky]

hidden_trap = Trap("^", "hidden", "trap", "white", 2)

item_size = random.randrange(4,7)

# call Labyrinth generation
wall(maze)
dfs_algorithm(maze, 1, 1)
dfs_algorithm(maze, 1, wall_col + 2)
rooms(maze)
deletewalls(maze)
arena(maze)
gen_item(maze, weapon.glyph, item_size)
gen_item(maze, armor.glyph, item_size)
gen_item(maze, hidden_trap.glyph, 3)

#create the coords
traps_coords = gen_item_coords(maze, [], "^")



# Spawn mobs dynamically as individual Entity instances
active_mobs = []

# Left side mobs
active_mobs.extend(spawn_mobs(maze, dragon, 1, arena_start_col - 2, 2, term_rows - 5, 1))
active_mobs.extend(spawn_mobs(maze, gremlin, 1, arena_start_col - 2, 2, term_rows - 5, 2))
active_mobs.extend(spawn_mobs(maze, jelly, 1, arena_start_col - 2, 2, term_rows - 5, 2))
active_mobs.extend(spawn_mobs(maze, gnome, 1, arena_start_col - 2, 2, term_rows - 5, 2))
active_mobs.extend(spawn_mobs(maze, bobklin, 1, arena_start_col - 2, 2, term_rows - 5, 1))

# Right side mobs
active_mobs.extend(spawn_mobs(maze, dragon, arena_start_col + arena_width + 2, term_cols - 4, 4, term_rows - 5, 1))
active_mobs.extend(spawn_mobs(maze, gremlin, arena_start_col + arena_width + 2, term_cols - 4, 4, term_rows - 5, 2))
active_mobs.extend(spawn_mobs(maze, jelly, arena_start_col + arena_width + 2, term_cols - 4, 4, term_rows - 5, 2))
active_mobs.extend(spawn_mobs(maze, gnome, arena_start_col + arena_width + 2, term_cols - 4, 4, term_rows - 5, 2))
active_mobs.extend(spawn_mobs(maze, bobklin, arena_start_col + arena_width + 2, term_cols - 4, 4, term_rows - 5, 1))

# initialise a lot of things AND the sound stuff
maze[1][1] = "S"
maze[len(maze) - 3][len(maze[0]) - 3] = "Z"

gamestat = 0
stepped_mob = None
track_fight = None
track_fight2 = None
track_item = None
track_trap = False
track_trap2 = False
track_item2 = None
player_alive = True
player2_alive = True
stepped_mob2 = None
track_mob_trap = None

playsong("sounds/theme2.mp3")
sound = 0

# game Loop
while True:
    print(
        "\033[H", end=""
    )  # nice way to clear the screen AND to fix the flickering (thank you stack overflow random user that I saw at the 3rd scroll xD)

    display_maze(
        maze,
        player.row,
        player.col,
        player.glyph,
        player2.row,
        player2.col,
        player2.glyph
    )
    print_statusline(player, player2, track_fight, track_item, track_trap, track_item2, track_fight2, track_trap2)
    track_fight = None
    track_item = None
    track_item2 = None
    track_trap = False
    track_trap2 = False
    track_fight2 = None
    doors_passed = False

    #list for player2 pathfinding
    weapon_coords = gen_item_coords(maze, [], weapon.glyph)
    armor_coords = gen_item_coords(maze, [], armor.glyph)

    item_list = []
    item_list.extend(armor_coords)
    item_list.extend(weapon_coords)

    move = readchar.readkey()

    next_row = player.row
    next_col = player.col

    anti_next_row = player2.row
    anti_next_col = player2.col

    if move == "w":
        next_row -= 1
    elif move == "a":
        next_col -= 1
    elif move == "s":
        next_row += 1
    elif move == "d":
        next_col += 1
    elif move == "q":
        gamestat = 0
        break

    if maze[next_row][next_col] not in ("█", "┃"):
        player.row = next_row
        player.col = next_col



    track_item = check_upgrade(maze, next_row, next_col, player, weapon, track_item, item_list)
    track_item = check_upgrade(maze, next_row, next_col, player, armor, track_item, item_list)


    if (maze[next_row][next_col] == "░" and sound == 0) or (maze[anti_next_row][anti_next_col] == "░" and sound == 0):
        pygame.mixer.music.stop()
        playsong("sounds/battle2.mp3")
        sound = 1

    #player2 Ai
    (anti_next_row, anti_next_col) = player2_move(maze, player2, player, item_list, active_mobs)
    player2.row = anti_next_row
    player2.col = anti_next_col

    #check doors
    if maze[player.row][player.col] == "╣":
        doors_passed = True
        player.col += 1
        maze[player.row][player.col - 1] = "█"
        player.level_up()
    elif maze[player2.row][player2.col] == "╠":
        doors_passed = True
        player2.col -= 1
        maze[player2.row][player2.col + 1] = "█"
        player2.level_up()

    track_item2 = check_upgrade(maze, anti_next_row, anti_next_col, player2, weapon, track_item, item_list)
    track_item2 = check_upgrade(maze, anti_next_row, anti_next_col, player2, armor, track_item, item_list)

    #first fight phase
    stepped_mob = None
    player_alive  , stepped_mob = check_fight(maze, stepped_mob, active_mobs, next_row, next_col, player, player_alive,1)
    if stepped_mob is not None:
        track_fight = stepped_mob

    #player2 fight phase 1
    stepped_mob2 = None
    player_alive2  , stepped_mob2 = check_fight(maze, stepped_mob2, active_mobs, anti_next_row, anti_next_col, player2, player2_alive,1)
    if stepped_mob2 is not None:
        track_fight2 = stepped_mob

    track_trap = check_trap(maze, traps_coords, player, track_trap)
    track_trap2 = check_trap(maze, traps_coords, player2, track_trap2)

    # move mobs dynamically
    move_mobs(maze, active_mobs, player, player2)
    stepped_mob = None
    stepped_mob2 = None

    for mob in active_mobs:
        track_mob_trap = check_trap(maze, traps_coords, mob, track_mob_trap)
        if mob.hp <= 0:
            active_mobs.remove(mob)
            if mob.col > wall_col:
                player2.level_up()
            else:
                player.level_up()
            maze[mob.row][mob.col] = ""


    #second player fight phase
    (player_alive, stepped_mob) = check_fight(maze, stepped_mob, active_mobs, next_row, next_col, player, player_alive,0)
    if stepped_mob is not None:
        track_fight = stepped_mob

    #second player2 fight phase
    (player_alive2, stepped_mob2) = check_fight(maze, stepped_mob2, active_mobs, anti_next_row, anti_next_col, player2, player2_alive,0)
    if stepped_mob2 is not None:
        track_fight2 = stepped_mob2

    #check for player fight
    if player.row == player2.row and player.col == player2.col:
        handle_fight(player, player2, 1)
        stepped_mob = player2


    if player.hp <= 0:
        player_alive = False

    if player2.hp <= 0:
        player_alive2 = False

    if not player_alive:
        gamestat = 0
        break
    if not player_alive2:
        gamestat = 1
        break





if gamestat == 0:
    gameover(player, stepped_mob)
    time.sleep(20)
else:
    game_won(player)
    time.sleep(20)
