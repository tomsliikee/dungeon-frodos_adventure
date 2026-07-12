import os
import random
import sys
import time

from colorist import BgColor, Color, bg_blue, red, yellow

import classes

terminal = os.get_terminal_size()
term_cols = terminal.columns
term_rows = terminal.lines - 3 #-3 because of status line again
sys.setrecursionlimit(2000)

# is used if the term_cols is even, to make it uneven for the arena in the middle
wall_col = term_cols // 2 - 3
if wall_col % 2 == 0:
    wall_col -= 1

# because we need it to be uneven, like the wall_col and global because i am going to use it later for the rooms
arena_width = (term_cols - 1) // 10
if arena_width % 2 == 0:
    arena_width -= 1

arena_start_row = (term_rows - 1) // 3
arena_start_col = wall_col - (arena_width // 2)


# build the arena
def arena(current_maze):

    for i in range((term_rows - 1) // 3):
        for j in range(arena_width):
            current_maze[arena_start_row + i][arena_start_col + j] = "░"

    for i in range((term_rows - 1) // 3):
        current_maze[arena_start_row + i][arena_start_col - 1] = "█"
        current_maze[arena_start_row + i][arena_start_col + arena_width] = "█"

    for j in range(arena_width):
        current_maze[arena_start_row - 1][arena_start_col + j] = "█"
        current_maze[arena_start_row + (term_rows - 1) // 3][arena_start_col + j] = "█"

    # too ensure that the maze infront of thew entrance is not blocked and a door exists
    entrance_hight = arena_start_row + (term_rows - 2) // 3 // 2
    if entrance_hight % 2 == 0:
        entrance_hight -= 1
    current_maze[entrance_hight][arena_start_col - 1] = "╣"
    current_maze[entrance_hight][arena_start_col - 2] = " "
    current_maze[entrance_hight][arena_start_col - 3] = " "
    current_maze[entrance_hight][arena_start_col - 4] = " "
    current_maze[entrance_hight][arena_start_col - 5] = " "

    current_maze[entrance_hight][arena_start_col + arena_width] = "╠"
    current_maze[entrance_hight][arena_start_col + arena_width + 1] = " "
    current_maze[entrance_hight][arena_start_col + arena_width + 2] = " "
    current_maze[entrance_hight][arena_start_col + arena_width + 3] = " "
    current_maze[entrance_hight][arena_start_col + arena_width + 4] = " "


# fill the maze to the finish with the DFS Algo, Depth first search, function because maybe i can use it later again idk
def dfs_algorithm(current_maze, row, col):
    current_maze[row][col] = " "
    directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
    random.shuffle(directions)

    for d_row, d_col in directions:
        new_row, new_col = row + d_row, col + d_col
        if (
            0 <= new_row < len(current_maze) - 1
            and 0 <= new_col < len(current_maze[0]) - 1
            and current_maze[new_row][new_col] == "█"
        ):
            wall_row = row + d_row // 2
            wall_col_idx = col + d_col // 2
            current_maze[wall_row][wall_col_idx] = " "
            dfs_algorithm(current_maze, new_row, new_col)


# build the wall in the middle duh xD
def wall(current_maze):
    for i in range(term_rows - 1):
        current_maze[i][wall_col] = "┃"


# creates the room dynamic to terminal size
def rooms(current_maze):
    size = 10
    roomsize = 4
    if term_cols > 180:
        size = 40
        roomsize = 5

    # left side
    for _ in range(size):
        rand_col = random.randrange(5, arena_start_col - 5)
        rand_row = random.randrange(5, term_rows - 10)
        radius = random.randrange(1, roomsize)

        for d_row in range(-radius, radius + 1):
            for d_col in range(-radius, radius + 1):
                current_maze[rand_row + d_row][rand_col + d_col] = " "

    # right side
    for _ in range(size):
        rand_col = random.randrange(arena_start_col + arena_width + 5, term_cols - 7)
        rand_row = random.randrange(4, term_rows - 10)
        radius = random.randrange(1, roomsize)

        for d_row in range(-radius, radius + 1):
            for d_col in range(-radius, radius + 1):
                current_maze[rand_row + d_row][rand_col + d_col] = " "


# deleting random walls
def deletewalls(current_maze):
    size = 40
    if term_cols > 180:
        size = 200

    # left side
    while size != 0:
        rand_col = random.randrange(1, arena_start_col - 2)
        rand_row = random.randrange(2, term_rows - 5)

        if current_maze[rand_row][rand_col] == "█":
            current_maze[rand_row][rand_col] = " "
            size = size - 1

    size = 40
    if term_cols > 180:
        size = 200

    # right side
    while size != 0:
        rand_col = random.randrange(arena_start_col + arena_width + 2, term_cols - 4)
        rand_row = random.randrange(4, term_rows - 5)

        if current_maze[rand_row][rand_col] == "█":
            current_maze[rand_row][rand_col] = " "
            size = size - 1


# generate the item for the player
def gen_item(current_maze, glyph, number):
    size = number
    if term_cols > 180:
        size *= 2

    # left side
    while size != 0:
        rand_col = random.randrange(1, arena_start_col - 2)
        rand_row = random.randrange(2, term_rows - 5)

        if current_maze[rand_row][rand_col] == " ":
            current_maze[rand_row][rand_col] = glyph
            size = size - 1

    size = number
    if term_cols > 180:
        size *= 2

    # right side
    while size != 0:
        rand_col = random.randrange(arena_start_col + arena_width + 2, term_cols - 4)
        rand_row = random.randrange(4, term_rows - 5)

        if current_maze[rand_row][rand_col] == " ":
            current_maze[rand_row][rand_col] = glyph
            size = size - 1


# Spawns a list of mobs
def spawn_mobs(current_maze, template_mob, min_col, max_col, min_row, max_row, number):
    created_mobs = []
    count = 0

    while count < number:
        rand_col = random.randrange(min_col, max_col)
        rand_row = random.randrange(min_row, max_row)

        if current_maze[rand_row][rand_col] == " ":
            # Create a brand new Entity object for this specific mob
            new_mob = classes.Entity(
                template_mob.glyph,
                template_mob.name,
                template_mob.hp,
                template_mob.atk,
                template_mob.defe,
                template_mob.sense,
                rand_row,  # row
                rand_col   # col
            )

            current_maze[rand_row][rand_col] = template_mob.glyph
            created_mobs.append(new_mob)
            count += 1

    return created_mobs

#generate list of coords for etc armor or traps
def gen_item_coords(current_maze, list, glyph):
    for r_idx, row in enumerate(current_maze):
        for c_idx, cell in enumerate(row):
                if cell == glyph:
                    list.append((r_idx, c_idx))
                if cell == "^":
                    current_maze[r_idx][c_idx] = " "
                    list.append((r_idx, c_idx))
    return list
