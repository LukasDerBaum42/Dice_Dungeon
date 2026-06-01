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




class Trape:
    def __init__(self, x, y, type, room):
        self.x = x
        self.y = y
        self.show = False
        self.coldown = 0
        self.type = type
        self.room = room

    def triger(self, player):
        clear()
        Graphic.print_titelbar("Trape", 16)
        temp = f"{self.type}"
        while len(temp) < 30:
            temp += " "
            if len(temp) < 30:
                temp = " " + temp
        printr(temp)
        printr(wrap_text(GTD.traps[self.type]["text"], 30))

        art_t = GTD.trap_art
        art_p = GTD.fight_art
        player_art = art_p["player"]
        trap_art = art_t[self.type]
        for i in range(len(trap_art["art"])):
            temp = "      "
            if i >= trap_art["player"][1] and (i - trap_art["player"][1]) < len(
                player_art
            ):
                for j in range(trap_art["player"][0]):
                    temp += " "
                temp += player_art[i - trap_art["player"][1]]
            temp += trap_art["art"][i]
            Graphic.fixed_width(temp, 28)
            printr(temp)
        if self.type == "Mimic":
            inputT("\nPress Enter to return...")
            level = self.room.level
            enemy = Enemy("Mimic", level, None,None, 0, 0)
            player = fight_loop(player, enemy, False)
        else:
            inputT("\nPress Enter to return...")
            if GTD.traps[self.type]["damage_type"] == 0:
                player.hp -= GTD.traps[self.type]["damage"]
            elif GTD.traps[self.type]["damage_type"] == 1:
                base = GTD.traps[self.type]["damage"]
                roll = Graphic.roll_dice(1, 6, 0)
                damage = int((base / 5) * (6 - roll))
                player.hp -= damage
            elif GTD.traps[self.type]["damage_type"] == 2:
                base = GTD.traps[self.type]["damage"]
                base = int((player.max_hp / 100) * base)
                roll = Graphic.roll_dice(1, 6, 0)
                damage = int((base / 5) * (6 - roll))
                player.hp -= damage
        self.show = True
        self.coldown = 10
