import math
import os
import random
import time
from random import Random, choice, randint
#from tkinter import TclError

from data import Game_text_data as GTD
from ..graphic import Graphic
from ..Items import GameItem

from ..dungeon import Room
from ..player import Player
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

        self.item: GameItem | None | str = self.gen_item()

    def gen_item(self) -> GameItem | None | str:
        layer: str = self.room.layer
        posbil_types: dict[str, int] = GTD.layers[layer]["cheasts"]
        rarety_temp_1: int = 0
        rarety_temp_2: int = 0
        rand_num: int = random.randint(1, 100)
        cheast_type: None | str = None
        for j in posbil_types:
            p: int = posbil_types[j]
            Graphic.printr(p)
            rarety_temp_1: int = rarety_temp_2
            rarety_temp_2 += p
            if (rarety_temp_1 < rand_num) and (rand_num <= rarety_temp_2):
                cheast_type = j
                break
        del rarety_temp_1, rarety_temp_2
        Graphic.printr(posbil_types)
        if cheast_type is None:
            return None
        
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
                Graphic.printr(f"You got {self.gold}")
            elif isinstance(self.item, GameItem):
                player.inventory.append(self.item)
                Graphic.printr(f"You got {self.item.name}")
            self.is_open = True
            _ = Graphic.inputT("\nPress Enter to return...")

