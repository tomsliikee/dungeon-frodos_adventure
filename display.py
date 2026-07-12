import os
import time
import readchar


from colorist import BgColor, Color, bg_blue, red, yellow, cyan, green
from colorist.model.foreground.bright_color import BrightColor
from colorist.print.foreground.color import magenta
from classes import Player
from logic import playsong

# get the terminal info
terminal = os.get_terminal_size()
term_cols = terminal.columns
term_rows = terminal.lines

def clear():
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")

def press_any_key(text="Press any key to continue..."):
    print("\n" * 2)
    yellow(text.center(term_cols))
    readchar.readkey()

#tutorial! Was.... fun but tedious hahaha
def run_tutorial():
    terminal = os.get_terminal_size()
    term_cols = terminal.columns

    clear()

    print("\n")
    yellow("One Ring to rule them all, One Ring to find them,".center(term_cols))
    yellow("One Ring to bring them all, and in the darkness bind them,".center(term_cols))
    yellow("In the Land of Mordor where the Shadows lie.".center(term_cols))
    print("\n")
    green("Frodo (@), your dream leads you into the perilous Dungeon Arena!".center(term_cols))
    green("Your opponent, the Mouth of Sauron (*), prepares on the other side...".center(term_cols))
    print("\n")
    yellow("You must grow stronger, breach the Arena, and defeat the evil!".center(term_cols))

    press_any_key("Press any key to learn the controls...")

    clear()
    cyan("--- CHAPTER I: CONTROLS & LAYOUT ---".center(term_cols))
    print("\n")
    print("The battlefield is divided into three regions:".center(term_cols))
    print("Left Maze (Frodo) | Central Arena (░) | Right Maze (AI Opponent)".center(term_cols))
    print("\n")
    yellow("MOVEMENT:".center(term_cols))
    print("W  -> Move UP".center(term_cols))
    print("A  -> Move LEFT".center(term_cols))
    print("S  -> Move DOWN".center(term_cols))
    print("D  -> Move RIGHT".center(term_cols))
    print("Q  -> QUIT the game immediately".center(term_cols))
    print("\n")
    print("Every step counts. In the status line below you will see your stats:".center(term_cols))
    green("Level | Health Points (HP) | Attack (ATK) | Defense (DEF)".center(term_cols))

    press_any_key("Press any key to see items and hazards...")

    clear()
    cyan("--- CHAPTER II: TREASURES & SHADOWS OF MORDOR ---".center(term_cols))
    print("\n")
    yellow("THE ITEMS:".center(term_cols))
    print("Collect relics to permanently boost your stats:".center(term_cols))
    print("(  -> Weapon (e.g. Anduril): Boosts your Attack (ATK)".center(term_cols))
    print("[  -> Armor (Mithril): Boosts your Defense (DEF)".center(term_cols))
    print("\n")
    red("THE BEASTS OF SAURON:".center(term_cols))
    print("Smaug (D), Gremlins (G), Gnomes (N), Jellies (J) and other mobs lurk in the dark.".center(term_cols))
    print("Once you enter their sense range, they will hunt you down!".center(term_cols))
    print("\n")
    yellow("THE HIDDEN TRAPS (^):".center(term_cols))
    print("Invisible traps lie on the ground. Once stepped on, they trigger".center(term_cols))
    print("and randomly reduce your HP, Attack (ATK), or Defense (DEF)!".center(term_cols))

    press_any_key("Press any key to learn combat & arena doors...")

    clear()
    cyan("--- CHAPTER III: COMBAT, ARENA & VICTORY ---".center(term_cols))
    print("\n")
    yellow("COMBAT:".center(term_cols))
    print("Triggered when you step on a mob's cell (or they step on yours).".center(term_cols))
    print("Whoever makes the move attacks first! Damage = max(ATK - DEF, 1).".center(term_cols))
    print("Every victory rewards you with a level-up: +10 HP, +1 ATK, +1 DEF!".center(term_cols))
    print("\n")
    yellow("THE ARENA DOORS:".center(term_cols))
    print("In the middle lies the Arena (░). You can only enter through your blue door.".center(term_cols))
    print("The first player to enter the Arena gets a bonus level-up!".center(term_cols))
    print("Your door closes behind you and opens your opponent's door to all characters.".center(term_cols))
    print("\n")
    green("VICTORY: Defeat the Mouth of Sauron (*) by reducing their HP to 0!".center(term_cols))
    red("DEFEAT: If your HP drops to 0, Middle-earth falls into darkness...".center(term_cols))

    press_any_key("Are you ready, Frodo? Press any key to begin the game!")
    clear()

#print the logo
def print_intro_logos():
       logo1 = r"""
    ___              _
   / __\ __ ___   __| | ___  ___
   / _\| '__/ _ \ / _` |/ _ \/ __|
   / /  | | | (_) | (_| | (_) \__ \
   \/   |_|  \___/ \__,_|\___/|___/
   """
       logo2 = r"""
    _       _                 _
   /_\   __| |_   _____ _ __ | |_ _   _ _ __ ___
   //_\\ / _` \ \ / / _ \ '_ \| __| | | | '__/ _ \
   /  _  \ (_| |\ V /  __/ | | | |_| |_| | | |  __/
   \_/ \_/\__,_| \_/ \___|_| |_|\__|\__,_|_|  \___|
   """
       for line in logo1.strip("\n").split("\n"):
           green(line.center(term_cols))
       for line in logo2.strip("\n").split("\n"):
           green(line.center(term_cols))

# prints the entire start screen of the game
def start(name_var):
    print("Welcome to the".center(term_cols))
    playsong("sounds/tutorial.mp3")
    print_intro_logos()

    print("\n")
    yellow("Ahhhh.... Welcome Frodo! You did fall asleep there!".center(term_cols))
    yellow("We are in a dream world full of wonderfull things!".center(term_cols))
    yellow("Do you want to have a little tutorial before we start?\n".center(term_cols))
    answer = input("\n(Answer yes / no, depending of your choice): ")

    if answer.lower() == "yes":
        run_tutorial()
    # looooooooooooooooooading

    list = ["█"]
    for i in range(1, 20):
        clear()
        list.append("█")
        print_intro_logos()
        print()
        print()
        print("Loading.....".center(term_cols))
        print()
        print("".join(list).center(term_cols))
        time.sleep(0.1)  # 0.5
    print("\nDone!")


# print the maze and the user movement or the cell block behind the player depending on the location of the player
def display_maze(current_maze, player_row, player_col, playersymbol, anti_row, anti_col, antisymbol):
    for r_idx, row in enumerate(current_maze):
        for c_idx, cell in enumerate(row):
            if r_idx == player_row and c_idx == player_col:
                print(f"{Color.GREEN}{playersymbol}{Color.OFF}", end="")
            elif r_idx == anti_row and c_idx == anti_col:
                print(f"{Color.MAGENTA}{antisymbol}{Color.OFF}", end="")
            else:
                if cell == "█":
                    print(f"{Color.YELLOW}{cell}{Color.OFF}", end="")
                elif cell == "D":
                    print(f"{BrightColor.RED}{cell}{Color.OFF}", end="")
                elif cell == "[":
                    print(f"{Color.CYAN}{cell}{Color.OFF}", end="")
                elif cell == "(":
                    print(f"{BrightColor.CYAN}{cell}{BrightColor.OFF}", end="")
                elif cell == "J":
                    print(f"{BrightColor.MAGENTA}{cell}{BrightColor.OFF}", end="")
                else:
                    print(cell, end="")
        print()

#prints the stats of the player for game over or win!
def stats(player):
    yellow(f"Player {player.name} did some truly wonderful (or bad) things!".center(term_cols))
    print()
    print(f"The player slayed {player.slayed_mobs} mobs.".center(term_cols))
    print("His stats where: ".center(term_cols))
    print(f"Level: {player.level}".center(term_cols))
    print(f"Health: {player.hp}".center(term_cols))
    print(f"Attack: {player.atk}".center(term_cols))
    print(f"Defense: {player.defe}".center(term_cols))


# if player presses q or dies this function is used
def gameover(player, stepped_mob):
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")

    playsong("sounds/game_over_sadness.mp3")

    for _ in range(term_rows // 7):
        print("\n")

    if stepped_mob is None:
        print(f"{BgColor.BLUE}", end="")
        print("GAME OVER | YOU QUIT THE GAME".center(term_cols))
        print(f"{BgColor.OFF}")
    else:
        print(f"{BgColor.RED}", end="")
        print("GAME OVER | YOU DIED".center(term_cols))
        print(f"{BgColor.OFF}")
        red(f"Frodo stepped on a {stepped_mob.name} and was slayed by it (Please insert the qoute of the white shores from gandalf).".center(term_cols))
        print()
        print()

    stats(player)

    for _ in range(term_rows // 6):
        print("\n")

def game_won(player):
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")

    playsong("sounds/win2.mp3")

    for _ in range(term_rows // 7):
        print("\n")

    print(f"{BgColor.GREEN}", end="")
    print("GAME WON | YOU WON THE GAME... but the fight isnt over".center(term_cols))
    print(f"{BgColor.OFF}")
    red(f"Frodo slayed the enemy and won! (or maybe he offed himself).".center(term_cols))
    print()
    print()

    stats(player)

    for _ in range(term_rows // 6):
        print("\n")


#prints the statusline of player 1 and player 2, the AI, in the last line
def print_statusline(player, ai, stepped_mob, track_item, track_trap, track_item2, stepped_mob2, track_trap2):
    current_term_cols = os.get_terminal_size().columns
    player1 = f"{player.glyph} {player.name} Level {player.level} HP: {player.hp} ATK: {player.atk} DEF: {player.defe}"
    playerai = f"{ai.glyph} {ai.name} Level {ai.level} HP: {ai.hp} ATK: {ai.atk} DEF: {ai.defe}"
    length_middle = current_term_cols - len(player1) - len(playerai) - 7
    if length_middle < 0:
        length_middle = 0
    x = " "

    print(f"{BgColor.GREEN}P1:", end="")
    print(player1, end="")
    print(f"{BgColor.OFF}", end="")

    print(f"{length_middle * x}{BgColor.MAGENTA}P2:", end="")
    print(playerai, end="")
    print(f"{BgColor.OFF}")

    if stepped_mob is not None:
        red(f"{player.name} got in a fight with {stepped_mob.name}, and he won! +1 Level and stats boost!".center(term_cols))
    elif track_item is not None:
        cyan(f"{player.name} found a {track_item.name} and got an upgrade of +{track_item.stat}!".center(term_cols))
    elif track_trap:
        yellow(f"{player.name} stepped on a trap and was damaged!".center(term_cols))
    elif track_item2 is not None:
        cyan(f"{ai.name} found a {track_item2.name} and got an upgrade of +{track_item2.stat}!".center(term_cols))
    elif stepped_mob2 is not None:
        red(f"{ai.name} got in a fight with {stepped_mob2.name}, and he won! +1 Level and stats boost!".center(term_cols))
    elif track_trap2:
        yellow(f"{ai.name} stepped on a trap and was damaged!".center(term_cols))
