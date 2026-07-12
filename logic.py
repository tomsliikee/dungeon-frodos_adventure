import pygame
import random

from classes import Node, Player, Entity

# handle the fight logic for the game, 1 for player first attack and 0 for mob first attack, it returns 2 if something wrong is entered
def handle_fight(player, mob, player_or_mob_atk):
        if player_or_mob_atk == 1:
            first = player
            second = mob
        elif player_or_mob_atk == 0:
            first = mob
            second = player
        else:
            return 2

        while True:
            damage_first = max(first.atk - second.defe, 1)
            second.hp -= damage_first
            if second.hp <= 0:
                return True if first == player else False

            # Zweiter Angriff
            damage_second = max(second.atk - first.defe, 1)
            first.hp -= damage_second
            if first.hp <= 0:
                return True if second == player else False



# basically a wrapper for the handle fight function, it handles deleting the mobs calculating levels up etc...
def entcounter(current_maze, row, col, player, mob, player_or_mob_atk):
    won = handle_fight(player, mob, player_or_mob_atk)
    playsound("sounds/fight.mp3")
    if won:
        current_maze[row][col] = " "
        player.level_up()
        return True
    else:
        return False

#checks if the player has stepped on a mob and if yes, initates a fight
def check_fight(current_maze, stepped_mob, active_mobs, next_row, next_col, player, player_alive, player_or_mob_atk):
    stepped_mob = None
    for mob in active_mobs:
        if mob.row == next_row and mob.col == next_col:
            stepped_mob = mob
            break

    if stepped_mob:
        won = entcounter(current_maze, next_row, next_col, player, stepped_mob, player_or_mob_atk)
        if won:
            active_mobs.remove(stepped_mob)
            player.slayed_mobs += 1
            return player_alive , stepped_mob
        else:
            player_alive = False

    return player_alive, stepped_mob


#function to move the mobs. first checks if the player is near their sense range, then performs A*, if not it just moves random
def move_mobs(current_maze, active_mobs, player, player2):
        wall_col = len(current_maze[0]) // 2

        for mob in active_mobs:
            if mob.col < wall_col:
                target = player
            else:
                target = player2

            manhatten_distance = abs(target.row - mob.row) + abs(target.col - mob.col)
            if manhatten_distance <= mob.sense:
                path = astar(current_maze, (mob.row, mob.col), (target.row, target.col))

                if path is not None and len(path) > 1:
                    (new_row, new_col) = path[1]
                    current_maze[mob.row][mob.col] = " "
                    current_maze[new_row][new_col] = mob.glyph
                    mob.row = new_row
                    mob.col = new_col
                else:
                    continue

            else:
                d_row, d_col = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
                new_row = mob.row + d_row
                new_col = mob.col + d_col

                if 0 <= new_row < len(current_maze) and 0 <= new_col < len(current_maze[0]):
                    if current_maze[new_row][new_col] == " ":
                        current_maze[mob.row][mob.col] = " "
                        current_maze[new_row][new_col] = mob.glyph
                        mob.row = new_row
                        mob.col = new_col



#for playing sounds and songs
def playsong(theme):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(theme)
    pygame.mixer.music.play()

def playsound(sound):
    sound_play = pygame.mixer.Sound(sound)
    sound_play.play()


 # simple function to check for upgrades and buff the player
def check_upgrade(current_maze, next_row, next_col, player, upgrade, item_track, upgrade_list):
    if current_maze[next_row][next_col] == upgrade.glyph:
        playsound("sounds/item.mp3")
        item_track = upgrade
        if upgrade.type == "armor":
            player.defe += upgrade.stat
        else:
            player.atk += upgrade.stat
        current_maze[next_row][next_col] = " "

        upgrade_list.remove((next_row, next_col))

    return item_track

#checks if a trap is placed there, if yes performs damaging and plays sound
def check_trap(current_maze, traps_coords, entity, track_trap):
    for traps in traps_coords:
        (trow, tcol) = traps
        if trow == entity.row and tcol == entity.col:
            track_trap = True
            playsound("sounds/trap.mp3")
            random_stat = random.randrange(1,4)
            random_number = random.randrange(1,5)
            traps_coords.remove(traps)
            current_maze[trow][tcol] = "^"
            if random_stat == 1:
                entity.atk = max(1, entity.atk - random_number)
            elif random_stat == 2:
               entity.defe = max(1, entity.defe - random_number)
            else:
                entity.hp -= random_number

    return track_trap



#Astar algo, holy moly that was painful.
def astar(current_maze, start, end):
    start_node = Node(start)
    end_node = Node(end)

    open_list = []
    closed_set = set()
    g_costs = {start: 0}

    open_list.append(start_node)
    while len(open_list) > 0:
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.fcost < current_node.fcost:
                current_node = item
                current_index = index

        open_list.pop(current_index)
        closed_set.add(current_node.position)

        #if goal found make path again
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.insert(0, current.position)  #insert pos 0, the node with lowest cost
                current = current.parent
            return path

        #gen the childs
        row = current_node.position[0]
        col = current_node.position[1]
        neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row , col + 1)]

        for next_pos in neighbors:
            if not ( 0 <= next_pos[0] < len(current_maze) and 0 <= next_pos[1] < len(current_maze[0])): #boundaries check
                continue
            if current_maze[next_pos[0]][next_pos[1]] in ("█", "┃"): #check if its a wall
                continue

            if next_pos in closed_set:
                continue

            tentative_g = current_node.gcost + 1

            if tentative_g >= g_costs.get(next_pos, float('inf')):
                continue

            neighbor_node = Node(next_pos, current_node)
            neighbor_node.gcost = tentative_g

            #manhatten distance stuff and calculate costs
            neighbor_node.hcost = abs(neighbor_node.position[0] - end_node.position[0]) + abs(neighbor_node.position[1] - end_node.position[1])
            neighbor_node.fcost = neighbor_node.gcost + neighbor_node.hcost

            g_costs[next_pos] = tentative_g
            open_list.append(neighbor_node)

    return None
