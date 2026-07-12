import random
import logic
import os

import classes

terminal = os.get_terminal_size()
term_cols = terminal.columns
term_rows = terminal.lines - 3

wall_col = term_cols // 2 - 3
if wall_col % 2 == 0:
    wall_col -= 1

def player2_phase_search(current_maze, player2, player, list,  active_mobs):

    closest_coords= None
    min_distance =  None
    path = None

    #phase1
    if list:
        min_distance = None
        closest_coords = None

        for r_idx, row in enumerate(current_maze):
            for c_idx, cell in enumerate(row):
                if c_idx > wall_col:
                    if (r_idx, c_idx) in list:
                        manhatten_distance = abs(r_idx - player2.row) + abs(c_idx - player2.col)
                        if min_distance is None or manhatten_distance < min_distance:
                            min_distance = manhatten_distance
                            closest_coords = (r_idx, c_idx)

        if closest_coords:
            path = logic.astar(current_maze, (player2.row, player2.col), closest_coords)
            if path is not None:
                return path

    # Phase 2:
    if active_mobs:
        weakest_mob = None

        for mob in active_mobs:
            if mob.col > wall_col:
                if weakest_mob is None or mob.hp < weakest_mob.hp:
                    weakest_mob = mob
                elif mob.hp == weakest_mob.hp:
                    manhatten_curr = abs(mob.row - player2.row) + abs(mob.col - player2.col)
                    manhatten_weak = abs(weakest_mob.row - player2.row) + abs(weakest_mob.col - player2.col)
                    if manhatten_curr < manhatten_weak:
                        weakest_mob = mob

        if weakest_mob:
            path = logic.astar(current_maze, (player2.row, player2.col), (weakest_mob.row, weakest_mob.col))
            if path is not None:
                return path

    # Phase 3:
    path = logic.astar(current_maze, (player2.row, player2.col), (player.row, player.col))
    if path is not None:
        return path

def player2_move(current_maze, player2, player, list, active_mobs):
    path = player2_phase_search(current_maze, player2, player, list,  active_mobs)
    if path is not None and len(path) > 1:
        return path[1]
    else:
        return player2.row, player2.col
