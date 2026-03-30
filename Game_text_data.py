import json
import os
import time

help_txt = {
    "page 0": """ --- HOW TO PLAY ---
- You roll a dice to move across the dungeon.
- Use W/A/S/D to choose a path.
- Encounter enemies, treasure, and merchants.
- Advantage if you find them first.
- Survive and reach the final floor."""
}

UNIQUE_ITEMS = {
    "Excalibur": {
        "type": "sword",
        "stats": {
            "max_hp": 200,
            "max_mp": 100,
            "atk": 80,
            "sp_atk": 40,
            "def_": 30,
            "sp_def": 20,
            "crit_chance": 15,
            "crit_bonus": 5,
            "price": 500,
        },
        "flavor": "Forged by forgotten gods in the heart of a dying star, this blade hums with the wisdom of ages. Legends say it can cut through reality itself.",
    },
    "Pan of Doom": {
        "type": "pan",
        "stats": {
            "atk": 60,
            "sp_atk": 0,
            "def_": 10,
            "crit_chance": 90,
            "crit_bonus": 1000,
            "price": 500,
        },
        "flavor": "Every meal it touches becomes a weapon. Every sound, a war drum. They say the last person who doubted this pan now rules a kingdom of delicious despair.",
    },
    "Crown of the Machine": {
        "type": "helmet",
        "stats": {
            "max_mp": 150,
            "sp_atk": 60,
            "sp_def": 40,
            "crit_chance": 5,
            "crit_bonus": 30,
            "price": 500,
        },
        "flavor": "Cold metal whispers secrets of lost civilizations. Once worn by a mind that could outthink gods, now it seeks a new master to enlighten.",
    },
}

wappon_sub_typse = [
    "sword",
    "knife",
    "bow",
    "stafe",
    "spear",
    "pan",
    "gloves",
]

stat_value = {
    "max_hp": 0.4,
    "max_mp": 0.4,
    "atk": 1.5,
    "sp_atk": 1.5,
    "def": 1,
    "sp_def": 1,
    "crit_chance": 3,
    "crit_bonus": 0.5,
}


elementare = {
    "fire": {
        "atk": ["plant", "ice", "metal"],
        "def": ["wind", "plant"],
        "color": "#E25822",
    },
    "water": {"atk": ["fire", "stone"], "def": ["fire", "ice"], "color": "#1CA3EC"},
    "ice": {"atk": ["stone", "wind", "water"], "def": ["water"], "color": "#AEEBFF"},
    "plant": {
        "atk": ["water", "stone"],
        "def": ["water", "electric", "stone"],
        "color": "#3CB043",
    },
    "stone": {
        "atk": ["fire", "electric", "poison"],
        "def": ["poison", "fire", "wind"],
        "color": "#8B7D6B",
    },
    "poison": {
        "atk": ["plant", "light"],
        "def": ["plant", "light"],
        "color": "#7A1FA2",
    },
    "electric": {
        "atk": ["water", "wind", "metal"],
        "def": ["wind"],
        "color": "#FFD700",
    },
    "wind": {"atk": ["plant", "poison"], "def": ["plant"], "color": "#B0E0E6"},
    "light": {"atk": ["dark", "poison"], "def": ["dark"], "color": "#FFF4B1"},
    "dark": {"atk": ["light", "psychic"], "def": ["light"], "color": "#2B2B2B"},
    # --- extended stuff ---
    "metal": {"atk": ["ice", "plant"], "def": ["plant", "poison"], "color": "#9EA7AD"},
    "psychic": {"atk": ["dark", "poison"], "def": ["poison"], "color": "#FF4FD8"},
    "sound": {"atk": ["psychic", "wind"], "def": ["psychic"], "color": "#6F42C1"},
    "lava": {"atk": ["stone", "metal", "ice"], "def": ["fire"], "color": "#CF1020"},
    "steam": {"atk": ["ice", "plant"], "def": ["fire", "water"], "color": "#D6EAF8"},
}


def update_ele_list():
    ele_list = []
    for i in elementare:
        ele_list.append(i)
    return ele_list


ele_list = update_ele_list()

fight_art = {
    "player": ["  `o^     ", "^\\/0\\_+---", "  /O\\     ", " _| /_    ", ""],
    "Zomby": ["   @      ", "  ==|     ", "    |     ", "   / \\    ", ""],
    "Mimic": [
        "._____.__.",
        "| O O |\33[9m°°\33[0m|",
        "|\33[9m ^^^ \33[0m|  |",
        "|_____|__|",
        "",
    ],
    "Skelet": ["  _@@_    ", "  \\__/    ", "   ||     ", "  _||_    ", ""],
    "Goblin": ["   o      ", "  /0\\     ", "  / \\     ", " /   \\    ", ""],
    "Orc": ["  /@\\     ", " _|||_    ", "  | |     ", " /   \\    ", ""],
    "Dark Elf": ["   @      ", "  /|\\     ", "  \\|/     ", "  / \\     ", ""],
    "Giant Spider": ["  /@\\     ", " /@@@\\    ", "  / \\     ", " /   \\    ", ""],
    "Goblin King": ["  \\@/     ", " __|__    ", "  / \\     ", " /   \\    ", ""],
    "Orc Warlord": ["  \\@/     ", " _|||_    ", " / | \\    ", "/  |  \\   ", ""],
    "Lich King": ["  \\@/     ", "  /|\\     ", "  \\|/     ", "  / \\     ", ""],
    "Wraith": ["   @      ", "  / \\     ", "  \\ /     ", '   "      ', ""],
    "Minotaur": ["  \\@/     ", " _|||_    ", " / | \\    ", "/  \\  \\   ", ""],
    "Dragon": ["  \\@/     ", " /@@@\\    ", "<@@@@@>   ", "  / \\     ", ""],
}


trap_art = {
    "Hole": {
        "player": [4, 0],
        "art": [
            "",
            "",
            "",
            "",
            "",
            "_______         ________",
            "       |       |       ",
            "       |       |       ",
            "       |       |       ",
            "       |_^_^_^_|       ",
            "",
        ],
    },
    "Tripwire": {
        "player": [1, 0],
        "art": [
            "      <––––<",
            "   <––––<",
            "        <––––<",
            "",
            "|",
            "__________________________",
        ],
    },
    "Falling Piano": {
        "player": [8, 4],
        "art": [
            "     ___________  ",
            "    /__/|______/___",
            "   /___|_______|__/  ",
            "      /  |   |  \\  ",
            "",
            "",
            "",
            "",
            "",
            "",
        ],
    },
    "Mimic": {
        "player": [0, 0],
        "art": [
            "  ._____.__.",
            "  | O O |\33[9m°°\33[0m|",
            "  |\33[9m ^^^ \33[0m|  |",
            "  |_____|__|",
            "",
        ],
    },
}
"""
._____.__.
| O O |\33[9m°°\33[0m|
|\33[9m ^^^ \33[0m|  |
|_____|__|
"""


# print("\033[1;4mFett UND unterstrichen\033[0m")
# print("\033[1;34mFetter blauer Text\033[0m")
# print("\033[4;31;7mChaos-Modus\033[0m")
# print("\033[2mDas hier sollte dunkler wirken\033[0m")
# print("\033[38;2;255;100;0mOrange Text\033[0m")
# print("\033[48;2;20;20;20mDarker Background\033[0m")


# for r in range(8):
#     row = ''
#    for g in range(8):
#         for b in range(8):
#             row += f'\033[48;2;{32*r};{32*g};{32*b}m▄\033[0m'
#     print(row)
# for r in range(6):
#     for g in range(6):
#         for b in range(6):
#             row = ''
#             for r_2 in range(6):
#               for g_2 in range(6):
#                     for b_2 in range(6):
#                         row += f'\033[48;5;{16+36*r +6*g+b};38;5;{16+36*r_2+6*g_2+b_2}m▄\033[0m'
#             print(row)

player_cls = {
    "Adventurer": {
        "stats": {
            "max_move": 6,
            "min_move": 1,
            "max_hp": 150,
            "max_mp": 40,
            "atk": 12,
            "sp_atk": 12,
            "def_": 12,
            "sp_def": 12,
            "crit_chance": 2,
            "crit_bonus": 10,
        },
        "item": ("common", "sword", 1),
        "affiliations": {
                "elements": {"fire": 150, "wind": 90, "water": 90, "stone": 70},
                "wapons": {"sword": 120, "bow": 95, "stafe": 90}
            },
        # the item types are
        "attacks": ("Sword slash", "Sword thrust", "Flame sword", "Fireball"),
    },
    "Tester": {
        "stats": {
            "max_move": 30,
            "min_move": 15,
            "max_hp": 500,
            "max_mp": 400,
            "atk": 50,
            "sp_atk": 50,
            "def_": 50,
            "sp_def": 50,
            "crit_chance": 10,
            "crit_bonus": 10,
        },
        "item": ("common", "sword", 10),
        "affiliations": {"elements": {}, "wapons": {}},
        # the item types are
        "attacks": ("Sword slash", "Axe Swing", "Flame sword", "Fireball"),
    },
    "Warrior": {
        "stats": {
            "max_move": 5,
            "min_move": 1,
            "max_hp": 180,
            "max_mp": 20,
            "atk": 18,
            "sp_atk": 8,
            "def_": 16,
            "sp_def": 8,
            "crit_chance": 5,
            "crit_bonus": 15,
        },
        "item": ("uncommon", "sword", 2),
        "affiliations": {
                "elements": {"stone": 140, "metal": 130, "fire": 110, "sound": 105, "dark": 85, "ice": 85, "wind": 85},
                "wapons": {"sword": 140, "sheald": 120, "hammer": 110, "axe": 100, "bow": 80, "stafe": 70, "knife": 70}
            },
        "attacks": ("Sword slash", "Axe Swing", "War Cry", "Brutal Smash"),
    },
    "Mage": {
        "stats": {
            "max_move": 6,
            "min_move": 1,
            "max_hp": 100,
            "max_mp": 80,
            "atk": 8,
            "sp_atk": 18,
            "def_": 8,
            "sp_def": 16,
            "crit_chance": 8,
            "crit_bonus": 12,
        },
        "item": ("uncommon", "stafe", 2),
        "affiliations": {
                "elements": {"fire": 130, "dark": 130, "ice": 120, "elecric": 120, "psychic": 110, "water": 95, "wind": 95, "stone": 80, "plant": 80},
                "wapons": {"stafe": 150, "sword": 85, "bow": 85, "knife": 80, "sheald": 70, "hammer": 70}
            },
        "attacks": ("Fireball", "Dark Bolt", "Shadow Strike", "Death Coil"),
    },
    "Rogue": {
        "stats": {
            "max_move": 7,
            "min_move": 1,
            "max_hp": 120,
            "max_mp": 30,
            "atk": 16,
            "sp_atk": 10,
            "def_": 10,
            "sp_def": 10,
            "crit_chance": 12,
            "crit_bonus": 20,
        },
        "item": ("uncommon", "knife", 2),
        "affiliations": {
                "elements": {"dark": 140, "poison": 130, "wind": 110, "plant": 105, "fire": 90, "ice": 90, "sound": 90, "light": 75, "stone": 75},
                "wapons": {"knife": 150, "bow": 110, "sword": 95, "stafe": 80, "hammer": 75, "sheald": 70}
            },
        "attacks": ("Sword thrust", "Shadow Strike", "Web Shot", "Dark Bolt"),
    },
    "Ranger": {
        "stats": {
            "max_move": 6,
            "min_move": 1,
            "max_hp": 130,
            "max_mp": 40,
            "atk": 14,
            "sp_atk": 14,
            "def_": 12,
            "sp_def": 12,
            "crit_chance": 10,
            "crit_bonus": 15,
        },
        "item": ("uncommon", "bow", 2),
        "affiliations": {
                "elements": {"plant": 130, "wind": 125, "fire": 115, "dark": 110, "poison": 105, "water": 95, "ice": 95, "stone": 90, "light": 85, "metal": 80},
                "wapons": {"bow": 150, "knife": 110, "sword": 95, "stafe": 85, "hammer": 80, "sheald": 75}
            },
        "attacks": ("Shadow Strike", "Web Shot", "Dark Bolt", "Fireball"),
    },
    "Paladin": {
        "stats": {
            "max_move": 5,
            "min_move": 1,
            "max_hp": 170,
            "max_mp": 50,
            "atk": 16,
            "sp_atk": 14,
            "def_": 18,
            "sp_def": 14,
            "crit_chance": 4,
            "crit_bonus": 12,
        },
        "item": ("uncommon", "sheald", 2),
        "affiliations": {
                "elements": {"light": 150, "fire": 130, "sound": 120, "metal": 110, "stone": 105, "dark": 75, "poison": 75, "ice": 85, "wind": 85},
                "wapons": {"sheald": 140, "sword": 130, "hammer": 100, "bow": 85, "stafe": 80, "knife": 75}
            },
        "attacks": ("Sword slash", "War Cry", "Healing Light", "Fireball"),
    },
    "Necromancer": {
        "stats": {
            "max_move": 6,
            "min_move": 1,
            "max_hp": 90,
            "max_mp": 100,
            "atk": 6,
            "sp_atk": 20,
            "def_": 8,
            "sp_def": 18,
            "crit_chance": 10,
            "crit_bonus": 18,
        },
        "item": ("rare", "stafe", 3),
        "affiliations": {
                "elements": {"dark": 160, "poison": 145, "psychic": 120, "ice": 95, "fire": 80, "light": 60, "stone": 90, "wind": 85},
                "wapons": {"stafe": 150, "knife": 105, "sword": 85, "bow": 80, "hammer": 75, "sheald": 70}
            },
        "attacks": ("Dark Bolt", "Death Coil", "Shadow Strike", "Poison Dart"),
    },
}


attacks = {
    "Sword slash": {
        "stats": {
            "atk": 100,
            "sp_atk": 0,
            "mp": 0,
            "max_use": 20,
            "crit_chance": 0,
            "crit_bonus": 10,
            "adv": 0,
        },
        "wapon": ["sword"],
        "ele": None,
        "discription": "A slash with a sword",
    },
    "Sword thrust": {
        "stats": {
            "atk": 60,
            "sp_atk": 0,
            "mp": 0,
            "max_use": 20,
            "crit_chance": 10,
            "crit_bonus": 20,
            "adv": 1,
        },
        "wapon": ["sword"],
        "ele": None,
        "discription": "A thrust with a sword",
    },
    "Flame sword": {
        "stats": {
            "atk": 50,
            "sp_atk": 50,
            "mp": 5,
            "max_use": 10,
            "crit_chance": 5,
            "crit_bonus": 10,
            "adv": 0,
        },
        "wapon": ["sword"],
        "ele": "fire",
        "discription": "A slash with a flaming sword",
    },
    "Fireball": {
        "stats": {
            "atk": 0,
            "sp_atk": 100,
            "mp": 5,
            "max_use": 10,
            "crit_chance": 0,
            "crit_bonus": 10,
            "adv": 0,
        },
        "wapon": [],
        "ele": "fire",
        "discription": "You throw a ball of fire at your enemy",
    },
    "Axe Swing": {
        "stats": {
            "atk": 120,
            "sp_atk": 0,
            "mp": 0,
            "max_use": 15,
            "crit_chance": 5,
            "crit_bonus": 15,
            "adv": 0,
        },
        "wapon": [],
        "ele": None,
        "discription": "A powerful swing with a heavy axe",
    },
    "Dark Bolt": {
        "stats": {
            "atk": 0,
            "sp_atk": 90,
            "mp": 4,
            "max_use": 12,
            "crit_chance": 8,
            "crit_bonus": 12,
            "adv": 0,
        },
        "wapon": [],
        "ele": "dark",
        "discription": "A bolt of dark energy",
    },
    "Shadow Strike": {
        "stats": {
            "atk": 70,
            "sp_atk": 30,
            "mp": 3,
            "max_use": 15,
            "crit_chance": 12,
            "crit_bonus": 18,
            "adv": 1,
        },
        "wapon": [],
        "ele": "dark",
        "discription": "A strike from the shadows",
    },
    "Web Shot": {
        "stats": {
            "atk": 40,
            "sp_atk": 20,
            "mp": 2,
            "max_use": 18,
            "crit_chance": 0,
            "crit_bonus": 0,
            "adv": -2,
        },
        "wapon": [],
        "ele": "plant",
        "discription": "Shoots sticky webs to immobilize",
    },
    "War Cry": {
        "stats": {
            "atk": 80,
            "sp_atk": 0,
            "mp": 0,
            "max_use": 10,
            "crit_chance": 10,
            "crit_bonus": 20,
            "adv": 2,
        },
        "wapon": [],
        "ele": "sound",
        "discription": "A terrifying battle cry",
    },
    "Brutal Smash": {
        "stats": {
            "atk": 140,
            "sp_atk": 0,
            "mp": 0,
            "max_use": 8,
            "crit_chance": 15,
            "crit_bonus": 25,
            "adv": -1,
        },
        "wapon": [],
        "ele": None,
        "discription": "A devastating smash attack",
    },
    "Death Coil": {
        "stats": {
            "atk": 0,
            "sp_atk": 130,
            "mp": 8,
            "max_use": 6,
            "crit_chance": 10,
            "crit_bonus": 20,
            "adv": 0,
        },
        "wapon": [],
        "ele": "dark",
        "discription": "Unleashes a coil of death energy",
    },
    "Ice Shard": {
        "stats": {
            "atk": 0,
            "sp_atk": 85,
            "mp": 3,
            "max_use": 15,
            "crit_chance": 5,
            "crit_bonus": 10,
            "adv": -1,
        },
        "wapon": [],
        "ele": "ice",
        "discription": "Launches sharp shards of ice",
    },
    "Lightning Strike": {
        "stats": {
            "atk": 0,
            "sp_atk": 110,
            "mp": 6,
            "max_use": 8,
            "crit_chance": 15,
            "crit_bonus": 25,
            "adv": 0,
        },
        "wapon": [],
        "ele": "elecric",
        "discription": "Calls down a powerful lightning bolt",
    },
    "Poison Dart": {
        "stats": {
            "atk": 45,
            "sp_atk": 25,
            "mp": 2,
            "max_use": 20,
            "crit_chance": 8,
            "crit_bonus": 15,
            "adv": 0,
        },
        "wapon": [],
        "ele": "poison",
        "discription": "A poisoned dart that weakens enemies",
    },
    "Healing Light": {
        "stats": {
            "atk": 0,
            "sp_atk": -80,
            "mp": 6,
            "max_use": 5,
            "crit_chance": 0,
            "crit_bonus": 0,
            "adv": 0,
        },
        "wapon": [],
        "ele": "light",
        "discription": "Restores health to the caster",
    },
    "Bone Crush": {
        "stats": {
            "atk": 95,
            "sp_atk": 0,
            "mp": 0,
            "max_use": 12,
            "crit_chance": 8,
            "crit_bonus": 15,
            "adv": 0,
        },
        "wapon": [],
        "ele": "stone",
        "discription": "A crushing blow that breaks bones",
    },
    "Venom Bite": {
        "stats": {
            "atk": 55,
            "sp_atk": 35,
            "mp": 3,
            "max_use": 15,
            "crit_chance": 12,
            "crit_bonus": 18,
            "adv": -1,
        },
        "wapon": [],
        "ele": "poison",
        "discription": "A poisonous bite that drains strength",
    },
    "Soul Drain": {
        "stats": {
            "atk": 0,
            "sp_atk": 75,
            "mp": 4,
            "max_use": 10,
            "crit_chance": 10,
            "crit_bonus": 20,
            "adv": 1,
        },
        "wapon": [],
        "ele": "dark",
        "discription": "Drains the life force from enemies",
    },
    "Earthquake": {
        "stats": {
            "atk": 110,
            "sp_atk": 0,
            "mp": 0,
            "max_use": 8,
            "crit_chance": 5,
            "crit_bonus": 15,
            "adv": -2,
        },
        "wapon": [],
        "ele": "stone",
        "discription": "Shakes the ground beneath enemies",
    },
    "Wind Slash": {
        "stats": {
            "atk": 65,
            "sp_atk": 45,
            "mp": 4,
            "max_use": 12,
            "crit_chance": 15,
            "crit_bonus": 20,
            "adv": 2,
        },
        "wapon": [],
        "ele": "wind",
        "discription": "A swift slash empowered by wind",
    },
    # FIRE
    "Inferno Wave": {
        "stats": {
            "atk": 0,
            "sp_atk": 120,
            "mp": 7,
            "max_use": 6,
            "crit_chance": 5,
            "crit_bonus": 15,
            "adv": -1,
        },
        "wapon": [],
        "ele": "fire",
        "discription": "A wave of intense flames scorches everything ahead",
    },
    # WATER
    "Tidal Bash": {
        "stats": {
            "atk": 70,
            "sp_atk": 40,
            "mp": 4,
            "max_use": 12,
            "crit_chance": 8,
            "crit_bonus": 15,
            "adv": 0,
        },
        "wapon": [],
        "ele": "water",
        "discription": "A crushing surge of water slams into the enemy",
    },
    # ICE
    "Frozen Bind": {
        "stats": {
            "atk": 30,
            "sp_atk": 60,
            "mp": 4,
            "max_use": 10,
            "crit_chance": 0,
            "crit_bonus": 0,
            "adv": -2,
        },
        "wapon": [],
        "ele": "ice",
        "discription": "Freezes the enemy in place",
    },
    # PLANT
    "Thorn Whip": {
        "stats": {
            "atk": 75,
            "sp_atk": 25,
            "mp": 3,
            "max_use": 15,
            "crit_chance": 10,
            "crit_bonus": 15,
            "adv": 1,
        },
        "wapon": [],
        "ele": "plant",
        "discription": "Lashes the enemy with razor-sharp vines",
    },
    # STONE
    "Rock Spear": {
        "stats": {
            "atk": 90,
            "sp_atk": 0,
            "mp": 0,
            "max_use": 14,
            "crit_chance": 5,
            "crit_bonus": 10,
            "adv": 0,
        },
        "wapon": [],
        "ele": "stone",
        "discription": "Launches a hardened spear of stone",
    },
    # POISON
    "Toxic Cloud": {
        "stats": {
            "atk": 20,
            "sp_atk": 70,
            "mp": 5,
            "max_use": 8,
            "crit_chance": 0,
            "crit_bonus": 0,
            "adv": -1,
        },
        "wapon": [],
        "ele": "poison",
        "discription": "Envelops enemies in a poisonous fog",
    },
    # ELECTRIC
    "Volt Dash": {
        "stats": {
            "atk": 60,
            "sp_atk": 40,
            "mp": 3,
            "max_use": 14,
            "crit_chance": 15,
            "crit_bonus": 20,
            "adv": 2,
        },
        "wapon": [],
        "ele": "electric",
        "discription": "A lightning-fast electrified dash attack",
    },
    # WIND
    "Gale Burst": {
        "stats": {
            "atk": 0,
            "sp_atk": 95,
            "mp": 5,
            "max_use": 10,
            "crit_chance": 10,
            "crit_bonus": 15,
            "adv": 1,
        },
        "wapon": [],
        "ele": "wind",
        "discription": "A violent burst of compressed air",
    },
    # LIGHT
    "Radiant Spear": {
        "stats": {
            "atk": 40,
            "sp_atk": 80,
            "mp": 6,
            "max_use": 8,
            "crit_chance": 10,
            "crit_bonus": 20,
            "adv": 0,
        },
        "wapon": [],
        "ele": "light",
        "discription": "A spear of pure light pierces the enemy",
    },
    # DARK
    "Void Rend": {
        "stats": {
            "atk": 85,
            "sp_atk": 35,
            "mp": 4,
            "max_use": 10,
            "crit_chance": 12,
            "crit_bonus": 20,
            "adv": 1,
        },
        "wapon": [],
        "ele": "dark",
        "discription": "Tears into the enemy with void energy",
    },
    # METAL
    "Steel Breaker": {
        "stats": {
            "atk": 110,
            "sp_atk": 0,
            "mp": 0,
            "max_use": 10,
            "crit_chance": 8,
            "crit_bonus": 15,
            "adv": -1,
        },
        "wapon": ["hammer"],
        "ele": "metal",
        "discription": "A crushing metallic strike that dents armor",
    },
    # PSYCHIC
    "Mind Spike": {
        "stats": {
            "atk": 0,
            "sp_atk": 100,
            "mp": 5,
            "max_use": 10,
            "crit_chance": 10,
            "crit_bonus": 20,
            "adv": 0,
        },
        "wapon": [],
        "ele": "psychic",
        "discription": "A piercing attack directly on the mind",
    },
    # SOUND
    "Sonic Screech": {
        "stats": {
            "atk": 50,
            "sp_atk": 50,
            "mp": 4,
            "max_use": 12,
            "crit_chance": 5,
            "crit_bonus": 10,
            "adv": 1,
        },
        "wapon": [],
        "ele": "sound",
        "discription": "A deafening screech that rattles enemies",
    },
    # LAVA
    "Magma Crash": {
        "stats": {
            "atk": 100,
            "sp_atk": 30,
            "mp": 6,
            "max_use": 8,
            "crit_chance": 5,
            "crit_bonus": 15,
            "adv": -1,
        },
        "wapon": [],
        "ele": "lava",
        "discription": "Molten rock smashes into the enemy",
    },
    # STEAM
    "Scalding Mist": {
        "stats": {
            "atk": 20,
            "sp_atk": 80,
            "mp": 4,
            "max_use": 12,
            "crit_chance": 0,
            "crit_bonus": 0,
            "adv": -2,
        },
        "wapon": [],
        "ele": "steam",
        "discription": "A burning mist that scalds everything nearby",
    },
}

enemy_cls = {
    "Mimic": {
        "stats": {
            "min_move": 0,
            "max_move": 0,
            "max_hp": 160,
            "max_mp": 20,
            "atk": 20,
            "sp_atk": 6,
            "def_": 18,
            "sp_def": 18,
            "xp": 12,
            "gold": 10,
            "crit_chance": 8,
            "crit_bonus": 20,
        },
        "affiliations": {
            "fire": 80,
            "water": 120,
            "stone": 150,
            "metal": 130,
            "dark": 60,
            "light": 40,
        },
        "Attacks": {
            "Brutal Smash": 50,
            "Axe Swing": 30,
            "War Cry": 20,
            "Earthquake": 40,
            "Bone Crush": 60,
        },
        "Items": {
            "sword": {
                "chance": 5,
                "rarety": {
                    "common": 40,
                    "uncommon": 30,
                    "rare": 15,
                    "epic": 10,
                    "legendary": 5,
                },
                "level": [-1, 5],
            },
            "spear": {
                "chance": 5,
                "rarety": {
                    "common": 40,
                    "uncommon": 30,
                    "rare": 15,
                    "epic": 10,
                    "legendary": 5,
                },
                "level": [-1, 5],
            },
            "chestplate": {
                "chance": 5,
                "rarety": {
                    "common": 40,
                    "uncommon": 30,
                    "rare": 15,
                    "epic": 10,
                    "legendary": 5,
                },
                "level": [-1, 5],
            },
            "helmet": {
                "chance": 5,
                "rarety": {
                    "common": 40,
                    "uncommon": 30,
                    "rare": 15,
                    "epic": 10,
                    "legendary": 5,
                },
                "level": [-1, 5],
            },
            "pants": {
                "chance": 5,
                "rarety": {
                    "common": 40,
                    "uncommon": 30,
                    "rare": 15,
                    "epic": 10,
                    "legendary": 5,
                },
                "level": [-1, 5],
            },
            "boots": {
                "chance": 5,
                "rarety": {
                    "common": 40,
                    "uncommon": 30,
                    "rare": 15,
                    "epic": 10,
                    "legendary": 5,
                },
                "level": [-1, 5],
            },
            "pan": {
                "chance": 5,
                "rarety": {
                    "common": 40,
                    "uncommon": 30,
                    "rare": 15,
                    "epic": 10,
                    "legendary": 5,
                },
                "level": [-1, 5],
            },
            "stafe": {
                "chance": 5,
                "rarety": {
                    "common": 40,
                    "uncommon": 30,
                    "rare": 15,
                    "epic": 10,
                    "legendary": 5,
                },
                "level": [-1, 5],
            },
            "knife": {
                "chance": 5,
                "rarety": {
                    "common": 40,
                    "uncommon": 30,
                    "rare": 15,
                    "epic": 10,
                    "legendary": 5,
                },
                "level": [-1, 5],
            },
            "sheald": {
                "chance": 5,
                "rarety": {
                    "common": 40,
                    "uncommon": 30,
                    "rare": 15,
                    "epic": 10,
                    "legendary": 5,
                },
                "level": [-1, 5],
            },
            "bow": {
                "chance": 5,
                "rarety": {
                    "common": 40,
                    "uncommon": 30,
                    "rare": 15,
                    "epic": 10,
                    "legendary": 5,
                },
                "level": [-1, 5],
            },
            "gloves": {
                "chance": 5,
                "rarety": {
                    "common": 40,
                    "uncommon": 30,
                    "rare": 15,
                    "epic": 10,
                    "legendary": 5,
                },
                "level": [-1, 5],
            },
        },
    },
    "Zomby": {
        "stats": {
            "min_move": 1,
            "max_move": 6,
            "max_hp": 75,
            "max_mp": 20,
            "atk": 12,
            "sp_atk": 6,
            "def_": 12,
            "sp_def": 6,
            "xp": 3,
            "gold": 2,
            "crit_chance": 0,
            "crit_bonus": 0,
        },
        "affiliations": {
            "dark": 160,
            "poison": 140,
            "fire": 60,
            "light": 30,
            "plant": 70,
            "ice": 90,
        },
        "Attacks": {
            "Sword slash": 80,
            "Axe Swing": 20,
            "Bone Crush": 60,
            "Shadow Strike": 40,
        },
        "Items": {
            "sword": {
                "chance": 10,
                "rarety": {"common": 70, "uncommon": 25, "rare": 5},
                "level": [-3, 3],
            },
            "knife": {
                "chance": 10,
                "rarety": {"common": 70, "uncommon": 25, "rare": 5},
                "level": [-3, 3],
            },
            "sheald": {
                "chance": 10,
                "rarety": {"common": 70, "uncommon": 25, "rare": 5},
                "level": [-3, 3],
            },
            "chestplate": {
                "chance": 10,
                "rarety": {"common": 70, "uncommon": 25, "rare": 5},
                "level": [-3, 3],
            },
            "pants": {
                "chance": 10,
                "rarety": {"common": 70, "uncommon": 25, "rare": 5},
                "level": [-3, 3],
            },
        },
    },
    "Skelet": {
        "stats": {
            "min_move": 1,
            "max_move": 6,
            "max_hp": 75,
            "max_mp": 50,
            "atk": 6,
            "sp_atk": 12,
            "def_": 6,
            "sp_def": 12,
            "xp": 3,
            "gold": 2,
            "crit_chance": 0,
            "crit_bonus": 0,
        },
        "affiliations": {
            "dark": 150,
            "ice": 140,
            "stone": 120,
            "fire": 50,
            "light": 40,
            "wind": 90,
        },
        "Attacks": {
            "Dark Bolt": 70,
            "Ice Shard": 30,
            "Bone Crush": 50,
            "Soul Drain": 40,
        },
        "Items": {
            "stafe": {
                "chance": 10,
                "rarety": {"common": 70, "uncommon": 25, "rare": 5},
                "level": [-3, 3],
            },
            "sheald": {
                "chance": 10,
                "rarety": {"common": 70, "uncommon": 25, "rare": 5},
                "level": [-3, 3],
            },
            "chestplate": {
                "chance": 10,
                "rarety": {"common": 70, "uncommon": 25, "rare": 5},
                "level": [-3, 3],
            },
            "pants": {
                "chance": 10,
                "rarety": {"common": 70, "uncommon": 25, "rare": 5},
                "level": [-3, 3],
            },
        },
    },
    "Goblin": {
        "stats": {
            "min_move": 1,
            "max_move": 6,
            "max_hp": 75,
            "max_mp": 50,
            "atk": 12,
            "sp_atk": 12,
            "def_": 12,
            "sp_def": 12,
            "xp": 6,
            "gold": 4,
            "crit_chance": 5,
            "crit_bonus": 10,
        },
        "affiliations": {
            "poison": 130,
            "dark": 120,
            "plant": 110,
            "fire": 80,
            "light": 70,
            "electric": 90,
        },
        "Attacks": {
            "Sword slash": 40,
            "Poison Dart": 40,
            "Shadow Strike": 20,
            "Web Shot": 50,
            "Venom Bite": 30,
        },
        "Items": {
            "stafe": {
                "chance": 10,
                "rarety": {"common": 70, "uncommon": 25, "rare": 5},
                "level": [-3, 3],
            },
            "sword": {
                "chance": 10,
                "rarety": {"common": 70, "uncommon": 25, "rare": 5},
                "level": [-3, 3],
            },
            "knife": {
                "chance": 10,
                "rarety": {"common": 70, "uncommon": 25, "rare": 5},
                "level": [-3, 3],
            },
            "sheald": {
                "chance": 10,
                "rarety": {"common": 70, "uncommon": 25, "rare": 5},
                "level": [-3, 3],
            },
            "chestplate": {
                "chance": 10,
                "rarety": {"common": 70, "uncommon": 25, "rare": 5},
                "level": [-3, 3],
            },
            "pants": {
                "chance": 10,
                "rarety": {"common": 70, "uncommon": 25, "rare": 5},
                "level": [-3, 3],
            },
        },
    },
    "Orc": {
        "stats": {
            "min_move": 1,
            "max_move": 5,
            "max_hp": 120,
            "max_mp": 30,
            "atk": 18,
            "sp_atk": 8,
            "def_": 15,
            "sp_def": 8,
            "xp": 8,
            "gold": 6,
            "crit_chance": 3,
            "crit_bonus": 15,
        },
        "affiliations": {
            "stone": 150,
            "sound": 140,
            "metal": 130,
            "fire": 90,
            "ice": 70,
            "electric": 80,
        },
        "Attacks": {
            "Axe Swing": 50,
            "War Cry": 30,
            "Brutal Smash": 20,
            "Earthquake": 40,
            "Sword slash": 60,
        },
        "Items": {
            "sword": {
                "chance": 15,
                "rarety": {"common": 60, "uncommon": 30, "rare": 10},
                "level": [-2, 4],
            },
            "spear": {
                "chance": 15,
                "rarety": {"common": 60, "uncommon": 30, "rare": 10},
                "level": [-2, 4],
            },
            "chestplate": {
                "chance": 15,
                "rarety": {"common": 60, "uncommon": 30, "rare": 10},
                "level": [-2, 4],
            },
            "helmet": {
                "chance": 10,
                "rarety": {"common": 60, "uncommon": 30, "rare": 10},
                "level": [-2, 4],
            },
            "boots": {
                "chance": 10,
                "rarety": {"common": 60, "uncommon": 30, "rare": 10},
                "level": [-2, 4],
            },
        },
    },
    "Dark Elf": {
        "stats": {
            "min_move": 1,
            "max_move": 7,
            "max_hp": 65,
            "max_mp": 80,
            "atk": 10,
            "sp_atk": 16,
            "def_": 8,
            "sp_def": 14,
            "xp": 7,
            "gold": 5,
            "crit_chance": 8,
            "crit_bonus": 12,
        },
        "affiliations": {
            "dark": 160,
            "wind": 140,
            "ice": 130,
            "poison": 120,
            "light": 40,
            "fire": 70,
        },
        "Attacks": {
            "Dark Bolt": 40,
            "Shadow Strike": 30,
            "Ice Shard": 20,
            "Poison Dart": 10,
            "Soul Drain": 50,
            "Wind Slash": 40,
        },
        "Items": {
            "bow": {
                "chance": 15,
                "rarety": {"common": 60, "uncommon": 30, "rare": 10},
                "level": [-2, 4],
            },
            "knife": {
                "chance": 15,
                "rarety": {"common": 60, "uncommon": 30, "rare": 10},
                "level": [-2, 4],
            },
            "stafe": {
                "chance": 20,
                "rarety": {"common": 60, "uncommon": 30, "rare": 10},
                "level": [-2, 4],
            },
            "gloves": {
                "chance": 10,
                "rarety": {"common": 60, "uncommon": 30, "rare": 10},
                "level": [-2, 4],
            },
        },
    },
    "Giant Spider": {
        "stats": {
            "min_move": 1,
            "max_move": 8,
            "max_hp": 90,
            "max_mp": 40,
            "atk": 14,
            "sp_atk": 10,
            "def_": 10,
            "sp_def": 10,
            "xp": 5,
            "gold": 3,
            "crit_chance": 6,
            "crit_bonus": 8,
        },
        "affiliations": {
            "poison": 170,
            "plant": 150,
            "dark": 130,
            "fire": 50,
            "ice": 60,
            "sound": 70,
        },
        "Attacks": {
            "Web Shot": 60,
            "Poison Dart": 30,
            "Shadow Strike": 10,
            "Venom Bite": 70,
            "Dark Bolt": 20,
        },
        "Items": {
            "pants": {
                "chance": 10,
                "rarety": {"common": 70, "uncommon": 25, "rare": 5},
                "level": [-3, 3],
            },
            "boots": {
                "chance": 15,
                "rarety": {"common": 70, "uncommon": 25, "rare": 5},
                "level": [-3, 3],
            },
            "gloves": {
                "chance": 10,
                "rarety": {"common": 70, "uncommon": 25, "rare": 5},
                "level": [-3, 3],
            },
        },
    },
    "Wraith": {
        "stats": {
            "min_move": 1,
            "max_move": 7,
            "max_hp": 60,
            "max_mp": 100,
            "atk": 8,
            "sp_atk": 18,
            "def_": 6,
            "sp_def": 16,
            "xp": 10,
            "gold": 8,
            "crit_chance": 10,
            "crit_bonus": 15,
        },
        "affiliations": {
            "dark": 180,
            "ice": 140,
            "psychic": 130,
            "light": 20,
            "fire": 60,
            "stone": 80,
        },
        "Attacks": {
            "Death Coil": 40,
            "Dark Bolt": 30,
            "Shadow Strike": 20,
            "Ice Shard": 10,
            "Soul Drain": 50,
            "Poison Dart": 25,
        },
        "Items": {
            "stafe": {
                "chance": 20,
                "rarety": {"common": 50, "uncommon": 35, "rare": 15},
                "level": [-1, 5],
            },
            "gloves": {
                "chance": 15,
                "rarety": {"common": 50, "uncommon": 35, "rare": 15},
                "level": [-1, 5],
            },
            "helmet": {
                "chance": 10,
                "rarety": {"common": 50, "uncommon": 35, "rare": 15},
                "level": [-1, 5],
            },
        },
    },
    "Minotaur": {
        "stats": {
            "min_move": 1,
            "max_move": 4,
            "max_hp": 160,
            "max_mp": 20,
            "atk": 20,
            "sp_atk": 6,
            "def_": 18,
            "sp_def": 8,
            "xp": 12,
            "gold": 10,
            "crit_chance": 8,
            "crit_bonus": 20,
        },
        "affiliations": {
            "stone": 160,
            "metal": 150,
            "fire": 120,
            "water": 80,
            "ice": 70,
            "electric": 90,
        },
        "Attacks": {
            "Brutal Smash": 50,
            "Axe Swing": 30,
            "War Cry": 20,
            "Earthquake": 40,
            "Bone Crush": 60,
        },
        "Items": {
            "sword": {
                "chance": 20,
                "rarety": {"common": 50, "uncommon": 35, "rare": 15},
                "level": [-1, 5],
            },
            "spear": {
                "chance": 20,
                "rarety": {"common": 50, "uncommon": 35, "rare": 15},
                "level": [-1, 5],
            },
            "chestplate": {
                "chance": 20,
                "rarety": {"common": 50, "uncommon": 35, "rare": 15},
                "level": [-1, 5],
            },
            "helmet": {
                "chance": 15,
                "rarety": {"common": 50, "uncommon": 35, "rare": 15},
                "level": [-1, 5],
            },
        },
    },
    # NEW ENEMIES
    "Fire Elemental": {
        "stats": {
            "min_move": 1,
            "max_move": 5,
            "max_hp": 100,
            "max_mp": 80,
            "atk": 14,
            "sp_atk": 18,
            "def_": 10,
            "sp_def": 16,
            "xp": 9,
            "gold": 7,
            "crit_chance": 7,
            "crit_bonus": 15,
        },
        "affiliations": {
            "fire": 200,
            "lava": 180,
            "steam": 150,
            "water": 40,
            "ice": 30,
            "stone": 90,
        },
        "Attacks": {
            "Fireball": 60,
            "Inferno Wave": 40,
            "Magma Crash": 50,
            "Flame sword": 30,
            "Scalding Mist": 20,
        },
        "Items": {
            "stafe": {
                "chance": 15,
                "rarety": {"common": 60, "uncommon": 30, "rare": 10},
                "level": [-2, 4],
            },
            "gloves": {
                "chance": 10,
                "rarety": {"common": 70, "uncommon": 25, "rare": 5},
                "level": [-3, 3],
            },
        },
    },
    "Ice Golem": {
        "stats": {
            "min_move": 1,
            "max_move": 4,
            "max_hp": 140,
            "max_mp": 40,
            "atk": 16,
            "sp_atk": 14,
            "def_": 22,
            "sp_def": 18,
            "xp": 11,
            "gold": 9,
            "crit_chance": 5,
            "crit_bonus": 12,
        },
        "affiliations": {
            "ice": 180,
            "water": 150,
            "stone": 130,
            "fire": 50,
            "lava": 40,
            "metal": 110,
        },
        "Attacks": {
            "Ice Shard": 60,
            "Frozen Bind": 40,
            "Rock Spear": 50,
            "Bone Crush": 30,
            "Tidal Bash": 20,
        },
        "Items": {
            "chestplate": {
                "chance": 15,
                "rarety": {"common": 60, "uncommon": 30, "rare": 10},
                "level": [-2, 4],
            },
            "gloves": {
                "chance": 10,
                "rarety": {"common": 70, "uncommon": 25, "rare": 5},
                "level": [-3, 3],
            },
        },
    },
    "Forest Treant": {
        "stats": {
            "min_move": 1,
            "max_move": 3,
            "max_hp": 130,
            "max_mp": 70,
            "atk": 15,
            "sp_atk": 16,
            "def_": 20,
            "sp_def": 15,
            "xp": 10,
            "gold": 8,
            "crit_chance": 6,
            "crit_bonus": 10,
        },
        "affiliations": {
            "plant": 180,
            "water": 160,
            "earth": 140,
            "fire": 40,
            "ice": 70,
            "poison": 110,
        },
        "Attacks": {
            "Thorn Whip": 60,
            "Web Shot": 40,
            "Rock Spear": 30,
            "Earthquake": 50,
            "Toxic Cloud": 20,
        },
        "Items": {
            "stafe": {
                "chance": 15,
                "rarety": {"common": 60, "uncommon": 30, "rare": 10},
                "level": [-2, 4],
            },
        },
    },
    "Thunder Wolf": {
        "stats": {
            "min_move": 1,
            "max_move": 8,
            "max_hp": 85,
            "max_mp": 50,
            "atk": 16,
            "sp_atk": 14,
            "def_": 12,
            "sp_def": 10,
            "xp": 8,
            "gold": 6,
            "crit_chance": 12,
            "crit_bonus": 18,
        },
        "affiliations": {
            "electric": 180,
            "wind": 160,
            "metal": 140,
            "earth": 70,
            "water": 60,
            "stone": 80,
        },
        "Attacks": {
            "Lightning Strike": 60,
            "Volt Dash": 50,
            "Wind Slash": 40,
            "Gale Burst": 30,
            "Shadow Strike": 20,
        },
        "Items": {
            "gloves": {
                "chance": 15,
                "rarety": {"common": 60, "uncommon": 30, "rare": 10},
                "level": [-2, 4],
            },
            "boots": {
                "chance": 15,
                "rarety": {"common": 60, "uncommon": 30, "rare": 10},
                "level": [-2, 4],
            },
        },
    },
    "Water Nymph": {
        "stats": {
            "min_move": 1,
            "max_move": 7,
            "max_hp": 70,
            "max_mp": 90,
            "atk": 10,
            "sp_atk": 17,
            "def_": 9,
            "sp_def": 16,
            "xp": 9,
            "gold": 7,
            "crit_chance": 9,
            "crit_bonus": 14,
        },
        "affiliations": {
            "water": 180,
            "ice": 160,
            "plant": 140,
            "electric": 60,
            "fire": 70,
            "stone": 90,
        },
        "Attacks": {
            "Tidal Bash": 60,
            "Ice Shard": 40,
            "Scalding Mist": 30,
            "Healing Light": 20,
            "Thorn Whip": 25,
        },
        "Items": {
            "stafe": {
                "chance": 20,
                "rarety": {"common": 60, "uncommon": 30, "rare": 10},
                "level": [-2, 4],
            },
            "gloves": {
                "chance": 10,
                "rarety": {"common": 70, "uncommon": 25, "rare": 5},
                "level": [-3, 3],
            },
        },
    },
    "Earth Drake": {
        "stats": {
            "min_move": 1,
            "max_move": 6,
            "max_hp": 150,
            "max_mp": 50,
            "atk": 19,
            "sp_atk": 12,
            "def_": 24,
            "sp_def": 14,
            "xp": 15,
            "gold": 12,
            "crit_chance": 7,
            "crit_bonus": 16,
        },
        "affiliations": {
            "stone": 190,
            "metal": 170,
            "lava": 150,
            "water": 60,
            "plant": 80,
            "ice": 70,
        },
        "Attacks": {
            "Earthquake": 70,
            "Rock Spear": 60,
            "Magma Crash": 50,
            "Brutal Smash": 40,
            "Steel Breaker": 30,
        },
        "Items": {
            "chestplate": {
                "chance": 20,
                "rarety": {"common": 50, "uncommon": 35, "rare": 15},
                "level": [-1, 5],
            },
            "helmet": {
                "chance": 15,
                "rarety": {"common": 50, "uncommon": 35, "rare": 15},
                "level": [-1, 5],
            },
            "sheald": {
                "chance": 15,
                "rarety": {"common": 50, "uncommon": 35, "rare": 15},
                "level": [-1, 5],
            },
        },
    },
    "Psychic Specter": {
        "stats": {
            "min_move": 1,
            "max_move": 7,
            "max_hp": 65,
            "max_mp": 110,
            "atk": 8,
            "sp_atk": 20,
            "def_": 7,
            "sp_def": 18,
            "xp": 11,
            "gold": 9,
            "crit_chance": 11,
            "crit_bonus": 17,
        },
        "affiliations": {
            "psychic": 200,
            "dark": 160,
            "sound": 140,
            "metal": 70,
            "stone": 60,
            "fire": 80,
        },
        "Attacks": {
            "Mind Spike": 70,
            "Soul Drain": 50,
            "Sonic Screech": 40,
            "Death Coil": 30,
            "Shadow Strike": 20,
        },
        "Items": {
            "stafe": {
                "chance": 25,
                "rarety": {"common": 50, "uncommon": 35, "rare": 15},
                "level": [-1, 5],
            },
            "gloves": {
                "chance": 15,
                "rarety": {"common": 50, "uncommon": 35, "rare": 15},
                "level": [-1, 5],
            },
        },
    },
}

bosses = {
    "Goblin King": {
        "stats": {
            "min_move": 1,
            "max_move": 6,
            "max_hp": 150,
            "max_mp": 60,
            "atk": 18,
            "sp_atk": 14,
            "def_": 16,
            "sp_def": 14,
            "xp": 25,
            "gold": 20,
            "crit_chance": 8,
            "crit_bonus": 15,
        },
        "affiliations": {
            "poison": 180,
            "dark": 160,
            "stone": 140,
            "fire": 60,
            "light": 50,
            "ice": 70,
        },
        "Attacks": {
            "Axe Swing": 30,
            "War Cry": 25,
            "Brutal Smash": 20,
            "Poison Dart": 15,
            "Shadow Strike": 10,
            "Venom Bite": 40,
            "Earthquake": 35,
        },
        "Items": {
            "stafe": {
                "chance": 20,
                "rarety": {"common": 50, "uncommon": 35, "rare": 15},
                "level": [0, 6],
            },
            "sword": {
                "chance": 20,
                "rarety": {"common": 50, "uncommon": 35, "rare": 15},
                "level": [0, 6],
            },
            "knife": {
                "chance": 20,
                "rarety": {"common": 50, "uncommon": 35, "rare": 15},
                "level": [0, 6],
            },
            "sheald": {
                "chance": 20,
                "rarety": {"common": 50, "uncommon": 35, "rare": 15},
                "level": [0, 6],
            },
            "chestplate": {
                "chance": 20,
                "rarety": {"common": 50, "uncommon": 35, "rare": 15},
                "level": [0, 6],
            },
            "pants": {
                "chance": 20,
                "rarety": {"common": 50, "uncommon": 35, "rare": 15},
                "level": [0, 6],
            },
        },
    },
    "Orc Warlord": {
        "stats": {
            "min_move": 1,
            "max_move": 5,
            "max_hp": 200,
            "max_mp": 50,
            "atk": 22,
            "sp_atk": 12,
            "def_": 20,
            "sp_def": 12,
            "xp": 35,
            "gold": 30,
            "crit_chance": 10,
            "crit_bonus": 20,
        },
        "affiliations": {
            "stone": 190,
            "metal": 170,
            "sound": 160,
            "fire": 70,
            "ice": 60,
            "water": 80,
        },
        "Attacks": {
            "Brutal Smash": 40,
            "Axe Swing": 30,
            "War Cry": 20,
            "Shadow Strike": 10,
            "Earthquake": 50,
            "Bone Crush": 45,
            "Wind Slash": 35,
        },
        "Items": {
            "sword": {
                "chance": 25,
                "rarety": {"common": 40, "uncommon": 40, "rare": 20},
                "level": [1, 7],
            },
            "spear": {
                "chance": 25,
                "rarety": {"common": 40, "uncommon": 40, "rare": 20},
                "level": [1, 7],
            },
            "chestplate": {
                "chance": 25,
                "rarety": {"common": 40, "uncommon": 40, "rare": 20},
                "level": [1, 7],
            },
            "helmet": {
                "chance": 20,
                "rarety": {"common": 40, "uncommon": 40, "rare": 20},
                "level": [1, 7],
            },
            "sheald": {
                "chance": 20,
                "rarety": {"common": 40, "uncommon": 40, "rare": 20},
                "level": [1, 7],
            },
        },
    },
    "Lich King": {
        "stats": {
            "min_move": 1,
            "max_move": 6,
            "max_hp": 180,
            "max_mp": 120,
            "atk": 12,
            "sp_atk": 24,
            "def_": 14,
            "sp_def": 20,
            "xp": 40,
            "gold": 35,
            "crit_chance": 12,
            "crit_bonus": 18,
        },
        "affiliations": {
            "dark": 200,
            "ice": 180,
            "psychic": 170,
            "light": 30,
            "fire": 60,
            "plant": 80,
        },
        "Attacks": {
            "Death Coil": 30,
            "Dark Bolt": 25,
            "Ice Shard": 20,
            "Shadow Strike": 15,
            "Lightning Strike": 10,
            "Soul Drain": 40,
            "Poison Dart": 35,
        },
        "Items": {
            "stafe": {
                "chance": 30,
                "rarety": {"common": 30, "uncommon": 40, "rare": 30},
                "level": [2, 8],
            },
            "bow": {
                "chance": 20,
                "rarety": {"common": 30, "uncommon": 40, "rare": 30},
                "level": [2, 8],
            },
            "gloves": {
                "chance": 20,
                "rarety": {"common": 30, "uncommon": 40, "rare": 30},
                "level": [2, 8],
            },
            "helmet": {
                "chance": 20,
                "rarety": {"common": 30, "uncommon": 40, "rare": 30},
                "level": [2, 8],
            },
            "consumable": {
                "chance": 25,
                "rarety": {"common": 30, "uncommon": 40, "rare": 30},
                "level": [2, 8],
            },
        },
    },
    "Dragon": {
        "stats": {
            "min_move": 1,
            "max_move": 8,
            "max_hp": 300,
            "max_mp": 100,
            "atk": 25,
            "sp_atk": 28,
            "def_": 22,
            "sp_def": 18,
            "xp": 60,
            "gold": 50,
            "crit_chance": 15,
            "crit_bonus": 25,
        },
        "affiliations": {
            "fire": 200,
            "lava": 190,
            "electric": 180,
            "wind": 170,
            "ice": 60,
            "water": 70,
        },
        "Attacks": {
            "Fireball": 30,
            "Lightning Strike": 25,
            "Brutal Smash": 20,
            "War Cry": 15,
            "Death Coil": 10,
            "Earthquake": 40,
            "Wind Slash": 35,
            "Venom Bite": 30,
        },
        "Items": {
            "sword": {
                "chance": 30,
                "rarety": {"common": 20, "uncommon": 40, "rare": 40},
                "level": [3, 9],
            },
            "stafe": {
                "chance": 30,
                "rarety": {"common": 20, "uncommon": 40, "rare": 40},
                "level": [3, 9],
            },
            "chestplate": {
                "chance": 30,
                "rarety": {"common": 20, "uncommon": 40, "rare": 40},
                "level": [3, 9],
            },
            "helmet": {
                "chance": 25,
                "rarety": {"common": 20, "uncommon": 40, "rare": 40},
                "level": [3, 9],
            },
            "sheald": {
                "chance": 25,
                "rarety": {"common": 20, "uncommon": 40, "rare": 40},
                "level": [3, 9],
            },
        },
    },
    # NEW BOSSES
    "Elemental Archon": {
        "stats": {
            "min_move": 1,
            "max_move": 7,
            "max_hp": 250,
            "max_mp": 150,
            "atk": 20,
            "sp_atk": 28,
            "def_": 18,
            "sp_def": 22,
            "xp": 50,
            "gold": 45,
            "crit_chance": 12,
            "crit_bonus": 20,
        },
        "affiliations": {
            "fire": 180,
            "water": 180,
            "ice": 180,
            "electric": 180,
            "stone": 180,
            "wind": 180,
            "dark": 100,
            "light": 100,
        },
        "Attacks": {
            "Inferno Wave": 30,
            "Tidal Bash": 30,
            "Ice Shard": 25,
            "Lightning Strike": 25,
            "Earthquake": 30,
            "Wind Slash": 20,
            "Radiant Spear": 20,
            "Void Rend": 20,
        },
        "Items": {
            "stafe": {
                "chance": 30,
                "rarety": {"common": 20, "uncommon": 40, "rare": 40},
                "level": [3, 9],
            },
            "chestplate": {
                "chance": 30,
                "rarety": {"common": 20, "uncommon": 40, "rare": 40},
                "level": [3, 9],
            },
            "gloves": {
                "chance": 25,
                "rarety": {"common": 20, "uncommon": 40, "rare": 40},
                "level": [3, 9],
            },
        },
    },
    "Ancient Treant King": {
        "stats": {
            "min_move": 1,
            "max_move": 4,
            "max_hp": 320,
            "max_mp": 100,
            "atk": 22,
            "sp_atk": 20,
            "def_": 26,
            "sp_def": 22,
            "xp": 55,
            "gold": 48,
            "crit_chance": 10,
            "crit_bonus": 18,
        },
        "affiliations": {
            "plant": 200,
            "water": 190,
            "earth": 180,
            "poison": 170,
            "fire": 40,
            "ice": 80,
            "dark": 110,
        },
        "Attacks": {
            "Thorn Whip": 40,
            "Toxic Cloud": 35,
            "Earthquake": 45,
            "Rock Spear": 30,
            "Web Shot": 25,
            "Venom Bite": 30,
            "Healing Light": 20,
        },
        "Items": {
            "stafe": {
                "chance": 30,
                "rarety": {"common": 20, "uncommon": 40, "rare": 40},
                "level": [3, 9],
            },
            "chestplate": {
                "chance": 25,
                "rarety": {"common": 20, "uncommon": 40, "rare": 40},
                "level": [3, 9],
            },
            "helmet": {
                "chance": 20,
                "rarety": {"common": 20, "uncommon": 40, "rare": 40},
                "level": [3, 9],
            },
        },
    },
    "Storm Titan": {
        "stats": {
            "min_move": 1,
            "max_move": 6,
            "max_hp": 280,
            "max_mp": 120,
            "atk": 24,
            "sp_atk": 26,
            "def_": 20,
            "sp_def": 18,
            "xp": 52,
            "gold": 46,
            "crit_chance": 14,
            "crit_bonus": 22,
        },
        "affiliations": {
            "electric": 200,
            "wind": 190,
            "water": 180,
            "ice": 170,
            "earth": 70,
            "fire": 80,
            "metal": 140,
        },
        "Attacks": {
            "Lightning Strike": 40,
            "Gale Burst": 35,
            "Volt Dash": 30,
            "Tidal Bash": 30,
            "Ice Shard": 25,
            "Wind Slash": 30,
            "Sonic Screech": 20,
        },
        "Items": {
            "gloves": {
                "chance": 30,
                "rarety": {"common": 20, "uncommon": 40, "rare": 40},
                "level": [3, 9],
            },
            "boots": {
                "chance": 30,
                "rarety": {"common": 20, "uncommon": 40, "rare": 40},
                "level": [3, 9],
            },
            "chestplate": {
                "chance": 25,
                "rarety": {"common": 20, "uncommon": 40, "rare": 40},
                "level": [3, 9],
            },
        },
    },
}
# type 0 a set amount of instent damage that cant be avoided
# type 1 a set amount of damage that can be decreast be rolling
# type 2 a procentage amount of damage that can be reduced be rolling
traps = {
    "Mimic": {
        "text": "You found a chest but as you were about to open it, it turned out to just be a mimic... Oh fuck!!!"
    },
    "Hole": {
        "text": "As you walked a hole opened under you, in witch you’ve fallen",
        "damage_type": 2,
        "damage": 10,
    },
    "Tripwire": {
        "text": "You stubbed over a string and out of nowhere came a bunch of arrows fling your way",
        "damage_type": 1,
        "damage": 10,
    },
    "Falling Piano": {
        "text": "Out of literally nowhere came a piano, falling right on top of you?!!?!",
        "damage_type": 0,
        "damage": 30,
    },
}

cheast = {
    "normal": {
        "rarety": {"common": 50, "uncommon": 35, "rare": 15, "epic": 0, "legendary": 0},
        "level": [-3, 4],
        "item type": {
            "sword": 8,
            "stafe": 8,
            "sheald": 8,
            "knife": 8,
            "spear": 8,
            "helmet": 8,
            "pants": 8,
            "boots": 8,
            "bow": 8,
            "gloves": 8,
            "pan": 8,
            "Gold": 12,
        },
    }
}

shops = {
    "common": {
        "level": [-3, 3],
        "price": 0,
        "size": [6, 18],
        "rarety": {"common": 50, "uncommon": 35, "rare": 15, "epic": 0, "legendary": 0},
        "item type": {
            "sword": 10,
            "stafe": 9,
            "sheald": 9,
            "knife": 9,
            "spear": 9,
            "helmet": 9,
            "pants": 9,
            "boots": 9,
            "bow": 9,
            "gloves": 9,
            "pan": 9,
        },
    },
    "uncommon": {
        "level": [-3, 3],
        "price": 0,
        "size": [6, 18],
        "rarety": {
            "common": 25,
            "uncommon": 50,
            "rare": 15,
            "epic": 10,
            "legendary": 0,
        },
        "item type": {
            "sword": 10,
            "stafe": 9,
            "sheald": 9,
            "knife": 9,
            "spear": 9,
            "helmet": 9,
            "pants": 9,
            "boots": 9,
            "bow": 9,
            "gloves": 9,
            "pan": 9,
        },
    },
    "rare": {
        "level": [-3, 3],
        "price": 0,
        "size": [6, 18],
        "rarety": {
            "common": 20,
            "uncommon": 25,
            "rare": 35,
            "epic": 15,
            "legendary": 5,
        },
        "item type": {
            "sword": 10,
            "stafe": 9,
            "sheald": 9,
            "knife": 9,
            "spear": 9,
            "helmet": 9,
            "pants": 9,
            "boots": 9,
            "bow": 9,
            "gloves": 9,
            "pan": 9,
        },
    },
}


layers: dict[
    str, dict[str, int | dict[str, int] | dict[str, float] | str | list[int]]
] = {
    "layer 1": {
        "level": 5,
        "min_level" : 1,
        "max_level":10,
        "mob": {"Zomby": 40, "Skelet": 40, "Goblin": 20},
        "boss": "Goblin King",
        "size": [1, 1],
        "traps": {"Hole": 25, "Tripwire": 25, "Falling Piano": 25, "Mimic": 25},
        "cheasts": {"normal": 100},
        "shops": {"common": 60, "uncommon": 30, "rare": 10},
        "rooms": {"merchant": 0.05},
    },
    "layer 2": {
        "level": 10,
        "min_level" : 6,
        "max_level":15,
        "mob": {"Orc": 35, "Dark Elf": 35, "Giant Spider": 30},
        "boss": "Orc Warlord",
        "size": [1, 1],
        "traps": {"Hole": 25, "Tripwire": 25, "Falling Piano": 25, "Mimic": 25},
        "cheasts": {"normal": 100},
        "shops": {"common": 60, "uncommon": 30, "rare": 10},
        "rooms": {"merchant": 0.05},
    },
    "layer 3": {
        "level": 15,
        "min_level" : 10,
        "max_level":20,
        "mob": {"Dark Elf": 40, "Orc": 30, "Goblin": 20, "Giant Spider": 10},
        "boss": "Lich King",
        "size": [1, 1],
        "traps": {"Hole": 25, "Tripwire": 25, "Falling Piano": 25, "Mimic": 25},
        "cheasts": {"normal": 100},
        "shops": {"common": 60, "uncommon": 30, "rare": 10},
        "rooms": {"merchant": 0.05},
    },
    "layer 4": {
        "level": 25,
        "min_level" : 18,
        "max_level":30,
        "mob": {"Wraith": 35, "Minotaur": 35, "Dark Elf": 20, "Orc": 10},
        "boss": "Lich King",
        "size": [1, 1],
        "traps": {"Hole": 25, "Tripwire": 25, "Falling Piano": 25, "Mimic": 25},
        "cheasts": {"normal": 100},
        "shops": {"common": 60, "uncommon": 30, "rare": 10},
        "rooms": {"merchant": 0.05},
    },
    "layer 5": {
        "level": 30,
        "min_level" : 25,
        "max_level":35,
        "mob": {"Wraith": 40, "Minotaur": 30, "Dark Elf": 20, "Giant Spider": 10},
        "boss": "Dragon",
        "size": [1, 1],
        "traps": {"Hole": 25, "Tripwire": 25, "Falling Piano": 25, "Mimic": 25},
        "cheasts": {"normal": 100},
        "shops": {"common": 60, "uncommon": 30, "rare": 10},
        "rooms": {"merchant": 0.05},
    },
    "layer 6": {
        "level": 40,
        "min_level" : 35,
        "max_level":50,
        "mob": {"Wraith": 50, "Minotaur": 30, "Dark Elf": 20},
        "boss": "Dragon",
        "size": [1, 1],
        "traps": {"Hole": 25, "Tripwire": 25, "Falling Piano": 25, "Mimic": 25},
        "cheasts": {"normal": 100},
        "shops": {"common": 60, "uncommon": 30, "rare": 10},
        "rooms": {"merchant": 0.05},
    },
    "layer 7": {
        "level": 50,
        "min_level" : 40,
        "max_level":60,
        "mob": {"Wraith": 40, "Minotaur": 40, "Dark Elf": 20},
        "boss": "Dragon",
        "size": [1, 1],
        "traps": {"Hole": 25, "Tripwire": 25, "Falling Piano": 25, "Mimic": 25},
        "cheasts": {"normal": 100},
        "shops": {"common": 60, "uncommon": 30, "rare": 10},
        "rooms": {"merchant": 0.05},
    },
    "layer 8": {
        "level": 60,
        "min_level" : 55,
        "max_level":70,
        "mob": {"Wraith": 50, "Minotaur": 50},
        "boss": "Lich King",
        "size": [1, 1],
        "traps": {"Hole": 25, "Tripwire": 25, "Falling Piano": 25, "Mimic": 25},
        "cheasts": {"normal": 100},
        "shops": {"common": 60, "uncommon": 30, "rare": 10},
        "rooms": {"merchant": 0.05},
    },
    "layer 9": {
        "level": 75,
        "min_level" : 60,
        "max_level":85,
        "mob": {"Wraith": 60, "Minotaur": 40},
        "boss": "Dragon",
        "size": [1, 1],
        "traps": {"Hole": 25, "Tripwire": 25, "Falling Piano": 25, "Mimic": 25},
        "cheasts": {"normal": 100},
        "shops": {"common": 60, "uncommon": 30, "rare": 10},
        "rooms": {"merchant": 0.05},
    },
    "layer 10": {
        "level": 90,
        "min_level" : 80,
        "max_level":100,
        "mob": {"Wraith": 70, "Minotaur": 30},
        "boss": "Dragon",
        "size": [1, 1],
        "traps": {"Hole": 25, "Tripwire": 25, "Falling Piano": 25, "Mimic": 25},
        "cheasts": {"normal": 100},
        "shops": {"common": 60, "uncommon": 30, "rare": 10},
        "rooms": {"merchant": 0.05},
    },
}


dungeons_preset = {
    "Standerd": {
        "L_size": 10,
        "liniar": {
            "layers": [
                {"layer": "layer 1", "level": 5, "Size": [10, 20]},
                {"layer": "layer 2", "level": 10, "Size": [10, 20]},
                {"layer": "layer 3", "level": 15, "Size": [10, 20]},
                {"layer": "layer 4", "level": 25, "Size": [10, 20]},
                {"layer": "layer 5", "level": 30, "Size": [10, 20]},
                {"layer": "layer 6", "level": 40, "Size": [10, 20]},
                {"layer": "layer 7", "level": 50, "Size": [10, 20]},
                {"layer": "layer 8", "level": 60, "Size": [10, 20]},
                {"layer": "layer 9", "level": 75, "Size": [10, 20]},
                {"layer": "layer 10", "level": 90, "Size": [10, 20]},
            ]
        },
        "endless": {
            "layers": [
                "layer 8",
                "layer 9",
                "layer 10",
            ],
            "start_level": 100,
            "Size": [10, 20],
            "Skale": 1.1,
        },
    },
    "Large": {
        "L_size": 10,
        "liniar": {
            "layers": [
                {"layer": "layer 1", "level": 5, "Size": [30, 40]},
                {"layer": "layer 2", "level": 10, "Size": [30, 40]},
                {"layer": "layer 3", "level": 15, "Size": [30, 40]},
                {"layer": "layer 4", "level": 25, "Size": [30, 40]},
                {"layer": "layer 5", "level": 30, "Size": [30, 40]},
                {"layer": "layer 6", "level": 40, "Size": [30, 40]},
                {"layer": "layer 7", "level": 50, "Size": [30, 40]},
                {"layer": "layer 8", "level": 60, "Size": [30, 40]},
                {"layer": "layer 9", "level": 75, "Size": [30, 40]},
                {"layer": "layer 10", "level": 90, "Size": [30, 40]},
            ]
        },
        "endless": {
            "layers": [
                "layer 8",
                "layer 9",
                "layer 10",
            ],
            "start_level": 100,
            "Size": [10, 20],
            "Skale": 1.1,
        },
    },
    "Very Large": {
        "liniar": {
            "layers": [
                {"layer": "layer 1", "level": 5, "Size": [50, 60]},
                {"layer": "layer 2", "level": 10, "Size": [50, 60]},
                {"layer": "layer 3", "level": 15, "Size": [50, 60]},
                {"layer": "layer 4", "level": 25, "Size": [50, 60]},
                {"layer": "layer 5", "level": 30, "Size": [50, 60]},
                {"layer": "layer 6", "level": 40, "Size": [50, 60]},
                {"layer": "layer 7", "level": 50, "Size": [50, 60]},
                {"layer": "layer 8", "level": 60, "Size": [50, 60]},
                {"layer": "layer 9", "level": 75, "Size": [50, 60]},
                {"layer": "layer 10", "level": 90, "Size": [50, 60]},
            ]
        },
        "endless": {
            "layers": [
                "layer 8",
                "layer 9",
                "layer 10",
            ],
            "start_level": 100,
            "Size": [10, 20],
            "Skale": 1.1,
        },
    },
}


# loads mods


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


test_for_mods = False
try:
    mods = os.listdir("mods")
    print(mods)
    velid_mods = [f for f in mods if f.lower().endswith(("_mod"))]
    test_for_mods = True
except:
    print("no mods found")
if test_for_mods:
    for mod in mods:
        files = os.listdir(f"mods/{mod}")
        mod_files = [f for f in files if f.lower().endswith((".json"))]
        for file in mod_files:
            try:
                load_json_as_variable(f"mods/{mod}/{file}")
            except:
                print("error while loading mod")
                time.sleep(1)
ele_list = update_ele_list()
