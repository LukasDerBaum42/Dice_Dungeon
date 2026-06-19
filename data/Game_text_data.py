import json
import os
from pickle import GLOBAL
import time
from .GTD_default import (
    base_help_txt,
    base_UNIQUE_ITEMS,
    base_wappon_sub_typse,
    base_stat_value,
    base_elementare,
    base_fight_art,
    base_trap_art,
    base_player_cls,
    base_attacks,
    base_enemy_cls,
    base_bosses,
    base_traps,
    base_cheast,
    base_shops,
    base_layers,
    base_dungeons_preset,
) 



def update_ele_list():
    ele_list = []
    for i in elementare:
        ele_list.append(i)
    return ele_list

# loads mods

help_txt = base_help_txt.copy()
UNIQUE_ITEMS = base_UNIQUE_ITEMS.copy()
wappon_sub_typse = base_wappon_sub_typse.copy()
stat_value = base_stat_value.copy()
elementare = base_elementare.copy()
fight_art = base_fight_art.copy()
trap_art = base_trap_art.copy()
player_cls = base_player_cls.copy()
attacks = base_attacks.copy()
enemy_cls = base_enemy_cls.copy()
bosses = base_bosses.copy()
traps = base_traps.copy()
cheast = base_cheast.copy()
shops = base_shops.copy()
layers = base_layers.copy()
dungeons_preset = base_dungeons_preset.copy()

ele_list = update_ele_list()

def load_json_as_variable(path):
    name = os.path.splitext(os.path.basename(path))[0]

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Dict existiert schon → mergen
    if name in globals():
        if not isinstance(globals()[name], dict):
            raise TypeError(f"{name} exists but is not a dict")
        globals()[name].update(data)
    else:
        # Falls es doch noch nicht existiert
        globals()[name] = data


def load_mods():
    global ele_list, mod_loader_settings, help_txt,UNIQUE_ITEMS,wappon_sub_typse,stat_value,elementare,fight_art,trap_art,player_cls,attacks,enemy_cls,bosses,traps,cheast,shops,layers,dungeons_preset
    help_txt = base_help_txt.copy()
    UNIQUE_ITEMS = base_UNIQUE_ITEMS.copy()
    wappon_sub_typse = base_wappon_sub_typse.copy()
    stat_value = base_stat_value.copy()
    elementare = base_elementare.copy()
    fight_art = base_fight_art.copy()
    trap_art = base_trap_art.copy()
    player_cls = base_player_cls.copy()
    attacks = base_attacks.copy()
    enemy_cls = base_enemy_cls.copy()
    bosses = base_bosses.copy()
    traps = base_traps.copy()
    cheast = base_cheast.copy()
    shops = base_shops.copy()
    layers = base_layers.copy()
    dungeons_preset = base_dungeons_preset.copy()
    
    mods_to_load = []
    with open("mods/mod_loader_settings.json","r") as file:
        mod_loader_settings = json.load(file)
    for mod in mod_loader_settings:
        if mod_loader_settings[mod]:
            mods_to_load.append(mod)
    
    for mod in mods_to_load:
        files = os.listdir(f"mods/{mod}")
        mod_files = [f for f in files if f.lower().endswith((".json"))]
        for file in mod_files:
            try:
                load_json_as_variable(f"mods/{mod}/{file}")
            except:
                print("error while loading mod")
                time.sleep(1)
    ele_list = update_ele_list()
    
def save_mod_loader_settings():
    with open("mods/mod_loader_settings.json","w") as file:
        json.dump(mod_loader_settings,file)


mod_found = False
try:
#if False:
    mods = os.listdir("mods")
    mod_loader_settings = {}
    #print(mods)
    if "mod_loader_settings.json" in mods:
        velid_mods = [f for f in mods if f.lower().endswith(("_mod"))]
        with open("mods/mod_loader_settings.json","r") as file:
            mod_loader_settings = json.load(file)
            
        for mod in velid_mods:
            if mod not in mod_loader_settings:
                mod_loader_settings[mod] = False
        
        mods_to_del = []
        for dead_mod in mod_loader_settings: 
            if dead_mod not in velid_mods:
                mods_to_del.append(dead_mod)
        for del_mod in mods_to_del:
            del mod_loader_settings[del_mod]
        del mods_to_del
    else:
        velid_mods = [f for f in mods if f.lower().endswith(("_mod"))]
        for mod in velid_mods:
            mod_loader_settings[mod] = False
    
    print(mod_loader_settings)
    save_mod_loader_settings()
    mod_found = True
except:
    print("no mods found")
    mod_found = False
    #time.sleep(1)
if __name__ == '__main__':
    with open('temp.json','w') as file:
        json.dump(base_wappon_sub_typse,file)