from bdb import Breakpoint
import math
import os
import random
import time
from ast import Return
from random import Random, choice, randint
from tkinter import TclError

import Game_text_data as GTD
import Graphic
from Graphic import clear, inputT, printr, wait
from Items import GameItem

# from collections import deque

OPPOSITE = {"top": "bottom", "bottom": "top", "left": "right", "right": "left"}
SIDES = ["top", "bottom", "left", "right"]


def wrap_text(text: str, width: int = 72):
    words: list[str] = text.split()
    lines: list[str] = []
    current_line = " "


def p_chois(opption: dict[str, int]) -> str:
    changs1 = 0
    changs2 = 0
    rand_num = random.randint(1, 100)
    ops: list[str] = []
    out = None
    for j in opption:
        ops.append(j)
        p = opption[j]
        changs1 = changs2
        changs2 += p
        if (changs1 < rand_num) and (rand_num <= changs2):
            out = j
            break
    if out == None:
        out: str = str(Random.choice(ops))
    return out


class Player:
    def __init__(self, cls: str):
        self.cls: str = cls

        stats: dict[str, int] = GTD.player_cls[cls]["stats"]
        self.moves: int = -2
        self.x: int = 2
        self.y: int = 2
        self.last_pos: list[int] = [self.x, self.y]
        self.level: int = 1
        self.xp: int = 0
        self.max_xp: int = self.next_level_xp(self.level)
        self.gold: int = 10
        self.inventory: list[GameItem] = []
        self.equiped_items: list[GameItem] = []
        self.favorit: list[GameItem] = []
        self.equipt_slots: dict[str, list[bool | GameItem]] = {
            "wappon": [False, None],
            "helmet": [False, None],
            "chestplate": [False, None],
            "pants": [False, None],
            "boots": [False, None],
            "sheald": [False, None],
        }
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
        self.wapon_ele = None
        self.add_to_inv(GameItem(*GTD.player_cls[cls]["item"]))
        self.attacks: list[str] = []
        self.attacks_used: dict[str, int] = {}
        for i in GTD.player_cls[cls]["attacks"]:
            self.attacks.append(GTD.attacks[i])
            self.attacks_used[i] = 0
        self.ele_afi = Afiliations(
            GTD.ele_list, GTD.player_cls[cls]["affiliations"]["elements"]
        )
        self.wapon_afi = Afiliations(
            GTD.wappon_sub_typse, GTD.player_cls[cls]["affiliations"]["wapons"]
        )

        self.hp: int = self.max_hp
        self.mp: int = self.max_mp
        self.item_stats_add()
        self.wapons_used = {}
        self.ele_afi_used = {}

    def ele_afi_up(self, afi):
        if afi:
            if afi in self.ele_afi_used:
                self.ele_afi_used[afi] += 1
                if self.ele_afi_used[afi] == 10:
                    new_stets = {f"{afi}": self.ele_afi.afi[afi] + 10}
                    self.ele_afi.change(new_stets, 5)
                    self.ele_afi_used[afi] = 0
            else:
                self.ele_afi_used[afi] = 1

    def next_level_xp(self, level: int):
        return (math.floor((((math.log(level**2, 10)) ** 2) + 1) * 5)) * 3

    def roll_for_move(self):
        roll = Graphic.roll_dice(self.min_move, self.max_move)
        self.moves = roll
        return roll

    def add_to_inv(self, item: GameItem):
        self.inventory.append(item)

    def equip_item(self, item: GameItem):
        if item.sub_type in self.equipt_slots:
            slot: str = item.sub_type
        elif item.sub_type == "consumable":
            slot = item.sub_type
        else:
            slot = "wappon"
        if item in self.equiped_items:
            self.equiped_items.remove(item)
            item.is_equiped = False
            self.equipt_slots[slot][0] = False
            self.equipt_slots[slot][1] = None
        else:
            if self.equipt_slots[slot][0]:
                # printr("\033[u")

                printr(f"You have laredy a {slot} equipped", pos=-1)
                choice = inputT("Do you want to swape? [y/n]>")
                if choice == "Y" or choice == "E":
                    self.equiped_items.remove(self.equipt_slots[slot][1])
                    self.equipt_slots[slot][1].is_equiped = False
                    self.equiped_items.append(item)
                    item.is_equiped = True
                    self.equipt_slots[slot][0] = True
                    self.equipt_slots[slot][1] = item
            else:
                self.equiped_items.append(item)
                item.is_equiped = True
                self.equipt_slots[slot][0] = True
                self.equipt_slots[slot][1] = item
        self.item_stats_add()

    def remove_item(self, item):
        if item in self.equiped_items:
            self.equip_item(item)
        if item in self.favorit:
            self.favorit.remove(item)
        self.inventory.remove(item)

    def show_inventory(self, is_shop=False):
        size = [2, 4]

        def items_per_page(is_selected: bool):
            out = 4 if is_selected else 8
            if out == 4:
                size = [2, 2]
            else:
                temp = Graphic.WIDTH // 40
                temp2 = (Graphic.HEIGHT - 10) // 6
                size = [temp, temp2]
                out = temp * temp2
                # size = [2,4]
            return out, size

        is_item_selected: bool = False
        page: int = 0
        is_fav: bool = False
        is_equ: bool = False
        item_fillter = self.inventory
        selected_item: None | GameItem = None
        selected_num = None
        show_inv = True
        curser = [0, 0, 0, 0]
        while show_inv:
            # clear()
            per_page, size = items_per_page(is_item_selected)
            max_page = max(0, (len(item_fillter) - 1) // per_page)

            choice, curser = Graphic.show_inventory(
                page,
                per_page,
                max_page,
                is_item_selected,
                item_fillter,
                selected_item,
                is_shop,
                self.gold,
                curser,
                size,
            )
            printr(choice)
            # choice = inputT("> ", True).upper().strip()
            if choice == "Q":
                show_inv = False
                break
            elif choice == "N":
                page += 1 if page < max_page else 0
            elif choice == "P":
                page -= 1 if page > 0 else 0
            elif choice == "E":
                if is_item_selected:
                    if is_shop:
                        choice = (
                            inputT(
                                f"You sure you want to sell this item?\nYou will get {selected_item.value} Gold\n [y/n] >"
                            )
                            .upper()
                            .strip()
                        )
                        if choice == "Y" or choice == "E":
                            self.remove_item(selected_item)
                            self.gold += selected_item.value
                            selected_item = None
                            is_item_selected = False
                            per_page, size = items_per_page(is_item_selected)
                            page = selected_num // per_page
                            selected_num = None
                    else:
                        self.equip_item(selected_item)
                else:
                    printr("No item select")
                    wait(1)
            elif choice == "SE":
                is_fav = False
                if is_equ:
                    is_equ = False
                    item_fillter = self.inventory
                    page = 0
                    selected_num = None
                else:
                    is_equ = True
                    item_fillter = self.equiped_items
                    page = 0
                    selected_num = None
            elif choice == "F":
                if is_item_selected:
                    if selected_item in self.favorit:
                        self.favorit.remove(selected_item)
                        selected_item.is_fav = False
                    else:
                        self.favorit.append(selected_item)
                        selected_item.is_fav = True
            elif choice == "SF":
                is_equ = False
                if is_fav:
                    is_fav = False
                    item_fillter = self.inventory
                    page = 0
                    selected_num = None
                else:
                    is_fav = True
                    item_fillter = self.favorit
                    page = 0
                    selected_num = None
            elif choice == "PAGE":
                choice = inputT("Selacte page > ", True, True).upper().strip()
                try:
                    if (int(choice) - 1) >= 0 and (int(choice) - 1) <= max_page:
                        page = int(choice) - 1
                except:
                    printr("Invalid inputT")
                    wait(1)
            elif is_item_selected and (choice == ""):
                selected_item = None
                is_item_selected = False
                per_page, size = items_per_page(is_item_selected)
                page = selected_num // per_page
                selected_num = None

            else:
                try:
                    choice = int(choice)
                    choice -= 1
                    if choice >= 0 and choice <= len(item_fillter):
                        if choice == selected_num:
                            selected_item = None
                            is_item_selected = False
                            selected_num = None
                            per_page, size = items_per_page(is_item_selected)
                            page = choice // per_page
                            curser[2] = curser[0]
                            curser[3] = curser[1]
                            temp = choice % per_page
                            curser[1] = temp % 2
                            curser[0] = temp // 2
                        else:
                            selected_item = item_fillter[choice]
                            is_item_selected = True
                            selected_num = choice
                            per_page, size = items_per_page(is_item_selected)
                            page = choice // per_page
                            curser[2] = curser[0]
                            curser[3] = curser[1]
                            temp = choice % per_page
                            curser[1] = temp % 2
                            curser[0] = temp // 2
                except:
                    printr("Invalid inputT\n Item can’t be selected")
                    printr(f"{choice}")
                    Graphic.update()
                    wait(1)
                    printr("done")
                    Graphic.update()

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
                self.max_hp_items += int(item.max_hp * afi)
                self.max_mp_items += int(item.max_mp * afi)
                self.atk_items += int(item.atk * afi)
                self.sp_atk_items += int(item.sp_atk * afi)
                self.def_items += int(item.def_ * afi)
                self.sp_def_items += int(item.sp_def * afi)
                self.crit_chance_items += int(item.crit_chance * afi)
                self.crit_bonus_items += int(item.crit_bonus * afi)

        if self.equipt_slots["wappon"][1]:
            self.wapon_ele = self.equipt_slots["wappon"][1].ele
        else:
            self.wapon_ele = None

        if self.hp > self.max_hp + self.max_hp_items:
            self.hp = self.max_hp + self.max_hp_items
        if self.mp > self.max_mp + self.max_mp_items:
            self.mp = self.max_mp + self.max_mp_items

    def Level(self, xp: int):
        self.xp += xp
        if self.xp >= self.max_xp:
            loop_levelup = True
            while loop_levelup:
                choice = Graphic.show_stats_level(self)
                # choice = inputT("> ").strip()
                if choice == "1":
                    rand = Graphic.roll_dice(1, 6, -1)
                    self.max_hp += rand
                    self.hp += rand
                    loop_levelup = False
                elif choice == "2":
                    rand = Graphic.roll_dice(1, 6, -1)
                    self.max_mp += rand
                    self.mp += rand
                    loop_levelup = False
                elif choice == "3":
                    self.atk += Graphic.roll_dice(1, 6, -1)
                    loop_levelup = False
                elif choice == "4":
                    self.sp_atk += Graphic.roll_dice(1, 6, -1)
                    loop_levelup = False
                elif choice == "5":
                    self.def_ += Graphic.roll_dice(1, 6, -1)
                    loop_levelup = False
                elif choice == "6":
                    self.sp_def += Graphic.roll_dice(1, 6, -1)
                    loop_levelup = False
                elif choice == "7":
                    self.crit_chance += Graphic.roll_dice(1, 6, -1)
                    loop_levelup = False
                elif choice == "8":
                    self.crit_bonus += Graphic.roll_dice(1, 6, -1)
                    loop_levelup = False
                elif choice == "9":
                    rand = Graphic.roll_dice(1, 6, -1)
                    self.min_move += rand
                    self.max_move += rand
                    loop_levelup = False
                else:
                    printr("Invalid inputT")
                    wait(1)
            self.xp -= self.max_xp
            self.level += 1
            self.max_xp += self.next_level_xp(self.level)
            self.max_hp += 3
            self.hp += 3
            self.max_mp += 3
            self.mp += 3
            self.atk += 1
            self.sp_atk += 1
            self.def_ += 1
            self.sp_def += 1
            self.crit_chance += 1
            self.crit_bonus += 2

    def show_stats(self):
        Graphic.show_stats(self)

    def move(self, dir: str, dungeon):
        global Curent_Layer, DUNGEON
        room = dungeon.rooms[dungeon.room]
        self.last_pos = [self.x, self.y]
        x, y = self.x, self.y
        if dir == "W":
            if y - 1 < 0:
                printr("Move in valed")
                return "brake"
            elif room.map[y - 1][x] != "#":
                self.y -= 1
                self.moves -= 1
            else:
                printr("Move in valed")
                printr(room.map[y - 1][x])
                return "brake"
        elif dir == "S":
            if y + 1 >= len(room.map):
                printr("Move in valed")
                return "brake"
            elif room.map[y + 1][x] != "#":
                self.y += 1
                self.moves -= 1
            else:
                printr("Move in valed")
                printr(room.map[y + 1][x])
                return "brake"
        elif dir == "D":
            if x + 1 >= len(room.map[0]):
                printr("Move in valed")
                return "brake"
            elif room.map[y][x + 1] != "#":
                self.x += 1
                self.moves -= 1
            else:
                printr("Move in valed")
                printr(room.map[y][x + 1])
                return "brake"
        elif dir == "A":
            if x - 1 < 0:
                printr("Move in valed")
                return "brake"
            elif room.map[y][x - 1] != "#":
                self.x -= 1
                self.moves -= 1
            else:
                printr("Move in valed")
                printr(room.map[y][x - 1])
                return "brake"
        x, y = self.x, self.y
        if room.map[y][x] == "D":
            door_num = room.door_positions.index((x, y))
            old_room = dungeon.room
            dungeon.room = room.doors[door_num]
            door_num = dungeon.rooms[dungeon.room].doors.index(old_room)
            px, py = dungeon.rooms[dungeon.room].door_positions[door_num]
            new_room = dungeon.rooms[dungeon.room]
            new_room.show_on_map = True
            # print(dungeon.rooms)
            for rom in dungeon.rooms:
                for sp in dungeon.rooms[rom].spawners:
                    sp.update(self, new_room)
            self.x, self.y = px, py
        elif room.map[y][x] == "S":
            if Curent_Layer <= 0:
                pass
            else:
                Curent_Layer -= 1
                DUNGEON = Layers[Curent_Layer]
                dungeon = DUNGEON
                new_room = dungeon.rooms[dungeon.room]
                new_room.show_on_map = True
                self.y = len(new_room.map) // 2
                self.x = len(new_room.map[0]) // 2
        elif room.map[y][x] == "s":
            Curent_Layer += 1
            if len(Layers) <= Curent_Layer:
                Layers.append(Dungeon(Curent_Layer, Dungeon_type))
            DUNGEON = Layers[Curent_Layer]
            dungeon = DUNGEON
            new_room = dungeon.rooms[dungeon.room]
            new_room.show_on_map = True
            self.y = len(new_room.map) // 2
            self.x = len(new_room.map[0]) // 2
        update_player(self, room)
        game_menu(self, dungeon)
        print_room_options(self)
        wait(0.2)
        return "fine"

    def rest(self):
        self.hp += (self.max_hp + self.max_hp_items) // 10
        self.mp += (self.max_mp + self.max_mp_items) // 10
        if self.hp > self.max_hp + self.max_hp_items:
            self.hp = self.max_hp + self.max_hp_items
        if self.mp > self.max_mp + self.max_mp_items:
            self.mp = self.max_mp + self.max_mp_items
        for i in self.attacks_used:
            self.attacks_used[i] = 0


class Enemy:
    def __init__(
        self, mob: str, level: int, room, spawner, x: int, y: int, is_boss: bool = False
    ) -> None:
        self.room: Room = room
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
        player_pos = [player.x, player.y]
        grid = room.map
        path = self.find_path(grid, enemy_pos, player_pos)
        if len(path) < rand:
            rand = len(path)
        for i in range(rand):
            printr(path[i])
            if path[i] == "N":
                self.y -= 1
            elif path[i] == "S":
                self.y += 1
            if path[i] == "W":
                self.x -= 1
            elif path[i] == "E":
                self.x += 1
            update_player(player, room)
            game_menu(player, dungeon)
            Graphic.update()
            wait(0.2)

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

        while q:
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
        while cur != start:
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


class EnemySpawner:
    def __init__(
        self,
        mob: str,
        level: int,
        room,
        x: int,
        y: int,
        min_l,
        max_l,
        is_boss: bool = False,
    ) -> None:
        self.room: Room = room
        self.mob: str = mob
        self.is_boss: bool = is_boss
        self.x: int = x
        self.y: int = y
        self.level: int = level
        self.min_l = min_l
        self.max_l = max_l
        self.has_spawned = False
        self.is_spawnd = False
        self.cool_down = 0
        self.enemy = None

    def spawn_enemy(self, player):
        if self.is_boss:
            e_level = self.level
        else:
            e_level = (self.level + player.level) // 2
            # print(e_level)
            # time.sleep(0.1)
            if e_level < self.min_l:
                e_level = self.min_l
            if e_level > self.max_l:
                e_level = self.max_l
            # print(e_level,self.min_l,self.max_l)
            # time.sleep(0.1)
        self.enemy = Enemy(
            self.mob, e_level, self.room, self, self.x, self.y, self.is_boss
        )
        self.room.enemys.append(self.enemy)
        self.is_spawnd = True
        self.has_spawned = True

    def update(self, player, room = None):
        if self.enemy:
            if self.enemy.is_del:
                self.is_spawnd = False
                self.enemy = None

        # if room == self.room:
        # print(self.is_spawnd)
        # print(f"{self.cool_down}")
        # time.sleep(0.1)

        if not self.is_spawnd and self.cool_down <= 0 and room == self.room:
            if self.is_boss and not self.has_spawned:
                self.spawn_enemy(player)
            else:
                self.spawn_enemy(player)
        elif not self.is_spawnd and self.cool_down > 0:
            self.cool_down -= 1
            # print(f"{self.cool_down}")
            # time.sleep(0.1)


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


class Dungeon:
    def __init__(self, layer, type):
        room = [
            ["#", "#", "#", "#", "#", "#"],
            ["#", ".", ".", ".", ".", "#"],
            ["#", ".", ".", ".", ".", "#"],
            [".", ".", ".", ".", ".", "."],
            ["#", ".", ".", ".", ".", "#"],
            ["#", ".", ".", ".", ".", "#"],
            ["#", "#", "#", "#", "#", "#"],
        ]
        self.no_child = ["boss", "start"]
        l_size = len(GTD.dungeons_preset[type]["liniar"]["layers"])
        gentype = "liniar" if layer < l_size else "endless"
        print(gentype)
        # self.layer_set = GTD.dungeons_preset[type][gentype]["layers"][layer]
        # self.layer = self.layer_set["layer"]
        if gentype == "liniar":
            self.layer_set = GTD.dungeons_preset[type][gentype]["layers"][layer]
            self.layer = self.layer_set["layer"]
            size_a = self.layer_set["Size"][0] * GTD.layers[self.layer]["size"][0]
            size_b = self.layer_set["Size"][1] * GTD.layers[self.layer]["size"][1]
            self.level = self.layer_set["level"]
        else:
            e_size = len(GTD.dungeons_preset[type]["endless"]["layers"])
            e_layer = layer - l_size
            self.layer = GTD.dungeons_preset[type][gentype]["layers"][e_layer % e_size]
            size_a = (
                GTD.dungeons_preset[type][gentype]["Size"][0]
                * GTD.layers[self.layer]["size"][0]
            )
            size_b = (
                GTD.dungeons_preset[type][gentype]["Size"][1]
                * GTD.layers[self.layer]["size"][1]
            )
            base_level = GTD.dungeons_preset[type][gentype]["start_level"]
            skale = GTD.dungeons_preset[type][gentype]["Skale"]
            self.level = int(base_level * (skale**e_layer))
        rand = random.randint(min(size_a, size_b), max(size_a, size_b))
        self.room_pos = []
        self.rooms = self.gen_dungeon(num_rooms=rand, layer=self.layer)
        self.rooms[0].show_on_map = True
        self.room = 0
        self.spwaners = []

    def print_room(self, player):
        # clear()
        room: Room = self.rooms[self.room]
        enemys: list[Enemy] = room.enemys
        traps: list[Trape] = room.traps
        cheasts: list[Cheast] = room.cheasts
        merchents: list[Merchent] = room.shops
        player_pos: tuple[int, int] = (player.x, player.y)
        Graphic.print_room(player_pos, room, enemys, traps, cheasts, merchents)

    def conect_rooms(self, current, rooms):
        pos = current.pos
        side = choice(["top", "bottom", "left", "right"])
        if side == "top":
            pos_2 = (pos[0], pos[1] - 1)
        elif side == "bottom":
            pos_2 = (pos[0], pos[1] + 1)
        elif side == "left":
            pos_2 = (pos[0] - 1, pos[1])
        elif side == "right":
            pos_2 = (pos[0] + 1, pos[1])
        safety_count = 0
        side_options = ["top", "bottom", "left", "right"]
        while side in current.sides_used or pos_2 not in self.room_pos:
            side = choice(side_options)
            side_options.remove(side)
            if side == "top":
                pos_2 = (pos[0], pos[1] - 1)
            elif side == "bottom":
                pos_2 = (pos[0], pos[1] + 1)
            elif side == "left":
                pos_2 = (pos[0] - 1, pos[1])
            elif side == "right":
                pos_2 = (pos[0] + 1, pos[1])
            safety_count += 1
            if safety_count > 3:
                break
        if safety_count > 3:
            return current, rooms
        other_id = self.room_pos.index(pos_2)
        other_room = rooms[other_id]
        if other_room.type == "start" or other_room.type == "boss":
            return current, rooms
        else:
            pos_a = current.add_door(side, self.room_pos, ignor_side=True)
            pos_b = other_room.add_door(
                OPPOSITE[side],
                self.room_pos,
                current.pos,
                mirror=pos_a,
                ignor_side=True,
            )
            if pos_a and pos_b:
                current.doors.append(other_id)
                other_room.doors.append(current.id)
        return current, rooms

    def gen_dungeon(self, num_rooms=8, layer="layer 1"):
        rooms = {0: Room(0, "start", 0, 0, width=5, height=5, layer=layer)}
        todo = [0]
        self.room_pos = [(0, 0)]
        next_id = 1

        SPECIAL_ROOMS = GTD.layers[layer]["rooms"]  # Easy to add more

        while next_id < num_rooms and todo:
            current = rooms[todo.pop(0)]

            # Decide connections (1-3, fewer near end)
            if current.id == 0:
                connections = 1
            elif current.type in self.no_child:
                connections = 0
            else:
                connections = min(
                    min(random.randint(1, 3), num_rooms - next_id),
                    len(current.free_sides),
                )

            for child in range(connections):
                clear()
                Graphic.print_titelbar("Generating Dungeon", 16)
                printr(todo)
                printr(current.id)
                printr(next_id)
                # if next_id >= num_rooms: break
                # if current.conn <= 0: continue
                # Find available sides and connect
                current.update_free_sides(self.room_pos)
                avail_sides = current.free_sides
                if current.id != 0:
                    if not avail_sides:
                        if random.randint(0, 5) == 0:
                            current, rooms = self.conect_rooms(current, rooms)
                            break
                        else:
                            break
                    if random.randint(0, 3) == 0 and len(todo) > 3:
                        current, rooms = self.conect_rooms(current, rooms)
                        continue

                # Determine room type
                room_type = "boss" if next_id == num_rooms - 1 else "normal"
                if room_type != "boss":
                    for (
                        special,
                        chance,
                    ) in SPECIAL_ROOMS.items():  # Willkommen bei der Freiheit
                        if random.random() < chance:
                            room_type = special
                            break

                # Create and connect room

                new_room = Room(next_id, room_type, layer=layer, level=self.level)
                rooms[next_id] = new_room

                dir_a = random.choice(avail_sides)
                dir_b = OPPOSITE[dir_a]

                pos_a = current.add_door(dir_a, self.room_pos)
                pos_b = new_room.add_door(
                    dir_b, self.room_pos, current.pos, mirror=pos_a
                )

                self.room_pos += [new_room.pos]

                if pos_a and pos_b:
                    current.doors.append(next_id)
                    new_room.doors.append(current.id)

                todo.append(next_id)
                next_id += 1

        for _ in range(len(rooms) // 6):
            current = choice(rooms)
            if current.type not in self.no_child:
                current, rooms = self.conect_rooms(current, rooms)

        # Clean up start/boss rooms
        # for room_id in [0, num_rooms - 1]:
        #     if room_id in rooms:
        #         room = rooms[room_id]
        #         room.doors = room.doors[:1]
        #         room.door_positions = room.door_positions[:1]
        #         room.free_sides = set(list(room.free_sides)[:1])

        return rooms


class Room:
    def __init__(
        self,
        room_id,
        room_type="normal",
        x=0,
        y=0,
        width=None,
        height=None,
        layer="layer 1",
        level=5,
    ):
        self.id = room_id
        self.level = level
        self.type = room_type
        self.pos = (x, y)
        self.layer = layer
        self.doors = []  # [target_room_id, ...]
        self.enemys = []
        self.spawners = []
        self.traps = []
        self.cheasts = []
        self.shops = []
        self.used_pos = []
        self.map = self.generate_room(room_type, width, height)
        self.door_positions = []  # [(x, y), ...]
        self.spawn_positions = []
        self.free_sides = [
            "top",
            "bottom",
            "left",
            "right",
        ]  # which walls already have no doors
        self.sides_used = []
        self.add_asets(layer)
        self.show_on_map = False
        self.conn = None

    def place_enemy(self, width, height, layer="layer 1"):
        x = random.randint(1, width)
        y = random.randint(1, height)
        while self.map[y][x] != ".":
            x = random.randint(1, width)
            y = random.randint(1, height)
        rarety_temp_1 = 0
        rarety_temp_2 = 0
        rand_num = random.randint(0, 100)
        layer = GTD.layers[layer]
        for j in layer["mob"]:
            p = layer["mob"][j]
            # printr(p)
            rarety_temp_1 = rarety_temp_2
            rarety_temp_2 += p
            if (rarety_temp_1 < rand_num) and (rand_num <= rarety_temp_2):
                e_level = self.level + random.randint(-3, 3)
                if e_level <= 0:
                    e_level = 1
                self.spawners.append(
                    EnemySpawner(
                        j, e_level, self, x, y, layer["min_level"], layer["max_level"]
                    )
                )
                self.used_pos.append((x, y))

    def place_boss(self, width, height, layer="layer 1"):
        x = width
        y = height
        layer = GTD.layers[layer]
        e_level = self.level + random.randint(-3, 3)
        if e_level <= 0:
            e_level = 1
        self.spawners.append(
            EnemySpawner(
                layer["boss"],
                e_level,
                self,
                x,
                y,
                layer["min_level"],
                layer["max_level"],
                True,
            )
        )
        # self.enemys.append(Enemy(layer["boss"], e_level, self, x, y, True))

    def place_trap(self, width, height, layer="layer 1"):
        rarety_temp_1 = 0
        rarety_temp_2 = 0
        rand_num = random.randint(0, 100)
        layer = GTD.layers[layer]
        for j in layer["traps"]:
            p = layer["traps"][j]
            # printr(p)
            rarety_temp_1 = rarety_temp_2
            rarety_temp_2 += p
            if (rarety_temp_1 < rand_num) and (rand_num <= rarety_temp_2):
                self.traps.append(Trape(width, height, j, self))

    def place_cheast(self, x, y):
        self.cheasts.append(Cheast(self, x, y))

    def get_enemy_pos(self):
        enemy_pos = []
        for e in self.enemys:
            enemy_pos.append([e.x, e.y])
        return enemy_pos

    def add_asets(self, layer="layer 1"):
        if self.type == "start":
            height = len(self.map) // 2
            width = len(self.map[0]) // 2
            self.map[height][width] = "S"
            printr("add assets")

        elif self.type == "boss":
            height = len(self.map) // 2
            width = len(self.map[0]) // 2
            self.place_boss(width, height, layer)
            printr("add assets")

        elif self.type == "merchant":
            height = len(self.map) // 2
            width = len(self.map[0]) // 2
            self.shops.append(Merchent(width, height, self))
            printr("add assets")

        elif self.type == "normal":
            height = len(self.map) - 2
            width = len(self.map[0]) - 2
            space = height * width
            rand = random.randint((space // 6), (space // 3))
            for i in range(rand):
                if i == 0:
                    self.place_enemy(width, height, layer)
                else:
                    rand_2 = random.randint(0, 3)
                    if rand_2 <= 0:
                        self.place_enemy(width, height, layer)
                    elif rand_2 == 1:
                        x = random.randint(2, width - 1)
                        y = random.randint(2, height - 1)
                        if self.map[y][x] == "." and (x, y) not in self.used_pos:
                            self.used_pos.append((x, y))
                            self.map[y][x] = "#"

                    elif rand_2 == 6:
                        x = random.randint(2, width - 1)
                        y = random.randint(2, height - 1)
                        if self.map[y][x] == "." and (x, y) not in self.used_pos:
                            self.used_pos.append((x, y))
                            self.map[y][x] = "#"
                    elif rand_2 == 5:
                        x = random.randint(2, width - 1)
                        y = random.randint(2, height - 1)
                        if self.map[y][x] == "." and (x, y) not in self.used_pos:
                            self.used_pos.append((x, y))
                            self.map[y][x] = "#"
                    elif rand_2 == 2:
                        x = random.randint(1, width)
                        y = random.randint(1, height)
                        if self.map[y][x] == "." and (x, y) not in self.used_pos:
                            self.used_pos.append((x, y))
                            self.place_cheast(x, y)
                    elif rand_2 == 3:
                        x = random.randint(1, width)
                        y = random.randint(1, height)
                        if self.map[y][x] == "." and (x, y) not in self.used_pos:
                            self.used_pos.append((x, y))
                            self.place_trap(x, y, layer)
                    elif rand_2 == 4:
                        x = random.randint(1, width)
                        y = random.randint(1, height)
                        if self.map[y][x] == "." and (x, y) not in self.used_pos:
                            self.used_pos.append((x, y))
                            self.map[y][x] = " "
                printr("add assets")

    def update_free_sides(self, grid):
        for i in self.free_sides:
            try:
                if i == "top" and (self.pos[0], self.pos[1] - 1) in grid:
                    self.free_sides.remove("top")
                if i == "bottom" and (self.pos[0], self.pos[1] + 1) in grid:
                    self.free_sides.remove("bottom")
                if i == "left" and (self.pos[0] - 1, self.pos[1]) in grid:
                    self.free_sides.remove("left")
                if i == "right" and (self.pos[0] + 1, self.pos[1]) in grid:
                    self.free_sides.remove("right")
            except:
                pass

    def add_door(self, side, grid, o_pos=None, mirror=None, ignor_side=False):
        if side not in self.free_sides and not ignor_side:
            return None  # already has a door on this side
        height = len(self.map)
        width = len(self.map[0])

        def clamp(val, min_val, max_val):
            return max(min_val, min(val, max_val))

        # compute door coordinates
        if mirror:
            mx, my = mirror
            if side == "left":
                x, y = 0, clamp(my, 1, height - 2)
                self.pos = (o_pos[0] + 1, o_pos[1])
            elif side == "right":
                x, y = width - 1, clamp(my, 1, height - 2)
                self.pos = (o_pos[0] - 1, o_pos[1])
            elif side == "top":
                x, y = clamp(mx, 1, width - 2), 0
                self.pos = (o_pos[0], o_pos[1] + 1)
            elif side == "bottom":
                x, y = clamp(mx, 1, width - 2), height - 1
                self.pos = (o_pos[0], o_pos[1] - 1)
        else:
            if side == "top":
                x, y = random.randint(1, width - 2), 0
            elif side == "bottom":
                x, y = random.randint(1, width - 2), height - 1
            elif side == "left":
                x, y = 0, random.randint(1, height - 2)
            elif side == "right":
                x, y = width - 1, random.randint(1, height - 2)

        self.map[y][x] = "D"
        self.door_positions.append((x, y))
        try:
            self.free_sides.remove(side)
        except:
            pass
        self.sides_used.append(side)
        self.update_free_sides(grid)
        return (x, y)

    def generate_room(self, room_type, width=None, height=None):
        width: int = width or random.randint(6, 10)
        height: int = height or random.randint(6, 10)
        return [
            [
                "#" if x in (0, width - 1) or y in (0, height - 1) else "."
                for x in range(width)
            ]
            for y in range(height)
        ]


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
            enemy = Enemy("Mimic", level, None, 0, 0)
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


class Merchent:
    def __init__(self, x, y, room):
        self.x = x
        self.y = y
        self.room = room
        self.layer = GTD.layers[room.layer]
        self.type = p_chois(self.layer["shops"])
        self.gtd_shop = GTD.shops[self.type]
        self.items = self.gen_items()

    def gen_items(self):
        size_temp = self.gtd_shop["size"]
        size = randint(*size_temp)
        items = []
        for _ in range(size):
            item_type = p_chois(self.gtd_shop["item type"])
            item_rarety = p_chois(self.gtd_shop["rarety"])
            level = self.room.level + randint(*self.gtd_shop["level"])
            items.append(GameItem(item_rarety, item_type, level))

        return items

    def shop_buy(self, player):
        def items_per_page(is_selected: bool) -> int:
            return 4 if is_selected else 8

        is_item_selected: bool = False
        page: int = 0
        item_fillter = self.items
        selected_item: None | GameItem = None
        selected_num = None
        show_inv = True
        curser = [0, 0, 0, 0]
        while show_inv:
            per_page = items_per_page(is_item_selected)
            max_page = max(0, (len(item_fillter) - 1) // per_page)

            choice, curser = Graphic.shop_buy_page(
                page,
                per_page,
                max_page,
                is_item_selected,
                item_fillter,
                selected_item,
                player.gold,
                curser,
            )
            # choice = inputT("> ", True).upper().strip()
            if choice == "Q":
                show_inv = False
                break
            elif choice == "N":
                page += 1 if page < max_page else 0
            elif choice == "P":
                page -= 1 if page > 0 else 0

            elif choice == "E":
                if is_item_selected:
                    if selected_item.value <= player.gold:
                        choice = (
                            inputT(
                                f"Do you want to buy this item?\nthe item costs {selected_item.value} gold\nyou have {player.gold}, after buying you’ll have {player.gold - selected_item.value}\n [Y/N] > "
                            )
                            .upper()
                            .strip()
                        )
                        if choice == "Y" or choice == "E":
                            player.add_to_inv(selected_item)
                            player.gold -= selected_item.value
                            self.items.remove(selected_item)
                            selected_item = None
                            is_item_selected = False
                            page = selected_num // items_per_page(is_item_selected)
                            selected_num = None
                    else:
                        printr("You don’t have enough gold to buy this item")
                        wait(1)
                else:
                    printr("No Item Selected")
                    wait(1)

            elif choice == "PAGE":
                choice = inputT("Selacte page > ", True, True).upper().strip()
                try:
                    if (int(choice) - 1) >= 0 and (int(choice) - 1) <= max_page:
                        page = int(choice) - 1
                except:
                    printr("Invalid inputT")
                    wait(1)
            elif is_item_selected and (choice == ""):
                selected_item = None
                is_item_selected = False
                page = selected_num // items_per_page(is_item_selected)
                selected_num = None

            else:
                try:
                    choice = int(choice)
                    choice -= 1
                    if choice >= 0 and choice <= len(item_fillter):
                        if choice == selected_num:
                            selected_item = None
                            is_item_selected = False
                            selected_num = None
                            page = choice // items_per_page(is_item_selected)
                            curser[2] = curser[0]
                            curser[3] = curser[1]
                            temp = choice % items_per_page(is_item_selected)
                            curser[1] = temp % 2
                            curser[0] = temp // 2
                        else:
                            selected_item = item_fillter[choice]
                            is_item_selected = True
                            selected_num = choice
                            page = choice // items_per_page(is_item_selected)
                            curser[2] = curser[0]
                            curser[3] = curser[1]
                            temp = choice % items_per_page(is_item_selected)
                            curser[1] = temp % 2
                            curser[0] = temp // 2
                except:
                    printr("Invalid inputT")
                    wait(1)

    def interact_player(self, player):
        is_in_shop: bool = True
        struc = {"buy": "Buy Items", "sell": "Sell Items", "Q": "Leave"}
        while is_in_shop:
            choice = Graphic.select_menu_page("Merchent", struc, {"Q": "Q"})
            if choice == "Q":
                is_in_shop = False
            elif choice == "sell":
                player.show_inventory(True)
            elif choice == "buy":
                self.shop_buy(player)


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
        enemy = steck.pop(0)
        if enemy.is_del:
            try:
                enemy.spawner.is_spawnd = False
                room.enemys.remove(enemy)
                del enemy
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


def print_room_options(player):
    printr("======== Your turn =========")
    if player.moves == -2:
        if player.cls == "Roghe":
            printr("R = Roll dice to move | F = Roll to check for traps")
        printr("R = Roll dice to move | P = Make a pause and rest")
    elif player.moves > 0:
        printr(f"Moves {player.moves} left")
    else:
        player.moves = -1
    Graphic.update()


def main_menu():
    struc = {"start": "Start Game", "help": "How to Play", "exit": "Quit"}
    while True:
        choice = Graphic.select_menu_page("DICE DUNGEON: DESCENT", struc, {"Q": "exit"})
        # printr(choice)
        if choice == "start":
            return "start"
        elif choice == "help":
            show_help_new()
        elif choice == "exit":
            printr("Goodbye, hero...")
            Graphic.update()
            wait(0.1)
            return "exit"
        else:
            printr("Invalid option.")
            Graphic.update()
            wait(1)


def show_help_new(page=0):
    max_page = 0
    help_text = GTD.help_txt
    while True:
        clear()
        printr(f"""=============
    Help Page {page} / {max_page}
P = Privios Page | N = Next """)
        printr(help_text[f"page {page}"])
        Graphic.update()
        choice = inputT("Press Enter to return... > ").upper().strip()
        if choice == "N":
            if page < max_page:
                page += 1
        elif choice == "P":
            if page > 0:
                page -= 1
        else:
            break


def game_menu(player, dungeon):
    Graphic.game_menu(player)
    if GAME_STATE == "map":
        dungeon.print_room(player)
    Graphic.update()
    return player


def select_player_class():
    cls = []
    for i in GTD.player_cls:
        cls.append(i)
    struc = {f"{cls[i]}": f"{cls[i]}" for i in range(len(cls))}

    while True:
        choice = Graphic.select_menu_page(
            "Selacte a player class", struc, {"Q": "Q"}
        )  #
        Graphic.update()
        return choice


def select_dungeon():
    d_type = []
    for i in GTD.dungeons_preset:
        d_type.append(i)
    struc = {f"{d_type[i]}": f"{d_type[i]}" for i in range(len(d_type))}
    while True:
        choice = Graphic.select_menu_page("Selacte a dungeon", struc, {"Q": "Q"})
        Graphic.update()
        return choice


def print_dungeon_map(dungeon, spacing=1, room_size=2):
    Graphic.print_dungeon_map(dungeon, spacing, room_size, CHEATS_ON)
    Graphic.update()
    inputT("\nPress Enter to return...")


def game_loop_room(player):
    global loop_room, Layers, DUNGEON, CHEATS_ON
    loop_room = True
    while loop_room:
        dungeon = DUNGEON
        game_menu(player, dungeon)
        print_room_options(player)
        choice = inputT("> ").upper().strip()
        if choice == "/":
            choice = inputT("> ", True).upper().strip()
        if choice == "H":
            show_help_new()
            continue
        elif choice == "T":
            player.show_stats()
            continue
        elif choice == "I":
            player.show_inventory()
            continue
        elif choice == "M":
            print_dungeon_map(dungeon)
            continue
        elif choice == "Q":
            choice = inputT("You sure you want to qite? [Y/N]>").upper().strip()
            if choice == "Y" or choice == "Q":
                loop_room = False
                break
        elif choice == "UP UP DOWN DOWN LEFT RIGHT LEFT RIGHT B A":
            CHEATS_ON = True
            continue

        elif player.moves >= 0:
            if any(c not in ("W", "A", "S", "D") for c in choice):
                printr("Invalid inputT")
                wait(1)
                continue
            elif len(choice) <= player.moves:
                for i in choice:
                    out = player.move(i, dungeon)
                    if out == "brake":
                        wait(1)
                        break
                continue
        elif player.moves == -2:
            if choice == "R":
                player.roll_for_move()
                continue
                # wait(1)
            elif choice == "P":
                player.rest()
                player.moves = -1
                continue

        elif choice == "GIVE ALL" and CHEATS_ON:
            for rarity in [
                "common",
                "uncommon",
                "rare",
                "epic",
                "legendary",
                "unique",
            ]:
                for item_type in [
                    "sword",
                    "knife",
                    "bow",
                    "stafe",
                    "spear",
                    "chestplate",
                    "helmet",
                    "boots",
                    "pants",
                    "pan",
                    "gloves",
                    "sheald",
                ]:  # , "consumable"
                    player.add_to_inv(GameItem(rarity, item_type, 100))
            continue
        elif choice == "GIVE ALL ALL" and CHEATS_ON:
            for _ in range(5):
                for rarity in [
                    "common",
                    "uncommon",
                    "rare",
                    "epic",
                    "legendary",
                    "unique",
                ]:
                    for item_type in [
                        "sword",
                        "knife",
                        "bow",
                        "stafe",
                        "spear",
                        "chestplate",
                        "helmet",
                        "boots",
                        "pants",
                        "pan",
                        "gloves",
                        "sheald",
                    ]:  # , "consumable"
                        for _ in range(5):
                            player.add_to_inv(GameItem(rarity, item_type, 100))
                continue
        elif choice == "LEVEL UP" and CHEATS_ON:
            player.Level(player.max_xp + 1)
            continue
        elif choice == "GIVE ITEM" and CHEATS_ON:
            player.add_to_inv(GameItem("common", "sword", 10))
            continue
        elif choice == "FIGHT" and CHEATS_ON:
            enemy = Enemy("Zomby", random.randint(1, 5), 0, 5, 5)
            player, loop_room = fight_loop(player, enemy)
            continue
        elif choice == "TP" and CHEATS_ON:
            choice = inputT("> ").upper().strip()
            dungeon.room = int(choice)
        elif player.moves == -1:
            enemy_move(dungeon, player)
            for rom in dungeon.rooms:
                for sp in dungeon.rooms[rom].spawners:
                    sp.update(player)
            player.moves = -2
        else:
            printr("Invalid inputT")
            wait(1)


def p_chance(chance):
    rand = random.randint(1, 100)
    return True if rand <= chance else False


def fight_won(player, enemy):
    gold_gain = f"{enemy.gold} Gold"
    while len(gold_gain) < 27:
        gold_gain = gold_gain + " "
        if len(gold_gain) < 27:
            gold_gain = " " + gold_gain
    xp_gain = f"{enemy.xp} XP"
    while len(xp_gain) < 27:
        xp_gain = xp_gain + " "
        if len(xp_gain) < 27:
            xp_gain = " " + xp_gain
    stats_gain = gold_gain + " " + xp_gain

    clear()
    Graphic.print_fight_UI(player, enemy)
    printr(stats_gain)
    printr("                          ITEMS                            ")
    for item in enemy.items:
        printr(item.Name())
        player.inventory.append(item)
    inputT("\nPress Enter to return...")
    player.gold += enemy.gold
    player.Level(enemy.xp)


def you_died():
    clear()
    printr("You died")
    inputT("\nPress Enter to return...")


def fight_selact_attack(player, enemy, curser):
    clear()
    choice, curser = Graphic.fight_selact_attack(player, enemy, curser)
    return choice, curser


def get_attaker_stats(attaker, defender, sel):
    attake = attaker.attacks[sel]
    atk_ele = attake["ele"]
    p_crit = (
        attaker.crit_chance + attaker.crit_chance_items + attake["stats"]["crit_chance"]
    )
    p_crit_bonus = (
        attaker.crit_bonus + attaker.crit_bonus_items + attake["stats"]["crit_bonus"]
    )

    crit = p_chance(p_crit)
    atk = attaker.atk + attaker.atk_items
    atk = int(atk * (attake["stats"]["atk"] / 100))
    sp_atk = attaker.sp_atk + attaker.sp_atk_items
    sp_atk = int(sp_atk * (attake["stats"]["sp_atk"] / 100))
    if atk_ele:
        afi_stat = attaker.ele_afi.fin_afi[atk_ele] / 100
        atk = int(atk * afi_stat)
        sp_atk = int(sp_atk * afi_stat)

        if attaker.wapon_ele == atk_ele:
            atk = int(atk * 1.5)
            sp_atk = int(sp_atk * 1.5)

        if defender.ele_afi.main_afi in GTD.elementare[atk_ele]["atk"]:
            atk = int(atk * 2)
            sp_atk = int(sp_atk * 2)
    atk += int(atk * (p_crit_bonus / 100)) if crit else 0
    sp_atk += int(sp_atk * (p_crit_bonus / 100)) if crit else 0
    attaker.ele_afi_up(atk_ele)
    return atk, sp_atk, crit


def get_deffender_stats(attaker, defender, sel):
    attake = attaker.attacks[sel]
    atk_ele = attake["ele"]

    def_ = defender.def_ + defender.def_items
    sp_def = defender.sp_def + defender.sp_def_items
    if atk_ele:
        afi_stat = defender.ele_afi.fin_afi[atk_ele] / 100
        def_ = int(def_ * afi_stat)
        sp_def = int(sp_def * afi_stat)

        if defender.ele_afi.main_afi in GTD.elementare[atk_ele]["def"]:
            def_ = int(def_ * 2)
            sp_def = int(sp_def * 2)
    return def_, sp_def


def enemy_fight_ai(attacker, deffender):
    rand = random.randint(0, 3)
    return rand


def fight_roll_dice(player, enemy, start, end, sel=0, advan=0, atk=True):
    rand = 0
    advan_e = 0
    if atk:
        attaker = player
        deffender = enemy
    else:
        attaker = enemy
        deffender = player
        sel = enemy_fight_ai(attaker, deffender)
    clear()
    Graphic.print_fight_UI(player, enemy)
    rand, rand_e = Graphic.fight_roll_dice(
        player, enemy, start, end, advan, advan_e, not (atk)
    )

    if atk:
        rand_a = rand
        rand_d = rand_e
    else:
        rand_a = rand_e
        rand_d = rand

    base_atk, base_sp_atk, crit = get_attaker_stats(attaker, deffender, sel)
    base_def, base_sp_def = get_deffender_stats(attaker, deffender, sel)
    # print("base atk:",base_atk)
    # print("base sp atk:",base_sp_atk)
    base_atk *= rand_a
    base_sp_atk *= rand_a
    # print("base def:",base_def)
    # print("base sp def:",base_sp_def)
    base_def *= rand_d
    base_sp_def *= rand_d
    # print("base atk:",base_atk)
    # print("base sp atk:",base_sp_atk)
    # print("base def:",base_def)
    # print("base sp def:",base_sp_def)
    strangth = base_atk - base_def
    sp_strangth = base_sp_atk - base_sp_def
    strangth = 0 if strangth < 0 else strangth
    sp_strangth = 0 if sp_strangth < 0 else sp_strangth
    # print("strangth:", strangth)
    # print("sp strangth:", sp_strangth)
    damage = strangth + sp_strangth
    # print("damage:",damage)
    deffender.hp -= damage
    sel_atk = list(attaker.attacks_used)[sel]
    Graphic.print_atk_damage(
        sel_atk, base_atk, base_sp_atk, base_def, base_sp_def, crit, damage, atk
    )
    inputT("\nPress Enter to return...")

    return player, enemy


def fight_loop(player, enemy, player_start=True):
    global loop_fight, loop_room
    loop_fight = True
    curser = [0, 0, 0, 0]
    turn = 1 if player_start else 0
    first_turn = True
    while loop_fight:
        if enemy.hp <= 0:
            fight_won(player, enemy)
            loop_fight = False
            loop_room = True
            return player, True
        elif player.hp <= 0:
            you_died()
            loop_fight = False
            loop_room = False
            return player, False
        # printr(turn)
        if turn == 0:
            clear()
            Graphic.print_fight_UI(player, enemy)
            choice = inputT("\nPress Enter to continue...").upper().strip()
            if choice == "Q":
                loop_fight = False
                return player, True
            elif choice == "S":
                printr(enemy)
                inputT("\nPress Enter to return...")
            else:
                player, enemy = fight_roll_dice(
                    player, enemy, 1, 6, advan=-1 if first_turn else 0, atk=False
                )
                turn = 1
                first_turn = False
        elif turn == 1:
            choice, curser = fight_selact_attack(player, enemy, curser)
            # choice = inputT(">").upper().strip()

            printr(choice)
            try:
                if choice == "Q":
                    loop_fight = False
                    return player, True
                elif choice == "S":
                    printr(enemy)
                    inputT("\nPress Enter to return...")
                elif (0 <= int(choice) - 1) and (int(choice) - 1 <= 3):
                    attack_num = int(choice) - 1
                    attack_used = list(player.attacks_used)[attack_num]
                    attack_max_used = player.attacks[attack_num]["stats"]["max_use"]
                    wappon = player.equipt_slots["wappon"]
                    needed_wappon = player.attacks[attack_num]["wapon"]
                    if needed_wappon == []:
                        pass
                    else:
                        if wappon[1] == None:
                            printr("You dont have a wapon")
                            # print(needed_wappon)
                            # print(wappon[1])
                            wait(10)
                            continue
                        elif not wappon[1].sub_type in needed_wappon:
                            printr(
                                f"You dont have the requred wapon, you need a {needed_wappon}"
                            )
                            # print(needed_wappon)
                            # print(wappon[1].sub_type)
                            wait(10)
                            continue
                    if player.attacks_used[attack_used] >= attack_max_used:
                        printr("No more uses of selected attack left")
                        wait(1)
                    elif player.attacks[attack_num]["stats"]["mp"] > player.mp:
                        printr("Not enough mp for this attack")
                        wait(1)
                    else:
                        player.attacks_used[attack_used] += 1
                        player.mp -= player.attacks[attack_num]["stats"]["mp"]
                        player, enemy = fight_roll_dice(
                            player, enemy, 1, 6, attack_num, 1 if first_turn else 0
                        )
                        turn = 0
                        first_turn = False
            except:
                printr("Invalid inputT lol")
                wait(1)


if __name__ == "__main__":
    main_loop = True
    loop_room = False
    loop_fight = False
    CHEATS_ON = True
    Layers = []
    Curent_Layer = 0
    while main_loop:
        out = main_menu()
        if out == "start":
            cls = select_player_class()
            if cls == "Q":
                continue
            Dungeon_type = select_dungeon()
            Layers = []
            Curent_Layer = 0
            if Dungeon_type == "Q":
                continue
            Layers.append(Dungeon(Curent_Layer, Dungeon_type))
            # for _ in range(0):
            #    Curent_Layer += 1
            #    Layers.append(Dungeon(Curent_Layer, Dungeon_type))
            # print(len(Layers))
            DUNGEON = Layers[Curent_Layer]
            player = Player(cls)
            player.add_to_inv(GameItem("legendary", "sword", 75))
            player.add_to_inv(GameItem("common", "sword", 10))
            GAME_STATE = "map"
            game_loop_room(player)
        # game_menu()
        # give all
        elif out == "exit":
            main_loop = False
            break
