import math
import os
import random
import time
from random import Random, choice, randint
#from tkinter import TclError

import Game_text_data as GTD
import Graphic
from Graphic import clear, inputT, printr, wait
from Items import GameItem
# from src import player, enemy, dungeon, afiliation, fight
# from src.player import *
# from src.enemy import *
# from src.dungeon import *
# from src.afiliation import *
# from src.fight import *


class Cheast:
    def __init__(self, room: Room, x: int, y: int):
        self.x: int = x
        self.y: int = y
        self.room: Room = room
        self.gold: int = 3
        self.is_open: bool = False

        self.item: GameItem | str = self.gen_item()

    def gen_item(self) -> GameItem | None:
        layer: str = self.room.layer
        posbil_types: dict[str, int] = GTD.layers[layer]["cheasts"]
        rarety_temp_1: int = 0
        rarety_temp_2: int = 0
        rand_num: int = random.randint(1, 100)
        for j in posbil_types:
            p: int = posbil_types[j]
            printr(p)
            rarety_temp_1: int = rarety_temp_2
            rarety_temp_2 += p
            if (rarety_temp_1 < rand_num) and (rand_num <= rarety_temp_2):
                cheast_type: str = j
                break
        del rarety_temp_1, rarety_temp_2
        printr(posbil_types)
        cheast = GTD.cheast[cheast_type]
        level = self.room.level + random.randint(*cheast["level"])
        rarety_temp_1 = 0
        rarety_temp_2 = 0
        rand_num = random.randint(0, 100)
        rarety = "common"
        for j in cheast["rarety"]:
            p = cheast["rarety"][j]
            rarety_temp_1 = rarety_temp_2
            rarety_temp_2 += p
            if (rarety_temp_1 < rand_num) and (rand_num <= rarety_temp_2):
                rarety = j
                break

        rarety_temp_1 = 0
        rarety_temp_2 = 0
        rand_num = random.randint(0, 100)
        item_type = "Gold"
        for j in cheast["item type"]:
            p = cheast["item type"][j]
            # printr(p)
            rarety_temp_1 = rarety_temp_2
            rarety_temp_2 += p
            if (rarety_temp_1 < rand_num) and (rand_num <= rarety_temp_2):
                item_type = j
                break

        if item_type == "Gold":
            self.gold += level
            return item_type
        else:
            item: GameItem = GameItem(rarety, item_type, level)
            return item

    def give_player(self, player: Player):
        if not self.is_open:
            if self.item == "Gold":
                player.gold += self.gold
                printr(f"You got {self.gold}")
            else:
                player.inventory.append(self.item)
                printr(f"You got {self.item.name}")
            self.is_open = True
            _ = inputT("\nPress Enter to return...")

