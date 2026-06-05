import json
import os
from random import sample
from typing import Dict
from gamestate import GameState
from .default_settings import base_settings


settings = base_settings.copy()

settings_change = {}

def op_menu_kate(GS:GameState):
    from src.graphic import Graphic
    kategorys = []
    for i in settings:
        kategorys.append(i)
        
    struc = {
        f"{kategorys[i]}": f"{kategorys[i]} >" for i in range(len(kategorys))
    }
    cursor_pos = 0
    struc['Q'] = 'Exit'
    choice,cursor_pos = Graphic.select_menu_page(
    "Options" , struc, {"Q": "Q"}, cursor_pos= cursor_pos
    )
    
    if choice == "Q":
        GS.ret_loop()
        return
    if GS.other is None:
        GS.other = {"kategory":choice}
    else:
        GS.other["kategory"] = choice

def options_menu(GS:GameState):
    global settings, settings_change
    from src.graphic import Graphic
    
    if GS.other is None or GS.other["kategory"] is None:
        op_menu_kate(GS)
    else:
        kategory = settings[GS.other["kategory"]]
        if  GS.other["kategory"] not in settings_change:
            settings_change[GS.other["kategory"]] = {}
        
        
        struc = {}
        for i in kategory:
            if isinstance(kategory[i],bool):
                if i not in settings_change[GS.other["kategory"]] or settings_change[GS.other["kategory"]][i] == kategory[i]:
                    struc[i] = f"[{'X' if kategory[i] else ' ' }] {i}"
                else:
                    struc[i] = f"[{'X' if settings_change[GS.other["kategory"]][i] else ' ' }] {i}"
            else:
                if i not in settings_change[GS.other["kategory"]] or settings_change[GS.other["kategory"]][i] == kategory[i]:
                    struc[i] = f"{i} :   <  {kategory[i]}  >"
                else:
                    struc[i] = f"{i} :   <  {settings_change[GS.other["kategory"]][i]}  >"

        cursor_pos = 0
        struc['Q'] = 'Exit'

        choice,cursor_pos = Graphic.select_menu_page(
            GS.other["kategory"] , struc, {"Q": "Q"}, "Changes get applyed the returning to previos page", cursor_pos=cursor_pos, take_lr=True
        )
        Graphic.update()
        if choice == "Q":
            change_setting(settings,settings_change)
            save_settings()
            GS.other["kategory"] = None
            return
        elif choice in kategory:
            if isinstance(kategory[choice],bool):
                if choice not in settings_change[GS.other["kategory"]]:
                    settings_change[GS.other["kategory"]][choice] = (not kategory[choice])
                else:
                    settings_change[GS.other["kategory"]][choice] = (not settings_change[GS.other["kategory"]][choice])
            else:
                pass


def change_setting(g_seting,g_seting_ch):
    global settings, settings_change
    for setting in g_seting_ch:
        if isinstance(g_seting_ch[setting],Dict):
            change_setting(g_seting[setting],g_seting_ch[setting])
        else:
            g_seting[setting] = g_seting_ch[setting]

def load_settings():
    global settings, settings_change
    change_setting(settings, settings_change)
        

def save_settings():
    change_setting(settings, settings_change)
    path = current_dir + "settings.json" 
    with open(path,"w") as f:
        json.dump(settings_change,f)




current_dir = os.path.dirname(os.path.abspath(__file__))
files_in_dir = os.listdir(current_dir)
if "settings.json" in files_in_dir:
    path = current_dir + "settings.json" 
    with open(path, "r") as f:
        settings_change = json.load(f)
        