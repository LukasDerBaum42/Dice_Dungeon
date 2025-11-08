help_txt = {
    "page 0":''' --- HOW TO PLAY ---
- You roll a dice to move across the dungeon.
- Use W/A/S/D to choose a path.
- Encounter enemies, treasure, and merchants.
- Advantage if you find them first.
- Survive and reach the final floor.'''}



fight_art = {
    'player':[
        '  `o^     ',
        '^\/0\_+---',
        '  /O\     ',
        ' _| /_    ',
        ''],
    'zomby': [
        '   @      ',
        '  ==|     ',
        '    |     ',
        '   / \    ',
        ''],
}





UNIQUE_ITEMS = {
        "Excalibur": {
            "type": "sword",
            "stats": {"max_hp": 200, "max_mp": 100, "atk": 80, "sp_atk": 40, "def_": 30, "sp_def": 20, "crit_chance": 15, "crit_bonus": 5},
            "flavor": "Forged by forgotten gods in the heart of a dying star, this blade hums with the wisdom of ages. Legends say it can cut through reality itself."
        },
        "Pan of Doom": {
            "type": "pans",
            "stats": {"atk": 60, "sp_atk": 0, "def_": 10, "crit_chance": 90, "crit_bonus": 1000},
            "flavor": "Every meal it touches becomes a weapon. Every sound, a war drum. They say the last person who doubted this pan now rules a kingdom of delicious despair."
        },
        "Crown of the Machine": {
            "type": "helmet",
            "stats": {"max_mp": 150, "sp_atk": 60, "sp_def": 40, "crit_chance": 5, "crit_bonus": 30},
            "flavor": "Cold metal whispers secrets of lost civilizations. Once worn by a mind that could outthink gods, now it seeks a new master to enlighten."
        }
    }

player_cls = {
    'Adventurer':{
        'stats': {'max_move': 6, 'min_move': 1, 'max_hp': 20, 'max_mp': 20, 'atk': 6, 'sp_atk': 6, 'def_': 6, 'sp_def': 6, 'crit_chance': 2, 'crit_bonus': 10},
        'item': ('common','sword',1),
        'attacks': ('Sword slash','Sword thrust','Flame sword','Fireball')
    }

}


attacks = {
    'Sword slash': {
        'stats': {'atk': 100, 'sp_atk': 0, 'mp': 0, 'max_use': 20,'crit_chance': 0,'crit_bonus': 10, 'adv': 0},
        'discription': 'A slash with a sword'
        },
    'Sword thrust': {
        'stats': {'atk': 60, 'sp_atk': 0, 'mp': 0, 'max_use': 20,'crit_chance': 10,'crit_bonus': 20, 'adv': 1},
        'discription': 'A thrust with a sword'
        },
    'Flame sword': {
        'stats': {'atk': 50, 'sp_atk': 50, 'mp': 5, 'max_use': 10,'crit_chance': 5,'crit_bonus': 10, 'adv': 0},
        'discription': 'A slash with a blaming sword'
        },
    'Fireball': {
        'stats': {'atk': 0, 'sp_atk': 100, 'mp': 5, 'max_use': 10,'crit_chance': 0,'crit_bonus': 10, 'adv': 0},
        'discription': 'You through a ball of fire a your enemy'
        },
    'atk 1': {
        'stats': {'atk': 50, 'sp_atk': 0, 'mp': 0, 'max_use': 20,'crit_chance': 0,'crit_bonus': 0, 'adv': 0},
        'discription': 'attack'
        },
    'atk 2': {
        'stats': {'atk': 100, 'sp_atk': 0, 'mp': 0, 'max_use': 10,'crit_chance': 0,'crit_bonus': 0, 'adv': 0},
        'discription': 'attack'
        },
    'atk 3': {
        'stats': {'atk': 40, 'sp_atk': 0, 'mp': 0, 'max_use': 20,'crit_chance': 0,'crit_bonus': 0, 'adv': 1},
        'discription': 'attack'
        },
    'atk 4': {
        'stats': {'atk': 110, 'sp_atk': 0, 'mp': 0, 'max_use': 5,'crit_chance': 0,'crit_bonus': 0, 'adv': -1},
        'discription': 'attack'
        },
    'sp atk 1': {
        'stats': {'atk': 0, 'sp_atk': 50, 'mp': 1, 'max_use': 20,'crit_chance': 0,'crit_bonus': 0, 'adv': 0},
        'discription': 'special attack'
        },
    'sp atk 2': {
        'stats': {'atk': 0, 'sp_atk': 100, 'mp': 2, 'max_use': 10,'crit_chance': 0,'crit_bonus': 0, 'adv': 0},
        'discription': 'special attack'
        },
    'sp atk 3': {
        'stats': {'atk': 0, 'sp_atk': 40, 'mp': 1, 'max_use': 20,'crit_chance': 0,'crit_bonus': 0, 'adv': 1},
        'discription': 'special attack'
        },
    'sp atk 4': {
        'stats': {'atk': 0, 'sp_atk': 110, 'mp': 2, 'max_use': 5,'crit_chance': 0,'crit_bonus': 0, 'adv': -1},
        'discription': 'special attack'
        }

    }

enemy_cls = {
    'zomby':{
        'stats': {'min_move': 1, 'max_move': 6, 'max_hp': 10, 'max_mp': 10, 'atk': 6, 'sp_atk': 6, 'def_': 6, 'sp_def':6, 'xp': 3, 'gold': 2, 'crit_chance': 0, 'crit_bonus': 0},
        'Attacks': {'atk 1':100, 'atk 2':100, 'atk 3':100, 'atk 4':100},
        'Items': {
            'sword':{'chance':10, 'rarety': {'common':70, 'uncommon':25,'rare':5}, 'level':[-3,3]},
            'knife':{'chance':10, 'rarety': {'common':70, 'uncommon':25,'rare':5}, 'level':[-3,3]},
            'sheald':{'chance':10, 'rarety': {'common':70, 'uncommon':25,'rare':5}, 'level':[-3,3]},
            'chestplate':{'chance':10, 'rarety': {'common':70, 'uncommon':25,'rare':5}, 'level':[-3,3]},
            'pants':{'chance':10, 'rarety': {'common':70, 'uncommon':25,'rare':5}, 'level':[-3,3]}
            }
        }
    }
