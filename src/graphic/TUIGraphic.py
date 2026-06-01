import random


from copy import deepcopy
from math import ceil

from .TUI_init import *
from data import Game_text_data as GTD
from . import TUIGraphicCommon as com
from .TUIGraphicCommon import clear, printr, wait, inputT, get_color_code


def roll_dice(start, end, advan=0):
    clear()
    rand = 0
    rand_str = str(rand)
    printr(lambda : f"""
=========================
Dice Roll
╭───────╮
│       │
│  {rand_str}  │
│       │
╰───────╯

=========================
""")
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
        if len(rand_str) == 1:
            rand_str = " " + rand_str
        if len(rand_str) == 2:
            rand_str = rand_str + " "
        wait((i + 1) / 50)
    inputT("\nPress Enter to return...")
    return rand


def show_inventory(
    page: int,
    per_page: int,
    max_page: int,
    is_item_selected: bool,
    item_fillter,
    selected_item,
    is_shop,
    gold,
    curser=[0, 0,0,0],
    size=[2,4]
):
    while True:
        clear()
        #printr(f"{[WIDTH // 40, (HEIGHT - 10) // 6]}  {size}")
        if [WIDTH // 40, (HEIGHT - 10) // 6] != size and not is_item_selected:
            return None , curser
        
        out, header_shape = render_inventory_header(page, max_page, is_shop, gold, curser)
        
        if is_item_selected:
            render_item_details(selected_item)
        start = page * per_page
        end = start + per_page
        items = item_fillter[start:end]
        offset = page * per_page

        item_render = build_item_render(items, is_shop,selected_item,offset)
        

        if curser[0] > -1:
            sel = (curser[0] * 2 + curser[1]) 
        else:
            sel = None
        # printr(ceil(len(item_render) / 2) - 1)
        #render_item_boxes(item_render, offset, sel)
        printr('')
        sel, box_shape = com.box_menu(item_render,curser,size)
        #menu_handler(curser,box_shape,header_shape,page,max_page)
        choice = inputT("> ", True)
        if choice not in ["UP", "DOWN", "LEFT", "RIGHT", "ENTER"]:
            return choice, curser
        else:
            if choice == "ENTER":
                if sel != None:
                    printr(sel + 1 + offset)
                    return sel + 1 + offset, curser
                elif out:
                    return out, curser
            elif choice == "UP":
                curser[3] = curser[1]
                curser[2] = curser[0]
                curser[0] -= 1
            elif choice == "DOWN":
                curser[3] = curser[1]
                curser[2] = curser[0]
                curser[0] += 1
            elif choice == "LEFT":
                curser[2] = curser[0]
                curser[3] = curser[1]
                curser[1] -= 1
            elif choice == "RIGHT":
                curser[2] = curser[0]
                curser[3] = curser[1]
                curser[1] += 1
                
            choice, curser = com.menu_handler(curser,box_shape,header_shape,page,max_page)
            if choice:
                return choice, curser
            


def render_inventory_header(page, max_page, is_shop, gold, curser):
    ops = {
        "SE": "Show Equipped",
        "SF": "Show Favorites",
        "Q": "Close",
        "PAGE": "Go to Page",
        "H": "Help",
        "N": "Next",
        "F": "Favorite",
        "E": f"{'Sell' if is_shop else 'Equip'}",
        "P": "Previous",
    }

    if is_shop:
        com.print_titelbar(f"Shop Page {page + 1} / {max_page + 1}", 78)
        printr(f"Gold {gold}")
        printr(com.center_text("", 78, "-"))
    else:
        com.print_titelbar(f"Inventory Page {page + 1} / {max_page + 1}", 78)
    # printr(f""" Q = Close | N = Next | P = Previous | H = Help
    # E = {"Sell" if is_shop else "Equip"} | F = Favorite | SF = Show Favorites
    # PAGE = Go to Page | Number = Select Item | SE = Show Equipped
    # ==============================================================================""")
    out, shape = com.header_options(ops, curser, 50, True)
    return out, shape



def build_item_render(items, is_shop=False,selected_item = None, offset = 0):
    item_render: list[com.BoxPreRender] = []
    for item in items:
        temp_render = com.BoxPreRender()
        line1 = f"{item.grade} {item.sub_type} (Lvl {item.level})"
        line2 = f"{item.name} {'*' if item.is_equiped else ''}"
        if is_shop:
            line3 = f"{item.value}G"
        else:
            line3 = ""
        
        # Grafik an Graphics delegieren
        line1 = com.fixed_width(line1, 34)
        line2 = com.fixed_width(line2, 34)
        while len(line3) < 22:
            line3 = " " + line3
            
        temp_render.texts.append(line1)
        temp_render.texts.append(line2)
        temp_render.num_line = line3
        
        color = "red" if item == selected_item else "blue" if item.is_equiped else "yellow" if item.is_fav else None
        if color:
            color = com.get_color_code(color)
            temp_render.color = color
        
        temp_render.num = items.index(item) + offset
        temp_render.numj = 11
        
        item_render.append(temp_render)

    return item_render


def render_item_details(selected_item) -> None:
    titel = f"Level {selected_item.level}/{selected_item.max_level} {selected_item.grade} {selected_item.sub_type}: {selected_item.name} {'*' if selected_item.is_equiped else ''}"
    stats = selected_item.get_stats()
    hp = com.center_text(f"HP {stats['max hp']}", 24)
    mp = com.center_text(f"MP {stats['max mp']}", 24)
    atk = com.center_text(f"ATK {stats['atk']}", 24)
    sp_atk = com.center_text(f"SP ATK {stats['sp atk']}", 24)
    def_ = com.center_text(f"DEF {stats['def']}", 24)
    sp_def = com.center_text(f"SP DEF {stats['sp def']}", 24)
    crit_chance = com.center_text(f"Crit Chance {stats['crit chance']}", 24)
    crit_bounus = com.center_text(f"Crit Bonus {stats['crit bonus']}", 24)
    item_price = com.center_text(f"Price {stats['price']}", 24)
    flavor_text = "Flavor text\n\n" + selected_item.flavor
    # flavor_text = wrap_text(selected_item.flavor, 73,1)
    if selected_item.ele:
        ele = f"\nElement: {com.get_color_code(GTD.elementare[selected_item.ele]["color"])}{selected_item.ele}{com.get_color_code('none')}"
    else:
        ele = "" #"Element: This item dosen’t have am element"
    #printr(f"┏{"━" * 78}┓")
    line2 = f"{mp} {atk} {sp_atk}"
    line3 = f"{hp} {def_} {sp_def}"
    line4 = f"{crit_chance} {crit_bounus} {item_price}"
    printr(
        com.put_in_box(f"""{titel}
{line2}
{line3}
{line4}
{ele}
{com.put_in_box(flavor_text,"round",75)}""","thick",max_width = 78),
        strip=True,
    )


def show_stats(self) -> None:
    mode = 0
    while True:
        clear()
        com.print_titelbar("Stets", 28)
        stet_text = f"{get_color_code('green')}S = Stets{get_color_code('none')}" if mode == 0 else "S = Stets"
        ele_text = f"{get_color_code('green')}E = Elements{get_color_code('none')}" if mode == 1 else "E = Elements"
        wap_text = f"{get_color_code('green')}W = Wapons{get_color_code('none')}" if mode == 2 else "W = Wapons"
        printr(f"{stet_text} | {ele_text} | {wap_text}")
        printr('')
        if mode == 0:
            printr(f"""Level {self.level}
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
""")
        elif mode == 1:
            print_afi(self.ele_afi)
        elif mode == 2:
            print_afi(self.wapon_afi)
        
        choice = inputT("\nPress Enter to return...")
        if choice == 'LEFT':
            mode = (mode - 1) % 3
        elif choice == 'RIGHT':
            mode = (mode + 1) % 3
        elif choice == "S":
            mode = 0
        elif choice == "E":
            mode = 1
        elif choice == "W":
            mode = 2
        elif choice == 'ENTER' or choice == 'Q' or choice == 'T':
            return
        


def show_stats_level(self):
    clear()
    #print_titelbar("Level Up", 28)
    printr(f"Level {self.level} => {self.level + 1}")
    printr(f"XP {self.xp}/{self.max_xp} => {self.xp - self.max_xp}/{self.next_level_xp(self.level+1)}")
    struc = {"1" :f"Max HP {self.max_hp}+3 => {self.max_hp + 3}",
    "2":f"Max MP {self.max_mp}+3 => {self.max_mp + 3}",
    "3":f"ATK {self.atk}+1 => {self.atk + 1}",
    "4":f"SP ATK {self.sp_atk}+1 => {self.sp_atk + 1}",
    "5":f"DEF {self.def_}+1 => {self.def_ + 1}",
    "6":f"SP DEF {self.sp_def}+1 => {self.sp_def + 1}",
    "7":f"Crit Chance {self.crit_chance}+1 => {self.crit_chance + 1}",
    "8":f"Crit Bounus {self.crit_bonus}+2 => {self.crit_bonus + 2}",
    "9":f"Move {self.min_move}-{self.max_move}",
    }
    other = f"Level {self.level} => {self.level + 1}\nXP {self.xp}/{self.max_xp} => {self.xp - self.max_xp}/{self.next_level_xp(self.level+1)}\nSelect stat to level up\n"
    choice,_ = com.select_menu_page(title="Level Up",structure=struc,other = other)
    return choice
    #printr(f"""Level {self.level} => {self.level + 1}
#XP {self.xp}/{self.max_xp} => {self.xp - self.max_xp}/{self.next_level_xp(self.level + 1)}
#[1]Max HP {self.max_hp}+3 => {self.max_hp + 3}
#[2]Max MP {self.max_mp}+3 => {self.max_mp + 3}
#[3]ATK {self.atk}+1 => {self.atk + 1}
#[4]SP ATK {self.sp_atk}+1 => {self.sp_atk + 1}
#[5]DEF {self.def_}+1 => {self.def_ + 1}
#[6]SP DEF {self.sp_def}+1 => {self.sp_def + 1}
#[7]Crit Chance {self.crit_chance}+1 => {self.crit_chance + 1}
#[8]Crit Bounus {self.crit_bonus}+2 => {self.crit_bonus + 2}
#[9]Move {self.min_move}-{self.max_move}
#============================
#Select stat to level up""")


def fight_art(player, enemy):
    art = GTD.fight_art
    player_art = art["player"]
    enemy_art = art[enemy.mob]
    for i in range(len(player_art)):
        temp = "      "
        temp += player_art[i]
        while len(temp) < 40:
            temp += " "
        temp += enemy_art[i]
        printr(temp)
    


def print_bars_player(self) -> None:
    bars = ""
    if self.hp < 0:
        self.hp = 0
    if self.mp < 0:
        self.mp = 0
    line_1 = f"HP{self.hp}/{self.max_hp + self.max_hp_items}"
    helf_bar_len = 57 - len(line_1)
    helf_left = int(helf_bar_len * (self.hp / (self.max_hp + self.max_hp_items)))
    helf_bar = "["
    for _ in range(helf_left):
        helf_bar += "#"
    for _ in range(helf_bar_len - helf_left):
        helf_bar += " "
    helf_bar += "]"
    line_2 = f"MP{self.mp}/{self.max_mp + self.max_mp_items}"
    mp_bar_len = 57 - len(line_2)
    mp_left = int(mp_bar_len * (self.mp / (self.max_mp + self.max_mp_items)))
    mp_bar = "["
    for _ in range(mp_left):
        mp_bar += "#"
    for _ in range(mp_bar_len - mp_left):
        mp_bar += " "
    mp_bar += "]"
    # bars = line_1 + helf_bar + ' ' + line_2 + mp_bar
    printr("===========================================================")
    printr(f"{line_1}\033[31m{helf_bar}\033[0m")
    printr(f"{line_2}\033[34m{mp_bar}\033[0m")
    printr("===========================================================")


def show_attack(self):
    def get_attack_stats_for_display(self, attack, i,num):
        temp_render = com.BoxPreRender()
        temp_render.num = num-1
        temp_render.numj = 6
        line_1 = com.fixed_width(
            f"{i} {attack['max_use'] - self.attacks_used[i]}/{attack['max_use']}", 18
        )
        line_2 = com.fixed_width(
            f"MP {attack['mp']} ATK {attack['atk']} SP ATK {attack['sp_atk']}", 25
        )
        line_3 = com.fixed_width(
            f"Adv {attack['adv']} Crit {attack['crit_chance']}% Crit {attack['crit_bonus']}",
            25,
        )
        temp_render.num_line = line_1
        temp_render.texts.append(line_2)
        temp_render.texts.append(line_3)
        temp_render.width = 25
        return temp_render

    temp_num = 0
    atk_render = []
    for j in self.attacks_used:
        attack = self.attacks[temp_num]["stats"]
        temp_num += 1
        atk_render.append(get_attack_stats_for_display(self, attack, j,temp_num))
    return atk_render


def print_fight_stats_enemy(self) -> None:
    if self.hp < 0:
        self.hp = 0
    if self.mp < 0:
        self.mp = 0
    line_1 = f"{self.mob} Lvl. {self.level}"
    while len(line_1) < 25:
        line_1 += " "
    line_2 = f"{self.hp}/{self.max_hp + self.max_hp_items }"
    helf_bar_len = 23 - len(line_2)
    helf_left = int(helf_bar_len * (self.hp / (self.max_hp + self.max_hp_items)))
    helf_bar = "["
    for _ in range(helf_left):
        helf_bar += "#"
    for _ in range(helf_bar_len - helf_left):
        helf_bar += " "
    helf_bar += "]"
    line_2 += f"\033[31m{helf_bar}\033[0m"

    printr(f"""
                         ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
                         ┃ {line_1} ┃
                         ┃ {line_2} ┃
                         ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━┛""")


def print_fight_UI(player, enemy):
    clear()
    com.print_titelbar("FIGHT", 59)
    #printr("Number to select attack")
    #printr("===========================================================")
    print_fight_stats_enemy(enemy)
    fight_art(player, enemy)
    print_bars_player(player)
        


def fight_selact_attack(player, enemy,curser = [0,0,0,0]):
    while True:
        clear()
        com.print_titelbar("FIGHT", 59)
        print_fight_stats_enemy(enemy)
        fight_art(player, enemy)
        print_bars_player(player)
        atk_render = show_attack(player)
        
        sel, box_shape = com.box_menu(atk_render,curser,[2,2])
        

        # printr(ceil(len(item_render) / 2) - 1)
        #render_item_boxes(item_render, offset, sel)
        choice = inputT("> ", True)
        if choice not in ["UP", "DOWN", "LEFT", "RIGHT", "ENTER"]:
            return choice, curser
        else:
            if choice == "ENTER":
                if sel != None:
                    #printr(sel)
                    return sel + 1, curser
            elif choice == "UP":
                curser[2] = curser[0]
                curser[3] = curser[1]
                curser[0] -= 1
            elif choice == "DOWN":
                curser[2] = curser[0]
                curser[3] = curser[1]
                curser[0] += 1
            elif curser[0] > 1:
                curser[0] = 1
            elif choice == "LEFT":
                curser[2] = curser[0]
                curser[3] = curser[1]
                curser[1] -= 1
            elif choice == "RIGHT":
                curser[2] = curser[0]
                curser[3] = curser[1]
                curser[1] += 1
            
            choice, curser = com.menu_handler(curser,box_menu_shape=box_shape,page=0,max_page=0)
            if choice:
                return choice, curser

def print_atk_damage(sel,atk,sp_atk,deff,sp_deff,crit,damage,who=True):
    if crit:
        printr("CRIT","red")
    if who:
        a = "you"
        d = "the enemy"
    else:
        a = "the enemy"
        d = "you"
    printr(f"{a} used {sel} to deal {get_color_code("red")}{damage}{get_color_code("none")} damage to {d}")
    printr(f"the attack had a normal attack power of {get_color_code("red")}{atk}{get_color_code("none")} and a special attack power of {get_color_code("red")}{sp_atk}{get_color_code("none")}")
    printr(f"{d} had a deffens of {get_color_code("blue")}{deff}{get_color_code("none")} and a special deffens of {get_color_code("blue")}{sp_deff}{get_color_code("none")}")
    
    

def fight_roll_dice(
    player, enemy, start: int, end: int, advan=0, advan_e=0, is_deff=False
) -> tuple[int,int]:
    rand = 0
    rand_e = 0
    rand_str = com.center_text(str(rand), 3)
    rand_str_e = com.center_text(str(rand_e), 3)
    if is_deff:
        l1 = com.center_text("Player Deffes", 28)
        l2 = com.center_text("Enemy Attack", 28)
    else:
        l1 = com.center_text("Player Attack", 28)
        l2 = com.center_text("Enemy Deffes", 28)
    
    dice_rool_f = lambda:f"""{com.center_text(f"{l1}┃{l2}", 59)}
{com.center_text("╭━━━━━━━╮", 29)}┃{com.center_text("╭━━━━━━━╮", 29)}
{com.center_text("┃       ┃", 29)}┃{com.center_text("┃       ┃", 29)}
{com.center_text(f"┃  {rand_str}  ┃", 29)}┃{com.center_text(f"┃  {rand_str_e}  ┃", 29)}
{com.center_text("┃       ┃", 29)}┃{com.center_text("┃       ┃", 29)}
{com.center_text("╰━━━━━━━╯", 29)}┃{com.center_text("╰━━━━━━━╯", 29)}
{com.center_text("┃", 59)}"""
    printr(dice_rool_f)
    for i in range(10):
        rand = 0
        rand_e = 0
        rand_o = rand
        while rand == rand_o:
            rand = random.randint(start, end)
        rand += advan
        if rand < start:
            rand = start
        elif rand > end:
            rand: int = end
        advan_e = 0
        rand_e = random.randint(start, end)
        rand_e += advan_e
        if rand_e < start:
            rand_e = start
        elif rand_e > end:
            rand_e: int = end
        rand_str = com.center_text(str(rand), 3)
        rand_str_e = com.center_text(str(rand_e), 3)
        
        wait((i + 1) / 50)
    return rand, rand_e


def print_room(
    player: tuple[int, int], room, enemys, traps, cheasts, merchents
) -> None:
    #printr(room.type)
    printr(f"{com.center_text(f' {room.type} ',(room.width + 4)*2 + len(room.type), '═')}")
    printr('')

    room_map: list[list[str]] = deepcopy(room.map)
    for t in traps:
        if t.show:
            room_map[t.y][t.x] = TRAP
    for c in cheasts:
        room_map[c.y][c.x] = CHEAST
    for m in merchents:
        room_map[m.y][m.x] = MERCHENT
    for e in enemys:
        if not e.is_del:
            room_map[e.y][e.x] = BOSS if e.is_boss else ENEMY
    room_map[player[1]][player[0]] = PLAYER

    for row in room_map:
        line: str = ""
        for i in row:
            tile: str = WALL if i == "#" else i
            line += tile + " "
        printr(line)



def shop_hader(page, max_page, gold, curser=[0, 0, 0, 0]):
    com.print_titelbar(f"Shop Page {page + 1} / {max_page + 1}", 78)
    printr(f"Gold {gold}")
    ops = {
        "Q": "Close",
        "N": "Next",
        "P": "Previous",
        "H": "Help",
        "E": "Buy",
        "PAGE": "Go to Page",
    }
    printr("")
    out,shape = com.header_options(ops, curser, 45, True)
    # printr(f""" Q = Close | N = Next | P = Previous | H = Help
    # E = Buy |  PAGE = Go to Page | Number = Select Item""")
    printr(com.center_text("", 78, "="))
    return out, shape


def shop_buy_page(
    page: int,
    per_page: int,
    max_page: int,
    is_item_selected: bool,
    item_fillter,
    selected_item,
    gold,
    curser=[0, 0,0,0],
    size=[2,4]
):
    while True:
        clear()
        out,header_shape = shop_hader(page, max_page, gold, curser)
        if is_item_selected:
            render_item_details(selected_item)

        start = page * per_page
        end = start + per_page
        items = item_fillter[start:end]
        offset = page * per_page
        item_render = build_item_render(items, True,selected_item,offset)
        
        if curser[0] > -1:
            sel = (curser[0] * 2 + curser[1]) 
        else:
            sel = None

        sel, box_shape = com.box_menu(item_render,curser,size)

        choice = inputT("> ", True)
        if choice not in ["UP", "DOWN", "LEFT", "RIGHT", "ENTER"]:
            return choice, curser
        else:
            if choice == "ENTER":
                if sel != None:
                    printr(sel + 1 + offset)
                    return sel + 1 + offset, curser
                elif out:
                    return out, curser
            elif choice == "UP":
                curser[2] = curser[0]
                curser[3] = curser[1]
                curser[0] -= 1
            elif choice == "DOWN":
                curser[2] = curser[0]
                curser[3] = curser[1]
                curser[0] += 1
            elif choice == "LEFT":
                curser[2] = curser[0]
                curser[3] = curser[1]
                curser[1] -= 1
            elif choice == "RIGHT":
                curser[2] = curser[0]
                curser[3] = curser[1]
                curser[1] += 1
                
            choice, curser = com.menu_handler(curser,box_shape,header_shape,page,max_page)
            if choice:
                return choice, curser
#            if curser[0] >= 0:
#                if curser[1] < 0:
#                    if page > 0:
#                        curser[1] = 1
#                        return "P", curser
#                    else:
#                        curser[1] = 0
#                elif curser[1] > 1:
#                    if page < max_page:
#                        curser[1] = 0
#                        return "N", curser
#                    else:
#                        curser[1] = 1
#                elif curser[0] > ceil(len(item_render) / 2) - 1:
#                    curser[0] = ceil(len(item_render) / 2) - 1



def game_menu(player,dungeon,game_state,curser=[0,0,0,0],is_enemy_turn=False) -> tuple[str,list[int]]:
    hp: str = f"HP {player.hp}/{player.max_hp + player.max_hp_items}"
    mp: str = f"MP {player.mp}/{player.max_mp + player.max_mp_items}"
    gold: str = f"Gold {player.gold}"
    xp: str = f"XP {player.xp}/{player.max_xp}"
    level: str = f"Level {player.level}"
    hp = com.center_text(hp, 13)
    mp = com.center_text(mp, 13)
    gold = com.center_text(gold, 13)
    xp = com.center_text(xp, 13)
    level = com.center_text(level, 13)
    while True:
        clear()
        #printr(curser)
        com.print_titelbar("Dice Dungeon", 40)
        ops = {
            'H':'Help',
            #'Q':'Quit Game',
            'Q':'Quit',
            #'T':'Show Stets',
            'T':'Stets',
            #'I':'Open Inventory',
            'I':'Inventory',
            #'M':'Open Map'
            'M':'Map'
        }
        if player.moves == -2:
            ops['R'] = 'Roll dice to move'
            ops['P'] = 'Make a pause and rest'
            if player.cls == "Roghe":
                ops['F'] = 'Roll to check for traps'
        printr(com.put_in_box(f"{hp}  {mp}  {gold}\n{level}  {xp}"),strip=True,)
        out, shape = com.header_options(ops,curser)
        if game_state == "map":
            room = dungeon.rooms[dungeon.room]
            enemys = room.enemys
            traps = room.traps
            cheasts = room.cheasts
            merchents = room.shops
            player_pos: tuple[int, int] = (player.x, player.y)
            printr('')
            #printr(f"{com.center_text('',(room.width + 4)*2, '═')}")
            print_room(player_pos, room, enemys, traps, cheasts, merchents)
            
        print_room_options(player)
        
        if is_enemy_turn:
            return
        
        choice = inputT("perss any unbount key to start enemy turn" if player.moves == -1 else "> ")
        if choice not in ["UP", "DOWN", "LEFT", "RIGHT", "ENTER"]:
            return choice, curser
        else:
            if choice == "ENTER":
                return out, curser
            elif choice == "UP":
                curser[3] = curser[1]
                curser[2] = curser[0]
                curser[0] -= 1
            elif choice == "DOWN":
                curser[3] = curser[1]
                curser[2] = curser[0]
                curser[0] += 1
            elif choice == "LEFT":
                curser[2] = curser[0]
                curser[3] = curser[1]
                curser[1] -= 1
            elif choice == "RIGHT":
                curser[2] = curser[0]
                curser[3] = curser[1]
                curser[1] += 1
                
            choice, curser = com.menu_handler(curser,header_menu_shape=shape)
            if choice:
                return choice, curser

def print_dungeon_map(dungeon, spacing=1, room_size=2, CHEATS_ON=False):
    # 1. BFS: relative Positionen bestimmen
    rooms = dungeon.rooms
    #printr(rooms)
    if len(str(rooms[len(rooms) - 1].id)) > room_size:
        room_size = len(str(rooms[len(rooms) - 1].id))
    clear()
    positions = [room.pos for room in dungeon.rooms.values()]

    # printr('conn:',conn,' px,py:',px,py,' w,h:',w,h,' dx,dy:',dx,dy)

    # 2. Grid vorbereiten
    xs = [p[0] for p in positions]
    ys = [p[1] for p in positions]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)

    width = (maxx - minx + 1) * (room_size + (spacing * 2)) - spacing
    if width % 2 == 1:
        width += 1
    height = (maxy - miny + 1) * (ceil(room_size/2) + spacing) - spacing

    grid = [[" " for _ in range(width)] for _ in range(height)]

    # 3. Räume zeichnen
    room_coords = {}
    for room in dungeon.rooms.values():
        # if room.show_on_map == False:
        # continue
        gx, gy = room.pos
        gx = (gx - minx) * (room_size + (spacing * 2))
        gy = (gy - miny) * (ceil(room_size/2) + spacing)

        rid_str = str(room.id)
        if room.show_on_map or CHEATS_ON:
            color = 'None'
            if room.id == dungeon.room:
                color = get_color_code('green')
            elif room.type == "boss":
                color = get_color_code('red')
            elif room.type == "merchant":
                color = get_color_code('blue')
            else:
                color = ''
                
            if len(rid_str) < room_size:
                for i in range(room_size - len(rid_str)):
                    grid[gy][gx + len(rid_str) + i] = f"{color}#\33[0m"
            grid[gy][gx : gx + len(rid_str)] = [f"{color}{i}\33[0m" for i in rid_str]
            
            for i in range(ceil(room_size/2) - 1):
                for j in range(room_size):
                    grid[gy + 1 + i][gx + j] = f"{color}#\33[0m"
                        
        room_coords[room.id] = (gx, gy)

    # 4. Linien nur zwischen Räumen in Zwischenzellen
    # printr(rooms)
    for room in dungeon.rooms.values():
        if room.show_on_map == False and CHEATS_ON == False:
            continue
        gx, gy = room_coords[room.id]
        for i, conn in enumerate(room.doors):
            cgx, cgy = room_coords[conn]
            # Vertikal
            if gx == cgx:
                start = min(gy , cgy + ceil(room_size/2)) 
                end = max(gy + ceil(room_size/2), cgy  )
                for y_pos in range(start, end):
                    if grid[y_pos][gx] == " ":
                        grid[y_pos][gx] = "|"
            # Horizontal
            elif gy == cgy:
                start = min(gx, cgx + room_size)
                end = max(gx + room_size, cgx)
                for x_pos in range(start, end):
                    if grid[gy][x_pos] == " ":
                        grid[gy][x_pos] = "–"

    # 5. Ausgabe
    # clear()
    # printr(dungeon.room_pos)
    com.print_titelbar("Dungeon Map",width+6)
    
    out = ''
    for row in grid:
        if any(i != " " for i in row):
            temp = "".join(row)
            # print(temp)
            # printr(plen(temp))
            # printr(len(temp))
            out += temp + '\n'
            #printr(temp, strip=False)
    printr(out, strip=False)
    # for i in rooms:
    # printr('room:',i,'doors',rooms[i].doors)


def print_afi(afi):
    size = 15
    max_afi = afi.afi[afi.main_afi]
    #clear()
    #print_titelbar("Affiliations",30)
    max_char_len = max(len(i) for i in afi.afi)
    #printr(max_char_len)
    num = 0
    for i in afi.afi:
        if i in GTD.elementare:
            color = get_color_code(GTD.elementare[i]['color'])
        else:
            match num:
                case 0:
                   color = get_color_code('none')
                case 1:
                    color = get_color_code('white')    
                case 2:
                    color = get_color_code('black',['hi'])
                case _:
                    color = get_color_code('none')
            
        num = (num + 1) % 3
        hight_p = afi.afi[i] / max_afi
        temp_hight = int((size*8)*hight_p)
        line = ""
        for _ in range(temp_hight//8):
            line += "█"
            
        frac = temp_hight % 8
        #printr(f"{temp_hight,frac}")
        if frac == 7:
            line += chr(0x2589)
        elif frac == 6:
            line += chr(0x258A)
        elif frac == 5:
            line += chr(0x258B)
        elif frac == 4:
            line += chr(0x258C)
        elif frac == 3:
            line += chr(0x258D)
        elif frac == 2:
            line += chr(0x258E)
        elif frac == 1:
            line += chr(0x258F)
        name = com.fixed_width("",max_char_len-len(i)) + i
        line = com.fixed_width(f"{color}{line}\x1b[0m {afi.afi[i]}",25)
        printr(f"{name}:{line}")
    #inputT()

def print_room_options(player):
    #printr("======== Your turn =========")
    printr('')
    if player.moves == -2:
        printr(f"\n{com.center_text(' Your turn ',28, '═')}")
        #if player.cls == "Roghe":
        #    printr("R = Roll dice to move | F = Roll to check for traps")
        #printr("R = Roll dice to move | P = Make a pause and rest")
    elif player.moves > 0:
        printr(f"\n{com.center_text(' Your turn ',28, '═')}")
        printr(f"Moves {player.moves} left")
        printr('use WASD to move')
    else:
        printr(f"\n{com.center_text(' Enemy turn ',28, '═')}")
        player.moves = -1