import os , time, random, math
import Game_text_data
from Items import GameItem
from collections import deque

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

def roll_dice(start,end,advan=0):
    rand = 0
    for i in range(20):
        rand_o = rand
        while rand == rand_o:
            rand = random.randint(start,end)
        rand += advan
        if rand < start: rand = start
        elif rand > end: rand = end
        rand_str = str(rand)
        if len(rand_str) == 1: rand_str =' ' + rand_str
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
        time.sleep((i+1)/50)
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
        next_level_xp(5)
        choice = input("> ").strip()
        if choice == "1":
            return "start"
        elif choice == "2":
            show_help_new()
        elif choice == "3":
            print("Goodbye, hero...")
            time.sleep(1)
            exit()
        else:
            print("Invalid option.")
            time.sleep(1)


def show_help():
    clear()
    print("""
--- HOW TO PLAY ---
- You roll a dice to move across the dungeon.
- Use W/A/S/D to choose a path.
- Encounter enemies, treasure, and merchants.
- Advantage if you find them first.
- Survive and reach the final floor.
""")
    input("\nPress Enter to return...")

def show_help_new(page = 0):
    max_page = 0
    help_text = Game_text_data.help_txt
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


    
def game_menu():

    HP = f'HP {player.hp}/{player.max_hp}'
    MP = f'MP {player.mp}/{player.max_mp}'
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
========================================
{HP}  {MP}  {gold}
{level}  {XP}
H = Help | I = Invetory | T = Stats
Q = Quit
========================================''')
    if GAME_STATE == 'map':
      dangeon.print_room(player= player)
    
    
def select_player_class():
    while True:
        clear()
        print('''
======================
Selacte a player class
======================
[1] Adventurer
    ''')
        choice = input("> ").strip()
        if choice == "1":
            return "Adventurer"
        else:
            print("Invalid option.")
            time.sleep(1)
    

def next_level_xp(level):
    return (math.floor((((math.log(level ** 2,10)) ** 2) + 1) * 5)) * 3


class Player:
    def __init__(self,cls):
        self.cls = cls
        self.moves = -1
        self.x = 2
        self.y = 2
        self.level = 1
        self.xp = 0
        self.max_xp = next_level_xp(self.level)
        self.gold = 10
        self.inventory = []
        self.equiped_items = []
        self.favorit = []
        self.equipt_slots = {'wappon': False, 'helmet': False, 'chestplate': False, 'pants': False, 'boots': False, 'sheald': False}
        if cls == 'Adventurer':
            self.max_move = 6
            self.min_move = 1
            self.max_hp = 20
            self.max_mp = 20
            self.atk = 2
            self.sp_atk = 2
            self.Def = 2
            self.sp_Def = 2
            self.crit_chance = 2
            self.crit_bounus = 10
            
        self.hp = self.max_hp
        self.mp = self.max_mp

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
            self.equipt_slots[slot] = False
        else:
            if self.equipt_slots[slot]:
                print(f'You have laredy a {slot} equipped')
                time.sleep(1)
            else:
                self.equiped_items.append(item)
                item.is_equiped = True
                self.equipt_slots[slot] = True



    def show_inventory(self):
        is_item_selected = False
        page = 0
        is_fav = False
        is_equ = False
        item_fillter = self.inventory
        selected_item = None
        selected_num = None
        while True:
            max_page = int(len(item_fillter) // (4 if is_item_selected else 6))
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
                titel = f'Level {selected_item.level}/{selected_item.max_level} {selected_item.grade} {selected_item.item_type}: {selected_item.name} {'*' if item.is_equiped else ''}'
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

    def Level(self,xp):
        self.xp += xp
        if self.xp >= self.max_xp:
            clear()
            print(f'''
===========================
        Level UP
Level {self.level} => {self.level+1}
XP {self.xp}/{self.max_xp} => {self.xp-self.max_xp}/{next_level_xp(self.level+1)}
[1]Max HP {self.max_hp}+3 => {self.max_hp+3}
[2]Max MP {self.max_mp}+3 => {self.max_mp+3}
[3]ATK {self.atk}+1 => {self.atk+1}
[4]SP ATK {self.sp_atk}+1 => {self.sp_atk+1}
[5]DEF {self.Def}+1 => {self.Def+1}
[6]SP DEF {self.sp_Def}+1 => {self.sp_Def+1}
[7]Crit Chance {self.crit_chance}+1 => {self.crit_chance+1}
[8]Crit Bounus {self.crit_bounus}+2 => {self.crit_bounus+2}
[9]Move {self.min_move}-{self.max_move}
============================
Select stat to level up
''')
            self.xp -= self.max_xp
            self.level += 1
            self.max_hp += 3
            self.max_mp += 3
            self.atk += 1
            self.sp_atk += 1
            self.Def += 1
            self.sp_Def += 1
            self.crit_chance += 1
            self.crit_bounus += 2
            choice = input("> ").strip()
            if choice == '1': self.max_hp += roll_dice(1,6,-1)
            elif choice == '2': self.max_mp += roll_dice(1,6,-1)
            elif choice == '3': self.atk += roll_dice(1,6,-1)
            elif choice == '4': self.sp_atk += roll_dice(1,6,-1)
            elif choice == '5': self.Def += roll_dice(1,6,-1)
            elif choice == '6': self.sp_Def += roll_dice(1,6,-1)
            elif choice == '7': self.crit_chance += roll_dice(1,6,-1)
            elif choice == '8': self.crit_bounus += roll_dice(1,6,-1)
            elif choice == '9':
                temp = roll_dice(1,6,-1)
                self.min_move += temp
                self.max_move += temp


    def show_stats(self):
        clear()
        print(f'''
===========================
        Stats
Level {self.level}
XP {self.xp}/{self.max_xp}
Max HP {self.max_hp}
Max MP {self.max_mp}
ATK {self.atk}
SP ATK {self.sp_atk}
DEF {self.Def}
SP DEF {self.sp_Def}
Crit Chance {self.crit_chance}
Crit Bounus {self.crit_bounus}
Move {self.min_move}-{self.max_move}
============================
''')
        input("\nPress Enter to return...")




class Dungeon:
    def __init__(self):
        room = [
        ['#','#','#','#','#','#'],
        ['#','.','.','.','.','#'],
        ['#','.','.','.','.','#'],
        ['.','.','.','.','.','.'],
        ['#','.','.','.','.','#'],
        ['#','.','.','.','.','#'],
        ['#','#','#','#','#','#']]
        rand = random.randint(5,15)
        self.rooms = self.gen_dungeon(num_rooms=rand)
        self.room = 0
        
    def print_room(self, player):
        #clear()
        room = self.rooms[self.room]
        #print("=====================")
        for y, row in enumerate(room.map):
            line = ""
            for x, tile in enumerate(row):
                if (x, y) == (player.x, player.y):
                    line += "P "
                else:
                    line += tile + " "
            print(line)
        #print(self.room)
        #print(room.doors)

    def gen_dungeon(self, num_rooms=8):
        rooms = {0: Room(0, "start")}
        todo = [0]
        next_id = 1

        SPECIAL_ROOMS = {"merchant": 0.15}  # Easy to add more

        while next_id < num_rooms and todo:
            current = rooms[todo.pop(0)]

            # Decide connections (1-3, fewer near end)
            if current.id == 0:
                connections = 1
            else:
                connections = min(random.randint(1, 3), num_rooms - next_id)

            for _ in range(connections):
                if next_id >= num_rooms: break

                # Determine room type
                room_type = "boss" if next_id == num_rooms - 1 else "normal"
                for special, chance in SPECIAL_ROOMS.items(): # Willkommen bei der Freiheit
                    if random.random() < chance: room_type = special; break

                # Create and connect room
                new_room = Room(next_id, room_type)
                rooms[next_id] = new_room

                # Find available sides and connect
                avail_sides = [s for s in SIDES if s not in current.used_sides]
                if not avail_sides: break

                dir_a = random.choice(avail_sides)
                dir_b = OPPOSITE[dir_a]

                pos_a = current.add_door(dir_a)
                pos_b = new_room.add_door(dir_b, mirror=pos_a)

                if pos_a and pos_b:
                    current.doors.append(next_id)
                    new_room.doors.append(current.id)

                todo.append(next_id)
                next_id += 1

        # Clean up start/boss rooms
        for room_id in [0, num_rooms - 1]:
            if room_id in rooms:
                room = rooms[room_id]
                room.doors = room.doors[:1]
                room.door_positions = room.door_positions[:1]
                room.used_sides = set(list(room.used_sides)[:1])

        return rooms




class Room:
    def __init__(self, room_id, room_type="normal", width=None, height=None):
        self.id = room_id
        self.type = room_type
        self.doors = []           # [target_room_id, ...]
        self.map = generate_room(width, height)
        self.door_positions = []  # [(x, y), ...]
        self.used_sides = set()   # which walls already have doors

    def add_door(self, side, mirror=None):
        if side in self.used_sides:
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
            elif side == "right":
                x, y = width - 1, clamp(my, 1, height - 2)
            elif side == "top":
                x, y = clamp(mx, 1, width - 2), 0
            elif side == "bottom":
                x, y = clamp(mx, 1, width - 2), height - 1
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
        self.used_sides.add(side)
        return (x, y)


def generate_room(width=None, height=None):
    width = width or random.randint(6, 10)
    height = height or random.randint(6, 10)
    return [["#" if x in (0, width - 1) or y in (0, height - 1) else "." for x in range(width)] for y in range(height)]


def print_room_options(player):
    print('======== Your turn =========')
    if player.moves == -1:
        if player.cls == 'Roghe':
          print('R = Roll dice to move | F = Roll to check for traps')
        print('R = Roll dice to move')
    elif player.moves > 0:
        print(f'Moves {player.moves} left')
    else:
        player.moves = -1

def move(dir,player,dungeon):
    room = dungeon.rooms[dungeon.room]
    x,y = player.x, player.y
    if dir == 'W':
        if room.map[y-1][x] != '#':
            player.y -=1
            player.moves -= 1
        else:
            print('Move in valed')
            return 'brake'
    elif dir == 'S':
        if room.map[y+1][x] != '#':
            player.y +=1
            player.moves -= 1
        else:
            print('Move in valed')
            return 'brake'
    elif dir == 'D':
        if room.map[y][x+1] != '#':
            player.x +=1
            player.moves -= 1
        else:
            print('Move in valed')
            return 'brake'
    elif dir == 'A':
        if room.map[y][x-1] != '#':
            player.x -=1
            player.moves -= 1
        else:
            print('Move in valed')
            return 'brake'
    x,y = player.x, player.y
    if room.map[y][x] == 'D':
        door_num = room.door_positions.index((x,y))
        old_room = dungeon.room
        dungeon.room = room.doors[door_num]
        door_num = dungeon.rooms[dungeon.room].doors.index(old_room)
        px,py = dungeon.rooms[dungeon.room].door_positions[door_num]
        player.x ,player.y = px,py

    game_menu()
    print_room_options(player)
    time.sleep(0.1)
    return 'fine'


def print_dungeon_map(rooms, spacing=1):
    # 1. BFS: relative Positionen bestimmen
    clear()
    positions = {0: (0,0)}
    positions_given = [(0,0)]
    placed = {0}
    queue = [0]

    while queue:
        rid = queue.pop(0)
        room = rooms[rid]
        x, y = positions[rid]
        print('rid:',rid,' x,y :',x,y)
        #print('doors', room.doors)

        for i, conn in enumerate(room.doors):
            if conn in placed: continue
            px, py = room.door_positions[i]
            w, h = len(room.map[0]), len(room.map)
            dx = dy = 0
            if py == 0: dy = -1
            elif py == h-1: dy = 1
            elif px == 0: dx = -1
            elif px == w-1: dx = 1
            positions[conn] = (x+dx, y+dy)
            placed.add(conn)
            queue.append(conn)
            print('conn:',conn,' px,py:',px,py,' w,h:',w,h,' dx,dy:',dx,dy)

    # 2. Grid vorbereiten
    xs = [p[0] for p in positions.values()]
    ys = [p[1] for p in positions.values()]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)

    room_size = 2
    width = (maxx-minx+1)*(room_size+spacing) - spacing
    height = (maxy-miny+1)*(room_size+spacing) - spacing
    grid = [[" " for _ in range(width)] for _ in range(height)]

    # 3. Räume zeichnen
    room_coords = {}
    for rid, (x, y) in positions.items():
        gx = (x-minx)*(room_size+spacing)
        gy = (y-miny)*(room_size+spacing)
        rid_str = str(rid)
        # ID oben links, max 2 Zeichen
        if len(rid_str) == 1: grid[gy][gx+1] = "#"
        grid[gy][gx:gx+len(rid_str)] = list(rid_str)
        grid[gy+1][gx] = "#"
        grid[gy+1][gx+1] = "#"
        room_coords[rid] = (gx, gy)

    # 4. Linien nur zwischen Räumen in Zwischenzellen
    print(rooms)
    for rid, room in rooms.items():
        gx, gy = room_coords[rid]
        for i, conn in enumerate(room.doors):
            cgx, cgy = room_coords[conn]

            # Vertikal
            if gx == cgx:
                start = min(gy+room_size, cgy)
                end = max(gy, cgy+room_size)
                for y_pos in range(start, end):
                    if grid[y_pos][gx] == " ":
                        grid[y_pos][gx] = "|"
            # Horizontal
            elif gy == cgy:
                start = min(gx+len(str(rid)), cgx)
                end = max(gx+1, cgx)
                for x_pos in range(start, end):
                    if grid[gy][x_pos] == " ":
                        grid[gy][x_pos] = "-"

    # 5. Ausgabe
    #clear()
    for row in grid:
        print("".join(row))
    for i in rooms:
        print('room:',i,'doors',rooms[i].doors)

    input("\nPress Enter to return...")


            
def game_loop_room(plyaer,dungeon):
    loop = True
    while loop:
        game_menu()
        print_room_options(player)
        choice = input("> ").upper().strip()
        if choice == 'H':
            show_help_new()
        elif choice == 'T':
            player.show_stats()
        elif choice == 'I':
            player.show_inventory()
        elif choice == 'M':
            print_dungeon_map(dungeon.rooms)
        elif choice == 'Q':
            loop = False
            break
        elif choice == 'GIVE ALL':
            for rarity in ["common", "uncommon", "rare", "epic", "legendary", "unique"]:
                for item_type in ["sword", "knife", "bow", "stafe", "spear", "chestplate", "helmet","boots", "pants", "pans", "gloves", "sheald"]: # , "consumable"
                    player.add_to_inv(GameItem(rarity,item_type,10))
        elif choice == 'LEVEL UP':
            player.Level(player.max_xp + 1)
        elif choice == 'GIVE ITEM':
            player.add_to_inv(GameItem('common','sword',10))
        elif choice == 'R':
            if player.moves == -1:
                player.roll_for_move()
                #time.sleep(1)
        elif player.moves != -1 :
            if any(c not in ('W', 'A', 'S', 'D') for c in choice):
                print('Invalid input')
                time.sleep(1)
            elif len(choice) <= player.moves:
                for i in choice:
                    out = move(i,player,dungeon)
                    if out == 'brake':
                        time.sleep(1)
                        break
        else:
            print('Invalid input')
            time.sleep(1)
    
    
    
    
if __name__ == "__main__":
    print('lol')
    out = main_menu()
    print(out)
    if out == 'start':
      cls = select_player_class()
      dangeon = Dungeon()
      player = Player(cls)
      player.add_to_inv(GameItem('common','sword',10))
      player.add_to_inv(GameItem('common','sword',10))
      GAME_STATE = 'map'
      game_loop_room(player,dangeon)
      # game_menu()
      # give all
