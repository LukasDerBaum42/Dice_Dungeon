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

# from src.player import *
# from src.enemy import *
# from src.dungeon import *
# from src.afiliation import *
# from src.fight import *



class Afiliations:
    def __init__(
        self, els: list[str], stats: dict[str, int] = {}, bonus: int = 0
    ) -> None:
        self.afi = {}
        self.temp_afi = {}
        self.len = len(self.afi)
        self.bonus = bonus
        self.main_afi = ""
        for i in els:
            self.afi[i] = 100
        add_l, sub_l, unblock_l = self.split_new(stats)
        # print(add_l)
        # print(sub_l)
        # print(unblock_l)
        # print(self)
        self.bonus = self.sub(stats, sub_l, unblock_l, self.bonus)
        self.bonus = self.add(stats, add_l, unblock_l, self.bonus)
        self.fin_afi = {}
        self.add_temp()

    def change(self, stats, bonus):
        self.bonus += bonus
        add_l, sub_l, unblock_l = self.split_new(stats)
        # print(add_l)
        # print(sub_l)
        # print(unblock_l)
        # print(self)
        self.bonus = self.sub(stats, sub_l, unblock_l, self.bonus)
        self.bonus = self.add(stats, add_l, unblock_l, self.bonus)
        self.add_temp()

    def update_temp_afi(self, stats):
        self.temp_afi = stats
        self.add_temp()

    def add_temp(self):
        for i in self.afi:
            if i in self.temp_afi:
                self.fin_afi[i] = self.afi[i] + self.temp_afi[i]
            else:
                self.fin_afi[i] = self.afi[i]
        self.main_afi = max(self.fin_afi, key=self.fin_afi.get)

    def split_new(self, stats: dict[str, int]):
        add_l = []
        sub_l = []
        unblock_l = []
        for i in self.afi:
            if i in stats:
                if self.afi[i] > stats[i]:
                    sub_l.append(i)
                elif self.afi[i] < stats[i]:
                    add_l.append(i)
            else:
                unblock_l.append(i)
        return add_l, sub_l, unblock_l

    def sub(self, stats, sub_l, unblock_l, bonus: int = 0):
        for i in sub_l:
            temp = self.afi[i] - stats[i]
            bonus += temp
            self.afi[i] = stats[i]

        # print(self)
        return bonus

    def compute_subtraction(
        self, afi: dict[str, int], unblock_l: list[str], needed: int
    ):
        keys = [k for k in unblock_l if k in afi and afi[k] > 0]
        result = {k: 0 for k in keys}

        remaining = needed
        active = keys.copy()

        while remaining > 0 and active:
            share = max(1, remaining // len(active))
            new_active = []

            for k in active:
                take = min(share, afi[k] - result[k])
                result[k] += take
                remaining -= take

                if result[k] < afi[k]:
                    new_active.append(k)

                if remaining == 0:
                    break

            active = new_active

        return result, remaining

    def add(self, stats, add_l, unblock_l, bonus: int = 0):
        needed = 0
        for i in add_l:
            temp = stats[i] - self.afi[i]
            needed += temp
        # print(needed)
        needed -= bonus
        if needed > 0:
            # print("not enough points")
            sub_ele, missing = self.compute_subtraction(self.afi, unblock_l, needed)
            for i in sub_ele:
                self.afi[i] -= sub_ele[i]
                bonus += sub_ele[i]

        for i in add_l:
            temp = stats[i] - self.afi[i]
            if bonus >= temp:
                bonus -= temp
            elif bonus < temp:
                temp = int(bonus)
                # print(temp,bonus)
                bonus = 0
                # print(temp,bonus)
            self.afi[i] = self.afi[i] + temp

        # print(self)
        return bonus

    def sum(self):
        sum = 0
        for i in self.afi:
            sum += self.afi[i]
        return sum

    # def __repr__(self) -> str:
    #    out = ''
    #    for i in self.afi:
    #        out += f'{i} = {self.afi[i]}  '
    #
    #    return out

