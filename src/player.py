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
from src.afiliation import Afiliations
from src.fight import fight_loop

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
        #Graphic.game_menu(self, dungeon,GAME_STATE)
        #print_room_options(self)
        wait(0.1)
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