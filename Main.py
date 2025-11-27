import os , time, random, math
from random import choice

import Game_text_data as GTD
from Items import GameItem
#from collections import deque

OPPOSITE = {"top": "bottom", "bottom": "top", "left": "right", "right": "left"}
SIDES = ["top", "bottom", "left", "right"]

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def wrap_text(text, width=72):
    words = text.split()
    lines = []
    current_line = " "

    for word in words:
        if len(current_line) + len(word) + 1 > width:
            lines.append(current_line.rstrip())
            current_line = word + " "
        else:
            current_line += word + " "
    lines.append(current_line.rstrip())
    return "\n ".join(lines)



class Player:
    def __init__(self,cls):
        self.cls = cls

        stats = GTD.player_cls[cls]['stats']
        self.moves = -2
        self.x = 2
        self.y = 2
        self.last_pos = [self.x,self.y]
        self.level = 1
        self.xp = 0
        self.max_xp = self.next_level_xp(self.level)
        self.gold = 10
        self.inventory = []
        self.equiped_items = []
        self.favorit = []
        self.equipt_slots = {'wappon': [False,None], 'helmet': [False,None], 'chestplate': [False,None], 'pants': [False,None], 'boots': [False,None], 'sheald': [False,None]}
        self.max_move = stats['max_move']
        self.min_move = stats['min_move']
        self.max_hp = stats['max_hp']
        self.max_mp = stats['max_mp']
        self.atk = stats['atk']
        self.sp_atk = stats['sp_atk']
        self.def_ = stats['def_']
        self.sp_def = stats['sp_def']
        self.crit_chance = stats['crit_chance']
        self.crit_bonus = stats['crit_bonus']
        self.add_to_inv(GameItem(*GTD.player_cls[cls]['item']))
        self.attacks = []
        self.attacks_used = {}
        for i in GTD.player_cls[cls]['attacks']:
            self.attacks.append(GTD.attacks[i])
            self.attacks_used[i] = 0
            
        self.hp = self.max_hp
        self.mp = self.max_mp
        self.item_stats_add()

    def next_level_xp(self,level):
        return (math.floor((((math.log(level ** 2,10)) ** 2) + 1) * 5)) * 3

    def roll_for_move(self):
        roll = roll_dice(self.min_move,self.max_move)
        self.moves = roll
        return roll

    def add_to_inv(self,item):
        self.inventory.append(item)

    def equip_item(self,item):
        if item.item_type in self.equipt_slots:
            slot = item.item_type
        elif item.item_type == 'consumable':
            slot = item.item_type
        else:
            slot = 'wappon'
        if item in self.equiped_items:
            self.equiped_items.remove(item)
            item.is_equiped = False
            self.equipt_slots[slot][0] = False
            self.equipt_slots[slot][1] = None
        else:
            if self.equipt_slots[slot][0]:
                print(f'You have laredy a {slot} equipped')
                choice = input('Do you want to swape? [y/n]>')
                if choice == 'y':
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



    def show_inventory(self):
        is_item_selected = False
        page = 0
        is_fav = False
        is_equ = False
        item_fillter = self.inventory
        selected_item = None
        selected_num = None
        while True:
            max_page = int((len(item_fillter) - 1) // (4 if is_item_selected else 6))
            item_render = []
            clear()
            for i in range(6 if is_item_selected == False else 4):
                i += page * (6 if is_item_selected == False else 4)
                try:
                    item = item_fillter[i]
                    item_render_temp = [f'{item.grade} {item.item_type} (Lvl {item.level})',f'{item.name} {'*' if item.is_equiped else ''}']
                    for j in range(len(item_render_temp)):
                        while len(item_render_temp [j]) < 34:
                            item_render_temp [j] += ' '
                        if len(item_render_temp[j]) > 34:
                            if item.is_equiped:
                                item_render_temp[j] = item_render_temp[j][:32] + ' *'
                            else:
                                item_render_temp[j] = item_render_temp[j][:34]
                    item_render.append(item_render_temp)
                except:
                    item_render.append(['                                  ','                                  '])

            titel = f'Invetory Page {page} / {max_page}'
            while len(titel) < 76:
                titel = ' ' + titel + ' '
            print(f'''==============================================================================
 {titel}
 Q = Close Invetory | N = Next Page | P = Privios Page  | H = Help
 E = Equip/Unequip    | F = add/remove Favorit| SF = show Favorits
 PAGE to go to a page | Number to select Item | SE = show Equipped
==============================================================================''')

            if is_item_selected:
                titel = f'Level {selected_item.level}/{selected_item.max_level} {selected_item.grade} {selected_item.item_type}: {selected_item.name} {'*' if selected_item.is_equiped else ''}'
                while len(titel) < 76:
                    titel = ' ' + titel + ' '
                stats = selected_item.get_stats()
                HP = f'HP {stats['max hp']}'
                while len(HP) < 16:
                    HP += ' '
                MP = f'MP {stats['max mp']}'
                while len(MP) < 16:
                    MP += ' '
                atk = f'ATK {stats['atk']}'
                while len(atk) < 16:
                    atk += ' '
                sp_atk = f'SP ATK {stats['sp atk']}'
                while len(sp_atk) < 16:
                    sp_atk += ' '
                def_ = f'DEF {stats['def']}'
                while len(def_) < 16:
                    def_ += ' '
                sp_def = f'SP DEF {stats['sp def']}'
                while len(sp_def) < 16:
                    sp_def += ' '
                crit_chance = f'Crit Chance {stats['crit chance']}'
                while len(crit_chance) < 16:
                    crit_chance += ' '
                crit_bounus = f'Crit Bonus  {stats['crit bonus']}'
                while len(crit_bounus) < 16:
                    crit_bounus += ' '
                flavor_text = wrap_text(selected_item.flavor,75)

                print(f''' {titel}
 {HP} {atk} {sp_atk} {crit_chance}
 {MP} {def_} {sp_def} {crit_bounus}
                              Flavor text
{flavor_text}
==============================================================================''')



            for i in range(len(item_render) // 2):
                num_1 = f'[{i*2+page * (6 if is_item_selected == False else 4)}]'
                num_2 = f'[{i*2+1+page * (6 if is_item_selected == False else 4)}]'
                while len(num_1) < 6:
                    num_1 = num_1 + ' '
                while len(num_2) < 6:
                    num_2 = num_2 + ' '
                print(f''' ––––––––––––––––––––––––––––––––––––    ––––––––––––––––––––––––––––––––––––
| {num_1}                             |  | {num_2}                             |
| {item_render[i*2][0]} |  | {item_render[i*2+1][0]} |
| {item_render[i*2][1]} |  | {item_render[i*2+1][1]} |
 ––––––––––––––––––––––––––––––––––––    –––––––––––––––––––––––––––––––––––– ''')
            choice = input("> ").upper().strip()
            if choice == 'Q': break
            elif choice == 'N':
                page += 1 if page < max_page else 0
            elif choice == 'P':
                page -= 1 if page > 0 else 0
            elif choice == 'E':
                if is_item_selected:
                    self.equip_item(selected_item)
                else:
                    print('No item select')
                    time.sleep(1)
            elif choice == 'SE':
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
            elif choice == 'F':
                if is_item_selected:
                    if selected_item in self.favorit:
                        self.favorit.remove(selected_item)
                    else:
                        self.favorit.append(selected_item)
            elif choice == 'SF':
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
            elif choice == 'PAGE':
                choice = input("Selacte page > ").upper().strip()
                try:
                    if int(choice) >= 0 and int(choice) <= max_page:
                        page = int(choice)
                except:
                    print('Invalid input')
                    time.sleep(1)
            elif is_item_selected and (choice == ''):
                iselected_item = None
                is_item_selected = False
                page = selected_num // 6
                selected_num = None

            else:
                try:
                    choice = int(choice)
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
                    print('Invalid input')
                    time.sleep(1)

    def item_stats_add(self):
        self.max_hp_items = 0
        self.max_mp_items = 0
        self.atk_items = 0
        self.sp_atk_items = 0
        self.def_items = 0
        self.sp_def_items = 0
        self.crit_chance_items = 0
        self.crit_bonus_items = 0
        for item in self.equiped_items:
            self.max_hp_items += item.max_hp
            self.max_mp_items += item.max_mp
            self.atk_items += item.atk
            self.sp_atk_items += item.sp_atk
            self.def_items += item.def_
            self.sp_def_items += item.sp_def
            self.crit_chance_items += item.crit_chance
            self.crit_bonus_items += item.crit_bonus

        if self.hp > self.max_hp + self.max_hp_items: self.hp = self.max_hp + self.max_hp_items
        if self.mp > self.max_mp + self.max_mp_items: self.mp = self.max_mp + self.max_mp_items



    def Level(self,xp):
        self.xp += xp
        if self.xp >= self.max_xp:
            loop_levelup = True
            while loop_levelup:
                clear()
                print(f'''
===========================
        Level UP
Level {self.level} => {self.level+1}
XP {self.xp}/{self.max_xp} => {self.xp-self.max_xp}/{self.next_level_xp(self.level+1)}
[1]Max HP {self.max_hp}+3 => {self.max_hp+3}
[2]Max MP {self.max_mp}+3 => {self.max_mp+3}
[3]ATK {self.atk}+1 => {self.atk+1}
[4]SP ATK {self.sp_atk}+1 => {self.sp_atk+1}
[5]DEF {self.def_}+1 => {self.def_+1}
[6]SP DEF {self.sp_def}+1 => {self.sp_def+1}
[7]Crit Chance {self.crit_chance}+1 => {self.crit_chance+1}
[8]Crit Bounus {self.crit_bonus}+2 => {self.crit_bonus+2}
[9]Move {self.min_move}-{self.max_move}
============================
Select stat to level up''')
                choice = input("> ").strip()
                if choice == '1':
                    rand = roll_dice(1,6,-1)
                    self.max_hp += rand
                    self.hp += rand
                    loop_levelup = False
                elif choice == '2':
                    rand = roll_dice(1,6,-1)
                    self.max_mp += rand
                    self.mp += rand
                    loop_levelup = False
                elif choice == '3':
                    self.atk += roll_dice(1,6,-1)
                    loop_levelup = False
                elif choice == '4':
                    self.sp_atk += roll_dice(1,6,-1)
                    loop_levelup = False
                elif choice == '5':
                    self.def_ += roll_dice(1,6,-1)
                    loop_levelup = False
                elif choice == '6':
                    self.sp_def += roll_dice(1,6,-1)
                    loop_levelup = False
                elif choice == '7':
                    self.crit_chance += roll_dice(1,6,-1)
                    loop_levelup = False
                elif choice == '8':
                    self.crit_bonus += roll_dice(1,6,-1)
                    loop_levelup = False
                elif choice == '9':
                    rand = roll_dice(1,6,-1)
                    self.min_move += rand
                    self.max_move += rand
                    loop_levelup = False
                else:
                    print('Invalid input')
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
        clear()
        print(f'''
===========================
        Stats
Level {self.level}
XP {self.xp}/{self.max_xp}
Max HP {self.max_hp} + {self.max_hp_items}
Max MP {self.max_mp} + {self.max_mp_items}
ATK {self.atk} + {self.atk_items}
SP ATK {self.sp_atk} + {self.sp_atk_items}
DEF {self.def_} + {self.def_items}
SP DEF {self.sp_def} + {self.sp_def_items}
Crit Chance {self.crit_chance} + {self.crit_chance_items}
Crit Bounus {self.crit_bonus} + {self.crit_bonus_items}
Move {self.min_move}-{self.max_move}
============================
''')
        input("\nPress Enter to return...")


    def move(self,dir,dungeon):
        global Curent_Layer ,DUNGEON
        room = dungeon.rooms[dungeon.room]
        self.last_pos = [self.x, self.y]
        x,y = self.x, self.y
        if dir == 'W':
            if room.map[y-1][x] != '#':
                self.y -=1
                self.moves -= 1
            else:
                print('Move in valed')
                return 'brake'
        elif dir == 'S':
            if room.map[y+1][x] != '#':
                self.y +=1
                self.moves -= 1
            else:
                print('Move in valed')
                return 'brake'
        elif dir == 'D':
            if room.map[y][x+1] != '#':
                self.x +=1
                self.moves -= 1
            else:
                print('Move in valed')
                return 'brake'
        elif dir == 'A':
            if room.map[y][x-1] != '#':
                self.x -=1
                self.moves -= 1
            else:
                print('Move in valed')
                return 'brake'
        x,y = self.x, self.y
        if room.map[y][x] == 'D':
            door_num = room.door_positions.index((x,y))
            old_room = dungeon.room
            dungeon.room = room.doors[door_num]
            door_num = dungeon.rooms[dungeon.room].doors.index(old_room)
            px,py = dungeon.rooms[dungeon.room].door_positions[door_num]
            new_room = dungeon.rooms[dungeon.room]
            new_room.show_on_map = True
            self.x ,self.y = px,py
        elif room.map[y][x] == 'S':
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
        elif room.map[y][x] == 's':
            Curent_Layer += 1
            if len(Layers) <= Curent_Layer:
                Layers.append(Dungeon(Curent_Layer,Dungeon_type))
            DUNGEON = Layers[Curent_Layer]
            dungeon = DUNGEON
            new_room = dungeon.rooms[dungeon.room]
            new_room.show_on_map = True
            self.y = len(new_room.map) // 2
            self.x = len(new_room.map[0]) // 2
        game_menu(self,dungeon)
        print_room_options(self)
        time.sleep(0.2)
        return 'fine'

    def print_fight_stats(self, show_atk = True):
        bars = ''
        if self.hp < 0: self.hp = 0
        if self.mp < 0: self.mp = 0
        line_1 = f'HP{self.hp}/{self.max_hp + self.max_hp_items}'
        helf_bar_len = 57 - len(line_1)
        helf_left = int(helf_bar_len * (self.hp / (self.max_hp + self.max_hp_items)))
        helf_bar = '['
        for _ in range(helf_left): helf_bar += '#'
        for _ in range(helf_bar_len - helf_left): helf_bar += ' '
        helf_bar += ']'
        line_2 = f'MP{self.mp}/{self.max_mp + self.max_mp_items}'
        mp_bar_len = 57 - len(line_2)
        mp_left = int(mp_bar_len * (self.mp / (self.max_mp + self.max_mp_items)))
        mp_bar = '['
        for _ in range(mp_left): mp_bar += '#'
        for _ in range(mp_bar_len - mp_left): mp_bar += ' '
        mp_bar += ']'
        #bars = line_1 + helf_bar + ' ' + line_2 + mp_bar
        print(f'''===========================================================
{line_1}\033[31m{helf_bar}\033[0m
{line_2}\033[34m{mp_bar}\033[0m''')
        del helf_bar,helf_bar_len,helf_left,mp_bar,mp_left,mp_bar_len
        if show_atk:
            asfd = [] # asfd stands for attack_stats_for_display
            temp_num = 0
            for i in self.attacks_used:
                attack = self.attacks[temp_num]['stats']
                temp_num += 1
                line_1 = f'{i} {attack["max_use"] - self.attacks_used[i]}/{attack["max_use"]}'
                while len(line_1) < 21: line_1 += ' '
                line_2 = f'MP {attack["mp"]} ATK {attack["atk"]} SP ATK {attack["sp_atk"]}'
                while len(line_2) < 25: line_2 += ' '
                line_3 = f'Adv {attack["adv"]} Crit {attack["crit_chance"]}% Crit {attack["crit_bonus"]}'
                while len(line_3) < 25: line_3 += ' '
                asfd.append([line_1,line_2,line_3])
            del temp_num
            print(f'''
 –––––––––––––––––––––––––––   ––––––––––––––––––––––––––– 
| [0] {asfd[0][0]} | | [1] {asfd[1][0]} |
| {asfd[0][1]} | | {asfd[1][1]} |
| {asfd[0][2]} | | {asfd[1][2]} |
 –––––––––––––––––––––––––––   ––––––––––––––––––––––––––– 
 –––––––––––––––––––––––––––   ––––––––––––––––––––––––––– 
| [2] {asfd[2][0]} | | [3] {asfd[3][0]} |
| {asfd[2][1]} | | {asfd[3][1]} |
| {asfd[2][2]} | | {asfd[3][2]} |
 –––––––––––––––––––––––––––   ––––––––––––––––––––––––––– ''')

    def rest(self):
        self.hp += (self.max_hp + self.max_hp_items) // 10
        self.mp += (self.max_mp + self.max_mp_items) // 10
        if self.hp > self.max_hp + self.max_hp_items: self.hp = self.max_hp + self.max_hp_items
        if self.mp > self.max_mp + self.max_mp_items: self.mp = self.max_mp + self.max_mp_items
        for i in self.attacks_used:
            self.attacks_used[i] = 0

class Enemy:

    def __init__(self,mob,level,room,x,y,is_boss = False):
        self.room = room
        self.mob = mob
        self.is_boss = is_boss
        self.x = x
        self.y = y
        self.is_del = False
        self.level = level
        if is_boss:
            stats = GTD.bosses[mob]['stats']
        else:
            stats = GTD.enemy_cls[mob]['stats']
        self.max_move = stats['max_move']
        self.min_move = stats['min_move']
        self.max_hp = stats['max_hp']
        self.max_mp = stats['max_mp']
        self.atk = stats['atk']
        self.sp_atk = stats['sp_atk']
        self.def_ = stats['def_']
        self.sp_def = stats['sp_def']
        self.crit_chance = stats['crit_chance']
        self.crit_bonus = stats['crit_bonus']
        self.xp = stats['xp']
        self.gold = stats['gold']
        self.level_up()
        self.hp = self.max_hp
        self.mp = self.max_mp
        self.get_attack_stats()
        self.items = []
        self.get_items()
        self.item_stats_add()

    def level_up(self):
        self.max_hp += 3 * (self.level - 1)
        self.max_mp += 3 * (self.level - 1)
        self.atk += 1 * (self.level - 1)
        self.sp_atk += 1 * (self.level - 1)
        self.def_ += 1 * (self.level - 1)
        self.sp_def += 1 * (self.level - 1)
        self.gold += 2 * (self.level - 1)
        self.xp += 2 * (self.level - 1)


    def item_stats_add(self):
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
            posbl_items = GTD.bosses[self.mob]['Items']
        else:
            posbl_items = GTD.enemy_cls[self.mob]['Items']
        for i in posbl_items:
            if random.randint(1,100) <= posbl_items[i]['chance']:
                try:
                    item_level = self.level + random.randint(posbl_items[i]['level'][0], posbl_items[i]['level'][1])
                    if item_level <= 0: item_level = 1
                    item = GameItem('unique',i,item_level,posbl_items[i]['name'])
                    self.items.append(item)
                except:
                    rarety_temp_1 = 0
                    rarety_temp_2 = 0
                    rand_num = random.randint(0,100)
                    for j in posbl_items[i]['rarety']:
                        rarety_temp_1 = rarety_temp_2
                        rarety_temp_2 += posbl_items[i]['rarety'][j]
                        if (rarety_temp_1 < rand_num) and (rand_num <= rarety_temp_2):
                            item_level = self.level + random.randint(posbl_items[i]['level'][0],posbl_items[i]['level'][1])
                            if item_level <= 0: item_level = 1
                            item = GameItem(j,i,item_level)
                            self.items.append(item)

    def get_attack_stats(self):
        self.attacks_used = {}
        attacks = []
        self.attacks = []
        for _ in range(4):
            attack_temp = []
            if self.is_boss:
                for i in GTD.bosses[self.mob]['Attacks']:
                    if i not in attacks:
                        for _ in range(GTD.bosses[self.mob]['Attacks'][i]):
                            attack_temp.append(i)
                attacks.append(random.choice(attack_temp))
            else:
                for i in GTD.enemy_cls[self.mob]['Attacks']:
                    if i not in attacks:
                        for _ in range(GTD.enemy_cls[self.mob]['Attacks'][i]):
                            attack_temp.append(i)
                attacks.append(random.choice(attack_temp))
        for i in attacks:
            self.attacks.append(GTD.attacks[i])
            self.attacks_used[i] = 0

    def move(self,player,room, dungeon):
        rand = random.randint(self.min_move,self.max_move)
        enemy_pos = room.get_enemy_pos()
        player_pos = [player.x,player.y]
        grid = room.map
        path = self.find_path(grid,enemy_pos,player_pos)
        if len(path) < rand: rand = len(path)
        for i in range(rand):
            print(path[i])
            if path[i] == 'N':
                self.y -= 1
            elif path[i] == 'S':
                self.y += 1
            if path[i] == 'W':
                self.x -= 1
            elif path[i] == 'E':
                self.x += 1
            game_menu(player,dungeon)
            time.sleep(0.2)



    def find_path(self,grid, enemy_pos, player_pos):
        from collections import deque

        target = (player_pos[0], player_pos[1])
        start = (self.x, self.y)
        blocked = set((e[0], e[1]) for e in enemy_pos)

        dirs = [(0, -1, 'N'), (0, 1, 'S'), (-1, 0, 'W'), (1, 0, 'E')]

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
                    if grid[ny][nx] == '#':
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


    def print_fight_stats(self):
        if self.hp < 0: self.hp = 0
        if self.mp < 0: self.mp = 0
        line_1 = f'{self.mob} Lvl. {self.level}'
        while len(line_1) < 25: line_1 += ' '
        line_2 = f'{self.hp}/{self.max_hp}'
        helf_bar_len = 23 - len(line_2)
        helf_left = int(helf_bar_len * (self.hp / self.max_hp))
        helf_bar = '['
        for _ in range(helf_left): helf_bar += '#'
        for _ in range(helf_bar_len-helf_left): helf_bar += ' '
        helf_bar += ']'
        line_2 += f'\033[31m{helf_bar}\033[0m'

        print(f'''
                              ––––––––––––––––––––––––––– 
                             | {line_1} |
                             | {line_2} |
                              ––––––––––––––––––––––––––– ''')


    def __repr__(self):
        return (f'HP={self.hp} MP={self.mp} Max HP={self.max_hp} Max MP={self.max_mp}\n'
                f'Atk={self.atk} SP Atk={self.sp_atk} Def={self.def_} SP Def={self.sp_def}\n'
                f'Crit Chance={self.crit_chance} Crit Bonus={self.crit_bonus} XP={self.xp}\n'
                f'Min Move={self.min_move} Max Move={self.max_move} Gold={self.gold}\n'
                f'Items={self.items}')

    def del_(self):
        if self.is_boss:
            self.room.map[self.y][self.x] = 's'
        self.x = -1
        self.y = -1
        self.is_del = True
        self.room.enemys.remove(self.room)
        del self.room, self.mob,self.level , self.max_move, self.min_move, self.max_hp, self.max_mp,self.atk, self.sp_atk, self.def_, self.sp_def, self.crit_chance, self.crit_bonus, self.xp,self.gold,self.hp,self.mp,self.items

class Dungeon:
    def __init__(self,layer,type):
        room = [
        ['#','#','#','#','#','#'],
        ['#','.','.','.','.','#'],
        ['#','.','.','.','.','#'],
        ['.','.','.','.','.','.'],
        ['#','.','.','.','.','#'],
        ['#','.','.','.','.','#'],
        ['#','#','#','#','#','#']]
        self.no_child = ['boss','start']
        self.layer = GTD.dungeons_preset[type]['layers'][layer]
        size_a = (GTD.dungeons_preset[type]['size'][0] + GTD.layers[self.layer]['size'][0]) // 2
        size_b = (GTD.dungeons_preset[type]['size'][1] + GTD.layers[self.layer]['size'][1]) // 2
        rand = random.randint(size_a, size_b)
        self.room_pos = []
        self.rooms = self.gen_dungeon(num_rooms=rand,layer=self.layer)
        self.rooms[0].show_on_map = True
        self.room = 0

        
    def print_room(self, player,triger_effect = True):
        #clear()
        room = self.rooms[self.room]
        enemys = room.enemys
        traps = room.traps
        #print("=====================")
        print(room.type)
        #print(room.enemys)
        fight_triger = [False,None]
        trap_triger = [False,None]
        for y, row in enumerate(room.map):
            line = ""
            for x, tile in enumerate(row):
                if (x, y) == (player.x, player.y):
                    for i in enemys:
                        if (x, y) == (i.x, i.y): fight_triger = [True,i]
                    for i in traps:
                        if (x,y) == (i.x,i.y): trap_triger = [True,i]
                    line += "P "
                else:
                    enemy_place = False
                    boss_place = False
                    trap_place = False
                    for i in enemys:
                        if (x,y) == (i.x,i.y):
                            if i.is_boss:
                                boss_place = True
                            else:
                                enemy_place = True
                    for i in traps:
                        if (x,y) == (i.x,i.y): trap_place = True
                    if enemy_place:
                        line += 'E '
                    elif boss_place:
                        line += 'B '
                    elif trap_place:
                        line += 'T '
                    else:
                        line += tile + " "
            print(line)
        if triger_effect:
            if fight_triger[0]:
                if player.moves < 0:
                    fight_loop(player,fight_triger[1],False)
                else:
                    fight_loop(player, fight_triger[1], True)
                if fight_triger[1].is_boss:
                    player.x, player.y = player.last_pos
                fight_triger[1].del_()
                player = game_menu(player,self,False)
            if trap_triger[0]:
                trap_triger[1].triger(player)
                player = game_menu(player,self,False)
        #print(room.doors)

    def conect_rooms(self,current,rooms):
        pos = current.pos
        side = choice(['top', 'bottom', 'left', 'right'])
        if side == 'top':
            pos_2 = (pos[0], pos[1] - 1)
        elif side == 'bottom':
            pos_2 = (pos[0], pos[1] + 1)
        elif side == 'left':
            pos_2 = (pos[0] - 1, pos[1])
        elif side == 'right':
            pos_2 = (pos[0] + 1, pos[1])
        safety_count = 0
        side_options = ['top', 'bottom', 'left', 'right']
        while side in current.sides_used or pos_2 not in self.room_pos:
            side = choice(side_options)
            side_options.remove(side)
            if side == 'top':
                pos_2 = (pos[0], pos[1] - 1)
            elif side == 'bottom':
                pos_2 = (pos[0], pos[1] + 1)
            elif side == 'left':
                pos_2 = (pos[0] - 1, pos[1])
            elif side == 'right':
                pos_2 = (pos[0] + 1, pos[1])
            safety_count += 1
            if safety_count > 3:
                break
        if safety_count > 3:
            return current,rooms
        other_id = self.room_pos.index(pos_2)
        other_room = rooms[other_id]
        if other_room.type == 'start' or other_room.type == 'boss':
            return current,rooms
        else:
            pos_a = current.add_door(side, self.room_pos, ignor_side=True)
            pos_b = other_room.add_door(OPPOSITE[side], self.room_pos, current.pos, mirror=pos_a, ignor_side=True)
            if pos_a and pos_b:
                current.doors.append(other_id)
                other_room.doors.append(current.id)
        return current,rooms

    def gen_dungeon(self, num_rooms=8, layer = 'layer 1'):
        rooms = {0: Room(0, "start",0,0, width=5,height=5,layer=layer)}
        todo = [0]
        self.room_pos = [(0,0)]
        next_id = 1

        SPECIAL_ROOMS = {"merchant": 0.05}  # Easy to add more

        while next_id < num_rooms and todo:
            current = rooms[todo.pop(0)]

            # Decide connections (1-3, fewer near end)
            if current.id == 0:
                connections = 1
            elif current.type in self.no_child:
                connections = 0
            else:
                connections = min(min(random.randint(1, 3),num_rooms - next_id),len(current.free_sides))


            for child in range(connections):
                clear()
                print('=========================')
                print('   Generating Dungeon')
                print('=========================')
                print(todo)
                print(current.id)
                print(next_id)
                #if next_id >= num_rooms: break
                # if current.conn <= 0: continue
                # Find available sides and connect
                current.update_free_sides(self.room_pos)
                avail_sides = current.free_sides
                if current.id != 0:
                    if not avail_sides:
                        if random.randint(0,3) == 0:
                            current, rooms = self.conect_rooms(current,rooms)
                            break
                        else:
                            break
                    if random.randint(0, 3) == 0 and len(todo) > 3:
                        current, rooms = self.conect_rooms(current, rooms)
                        continue

                # Determine room type
                room_type = "boss" if next_id == num_rooms - 1 else "normal"
                if room_type != 'boss':
                    for special, chance in SPECIAL_ROOMS.items(): # Willkommen bei der Freiheit
                        if random.random() < chance: room_type = special; break

                # Create and connect room

                new_room = Room(next_id, room_type,layer=layer)
                rooms[next_id] = new_room



                dir_a = random.choice(avail_sides)
                dir_b = OPPOSITE[dir_a]

                pos_a = current.add_door(dir_a,self.room_pos)
                pos_b = new_room.add_door(dir_b,self.room_pos,current.pos, mirror=pos_a)

                self.room_pos += [new_room.pos]


                if pos_a and pos_b:
                    current.doors.append(next_id)
                    new_room.doors.append(current.id)


                todo.append(next_id)
                next_id += 1

        for _ in range(len(rooms)//6):
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
    def __init__(self, room_id, room_type="normal",x=0,y=0, width=None, height=None , layer = 'layer 1'):
        self.id = room_id
        self.type = room_type
        self.pos = (x,y)
        self.doors = []           # [target_room_id, ...]
        self.enemys = []
        self.traps = []
        self.map = self.generate_room(room_type,width, height)
        self.door_positions = []  # [(x, y), ...]
        self.spawn_positions = []
        self.free_sides = ["top", "bottom", "left", "right"]  # which walls already have no doors
        self.sides_used = []
        self.add_asets(layer)
        self.show_on_map = False
        self.conn = None


    def place_enemy(self,width, height,layer = 'layer 1'):
        x = random.randint(1, width)
        y = random.randint(1, height)
        while self.map[y][x] != '.':
            x = random.randint(1, width)
            y = random.randint(1, height)
        rarety_temp_1 = 0
        rarety_temp_2 = 0
        rand_num = random.randint(0, 100)
        layer = GTD.layers[layer]
        for j in layer['mob']:
            p = layer['mob'][j]
            # print(p)
            time.sleep(0.1)
            rarety_temp_1 = rarety_temp_2
            rarety_temp_2 += p
            if (rarety_temp_1 < rand_num) and (rand_num <= rarety_temp_2):
                e_level = layer['level'] + random.randint(-3,3)
                if e_level <= 0: e_level = 1
                self.enemys.append(Enemy(j,e_level,self,x,y))

    def place_boss(self,width, height,layer = 'layer 1'):
        x = width
        y = height
        layer = GTD.layers[layer]
        e_level = layer['level'] + random.randint(-3,3)
        if e_level <= 0: e_level = 1
        self.enemys.append(Enemy(layer['boss'],e_level,self,x,y,True))

    def place_trap(self,width,height,layer = 'layer 1'):
        rarety_temp_1 = 0
        rarety_temp_2 = 0                                                        
        rand_num = random.randint(0, 100)                                        
        layer = GTD.layers[layer]                                                
        for j in layer['traps']:
            p = layer['traps'][j]
            # print(p)                                                           
            time.sleep(0.1)                                                      
            rarety_temp_1 = rarety_temp_2                                        
            rarety_temp_2 += p                                                   
            if (rarety_temp_1 < rand_num) and (rand_num <= rarety_temp_2):       
                self.traps.append(Trape(width,height,j))

    def get_enemy_pos(self):
        enemy_pos = []
        for e in self.enemys:
            enemy_pos.append([e.x,e.y])
        return enemy_pos

    def add_asets(self,layer='layer 1'):
        if self.type == 'start':
            height = len(self.map) // 2
            width = len(self.map[0]) // 2
            self.map[height][width] = 'S'
            print('add assets')

        elif self.type == 'boss':
            height = len(self.map) // 2
            width = len(self.map[0]) // 2
            self.place_boss(width, height, layer)
            print('add assets')


        elif self.type == 'normal':
            height = len(self.map) - 2
            width = len(self.map[0]) - 2
            space = height * width
            rand = random.randint((space//12),(space//4))
            for i in range(rand):
                if i == 0:
                    self.place_enemy(width,height,layer)
                else:
                    rand_2 = random.randint(-1,5)
                    if rand_2 <= 0:
                        self.place_enemy(width,height,layer)
                    elif rand_2 == 1:
                        x = random.randint(2,width-1)
                        y = random.randint(2,height-1)
                        if self.map[y][x] == '.': self.map[y][x] = '#'

                    elif rand_2 == 6:
                        x = random.randint(2,width-1)
                        y = random.randint(2,height-1)
                        if self.map[y][x] == '.': self.map[y][x] = '#'
                    elif rand_2 == 5:
                        x = random.randint(2,width-1)
                        y = random.randint(2,height-1)
                        if self.map[y][x] == '.': self.map[y][x] = '#'
                    elif rand_2 == 2:
                        x = random.randint(1,width)
                        y = random.randint(1,height)
                        if self.map[y][x] == '.': self.map[y][x] = 'C'
                    elif rand_2 == 3:
                        x = random.randint(1,width)
                        y = random.randint(1,height)
                        if self.map[y][x] == '.': self.place_trap(x,y,layer)
                    elif rand_2 == 4:
                        x = random.randint(1,width)
                        y = random.randint(1,height)
                        if self.map[y][x] == '.': self.map[y][x] = ' '
                print('add assets')



    def update_free_sides(self,grid):
        for i in self.free_sides:
            try:
                if i == 'top' and (self.pos[0],self.pos[1] - 1) in grid: self.free_sides.remove('top')
                if i == 'bottom' and (self.pos[0], self.pos[1] + 1) in grid: self.free_sides.remove('bottom')
                if i == 'left' and (self.pos[0] - 1, self.pos[1]) in grid: self.free_sides.remove('left')
                if i == 'right' and (self.pos[0] + 1, self.pos[1]) in grid: self.free_sides.remove('right')
            except:
                pass

    def add_door(self, side,grid,o_pos=None, mirror=None, ignor_side = False):
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
                self.pos = (o_pos[0] + 1,o_pos[1])
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

    def generate_room(self,room_type ,width=None, height=None):
        width = width or random.randint(6, 10)
        height = height or random.randint(6, 10)
        return [["#" if x in (0, width - 1) or y in (0, height - 1) else "." for x in range(width)] for y in range(height)]

class Trape:
    def __init__(self,x,y,type):
        self.x = x
        self.y = y
        self.show = False
        self.type = type

    def triger(self,player):
        clear()
        print('=============Trap=============')
        temp = f'{self.type}'
        while len(temp) < 30:
            temp += ' '
            if len(temp) < 30:
                temp = ' ' + temp
        print(temp)
        print(wrap_text(GTD.traps[self.type]['text'],30))

        art_t = GTD.trap_art
        art_p = GTD.fight_art
        player_art = art_p['player']
        trap_art = art_t[self.type]
        for i in range(len(trap_art['art'])):
            temp = '      '
            if i >= trap_art['player'][1] and (i - trap_art['player'][1]) < len(player_art):
                for j in range(trap_art['player'][0]):
                    temp += ' '
                temp += player_art[i - trap_art['player'][1]]
            temp += trap_art['art'][i]
            print(temp)
        if self.type == 'Mimic':
            input("\nPress Enter to return...")
            level = GTD.layers[Layers[Curent_Layer].layer]['level']
            enemy = Enemy('Mimic',level,None,0,0)
            player = fight_loop(player, enemy,False)
        else:
            input("\nPress Enter to return...")
            if GTD.traps[self.type]['damage_type'] == 0:
                player.hp -= GTD.traps[self.type]['damage']
            elif GTD.traps[self.type]['damage_type'] == 1:
                base = GTD.traps[self.type]['damage']
                roll = roll_dice(1,6,0)
                damage = int((base / 5)* ( 6 - roll))
                player.hp -= damage
            elif GTD.traps[self.type]['damage_type'] == 2:
                base = GTD.traps[self.type]['damage']
                base = int((player.max_hp / 100) * base)
                roll = roll_dice(1,6,0)
                damage = int((base / 5)* ( 6 - roll))
                player.hp -= damage




def enemy_move(dungeon, player):
    room = dungeon.rooms[dungeon.room]
    #print('enemys in room', len(room.enemys))
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
            enemy.move(player,room,dungeon)
        try:
            if enemy.is_del:
                room.enemys.remove(enemy)
                del enemy
        except:
            continue


def print_room_options(player):
    print('======== Your turn =========')
    if player.moves == -2:
        if player.cls == 'Roghe':
          print('R = Roll dice to move | F = Roll to check for traps')
        print('R = Roll dice to move | P = Make a pause and restr')
    elif player.moves > 0:
        print(f'Moves {player.moves} left')
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
        if len(rand_str) == 1: rand_str = ' ' + rand_str
        if len(rand_str) == 2: rand_str = rand_str + ' '
        clear()
        print(f'''
=========================
        Dice Roll
         –––––––
        |       |
        |  {rand_str}  |
        |       |
         –––––––

=========================
''')
        time.sleep((i + 1) / 50)
    input("\nPress Enter to return...")
    return rand


def main_menu():
    while True:
        clear()
        print("""
===================================
       DICE DUNGEON: DESCENT
===================================
 [1] Start Game
 [2] How to Play
 [3] Quit
""")
        choice = input("> ").upper().strip()
        if choice == "1":
            return "start"
        elif choice == "2":
            show_help_new()
        elif choice == "3" or 'Q':
            print("Goodbye, hero...")
            time.sleep(1)
            return 'exit'
        else:
            print("Invalid option.")
            time.sleep(1)

def show_help_new(page=0):
    max_page = 0
    help_text = GTD.help_txt
    while True:
        clear()
        print(f'''=============
    Help Page {page} / {max_page}
P = Privios Page | N = Next ''')
        print(help_text[f'page {page}'])
        choice = input("Press Enter to return... > ").upper().strip()
        if choice == 'N':
            if page < max_page:
                page += 1
        elif choice == 'P':
            if page > 0:
                page -= 1
        else:
            break

def game_menu(player,dungeon,triger_effect = True):
    HP = f'HP {player.hp}/{player.max_hp + player.max_hp_items}'
    MP = f'MP {player.mp}/{player.max_mp + player.max_mp_items}'
    gold = f'Gold {player.gold}'
    XP = f'XP {player.xp}/{player.max_xp}'
    level = f'Level {player.level}'
    while len(HP) < 13:
        HP += ' '
    while len(MP) < 13:
        MP += ' '
    while len(gold) < 13:
        gold += ' '
    while len(XP) < 13:
        XP += ' '
    while len(level) < 13:
        level += ' '
    clear()
    print(f'''
========================================
              Dice Dungeon
{HP}  {MP}  {gold}
{level}  {XP}
H = Help | I = Invetory | T = Stats
Q = Quit
========================================''')
    if GAME_STATE == 'map':
        dungeon.print_room(player,triger_effect)
    return player


def select_player_class():
    cls = []
    for i in GTD.player_cls:
        cls.append(i)
    while True:
        clear()
        print('''
======================
Selacte a player class
======================''')
        for i in range(len(cls)):
            print(f'[{i}] {cls[i]}')
        choice = input("> ").strip().upper()

        if choice == "Q":
            return "Q"
        try:
            if int(choice) >= 0 and int(choice) < len(cls):
                return cls[int(choice)]
            else:
                print("Invalid option.")
                time.sleep(1)
        except:
            print("Invalid option.")
            time.sleep(1)


def select_dungeon():
    d_type = []
    for i in GTD.dungeons_preset:
        d_type.append(i)
    while True:
        clear()
        print('''
======================
Selacte a dungeon
======================''')
        for i in range(len(d_type)):
            print(f'[{i}] {d_type[i]}')
        choice = input("> ").strip().upper()

        if choice == "Q":
            return "Q"
        try:
            if int(choice) >= 0 and int(choice) < len(d_type):
                return d_type[int(choice)]
            else:
                print("Invalid option.")
                time.sleep(1)
        except:
            print("Invalid option.")
            time.sleep(1)


def fight_art(player, enemy):
    art = GTD.fight_art
    player_art = art['player']
    enemy_art = art[enemy.mob]
    for i in range(len(player_art)):
        temp = '      '
        temp += player_art[i]
        while len(temp) < 40: temp += ' '
        temp += enemy_art[i]
        print(temp)

def print_dungeon_map(dungeon, spacing=1, room_size=2):
    # 1. BFS: relative Positionen bestimmen
    rooms = dungeon.rooms
    print(rooms)
    if len(str(rooms[len(rooms) - 1].id)) > room_size: room_size = len(str(rooms[len(rooms) - 1].id))
    clear()
    positions = [room.pos for room in dungeon.rooms.values()]

            # print('conn:',conn,' px,py:',px,py,' w,h:',w,h,' dx,dy:',dx,dy)

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
        #if room.show_on_map == False:
            #continue
        gx, gy = room.pos
        gx = (gx - minx) * (room_size + (spacing * 2))
        gy = (gy - miny) * (room_size + spacing)

        rid_str = str(room.id)
        if room.show_on_map or CHEATS_ON:
            if room.id == dungeon.room:
                if len(rid_str) < room_size:
                    for i in range(room_size - len(rid_str)):
                        grid[gy][gx + len(rid_str) + i] = "\33[32m#\33[0m"
                grid[gy][gx:gx + len(rid_str)] = [f'\33[32m{i}\33[0m' for i in rid_str]
                for i in range(room_size-1):
                    for j in range(room_size):
                        grid[gy + 1 + i][gx + j] = "\33[32m#\33[0m"
            elif room.type == 'boss':
                if len(rid_str) < room_size:
                    for i in range(room_size - len(rid_str)):
                        grid[gy][gx + len(rid_str) + i] = "\33[31m#\33[0m"
                grid[gy][gx:gx + len(rid_str)] = [f'\33[31m{i}\33[0m' for i in rid_str]
                for i in range(room_size-1):
                    for j in range(room_size):
                        grid[gy + 1 + i][gx + j] = "\33[31m#\33[0m"
            elif room.type == 'merchant':
                if len(rid_str) < room_size:
                    for i in range(room_size - len(rid_str)):
                        grid[gy][gx + len(rid_str) + i] = "\33[34m#\33[0m"
                grid[gy][gx:gx + len(rid_str)] = [f'\33[34m{i}\33[0m' for i in rid_str]
                for i in range(room_size-1):
                    for j in range(room_size):
                        grid[gy + 1 + i][gx + j] = "\33[34m#\33[0m"
            else:
                if len(rid_str) < room_size:
                    for i in range(room_size - len(rid_str)):
                        grid[gy][gx + len(rid_str) + i] = "#"
                grid[gy][gx:gx + len(rid_str)] = list(rid_str)
                for i in range(room_size-1):
                    for j in range(room_size):
                        grid[gy + 1 + i][gx + j] = "#"
        room_coords[room.id] = (gx, gy)


    # 4. Linien nur zwischen Räumen in Zwischenzellen
    # print(rooms)
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
    #clear()
    #print(dungeon.room_pos)
    print('='*width)
    text = 'Dungeon Map'
    while len(text) < width:
        text += ' '
        if len(text) < width:
            text = ' ' + text
    print(text)
    for row in grid:
        if any(i != ' ' for i in row):
            print("".join(row))
    #for i in rooms:
        #print('room:',i,'doors',rooms[i].doors)


    input("\nPress Enter to return...")

            
def game_loop_room(player):
    global loop_room, Layers, DUNGEON,CHEATS_ON
    loop_room = True
    while loop_room:
        dungeon = DUNGEON
        game_menu(player,dungeon)
        print_room_options(player)
        choice = input("> ").upper().strip()
        if choice == 'H':
            show_help_new()
            continue
        elif choice == 'T':
            player.show_stats()
            continue
        elif choice == 'I':
            player.show_inventory()
            continue
        elif choice == 'M':
            print_dungeon_map(dungeon)
            continue
        elif choice == 'Q':
            choice = input('You sure you want to qite? [Y/N]>').upper().strip()
            if choice == 'Y' or choice == 'Q':
                loop_room = False
                break
        elif choice == 'UP UP DOWN DOWN LEFT RIGHT LEFT RIGHT B A':
            CHEATS_ON = True
            continue
        if CHEATS_ON:
            if choice == 'GIVE ALL':
                for rarity in ["common", "uncommon", "rare", "epic", "legendary", "unique"]:
                    for item_type in ["sword", "knife", "bow", "stafe", "spear", "chestplate", "helmet","boots", "pants", "pans", "gloves", "sheald"]: # , "consumable"
                        player.add_to_inv(GameItem(rarity,item_type,100))
                continue
            elif choice == 'LEVEL UP':
                player.Level(player.max_xp + 1)
                continue
            elif choice == 'GIVE ITEM':
                player.add_to_inv(GameItem('common','sword',10))
                continue
            elif choice == 'FIGHT':
                enemy = Enemy('zomby',random.randint(1,5),0,5,5)
                player, loop_room = fight_loop(player,enemy)
                continue
            elif choice == 'TP':
                choice = input("> ").upper().strip()
                dungeon.room = int(choice)
        if player.moves == -2:
            if choice == 'R':
                player.roll_for_move()
                continue
                #time.sleep(1)
            elif choice == 'P':
                player.rest()
                player.moves = -1
                continue

        if player.moves >= 0 :
            if any(c not in ('W', 'A', 'S', 'D') for c in choice):
                print('Invalid input')
                time.sleep(1)
                continue
            elif len(choice) <= player.moves:
                for i in choice:
                    out = player.move(i,dungeon)
                    if out == 'brake':
                        time.sleep(1)
                        break
                continue
        if player.moves == -1 and choice == '':
            enemy_move(dungeon, player)
            player.moves = -2
        else:
            print('Invalid input')
            time.sleep(1)


def fight_selact_attack(player,enemy):
    clear()
    print('========================== FIGHT ==========================')
    print('Number to select attack')
    print('===========================================================')
    enemy.print_fight_stats()
    fight_art(player, enemy)
    player.print_fight_stats()

def p_chance(chance):
    rand = random.randint(1,100)
    return True if rand <= chance else False


def fight_roll_dice(player,enemy,start,end,sel = 0,advan=0,atk=True):
    rand = 0
    if atk:
        advan += player.attacks[sel]['stats']['adv']
        player.mp -= player.attacks[sel]['stats']['mp']
        for i in range(20):
            rand_o = rand
            while rand == rand_o:
                rand = random.randint(start, end)
            rand += advan
            if rand < start:
                rand = start
            elif rand > end:
                rand = end
            advan_e = 0
            rand_e = random.randint(start, end)
            rand_e += advan_e
            if rand_e < start:
                rand_e = start
            elif rand_e > end:
                rand_e = end
            rand_str = str(rand)
            if len(rand_str) == 1: rand_str = ' ' + rand_str
            if len(rand_str) == 2: rand_str = rand_str + ' '
            rand_str_e = str(rand_e)
            if len(rand_str_e) == 1: rand_str_e = ' ' + rand_str_e
            if len(rand_str_e) == 2: rand_str_e = rand_str_e + ' '
            clear()
            print('========================== FIGHT ==========================')
            enemy.print_fight_stats()
            fight_art(player, enemy)
            player.print_fight_stats(False)
            print(f'''===========================================================
        Player Attack        |        Enemy Deffens
           –––––––           |            –––––––
          |       |          |           |       |
          |  {rand_str}  |          |           |  {rand_str_e}  |
          |       |          |           |       |
           –––––––           |            ––––––– 
                             |
===========================================================
        ''')

            time.sleep((i + 1) / 50)

        p_crit = player.crit_chance + player.crit_chance_items + player.attacks[sel]['stats']['crit_chance']
        p_crit = p_chance(p_crit)
        if p_crit: print('Crit')

        p_atk = player.atk + player.atk_items
        p_atk = int(p_atk * (player.attacks[sel]['stats']['atk'] / 100))
        p_crit_bonus = player.crit_bonus + player.crit_bonus_items + player.attacks[sel]['stats']['crit_bonus']
        p_atk += int( p_atk * (p_crit_bonus / 100)) if p_crit else 0
        stranth = p_atk * rand
        print('stranth', stranth)

        p_sp_atk = player.sp_atk + player.sp_atk_items
        p_sp_atk = int(p_sp_atk * (player.attacks[sel]['stats']['sp_atk'] / 100))
        p_crit_bonus = player.crit_bonus + player.crit_bonus_items + player.attacks[sel]['stats']['crit_bonus']
        p_sp_atk += int(p_sp_atk * (p_crit_bonus / 100)) if p_crit else 0
        sp_stranth = p_sp_atk * rand
        print('sp_stranth', sp_stranth)

        e_def = enemy.def_
        e_def = e_def * rand_e
        print('e_def', e_def)

        e_sp_def = enemy.sp_def
        e_sp_def = e_sp_def * rand_e
        print('e_sp_def', e_sp_def)

        demage = stranth - e_def
        if demage < 0: demage = 0
        sp_damage = sp_stranth - e_sp_def
        if sp_damage < 0: sp_damage = 0
        demage += sp_damage
        print(f'Damage {demage}')
        enemy.hp -= demage

        input("\nPress Enter to return...")
        return player, enemy
    else:
        advan_e = 0
        e_attack_num = random.randint(0, 3)
        e_attack_used = list(enemy.attacks_used)[e_attack_num]
        print(enemy.attacks)
        print(type(enemy.attacks))
        e_attack_mp_use = enemy.attacks[e_attack_num]['stats']['mp']
        e_attack_max_used = enemy.attacks[e_attack_num]['stats']['max_use']
        while (enemy.attacks_used[e_attack_used] >= e_attack_max_used) or (enemy.mp < e_attack_mp_use) :
            e_attack_num = random.randint(0, 3)
            e_attack_used = list(enemy.attacks_used)[e_attack_num]
            e_attack_mp_use = enemy.attacks[e_attack_num]['stats']['mp']
            e_attack_max_used = enemy.attacks[e_attack_num]['stats']['max_use']
        e_attack = enemy.attacks[e_attack_num]['stats']
        enemy.attacks_used[e_attack_used] += 1
        print(e_attack)
        advan_e = e_attack['adv']
        advan += player.attacks[sel]['stats']['adv']
        for i in range(20):
            rand_o = rand
            while rand == rand_o:
                rand = random.randint(start, end)
            rand += advan
            if rand < start:
                rand = start
            elif rand > end:
                rand = end
            rand_e = random.randint(start, end)
            rand_e += advan_e
            if rand_e < start:
                rand_e = start
            elif rand_e > end:
                rand_e = end
            rand_str = str(rand)
            if len(rand_str) == 1: rand_str = ' ' + rand_str
            if len(rand_str) == 2: rand_str = rand_str + ' '
            rand_str_e = str(rand_e)
            if len(rand_str_e) == 1: rand_str_e = ' ' + rand_str_e
            if len(rand_str_e) == 2: rand_str_e = rand_str_e + ' '
            clear()
            print('========================== FIGHT ==========================')
            enemy.print_fight_stats()
            fight_art(player, enemy)
            player.print_fight_stats(False)
            print(f'''===========================================================
        Player Deffens       |        Enemy Attack
           –––––––           |            –––––––
          |       |          |           |       |
          |  {rand_str}  |          |           |  {rand_str_e}  |
          |       |          |           |       |
           –––––––           |            ––––––– 
                             |
===========================================================
                ''')
            time.sleep((i + 1) / 50)

        e_crit = enemy.crit_chance + e_attack['crit_chance']
        e_crit = p_chance(e_crit)
        if e_crit: print('Enemy Crit')

        e_atk = enemy.atk
        e_atk = int(e_atk * (e_attack['atk'] / 100))
        e_crit_bonus = enemy.crit_bonus  + e_attack['crit_bonus']
        e_atk += int(e_atk * (e_crit_bonus / 100)) if e_crit else 0
        stranth = e_atk * rand_e
        print('stranth', stranth)

        e_sp_atk = enemy.sp_atk
        e_sp_atk = int(e_sp_atk * (e_attack['sp_atk'] / 100))
        e_crit_bonus = enemy.crit_bonus + e_attack['crit_bonus']
        e_sp_atk += int(e_sp_atk * (e_crit_bonus / 100)) if e_crit else 0
        sp_stranth = e_sp_atk * rand_e
        print('sp_stranth', sp_stranth)

        p_def = player.def_ + player.def_items
        p_def = p_def * rand
        print('p_def', p_def)

        p_sp_def = player.sp_def + player.sp_def_items
        p_sp_def = p_sp_def * rand
        print('p_sp_def', p_sp_def)

        demage = stranth - p_def
        if demage < 0: demage = 0
        sp_damage = sp_stranth - p_sp_def
        if sp_damage < 0: sp_damage = 0
        demage += sp_damage
        print(f'Damage {demage}')
        player.hp -= demage
        enemy.mp -= e_attack_mp_use

        input("\nPress Enter to return...")
        return player, enemy


def fight_won(player,enemy):
    gold_gain = f'{enemy.gold} Gold'
    while len(gold_gain) < 27:
        gold_gain = gold_gain + ' '
        if len(gold_gain) < 27: gold_gain = ' ' + gold_gain
    xp_gain = f'{enemy.xp} XP'
    while len(xp_gain) < 27:
        xp_gain = xp_gain + ' '
        if len(xp_gain) < 27: xp_gain = ' ' + xp_gain
    stats_gain = gold_gain + ' ' + xp_gain

    clear()
    print('========================= FIGHT ===========================')
    enemy.print_fight_stats()
    fight_art(player, enemy)
    player.print_fight_stats(False)
    print('========================= REWARD ==========================')
    print(stats_gain)
    print('                          ITEMS                            ')
    for item in enemy.items:
        print(item.Name())
        player.inventory.append(item)
    input("\nPress Enter to return...")
    player.gold += enemy.gold
    player.Level(enemy.xp)


def you_died():
    clear()
    print('You died')
    input("\nPress Enter to return...")


def fight_loop(player,enemy,player_start = True):
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

        elif first_turn:
            if turn == 0:
                clear()
                print('========================== FIGHT ==========================')
                enemy.print_fight_stats()
                fight_art(player, enemy)
                player.print_fight_stats(False)
                print('===========================================================')
                choice = input('\nPress Enter to continue...').upper().strip()
                if choice == 'Q':
                    loop_fight = False
                    return player, True
                elif choice == 'S':
                    print(enemy)
                    input("\nPress Enter to return...")
                else:
                    player, enemy = fight_roll_dice(player, enemy, 1, 6, advan=-1,atk=False)
                    turn = 1
                    first_turn = False
            elif turn == 1:
                fight_selact_attack(player,enemy)
                choice = input('>').upper().strip()
                try:
                    if choice == 'Q':
                        loop_fight = False
                        return player, True
                    elif choice == 'S':
                        print(enemy)
                        input("\nPress Enter to return...")
                    elif (0 <= int(choice)) and (int(choice) <= 3):
                        attack_num = int(choice)
                        attack_used = list(player.attacks_used)[attack_num]
                        attack_max_used = player.attacks[attack_num]['stats']['max_use']
                        if player.attacks_used[attack_used] >= attack_max_used:
                            print('No more uses of selected attack left')
                            time.sleep(1)
                        elif player.attacks[attack_num]['stats']['mp'] > player.mp:
                            print('Not enough mp for this attack')
                            time.sleep(1)
                        else:
                            player.attacks_used[attack_used] += 1
                            player, enemy = fight_roll_dice(player,enemy,1,6,attack_num,1)
                            turn = 0
                            first_turn = False
                except:
                    print('Invalid input')
                    time.sleep(1)

        elif first_turn == False:
            if turn == 0:
                clear()
                print('========================== FIGHT ==========================')
                enemy.print_fight_stats()
                fight_art(player, enemy)
                player.print_fight_stats(False)
                print('===========================================================')
                choice = input('\nPress Enter to continue...').upper().strip()
                if choice == 'Q':
                    loop_fight = False
                elif choice == 'S':
                    print(enemy)
                    input("\nPress Enter to return...")
                else:
                    player, enemy = fight_roll_dice(player, enemy, 1, 6, atk=False)
                    turn = 1
            elif turn == 1:
                fight_selact_attack(player, enemy)
                choice = input('>').upper().strip()
                try:
                    if choice == 'Q':
                        loop_fight = False
                    elif choice == 'S':
                        print(enemy)
                        input("\nPress Enter to return...")
                    elif (0 <= int(choice)) and (int(choice) <= 3):
                        attack_num = int(choice)
                        attack_used = list(player.attacks_used)[attack_num]
                        attack_max_used = player.attacks[attack_num]['stats']['max_use']
                        if player.attacks_used[attack_used] >= attack_max_used:
                            print('No more uses of selected attack left')
                            time.sleep(1)
                        elif player.attacks[attack_num]['stats']['mp'] > player.mp:
                            print('Not enough mp for this attack')
                            time.sleep(1)
                        else:
                            player.attacks_used[attack_used] += 1
                            player, enemy = fight_roll_dice(player, enemy, 1, 6, attack_num)
                            turn = 0
                except:
                    print('Invalid input')
                    time.sleep(1)



if __name__ == "__main__":
    main_loop = True
    loop_room = False
    loop_fight = False
    CHEATS_ON = True #False
    Layers = []
    Curent_Layer = 0
    while main_loop:
        out = main_menu()
        if out == 'start':
            cls = select_player_class()
            if cls == 'Q': continue
            Dungeon_type = select_dungeon()
            if Dungeon_type == 'Q': continue
            Layers.append(Dungeon(Curent_Layer,Dungeon_type))
            DUNGEON = Layers[Curent_Layer]
            player = Player(cls)
            player.add_to_inv(GameItem('legendary','sword',75))
            player.add_to_inv(GameItem('common','sword',10))
            GAME_STATE = 'map'
            game_loop_room(player)
        # game_menu()
        # give all
        elif out == 'exit':
            main_loop = False
            break
