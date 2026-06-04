import random
    
from data import Game_text_data as GTD
from src.graphic import Graphic
from src.Items import GameItem
from gamestate import GameState
    
    
from src import player as Mply
from src import enemy as Mene
from src import dungeon as Mdun
from src import fight as Mfight


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
        


def show_help_new(GS:GameState):
    max_page = 0
    if GS.other is None:
        raise LookupError("GameState has other no other set: show_help_new needs other to have element 'page'")
    page = GS.other["page"]
    help_text = GTD.help_txt
    while True:
        Graphic.clear()
        Graphic.printr(f"""=============
    Help Page {page} / {max_page}
P = Privios Page | N = Next """)
        Graphic.printr(help_text[f"page {page}"])
        Graphic.update()
        choice = Graphic.inputT("Press Enter to return... > ").upper().strip()
        if choice == "N":
            if page < max_page:
                page += 1
        elif choice == "P":
            if page > 0:
                page -= 1
        elif choice == "Q":
            GS.ret_loop()
            return





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


def print_dungeon_map(GS:GameState, spacing=1, room_size=2):
    Graphic.print_dungeon_map(GS.dungeon, spacing, room_size, GS.cheats_on)
    Graphic.update()
    Graphic.inputT("\nPress Enter to return...")


def cheats(choice,GS) -> bool:
    player = GS.player
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
        return True
    elif choice == "GIVE ALL ALL":
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
        return True
    elif choice == "LEVEL UP":
        player.Level(player.max_xp + 1)
        return True
    elif choice == "GIVE ITEM":
        player.add_to_inv(GameItem("common", "sword", 10))
        return True
    elif choice == "FIGHT":
        enemy = Mene.Enemy("Zomby", random.randint(1, 5),0,None, 5, 5)
        player, loop_room = Mfight.fight_loop(player, enemy)
        return True
    elif choice == "TP":
        choice = Graphic.inputT("> ").upper().strip()
        GS.dungeon.room = int(choice)
        return True
    else:
        return False




def game_loop_room(GS:GameState):
        dungeon: Mdun.Dungeon = GS.dungeon
        player :Mply.Player = GS.player
        choice = Graphic.game_menu(GS)
        choice = str(choice).upper().strip()
        if choice == "/":
            choice = Graphic.inputT("> ", True).upper().strip()
        if choice == "H":
            GS.new_loop("help",{"page":0})
            return
        elif choice == "T":
            player.show_stats()
            return
        elif choice == "I":
            player.show_inventory()
            return
        elif choice == "M":
            
            print_dungeon_map(GS)
            return
        elif choice == "Q":
            choice = Graphic.inputT("You sure you want to qite? [Y/N]>").upper().strip()
            if choice == "Y" or choice == "Q":
                GS.ret_loop()
                return
        elif choice == "UP UP DOWN DOWN LEFT RIGHT LEFT RIGHT B A":
            GS.cheats_on = True
            Graphic.printr("Cheats Enabled")
            return
        if GS.cheats_on:
            cheat_used = cheats(choice,GS)
            if cheat_used: return
        if player.moves >= 0:
            if any(c not in ("W", "A", "S", "D") for c in choice):
                Graphic.printr("Invalid inputT")
                Graphic.wait(1)
                return
            elif len(choice) <= player.moves:
                for i in choice:
                    out = player.move(i, GS)
                    if out == "brake":
                        Graphic.wait(1)
                        break
                return
        elif player.moves == -2:
            if choice == "R":
                player.roll_for_move()
                return
                # wait(1)
            elif choice == "P":
                player.rest()
                player.moves = -1
                return
        elif player.moves == -1:
            Mene.enemy_move(GS)
            for rom in dungeon.rooms:
                for sp in dungeon.rooms[rom].spawners:
                    sp.update(player)
            player.moves = -2
        else:
            Graphic.printr("Invalid inputT")
            Graphic.wait(1)



def main_loop(gamestate:GameState):
    struc = {"start": "Start Game", "help": "How to Play","mods":"Mod opptions", "exit": "Quit"}
    choice,_ = Graphic.select_menu_page("DICE DUNGEON: DESCENT", struc, {"Q": "exit"})
    # printr(choice)
    if choice == "start":
        GTD.load_mods()
        cls = select_player_class()
        if cls == "Q":
            return
        sel_d_type = select_dungeon()
        if sel_d_type == "Q":
            return
        else:
            gamestate.dungeon_type = sel_d_type
        gamestate.layers.append(Mdun.Dungeon(gamestate.curent_Layer, gamestate.dungeon_type))
        gamestate.dungeon = gamestate.layers[gamestate.curent_Layer]
        gamestate.player = Mply.Player(cls)
        gamestate.new_loop("room")
    elif choice == "help":
        gamestate.new_loop("help",{"page":0})
    elif choice == "mods":
        mod_menu()
    elif choice == "exit":
        Graphic.printr("Goodbye, hero...")
        Graphic.update()
        Graphic.wait(0.1)
        gamestate.running = False
    else:
        Graphic.printr("Invalid option.")
        Graphic.update()
        Graphic.wait(1)


GAMESTATE = GameState()
GAMESTATE.running = True
if __name__ == "__main__":

    while GAMESTATE.running:
        
        match GAMESTATE.loop:
            case "main":
                main_loop(GAMESTATE)
            case "room":
                game_loop_room(GAMESTATE)
            case "help":
                show_help_new(GAMESTATE)
        
        