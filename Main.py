import math
import os
import random
import time
from random import Random, choice, randint

import Game_text_data as GTD
import Graphic
from Graphic import inputT, printr
from Items import GameItem

# from collections import deque

OPPOSITE = {"top": "bottom", "bottom": "top", "left": "right", "right": "left"}
SIDES = ["top", "bottom", "left", "right"]


def clear():
    os.system("cls" if os.name == "nt" else "clear")


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
        self.add_to_inv(GameItem(*GTD.player_cls[cls]["item"]))
        self.attacks: list[str] = []
        self.attacks_used: dict[str, int] = {}
        for i in GTD.player_cls[cls]["attacks"]:
            self.attacks.append(GTD.attacks[i])
            self.attacks_used[i] = 0

        self.hp: int = self.max_hp
        self.mp: int = self.max_mp
        self.item_stats_add()

    def next_level_xp(self, level: int):
        return (math.floor((((math.log(level**2, 10)) ** 2) + 1) * 5)) * 3

    def roll_for_move(self):
        roll = roll_dice(self.min_move, self.max_move)
        self.moves = roll
        return roll

    def add_to_inv(self, item: GameItem):
        self.inventory.append(item)

    def equip_item(self, item: GameItem):
        if item.item_type in self.equipt_slots:
            slot: str = item.item_type
        elif item.item_type == "consumable":
            slot = item.item_type
        else:
            slot = "wappon"
        if item in self.equiped_items:
            self.equiped_items.remove(item)
            item.is_equiped = False
            self.equipt_slots[slot][0] = False
            self.equipt_slots[slot][1] = None
        else:
            if self.equipt_slots[slot][0]:
                printr(f"You have laredy a {slot} equipped")
                choice = inputT("Do you want to swape? [y/n]>")
                if choice == "y":
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
        def items_per_page(is_selected: bool) -> int:
            return 4 if is_selected else 6

        is_item_selected: bool = False
        page: int = 0
        is_fav: bool = False
        is_equ: bool = False
        item_fillter = self.inventory
        selected_item: None | GameItem = None
        selected_num = None
        show_inv = True
        while show_inv:
            # clear()
            per_page = items_per_page(is_item_selected)
            max_page = max(0, (len(item_fillter) - 1) // per_page)

            Graphic.show_inventory(
                page,
                per_page,
                max_page,
                is_item_selected,
                item_fillter,
                selected_item,
                is_shop,
                self.gold,
            )

            choice = inputT("> ").upper().strip()
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
                            page = selected_num // 6
                            selected_num = None
                    else:
                        self.equip_item(selected_item)
                else:
                    printr("No item select")
                    time.sleep(1)
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
                    else:
                        self.favorit.append(selected_item)
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
                choice = inputT("Selacte page > ").upper().strip()
                try:
                    if (int(choice) - 1) >= 0 and (int(choice) - 1) <= max_page:
                        page = int(choice) - 1
                except:
                    printr("Invalid inputT")
                    time.sleep(1)
            elif is_item_selected and (choice == ""):
                selected_item = None
                is_item_selected = False
                page = selected_num // 6
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
                            page = choice // 6
                        else:
                            selected_item = item_fillter[choice]
                            is_item_selected = True
                            selected_num = choice
                            page = choice // 4
                except:
                    printr("Invalid inputT")
                    time.sleep(1)

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
            self.max_hp_items += item.max_hp
            self.max_mp_items += item.max_mp
            self.atk_items += item.atk
            self.sp_atk_items += item.sp_atk
            self.def_items += item.def_
            self.sp_def_items += item.sp_def
            self.crit_chance_items += item.crit_chance
            self.crit_bonus_items += item.crit_bonus

        if self.hp > self.max_hp + self.max_hp_items:
            self.hp = self.max_hp + self.max_hp_items
        if self.mp > self.max_mp + self.max_mp_items:
            self.mp = self.max_mp + self.max_mp_items

    def Level(self, xp: int):
        self.xp += xp
        if self.xp >= self.max_xp:
            loop_levelup = True
            while loop_levelup:
                Graphic.show_stats_level(self)
                choice = inputT("> ").strip()
                if choice == "1":
                    rand = roll_dice(1, 6, -1)
                    self.max_hp += rand
                    self.hp += rand
                    loop_levelup = False
                elif choice == "2":
                    rand = roll_dice(1, 6, -1)
                    self.max_mp += rand
                    self.mp += rand
                    loop_levelup = False
                elif choice == "3":
                    self.atk += roll_dice(1, 6, -1)
                    loop_levelup = False
                elif choice == "4":
                    self.sp_atk += roll_dice(1, 6, -1)
                    loop_levelup = False
                elif choice == "5":
                    self.def_ += roll_dice(1, 6, -1)
                    loop_levelup = False
                elif choice == "6":
                    self.sp_def += roll_dice(1, 6, -1)
                    loop_levelup = False
                elif choice == "7":
                    self.crit_chance += roll_dice(1, 6, -1)
                    loop_levelup = False
                elif choice == "8":
                    self.crit_bonus += roll_dice(1, 6, -1)
                    loop_levelup = False
                elif choice == "9":
                    rand = roll_dice(1, 6, -1)
                    self.min_move += rand
                    self.max_move += rand
                    loop_levelup = False
                else:
                    printr("Invalid inputT")
                    time.sleep(1)
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

    def move(self, dir: str, dungeon: Dungeon):
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
        time.sleep(0.2)
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
        self, mob: str, level: int, room: Room, x: int, y: int, is_boss: bool = False
    ) -> None:
        self.room: Room = room
        self.mob: str = mob
        self.is_boss: bool = is_boss
        self.x: int = x
        self.y: int = y
        self.is_del: bool = False
        self.level: int = level
        if is_boss:
            stats: dict[str, int] = GTD.bosses[mob]["stats"]
        else:
            stats: dict[str, int] = GTD.enemy_cls[mob]["stats"]
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
        self.level_up()
        self.hp: int = self.max_hp
        self.mp: int = self.max_mp
        self.get_attack_stats()
        self.items: list[GameItem] = []
        self.get_items()
        self.item_stats_add()

    def level_up(self) -> None:
        self.max_hp += 3 * (self.level - 1)
        self.max_mp += 3 * (self.level - 1)
        self.atk += 1 * (self.level - 1)
        self.sp_atk += 1 * (self.level - 1)
        self.def_ += 1 * (self.level - 1)
        self.sp_def += 1 * (self.level - 1)
        self.gold += 2 * (self.level - 1)
        self.xp += 2 * (self.level - 1)

    def item_stats_add(self) -> None:
        for item in self.items:
            self.max_hp += item.max_hp
            self.max_mp += item.max_mp
            self.atk += item.atk
            self.sp_atk += item.sp_atk
            self.def_ += item.def_
            self.sp_def += item.sp_def
            self.crit_chance += item.crit_chance
            self.crit_bonus += item.crit_bonus

        self.hp = self.max_hp
        self.mp = self.max_mp

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
            time.sleep(0.2)

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
        try:
            self.room.enemys.remove(self.room)
        except:
            pass
        del (
            self.room,
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
        self.layer = GTD.dungeons_preset[type]["layers"][layer]
        size_a = (
            GTD.dungeons_preset[type]["size"][0] + GTD.layers[self.layer]["size"][0]
        ) // 2
        size_b = (
            GTD.dungeons_preset[type]["size"][1] + GTD.layers[self.layer]["size"][1]
        ) // 2
        rand = random.randint(size_a, size_b)
        self.room_pos = []
        self.rooms = self.gen_dungeon(num_rooms=rand, layer=self.layer)
        self.rooms[0].show_on_map = True
        self.room = 0

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
                        if random.randint(0, 3) == 0:
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

                new_room = Room(next_id, room_type, layer=layer)
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
    ):
        self.id = room_id
        self.type = room_type
        self.pos = (x, y)
        self.layer = layer
        self.doors = []  # [target_room_id, ...]
        self.enemys = []
        self.traps = []
        self.cheasts = []
        self.shops = []
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
                e_level = layer["level"] + random.randint(-3, 3)
                if e_level <= 0:
                    e_level = 1
                self.enemys.append(Enemy(j, e_level, self, x, y))

    def place_boss(self, width, height, layer="layer 1"):
        x = width
        y = height
        layer = GTD.layers[layer]
        e_level = layer["level"] + random.randint(-3, 3)
        if e_level <= 0:
            e_level = 1
        self.enemys.append(Enemy(layer["boss"], e_level, self, x, y, True))

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
                self.traps.append(Trape(width, height, j))

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
                        if self.map[y][x] == ".":
                            self.map[y][x] = "#"

                    elif rand_2 == 6:
                        x = random.randint(2, width - 1)
                        y = random.randint(2, height - 1)
                        if self.map[y][x] == ".":
                            self.map[y][x] = "#"
                    elif rand_2 == 5:
                        x = random.randint(2, width - 1)
                        y = random.randint(2, height - 1)
                        if self.map[y][x] == ".":
                            self.map[y][x] = "#"
                    elif rand_2 == 2:
                        x = random.randint(1, width)
                        y = random.randint(1, height)
                        if self.map[y][x] == ".":
                            self.place_cheast(x, y)
                    elif rand_2 == 3:
                        x = random.randint(1, width)
                        y = random.randint(1, height)
                        if self.map[y][x] == ".":
                            self.place_trap(x, y, layer)
                    elif rand_2 == 4:
                        x = random.randint(1, width)
                        y = random.randint(1, height)
                        if self.map[y][x] == ".":
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
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.show = False
        self.coldown = 0
        self.type = type

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
            printr(temp)
        if self.type == "Mimic":
            inputT("\nPress Enter to return...")
            level = GTD.layers[Layers[Curent_Layer].layer]["level"]
            enemy = Enemy("Mimic", level, None, 0, 0)
            player = fight_loop(player, enemy, False)
        else:
            inputT("\nPress Enter to return...")
            if GTD.traps[self.type]["damage_type"] == 0:
                player.hp -= GTD.traps[self.type]["damage"]
            elif GTD.traps[self.type]["damage_type"] == 1:
                base = GTD.traps[self.type]["damage"]
                roll = roll_dice(1, 6, 0)
                damage = int((base / 5) * (6 - roll))
                player.hp -= damage
            elif GTD.traps[self.type]["damage_type"] == 2:
                base = GTD.traps[self.type]["damage"]
                base = int((player.max_hp / 100) * base)
                roll = roll_dice(1, 6, 0)
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
        level = GTD.layers[layer]["level"] + random.randint(*cheast["level"])
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
            level = self.layer["level"] + randint(*self.gtd_shop["level"])
            items.append(GameItem(item_rarety, item_type, level))

        return items

    def shop_buy(self, player):
        def items_per_page(is_selected: bool) -> int:
            return 4 if is_selected else 6

        is_item_selected: bool = False
        page: int = 0
        item_fillter = self.items
        selected_item: None | GameItem = None
        selected_num = None
        show_inv = True
        while show_inv:
            per_page = items_per_page(is_item_selected)
            max_page = max(0, (len(item_fillter) - 1) // per_page)

            Graphic.shop_buy_page(
                page,
                per_page,
                max_page,
                is_item_selected,
                item_fillter,
                selected_item,
                player.gold,
            )
            choice = inputT("> ").upper().strip()
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
                            page = selected_num // 6
                            selected_num = None
                    else:
                        printr("You don’t have enough gold to buy this item")
                        time.sleep(1)
                else:
                    printr("No Item Selected")
                    time.sleep(1)

            elif choice == "PAGE":
                choice = inputT("Selacte page > ").upper().strip()
                try:
                    if (int(choice) - 1) >= 0 and (int(choice) - 1) <= max_page:
                        page = int(choice) - 1
                except:
                    printr("Invalid inputT")
                    time.sleep(1)
            elif is_item_selected and (choice == ""):
                selected_item = None
                is_item_selected = False
                page = selected_num // 6
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
                            page = choice // 6
                        else:
                            selected_item = item_fillter[choice]
                            is_item_selected = True
                            selected_num = choice
                            page = choice // 4
                except:
                    printr("Invalid inputT")
                    time.sleep(1)

    def interact_player(self, player):
        is_in_shop: bool = True
        while is_in_shop:
            Graphic.shop_start_page()
            choice = inputT("> ").upper().strip()
            if choice == "Q" or choice == "3":
                is_in_shop = False
            elif choice == "2":
                player.show_inventory(True)
            elif choice == "1":
                self.shop_buy(player)
            else:
                printr("Invalid inputT")


def update_player(player, room):
    enemys: list[Enemy] = room.enemys
    traps: list[Trape] = room.traps
    cheasts: list[Cheast] = room.cheasts
    shops: list[Merchent] = room.shops
    px, py = player.x, player.y
    for e in enemys:
        if e.x == px and e.y == py:
            if player.moves < 0:
                fight_loop(player, e, False)
            else:
                fight_loop(player, e, True)
            if e.is_boss:
                player.x, player.y = player.last_pos
            e.del_()
    for t in traps:
        if t.coldown > 0:
            t.coldown -= 1
            continue
        elif t.x == px and t.y == py:
            t.triger(player)
    for c in cheasts:
        if c.x == px and c.y == py:
            c.give_player(player)
    for m in shops:
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
        enemy = steck.pop(0)
        if enemy.is_del:
            try:
                room.enemys.remove(enemy)
                del enemy
            except:
                continue
        else:
            enemy.move(player, room, dungeon)
        try:
            if enemy.is_del:
                room.enemys.remove(enemy)
                del enemy
        except:
            continue


def print_room_options(player):
    printr("======== Your turn =========")
    if player.moves == -2:
        if player.cls == "Roghe":
            printr("R = Roll dice to move | F = Roll to check for traps")
        printr("R = Roll dice to move | P = Make a pause and restr")
    elif player.moves > 0:
        printr(f"Moves {player.moves} left")
    else:
        player.moves = -1


def roll_dice(start, end, advan=0):
    rand = 0
    for i in range(10):
        rand_o = rand
        while rand == rand_o:
            rand = random.randint(start, end)
        rand += advan
        if rand < start:
            rand = start
        elif rand > end:
            rand = end
        rand_str = str(rand)
        if len(rand_str) == 1:
            rand_str = " " + rand_str
        if len(rand_str) == 2:
            rand_str = rand_str + " "
        clear()
        printr(f"""
=========================
        Dice Roll
         –––––––
        |       |
        |  {rand_str}  |
        |       |
         –––––––

=========================
""")
        time.sleep((i + 1) / 50)
    inputT("\nPress Enter to return...")
    return rand


def main_menu():
    while True:
        clear()
        printr("""
===================================
       DICE DUNGEON: DESCENT
===================================
 [1] Start Game
 [2] How to Play
 [3] Quit
""")
        choice = inputT("> ").upper().strip()
        if choice == "1":
            return "start"
        elif choice == "2":
            show_help_new()
        elif choice == "3" or "Q":
            printr("Goodbye, hero...")
            time.sleep(1)
            return "exit"
        else:
            printr("Invalid option.")
            time.sleep(1)


def show_help_new(page=0):
    max_page = 0
    help_text = GTD.help_txt
    while True:
        clear()
        printr(f"""=============
    Help Page {page} / {max_page}
P = Privios Page | N = Next """)
        printr(help_text[f"page {page}"])
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
    hp: str = f"HP {player.hp}/{player.max_hp + player.max_hp_items}"
    mp: str = f"MP {player.mp}/{player.max_mp + player.max_mp_items}"
    gold: str = f"Gold {player.gold}"
    xp: str = f"XP {player.xp}/{player.max_xp}"
    level: str = f"Level {player.level}"
    while len(hp) < 13:
        hp += " "
    while len(mp) < 13:
        mp += " "
    while len(gold) < 13:
        gold += " "
    while len(xp) < 13:
        xp += " "
    while len(level) < 13:
        level += " "
    clear()
    printr(f"""
========================================
              Dice Dungeon
{hp}  {mp}  {gold}
{level}  {xp}
H = Help | I = Invetory | T = Stats
Q = Quit
========================================""")
    if GAME_STATE == "map":
        dungeon.print_room(player)
    return player


def select_player_class():
    cls = []
    for i in GTD.player_cls:
        cls.append(i)
    while True:
        clear()
        printr("""
======================
Selacte a player class
======================""")
        for i in range(len(cls)):
            printr(f"[{i}] {cls[i]}")
        choice = inputT("> ").strip().upper()

        if choice == "Q":
            return "Q"
        try:
            if int(choice) >= 0 and int(choice) < len(cls):
                return cls[int(choice)]
            else:
                printr("Invalid option.")
                time.sleep(1)
        except:
            printr("Invalid option.")
            time.sleep(1)


def select_dungeon():
    d_type = []
    for i in GTD.dungeons_preset:
        d_type.append(i)
    while True:
        clear()
        printr("""
======================
Selacte a dungeon
======================""")
        for i in range(len(d_type)):
            printr(f"[{i}] {d_type[i]}")
        choice = inputT("> ").strip().upper()

        if choice == "Q":
            return "Q"
        try:
            if int(choice) >= 0 and int(choice) < len(d_type):
                return d_type[int(choice)]
            else:
                printr("Invalid option.")
                time.sleep(1)
        except:
            printr("Invalid option.")
            time.sleep(1)


def print_dungeon_map(dungeon, spacing=1, room_size=2):
    # 1. BFS: relative Positionen bestimmen
    rooms = dungeon.rooms
    printr(rooms)
    if len(str(rooms[len(rooms) - 1].id)) > room_size:
        room_size = len(str(rooms[len(rooms) - 1].id))
    clear()
    positions = [room.pos for room in dungeon.rooms.values()]

    # printr('conn:',conn,' px,py:',px,py,' w,h:',w,h,' dx,dy:',dx,dy)

    # 2. Grid vorbereiten
    xs = [p[0] for p in positions]
    ys = [p[1] for p in positions]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)

    width = (maxx - minx + 1) * (room_size + (spacing * 2)) - spacing
    height = (maxy - miny + 1) * (room_size + spacing) - spacing

    grid = [[" " for _ in range(width)] for _ in range(height)]

    # 3. Räume zeichnen
    room_coords = {}
    for room in dungeon.rooms.values():
        # if room.show_on_map == False:
        # continue
        gx, gy = room.pos
        gx = (gx - minx) * (room_size + (spacing * 2))
        gy = (gy - miny) * (room_size + spacing)

        rid_str = str(room.id)
        if room.show_on_map or CHEATS_ON:
            if room.id == dungeon.room:
                if len(rid_str) < room_size:
                    for i in range(room_size - len(rid_str)):
                        grid[gy][gx + len(rid_str) + i] = "\33[32m#\33[0m"
                grid[gy][gx : gx + len(rid_str)] = [
                    f"\33[32m{i}\33[0m" for i in rid_str
                ]
                for i in range(room_size - 1):
                    for j in range(room_size):
                        grid[gy + 1 + i][gx + j] = "\33[32m#\33[0m"
            elif room.type == "boss":
                if len(rid_str) < room_size:
                    for i in range(room_size - len(rid_str)):
                        grid[gy][gx + len(rid_str) + i] = "\33[31m#\33[0m"
                grid[gy][gx : gx + len(rid_str)] = [
                    f"\33[31m{i}\33[0m" for i in rid_str
                ]
                for i in range(room_size - 1):
                    for j in range(room_size):
                        grid[gy + 1 + i][gx + j] = "\33[31m#\33[0m"
            elif room.type == "merchant":
                if len(rid_str) < room_size:
                    for i in range(room_size - len(rid_str)):
                        grid[gy][gx + len(rid_str) + i] = "\33[34m#\33[0m"
                grid[gy][gx : gx + len(rid_str)] = [
                    f"\33[34m{i}\33[0m" for i in rid_str
                ]
                for i in range(room_size - 1):
                    for j in range(room_size):
                        grid[gy + 1 + i][gx + j] = "\33[34m#\33[0m"
            else:
                if len(rid_str) < room_size:
                    for i in range(room_size - len(rid_str)):
                        grid[gy][gx + len(rid_str) + i] = "#"
                grid[gy][gx : gx + len(rid_str)] = list(rid_str)
                for i in range(room_size - 1):
                    for j in range(room_size):
                        grid[gy + 1 + i][gx + j] = "#"
        room_coords[room.id] = (gx, gy)

    # 4. Linien nur zwischen Räumen in Zwischenzellen
    # printr(rooms)
    for room in dungeon.rooms.values():
        if room.show_on_map == False and CHEATS_ON == False:
            continue
        gx, gy = room_coords[room.id]
        for i, conn in enumerate(room.doors):
            cgx, cgy = room_coords[conn]
            # Vertikal
            if gx == cgx:
                start = min(gy + room_size, cgy)
                end = max(gy, cgy + room_size)
                for y_pos in range(start, end):
                    if grid[y_pos][gx] == " ":
                        grid[y_pos][gx] = "|"
            # Horizontal
            elif gy == cgy:
                start = min(gx + room_size, cgx)
                end = max(gx + 1, cgx)
                for x_pos in range(start, end):
                    if grid[gy][x_pos] == " ":
                        grid[gy][x_pos] = "–"

    # 5. Ausgabe
    # clear()
    # printr(dungeon.room_pos)
    printr("=" * width)
    text = "Dungeon Map"
    while len(text) < width:
        text += " "
        if len(text) < width:
            text = " " + text
    printr(text)
    for row in grid:
        if any(i != " " for i in row):
            printr("".join(row))
    # for i in rooms:
    # printr('room:',i,'doors',rooms[i].doors)

    inputT("\nPress Enter to return...")


def game_loop_room(player):
    global loop_room, Layers, DUNGEON, CHEATS_ON
    loop_room = True
    while loop_room:
        dungeon = DUNGEON
        game_menu(player, dungeon)
        print_room_options(player)
        choice = inputT("> ").upper().strip()
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
        if CHEATS_ON:
            if choice == "GIVE ALL":
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
            elif choice == "LEVEL UP":
                player.Level(player.max_xp + 1)
                continue
            elif choice == "GIVE ITEM":
                player.add_to_inv(GameItem("common", "sword", 10))
                continue
            elif choice == "FIGHT":
                enemy = Enemy("zomby", random.randint(1, 5), 0, 5, 5)
                player, loop_room = fight_loop(player, enemy)
                continue
            elif choice == "TP":
                choice = inputT("> ").upper().strip()
                dungeon.room = int(choice)
        if player.moves == -2:
            if choice == "R":
                player.roll_for_move()
                continue
                # time.sleep(1)
            elif choice == "P":
                player.rest()
                player.moves = -1
                continue

        if player.moves >= 0:
            if any(c not in ("W", "A", "S", "D") for c in choice):
                printr("Invalid inputT")
                time.sleep(1)
                continue
            elif len(choice) <= player.moves:
                for i in choice:
                    out = player.move(i, dungeon)
                    if out == "brake":
                        time.sleep(1)
                        break
                continue
        if player.moves == -1 and choice == "":
            enemy_move(dungeon, player)
            player.moves = -2
        else:
            printr("Invalid inputT")
            time.sleep(1)


def fight_selact_attack(player, enemy):
    clear()
    Graphic.print_fight_UI(player, enemy)


def p_chance(chance):
    rand = random.randint(1, 100)
    return True if rand <= chance else False


def fight_roll_dice(player, enemy, start, end, sel=0, advan=0, atk=True):
    rand = 0
    if atk:
        advan += player.attacks[sel]["stats"]["adv"]
        player.mp -= player.attacks[sel]["stats"]["mp"]
        for i in range(20):
            clear()
            Graphic.print_fight_UI(player, enemy, False)
            Graphic.fight_roll_dice(player, enemy, start, end, advan, atk, False)
            time.sleep((i + 1) / 50)
        clear()
        Graphic.print_fight_UI(player, enemy, False)
        rand, rand_e = Graphic.fight_roll_dice(
            player, enemy, start, end, advan, atk, False
        )

        p_crit = (
            player.crit_chance
            + player.crit_chance_items
            + player.attacks[sel]["stats"]["crit_chance"]
        )
        p_crit = p_chance(p_crit)
        if p_crit:
            printr("Crit")

        p_atk = player.atk + player.atk_items
        p_atk = int(p_atk * (player.attacks[sel]["stats"]["atk"] / 100))
        p_crit_bonus = (
            player.crit_bonus
            + player.crit_bonus_items
            + player.attacks[sel]["stats"]["crit_bonus"]
        )
        p_atk += int(p_atk * (p_crit_bonus / 100)) if p_crit else 0
        stranth = p_atk * rand
        printr("stranth", stranth)

        p_sp_atk = player.sp_atk + player.sp_atk_items
        p_sp_atk = int(p_sp_atk * (player.attacks[sel]["stats"]["sp_atk"] / 100))
        p_crit_bonus = (
            player.crit_bonus
            + player.crit_bonus_items
            + player.attacks[sel]["stats"]["crit_bonus"]
        )
        p_sp_atk += int(p_sp_atk * (p_crit_bonus / 100)) if p_crit else 0
        sp_stranth = p_sp_atk * rand
        printr("sp_stranth", sp_stranth)

        e_def = enemy.def_
        e_def = e_def * rand_e
        printr("e_def", e_def)

        e_sp_def = enemy.sp_def
        e_sp_def = e_sp_def * rand_e
        printr("e_sp_def", e_sp_def)

        demage = stranth - e_def
        if demage < 0:
            demage = 0
        sp_damage = sp_stranth - e_sp_def
        if sp_damage < 0:
            sp_damage = 0
        demage += sp_damage
        printr(f"Damage {demage}")
        enemy.hp -= demage

        inputT("\nPress Enter to return...")
        return player, enemy
    else:
        advan_e = 0
        e_attack_num = random.randint(0, 3)
        e_attack_used = list(enemy.attacks_used)[e_attack_num]
        printr(enemy.attacks)
        printr(type(enemy.attacks))
        e_attack_mp_use = enemy.attacks[e_attack_num]["stats"]["mp"]
        e_attack_max_used = enemy.attacks[e_attack_num]["stats"]["max_use"]
        while (enemy.attacks_used[e_attack_used] >= e_attack_max_used) or (
            enemy.mp < e_attack_mp_use
        ):
            e_attack_num = random.randint(0, 3)
            e_attack_used = list(enemy.attacks_used)[e_attack_num]
            e_attack_mp_use = enemy.attacks[e_attack_num]["stats"]["mp"]
            e_attack_max_used = enemy.attacks[e_attack_num]["stats"]["max_use"]
        e_attack = enemy.attacks[e_attack_num]["stats"]
        enemy.attacks_used[e_attack_used] += 1
        printr(e_attack)
        advan_e = e_attack["adv"]
        advan += player.attacks[sel]["stats"]["adv"]
        for i in range(20):
            clear()
            Graphic.print_fight_UI(player, enemy, False)
            Graphic.fight_roll_dice(
                player, enemy, start, end, advan, advan_e, atk, True
            )
            time.sleep((i + 1) / 50)
        clear()
        Graphic.print_fight_UI(player, enemy, False)
        rand, rand_e = Graphic.fight_roll_dice(
            player, enemy, start, end, advan, advan_e, atk, True
        )

        e_crit = enemy.crit_chance + e_attack["crit_chance"]
        e_crit = p_chance(e_crit)
        if e_crit:
            printr("Enemy Crit")

        e_atk = enemy.atk
        e_atk = int(e_atk * (e_attack["atk"] / 100))
        e_crit_bonus = enemy.crit_bonus + e_attack["crit_bonus"]
        e_atk += int(e_atk * (e_crit_bonus / 100)) if e_crit else 0
        stranth = e_atk * rand_e
        printr("stranth", stranth)

        e_sp_atk = enemy.sp_atk
        e_sp_atk = int(e_sp_atk * (e_attack["sp_atk"] / 100))
        e_crit_bonus = enemy.crit_bonus + e_attack["crit_bonus"]
        e_sp_atk += int(e_sp_atk * (e_crit_bonus / 100)) if e_crit else 0
        sp_stranth = e_sp_atk * rand_e
        printr("sp_stranth", sp_stranth)

        p_def = player.def_ + player.def_items
        p_def = p_def * rand
        printr("p_def", p_def)

        p_sp_def = player.sp_def + player.sp_def_items
        p_sp_def = p_sp_def * rand
        printr("p_sp_def", p_sp_def)

        demage = stranth - p_def
        if demage < 0:
            demage = 0
        sp_damage = sp_stranth - p_sp_def
        if sp_damage < 0:
            sp_damage = 0
        demage += sp_damage
        printr(f"Damage {demage}")
        player.hp -= demage
        enemy.mp -= e_attack_mp_use

        inputT("\nPress Enter to return...")
        return player, enemy


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
    Graphic.print_fight_UI(player, enemy, False)
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


def fight_loop(player, enemy, player_start=True):
    global loop_fight, loop_room
    loop_fight = True
    turn = 1 if player_start else 0
    first_turn = True
    while loop_fight:
        if enemy.hp <= 0:
            fight_won(player, enemy)
            loop_fight = False
            loop_room = True
            return player
        elif player.hp <= 0:
            you_died()
            loop_fight = False
            loop_room = False
            return player

        if turn == 0:
            clear()
            Graphic.print_fight_UI(player, enemy, False)
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
            fight_selact_attack(player, enemy)
            choice = inputT(">").upper().strip()
            try:
                if choice == "Q":
                    loop_fight = False
                    return player, True
                elif choice == "S":
                    printr(enemy)
                    inputT("\nPress Enter to return...")
                elif (0 <= int(choice)) and (int(choice) <= 3):
                    attack_num = int(choice)
                    attack_used = list(player.attacks_used)[attack_num]
                    attack_max_used = player.attacks[attack_num]["stats"]["max_use"]
                    if player.attacks_used[attack_used] >= attack_max_used:
                        printr("No more uses of selected attack left")
                        time.sleep(1)
                    elif player.attacks[attack_num]["stats"]["mp"] > player.mp:
                        printr("Not enough mp for this attack")
                        time.sleep(1)
                    else:
                        player.attacks_used[attack_used] += 1
                        player, enemy = fight_roll_dice(
                            player, enemy, 1, 6, attack_num, 1 if first_turn else 0
                        )
                        turn = 0
                        first_turn = False
            except:
                printr("Invalid inputT")
                time.sleep(1)


if __name__ == "__main__":
    main_loop = True
    loop_room = False
    loop_fight = False
    CHEATS_ON = False
    Layers = []
    Curent_Layer = 0
    while main_loop:
        out = main_menu()
        if out == "start":
            cls = select_player_class()
            if cls == "Q":
                continue
            Dungeon_type = select_dungeon()
            if Dungeon_type == "Q":
                continue
            Layers.append(Dungeon(Curent_Layer, Dungeon_type))
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
