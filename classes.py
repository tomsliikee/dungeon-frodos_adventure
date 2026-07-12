class Entity:
    def __init__(self, glyph, name, hp, atk, defe, sense, row=0, col=0):
        self.glyph = glyph
        self.name = name
        self.hp = hp
        self.atk = atk
        self.defe = defe
        self.sense = sense
        self.row = row
        self.col = col


class Item:
    def __init__(self, glyph, name, type, stat):
        self.glyph = glyph
        self.name = name
        self.type = type
        self.stat = stat

#pathfinding class
class Node:
    def __init__(self, position, parent = None):
        self.position = position
        self.parent = parent
        self.gcost = 0 #start cost
        self.hcost = 0 #heuristic cost
        self.fcost = 0 #g + h cost thing

    def __eq__(self,other):
        return self.position == other.position



class Trap:
    def __init__(self, glyph, name, type, color, damage):
        self.glyph = glyph
        self.name = name
        self.type = type
        self.color = color
        self.damage = damage


class Player(Entity):
    def __init__(self, glyph, name, hp, atk, defe, sense, level, slayed_mobs, row=0, col=0):
        super().__init__(
            glyph, name, hp, atk, defe, sense, row, col
        )  # skips the new self initialise part
        self.level = level
        self.slayed_mobs = slayed_mobs

    def print(self):
        print(
            f"{self.glyph} {self.name} Level {self.level} HP: {self.hp} ATK: {self.atk} DEF: {self.defe}",
            end="",
        )

    def level_up(self):
        self.level += 1
        self.atk += 1
        self.hp += 10
        self.defe += 1


class Weapon(Item):
    def __init__(self, glyph, name, type, stat):
        super().__init__(glyph, name, type, stat)


class Armor(Item):
    def __init__(self, glyph, name, type, stat):
        super().__init__(glyph, name, type, stat)
