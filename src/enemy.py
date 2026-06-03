import math
import os
import random
import time
from random import Random, choice, randint
#from tkinter import TclError

from data import Game_text_data as GTD
from .graphic import Graphic

from .Items import GameItem
from .afiliation import Afiliations
# from .room import Room
# from .player import update_player
from gamestate import GameState
from . import dungeon as Mdun
# from src.player import *
# from src.enemy import *
# from src.dungeon import *
# from src.afiliation import Afiliations
# from src.fight import *



class Enemy:
    def __init__(
        self, mob: str, level: int, room, spawner, x: int, y: int, is_boss: bool = False
    ) -> None:
        self.room: Mdun.Room = room
        self.mob: str = mob
        self.is_boss: bool = is_boss
        self.x: int = x
        self.y: int = y
        self.is_del: bool = False
        self.level: int = level
        self.spawner = spawner
        if is_boss:
            stats: dict[str, int] = GTD.bosses[mob]["stats"]
            self.ele_afi = Afiliations(GTD.ele_list, GTD.bosses[mob]["affiliations"])
        else:
            stats: dict[str, int] = GTD.enemy_cls[mob]["stats"]
            self.ele_afi = Afiliations(GTD.ele_list, GTD.enemy_cls[mob]["affiliations"])
        self.max_move: int = stats["max_move"]
        self.min_move: int = stats["min_move"]
        self.max_hp: int = stats["max_hp"]
        self.max_mp: int = stats["max_mp"]
        self.atk: int = stats["atk"]
        self.sp_atk: int = stats["sp_atk"]
        self.def_: int = stats["def_"]
        self.sp_def: int = stats["sp_def"]
        self.crit_chance: int = stats["crit_chance"]
        self.crit_bonus: int = stats["crit_bonus"]
        self.xp: int = stats["xp"]
        self.gold: int = stats["gold"]
        self.wapon_ele = None
        self.level_up()
        self.hp: int = self.max_hp
        self.mp: int = self.max_mp
        self.wapon_afi = Afiliations(GTD.wappon_sub_typse)
        self.get_attack_stats()
        self.items: list[GameItem] = []
        self.get_items()
        self.equiped_items = self.items
        self.item_stats_add()
        self.wapons_used = {}
        self.ele_afi_used = {}

    def ele_afi_up(self, afi):
        if afi in self.ele_afi_used:
            self.ele_afi_used[afi] += 1
            if self.ele_afi_used[afi] == 10:
                new_stets = {f"{afi}": self.ele_afi.afi[afi] + 10}
                self.ele_afi.change(new_stets, 5)
                self.ele_afi_used[afi] = 0
        else:
            self.ele_afi_used[afi] = 1

    def level_up(self) -> None:
        self.max_hp += 3 * (self.level - 1)
        self.max_mp += 3 * (self.level - 1)
        self.atk += 1 * (self.level - 1)
        self.sp_atk += 1 * (self.level - 1)
        self.def_ += 1 * (self.level - 1)
        self.sp_def += 1 * (self.level - 1)
        self.gold += 2 * (self.level - 1)
        self.xp += 2 * (self.level - 1)

    def item_stats_add(self):
        self.max_hp_items: int = 0
        self.max_mp_items: int = 0
        self.atk_items: int = 0
        self.sp_atk_items: int = 0
        self.def_items: int = 0
        self.sp_def_items: int = 0
        self.crit_chance_items: int = 0
        self.crit_bonus_items: int = 0
        for item in self.equiped_items:
            if item.main_type == "wareable":
                self.max_hp_items += item.max_hp
                self.max_mp_items += item.max_mp
                self.atk_items += item.atk
                self.sp_atk_items += item.sp_atk
                self.def_items += item.def_
                self.sp_def_items += item.sp_def
                self.crit_chance_items += item.crit_chance
                self.crit_bonus_items += item.crit_bonus
            elif item.main_type == "wapon":
                afi = self.wapon_afi.afi[item.sub_type] / 100
                self.wapon_ele = item.ele
                self.max_hp_items += int(item.max_hp * afi)
                self.max_mp_items += int(item.max_mp * afi)
                self.atk_items += int(item.atk * afi)
                self.sp_atk_items += int(item.sp_atk * afi)
                self.def_items += int(item.def_ * afi)
                self.sp_def_items += int(item.sp_def * afi)
                self.crit_chance_items += int(item.crit_chance * afi)
                self.crit_bonus_items += int(item.crit_bonus * afi)

            self.hp = self.max_hp + self.max_hp_items
            self.mp = self.max_mp + self.max_mp_items

    def get_items(self):
        if self.is_boss:
            posbl_items = GTD.bosses[self.mob]["Items"]
        else:
            posbl_items = GTD.enemy_cls[self.mob]["Items"]
        for i in posbl_items:
            if random.randint(1, 100) <= posbl_items[i]["chance"]:
                try:
                    item_level = self.level + random.randint(
                        posbl_items[i]["level"][0], posbl_items[i]["level"][1]
                    )
                    if item_level <= 0:
                        item_level = 1
                    item = GameItem("unique", i, item_level, posbl_items[i]["name"])
                    self.items.append(item)
                except:
                    rarety_temp_1 = 0
                    rarety_temp_2 = 0
                    rand_num = random.randint(0, 100)
                    for j in posbl_items[i]["rarety"]:
                        rarety_temp_1 = rarety_temp_2
                        rarety_temp_2 += posbl_items[i]["rarety"][j]
                        if (rarety_temp_1 < rand_num) and (rand_num <= rarety_temp_2):
                            item_level = self.level + random.randint(
                                posbl_items[i]["level"][0], posbl_items[i]["level"][1]
                            )
                            if item_level <= 0:
                                item_level = 1
                            item = GameItem(j, i, item_level)
                            self.items.append(item)

    def get_attack_stats(self):
        self.attacks_used = {}
        attacks = []
        self.attacks = []
        for _ in range(4):
            attack_temp = []
            if self.is_boss:
                for i in GTD.bosses[self.mob]["Attacks"]:
                    if i not in attacks:
                        for _ in range(GTD.bosses[self.mob]["Attacks"][i]):
                            attack_temp.append(i)
                attacks.append(random.choice(attack_temp))
            else:
                for i in GTD.enemy_cls[self.mob]["Attacks"]:
                    if i not in attacks:
                        for _ in range(GTD.enemy_cls[self.mob]["Attacks"][i]):
                            attack_temp.append(i)
                attacks.append(random.choice(attack_temp))
        for i in attacks:
            self.attacks.append(GTD.attacks[i])
            self.attacks_used[i] = 0

    def move(self, player, room, dungeon):
        rand = random.randint(self.min_move, self.max_move)
        enemy_pos = room.get_enemy_pos()
        player_pos : tuple[int, int] = player.x, player.y
        grid = room.map
        path = self.find_path(grid, enemy_pos, player_pos)
        if len(path) < rand:
            rand = len(path)
        for i in range(rand):
            Graphic.printr(path[i])
            if path[i] == "N":
                self.y -= 1
            elif path[i] == "S":
                self.y += 1
            if path[i] == "W":
                self.x -= 1
            elif path[i] == "E":
                self.x += 1
            update_player(player, room)
            Graphic.game_menu(player, dungeon,GAME_STATE,is_enemy_turn=True)
            #Graphic.update()
            Graphic.wait(0.2)

    def find_path(
        self,
        grid: list[list[str]],
        enemy_pos: list[tuple[int, int]],
        player_pos: tuple[int, int],
    ):
        from collections import deque

        target: tuple[int, int] = (player_pos[0], player_pos[1])
        start: tuple[int, int] = (self.x, self.y)
        blocked: set[tuple[int, int]] = set((e[0], e[1]) for e in enemy_pos)

        dirs = [(0, -1, "N"), (0, 1, "S"), (-1, 0, "W"), (1, 0, "E")]

        q = deque([start])
        prev = {start: None}
        prev_dir = {}
        steps = 0
        while q and steps < 1000:
            x, y = q.popleft()
            if (x, y) == target:
                break
            for dx, dy, d in dirs:
                nx, ny = x + dx, y + dy
                try:
                    if grid[ny][nx] == "#":
                        continue
                except:
                    pass
                if (nx, ny) in blocked:
                    continue
                if (nx, ny) in prev:
                    continue
                prev[(nx, ny)] = (x, y)
                prev_dir[(nx, ny)] = d
                q.append((nx, ny))

        if target not in prev:
            return []

        path = []
        cur = target
        steps = 0
        while cur != start and steps < 1000:
            path.append(prev_dir[cur])
            cur = prev[cur]
        path.reverse()
        return path

    def __repr__(self):
        return (
            f"HP={self.hp} MP={self.mp} Max HP={self.max_hp} Max MP={self.max_mp}\n"
            f"Atk={self.atk} SP Atk={self.sp_atk} Def={self.def_} SP Def={self.sp_def}\n"
            f"Crit Chance={self.crit_chance} Crit Bonus={self.crit_bonus} XP={self.xp}\n"
            f"Min Move={self.min_move} Max Move={self.max_move} Gold={self.gold}\n"
            f"Items={self.items}"
        )

    def del_(self) -> None:
        if self.is_boss:
            self.room.map[self.y][self.x] = "s"
        self.x = -1
        self.y = -1
        self.is_del = True
        self.spawner.is_spawned = False
        self.spawner.cool_down = 10
        try:
            self.room.enemys.remove(self.room)
        except:
            pass
        del (
            self.room,
            self.spawner,
            self.mob,
            self.level,
            self.max_move,
            self.min_move,
            self.max_hp,
            self.max_mp,
            self.atk,
            self.sp_atk,
            self.def_,
            self.sp_def,
            self.crit_chance,
            self.crit_bonus,
            self.xp,
            self.gold,
            self.hp,
            self.mp,
            self.items,
        )



def enemy_move(dungeon, player):
    room = dungeon.rooms[dungeon.room]
    # printr('enemys in room', len(room.enemys))
    steck = []
    for enemy in room.enemys:
        if enemy.is_boss:
            pass
        else:
            steck.append(enemy)
    while len(steck) > 0:
        if player.hp <= 0:
            break
        enemy: Enemy = steck.pop(0)
        if enemy.is_del:
            try:
                enemy.spawner.is_spawnd = False
                room.enemys.remove(enemy)
            except:
                continue
        else:
            enemy.move(player, room, dungeon)
        try:
            if enemy.is_del:
                enemy.spawner.is_spawnd = False
                room.enemys.remove(enemy)
                del enemy
        except:
            continue


def update_player(player, room):
    enemys: list[Enemy] = room.enemys
    traps: list[Trape] = room.traps
    cheasts: list[Cheast] = room.cheasts
    shops: list[Merchent] = room.shops
    px, py = player.x, player.y
    for e in enemys:
        Graphic.update()
        if e.x == px and e.y == py:
            if player.moves < 0:
                fight_loop(player, e, False)
            else:
                fight_loop(player, e, True)
            if e.is_boss:
                player.x, player.y = player.last_pos
            e.del_()
    for t in traps:
        Graphic.update()
        if t.coldown > 0:
            t.coldown -= 1
            continue
        elif t.x == px and t.y == py:
            t.triger(player)
    for c in cheasts:
        Graphic.update()
        if c.x == px and c.y == py:
            c.give_player(player)
    for m in shops:
        Graphic.update()
        if m.x == px and m.y == py:
            m.interact_player(player)
            player.x, player.y = player.last_pos