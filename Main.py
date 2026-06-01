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



from src.player import Player
from src.enemy import enemy_move
from src.dungeon import Dungeon
# from src.afiliation import *
# from src.fight import *

# from collections import deque


def wrap_text(text: str, width: int = 72):
    words: list[str] = text.split()
    lines: list[str] = []
    current_line = " "


def mod_menu():
    if GTD.mod_found:
        mods = []
        for i in GTD.mod_loader_settings:
            mods.append(i)
        struc = {f"{mods[i]}": f"[{'X' if GTD.mod_loader_settings[mods[i]] else ' ' }] {mods[i][:-4]}" for i in range(len(mods))}
        cursor_pos = 0
        struc['Q'] = 'Exit'
        while True:
            choice,cursor_pos = Graphic.select_menu_page(
            "Mod menu" , struc, {"Q": "Q"},"Selecte what mods to use\n", cursor_pos
            )
            Graphic.update()
            if choice == "Q":
                GTD.save_mod_loader_settings()
                return
            elif choice in GTD.mod_loader_settings:
                if GTD.mod_loader_settings[choice]:
                    GTD.mod_loader_settings[choice] = False
                else:
                    GTD.mod_loader_settings[choice] = True
                    
                struc = {f"{mods[i]}": f"[{'X' if GTD.mod_loader_settings[mods[i]] else ' ' }] {mods[i][:-4]}" for i in range(len(mods))}
                struc['Q'] = 'Exit'
    else:
        
        choice,_ = Graphic.select_menu_page(
        "Mod menu" ,{'':''}, {"Q": "Q"},"No mods have been found\n\nYou can install mods by creating a folder with the ending\n'_mod'\ninside the mods folder\n\nNormaly there should be an exaple mod\nbut it wasn’t found", 
        )
        Graphic.update()
        return
        

def main_menu():
    struc = {"start": "Start Game", "help": "How to Play","mods":"Mod opptions", "exit": "Quit"}
    while True:
        choice,_ = Graphic.select_menu_page("DICE DUNGEON: DESCENT", struc, {"Q": "exit"})
        # printr(choice)
        if choice == "start":
            return "start"
        elif choice == "help":
            show_help_new()
        elif choice == "mods":
            mod_menu()
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





def select_player_class():
    cls = []
    for i in GTD.player_cls:
        cls.append(i)
    struc = {f"{cls[i]}": f"{cls[i]}" for i in range(len(cls))}

    while True:
        choice,_ = Graphic.select_menu_page(
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
        choice,_ = Graphic.select_menu_page("Selacte a dungeon", struc, {"Q": "Q"})
        Graphic.update()
        return choice


def print_dungeon_map(dungeon, spacing=1, room_size=2):
    Graphic.print_dungeon_map(dungeon, spacing, room_size, CHEATS_ON)
    Graphic.update()
    inputT("\nPress Enter to return...")


def game_loop_room(player):
    global loop_room, Layers, DUNGEON, CHEATS_ON
    loop_room = True
    cursor = [0,0,0,0]
    while loop_room:
        dungeon: Dungeon = DUNGEON
        choice, cursor = Graphic.game_menu(player, dungeon,GAME_STATE,cursor)
        #print_room_options(player)
        choice = str(choice).upper().strip()
        #choice = inputT("> ").upper().strip()
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




if __name__ == "__main__":
    main_loop = True
    loop_room = False
    loop_fight = False
    while main_loop:
        Layers = []
        Curent_Layer = 0
        CHEATS_ON = True
        out = main_menu()
        if out == "start":
            GTD.load_mods()
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
            #player.add_to_inv(GameItem("legendary", "sword", 75))
            #player.add_to_inv(GameItem("common", "sword", 10))
            GAME_STATE = "map"
            game_loop_room(player)
        # game_menu()
        # give all
        elif out == "exit":
            main_loop = False
            break
