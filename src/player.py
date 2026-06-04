import math
#from tkinter import TclError

from data import Game_text_data as GTD
from .graphic import Graphic
from .Items import GameItem
from gamestate import GameState

from . import afiliation as Mafi
from . import dungeon as Mdun
from . import fight as Mfight 
from . import enemy as Mene
from . import inventory as Minv 

from .room_object.cheast import Cheast
from .room_object.trape import Trape
from .room_object.merchent import Merchent

# from src.player import *
# from src.enemy import *
# from src.dungeon import *
# from src.afiliation import Afiliations
# from src.fight import fight_loop

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
        self.inventory : Minv.Inventory = Minv.Inventory()
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
        self.inventory.add(GameItem(*GTD.player_cls[cls]["item"]))
        self.attacks: list = []
        self.attacks_used: dict[str, int] = {}
        for i in GTD.player_cls[cls]["attacks"]:
            self.attacks.append(GTD.attacks[i])
            self.attacks_used[i] = 0
        self.ele_afi = Mafi.Afiliations(
            GTD.ele_list, GTD.player_cls[cls]["affiliations"]["elements"]
        )
        self.wapon_afi = Mafi.Afiliations(
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
    

    def item_stats_add(self):
        self.max_hp_items: int = 0
        self.max_mp_items: int = 0
        self.atk_items: int = 0
        self.sp_atk_items: int = 0
        self.def_items: int = 0
        self.sp_def_items: int = 0
        self.crit_chance_items: int = 0
        self.crit_bonus_items: int = 0
        for item in self.inventory.equiped_items:
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

        if self.inventory.equipt_slots["wappon"][1]:
            self.wapon_ele = self.inventory.equipt_slots["wappon"][1].ele
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
                    Graphic.printr("Invalid inputT")
                    Graphic.wait(1)
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

    def move(self, dir: str, GS: GameState):
        dungeon = GS.dungeon
        room = dungeon.rooms[dungeon.room]
        self.last_pos = [self.x, self.y]
        x, y = self.x, self.y
        if dir == "W":
            if y - 1 < 0:
                Graphic.printr("Move in valed")
                return "brake"
            elif room.map[y - 1][x] != "#":
                self.y -= 1
                self.moves -= 1
            else:
                Graphic.printr("Move in valed")
                Graphic.printr(room.map[y - 1][x])
                return "brake"
        elif dir == "S":
            if y + 1 >= len(room.map):
                Graphic.printr("Move in valed")
                return "brake"
            elif room.map[y + 1][x] != "#":
                self.y += 1
                self.moves -= 1
            else:
                Graphic.printr("Move in valed")
                Graphic.printr(room.map[y + 1][x])
                return "brake"
        elif dir == "D":
            if x + 1 >= len(room.map[0]):
                Graphic.printr("Move in valed")
                return "brake"
            elif room.map[y][x + 1] != "#":
                self.x += 1
                self.moves -= 1
            else:
                Graphic.printr("Move in valed")
                Graphic.printr(room.map[y][x + 1])
                return "brake"
        elif dir == "A":
            if x - 1 < 0:
                Graphic.printr("Move in valed")
                return "brake"
            elif room.map[y][x - 1] != "#":
                self.x -= 1
                self.moves -= 1
            else:
                Graphic.printr("Move in valed")
                Graphic.printr(room.map[y][x - 1])
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
            if GS.curent_Layer <= 0:
                pass
            else:
                GS.curent_Layer -= 1
                dungeon = GS.layers[GS.curent_Layer]
                new_room = dungeon.rooms[dungeon.room]
                new_room.show_on_map = True
                self.y = len(new_room.map) // 2
                self.x = len(new_room.map[0]) // 2
        elif room.map[y][x] == "s":
            GS.curent_Layer += 1
            if len(GS.layers) <= GS.curent_Layer:
                GS.layers.append(Mdun.Dungeon(GS.Curent_Layer, GS.Dungeon_type))
            dungeon = GS.layers[GS.curent_Layer]
            new_room = dungeon.rooms[dungeon.room]
            new_room.show_on_map = True
            self.y = len(new_room.map) // 2
            self.x = len(new_room.map[0]) // 2
        update_player(self, room)
        #Graphic.game_menu(self, dungeon,GAME_STATE)
        #print_room_options(self)
        Graphic.wait(0.1)
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
    enemys: list[Mene.Enemy] = room.enemys
    traps: list[Trape] = room.traps
    cheasts: list[Cheast] = room.cheasts
    shops: list[Merchent] = room.shops
    px, py = player.x, player.y
    for e in enemys:
        Graphic.update()
        if e.x == px and e.y == py:
            if player.moves < 0:
                Mfight.fight_loop(player, e, False)
            else:
                Mfight.fight_loop(player, e, True)
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