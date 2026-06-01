import json
import os
from typing import Dict

from .default_settings import base_settings

settings = base_settings.copy()

settings_change = {}


def change_setting(g_seting,g_seting_ch):
    for setting in g_seting_ch:
        if g_seting_ch[setting].type == Dict:
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
        