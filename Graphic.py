import os
import random
from copy import deepcopy
from math import ceil

import Game_text_data as GTD

PLAYER = "P"
TRAP = "T"
CHEAST = "C"
WALL = "#"
BOSS = "B"
ENEMY = "E"
MERCHENT = "M"


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def fixed_width(text: str, width: int) -> str:
    if len(text) > width:
        return text[:width]
    return text + " " * (width - len(text))


def center_text(text: str, width: int, fill: str = " ") -> str:
    text = text.strip()
    while len(text) < width:
        if len(text) == width - 1:
            text = fill + text
        else:
            text = fill + text + fill
    return text


def wrap_text(text: str, width: int = 72, buffer: int = 4):
    words: list[str] = text.split()
    lines: list[str] = []
    current_line = " "

    for word in words:
        if len(current_line) + len(word) + 1 > width:
            lines.append(center_text(current_line.rstrip(), width + buffer))
            current_line = word + " "
        else:
            current_line += word + " "
    lines.append(center_text(current_line.rstrip(), width + buffer))
    return "\n".join(lines)


def print_titelbar(text: str, width: int = 16):
    sep = "=" * width
    text = center_text(text, width)
    print(sep)
    print(text)
    print(sep)


def show_inventory(
    page: int,
    per_page: int,
    max_page: int,
    is_item_selected: bool,
    item_fillter,
    selected_item,
    is_shop,
    gold,
):
    clear()
    render_inventory_header(page, max_page, is_shop, gold)
    if is_item_selected:
        render_item_details(selected_item)
    start = page * per_page
    end = start + per_page
    items = item_fillter[start:end]
    offset = page * per_page

    item_render = build_item_render(items)

    render_item_boxes(item_render, offset)


def render_inventory_header(page, max_page, is_shop, gold) -> None:
    if is_shop:
        print_titelbar(f"Shop Page {page + 1} / {max_page + 1}", 78)
        print(center_text(f"Gold {gold}", 78))
        print(center_text("", 78, "-"))
    else:
        print_titelbar(f"Inventory Page {page + 1} / {max_page + 1}", 78)
    print(f""" Q = Close | N = Next | P = Previous | H = Help
 E = {"Sell" if is_shop else "Equip"} | F = Favorite | SF = Show Favorites
 PAGE = Go to Page | Number = Select Item | SE = Show Equipped
==============================================================================""")


def render_item_boxes(item_render, offset) -> None:
    offset += 1

    def print_render(j: int, line: int) -> str:
        # prints a blank if there is no item in that slot
        if j >= len(item_render):
            return fixed_width(" ", 34)
        else:
            return item_render[j][line]

    for i in range(ceil(len(item_render) / 2)):
        num1 = f"[{i * 2 + offset}]".ljust(6)
        num2 = f"[{i * 2 + 1 + offset}]".ljust(6)

        print(f""" ––––––––––––––––––––––––––––––––––––    ––––––––––––––––––––––––––––––––––––
| {num1}                             |  | {num2}                             |
| {print_render(i * 2, 0)} |  | {print_render(i * 2 + 1, 0)} |
| {print_render(i * 2, 1)} |  | {print_render(i * 2 + 1, 1)} |
 ––––––––––––––––––––––––––––––––––––    –––––––––––––––––––––––––––––––––––– """)


def build_item_render(items):
    item_render = []
    for item in items:
        line1 = f"{item.grade} {item.item_type} (Lvl {item.level})"
        line2 = f"{item.name} {'*' if item.is_equiped else ''}"

        # Grafik an Graphics delegieren
        line1 = fixed_width(line1, 34)
        line2 = fixed_width(line2, 34)

        item_render.append([line1, line2])

    return item_render


def render_item_details(selected_item) -> None:
    titel = f"Level {selected_item.level}/{selected_item.max_level} {selected_item.grade} {selected_item.item_type}: {selected_item.name} {'*' if selected_item.is_equiped else ''}"
    titel = center_text(titel, 78)
    stats = selected_item.get_stats()
    hp = fixed_width(f"HP {stats['max hp']}", 26)
    mp = fixed_width(f"MP {stats['max mp']}", 26)
    atk = fixed_width(f"ATK {stats['atk']}", 26)
    sp_atk = fixed_width(f"SP ATK {stats['sp atk']}", 26)
    def_ = fixed_width(f"DEF {stats['def']}", 26)
    sp_def = fixed_width(f"SP DEF {stats['sp def']}", 26)
    crit_chance = fixed_width(f"Crit Chance {stats['crit chance']}", 26)
    crit_bounus = fixed_width(f"Crit Bonus {stats['crit bonus']}", 26)
    item_price = fixed_width(f"Price {stats['price']}", 26)
    flavor_text = wrap_text(selected_item.flavor, 73)

    print(f""" {titel}
  {mp} {atk} {sp_atk}
  {hp} {def_} {sp_def}
  {crit_chance} {crit_bounus} {item_price}
{center_text("", 78, "-")}
                                  Flavor text
{flavor_text}
==============================================================================""")


def show_stats(self) -> None:
    clear()
    print_titelbar("Stets", 28)
    print(f"""Level {self.level}
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
""")
    _ = input("\nPress Enter to return...")


def show_stats_level(self) -> None:
    clear()
    print_titelbar("Level Up", 28)
    print(f"""Level {self.level} => {self.level + 1}
XP {self.xp}/{self.max_xp} => {self.xp - self.max_xp}/{self.next_level_xp(self.level + 1)}
[1]Max HP {self.max_hp}+3 => {self.max_hp + 3}
[2]Max MP {self.max_mp}+3 => {self.max_mp + 3}
[3]ATK {self.atk}+1 => {self.atk + 1}
[4]SP ATK {self.sp_atk}+1 => {self.sp_atk + 1}
[5]DEF {self.def_}+1 => {self.def_ + 1}
[6]SP DEF {self.sp_def}+1 => {self.sp_def + 1}
[7]Crit Chance {self.crit_chance}+1 => {self.crit_chance + 1}
[8]Crit Bounus {self.crit_bonus}+2 => {self.crit_bonus + 2}
[9]Move {self.min_move}-{self.max_move}
============================
Select stat to level up""")


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
        print(temp)


def show_fight_stats_player(self, show_atk: bool) -> None:
    print_bars_player(self)
    print(center_text("", 59, "="))
    if show_atk:
        show_attack(self)
        print(center_text("", 59, "="))


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
    print(f"""===========================================================
{line_1}\033[31m{helf_bar}\033[0m
{line_2}\033[34m{mp_bar}\033[0m""")


def show_attack(self) -> None:
    def get_attack_stats_for_display(self, attack, i):
        line_1 = fixed_width(
            f"{i} {attack['max_use'] - self.attacks_used[i]}/{attack['max_use']}", 21
        )
        line_2 = fixed_width(
            f"MP {attack['mp']} ATK {attack['atk']} SP ATK {attack['sp_atk']}", 25
        )
        line_3 = fixed_width(
            f"Adv {attack['adv']} Crit {attack['crit_chance']}% Crit {attack['crit_bonus']}",
            25,
        )
        return [line_1, line_2, line_3]

    asfd = []  # asfd stands for attack_stats_for_display
    temp_num = 0
    for j in self.attacks_used:
        attack = self.attacks[temp_num]["stats"]
        temp_num += 1
        asfd.append(get_attack_stats_for_display(self, attack, j))
    del temp_num
    print(f"""
 –––––––––––––––––––––––––––   –––––––––––––––––––––––––––
| [0] {asfd[0][0]} | | [1] {asfd[1][0]} |
| {asfd[0][1]} | | {asfd[1][1]} |
| {asfd[0][2]} | | {asfd[1][2]} |
 –––––––––––––––––––––––––––   –––––––––––––––––––––––––––
 –––––––––––––––––––––––––––   –––––––––––––––––––––––––––
| [2] {asfd[2][0]} | | [3] {asfd[3][0]} |
| {asfd[2][1]} | | {asfd[3][1]}
| {asfd[2][2]} | | {asfd[3][2]} |
 –––––––––––––––––––––––––––   ––––––––––––––––––––––––––– """)


def print_fight_stats_enemy(self) -> None:
    if self.hp < 0:
        self.hp = 0
    if self.mp < 0:
        self.mp = 0
    line_1 = f"{self.mob} Lvl. {self.level}"
    while len(line_1) < 25:
        line_1 += " "
    line_2 = f"{self.hp}/{self.max_hp}"
    helf_bar_len = 23 - len(line_2)
    helf_left = int(helf_bar_len * (self.hp / self.max_hp))
    helf_bar = "["
    for _ in range(helf_left):
        helf_bar += "#"
    for _ in range(helf_bar_len - helf_left):
        helf_bar += " "
    helf_bar += "]"
    line_2 += f"\033[31m{helf_bar}\033[0m"

    print(f"""
                          –––––––––––––––––––––––––––
                         | {line_1} |
                         | {line_2} |
                          ––––––––––––––––––––––––––– """)


def print_fight_UI(player, enemy, show_atk=True):
    print_titelbar("FIGHT", 59)
    print("Number to select attack")
    print("===========================================================")
    print_fight_stats_enemy(enemy)
    fight_art(player, enemy)
    show_fight_stats_player(player, show_atk)


def fight_roll_dice(
    player, enemy, start: int, end: int, advan=0, advan_e=0, atk=True, is_deff=False
) -> int:
    rand = 0
    rand_o = rand
    while rand == rand_o:
        rand = random.randint(start, end)
    rand += advan
    if rand < start:
        rand: int = start
    elif rand > end:
        rand: int = end
    advan_e = 0
    rand_e: int = random.randint(start, end)
    rand_e += advan_e
    if rand_e < start:
        rand_e: int = start
    elif rand_e > end:
        rand_e: int = end
    rand_str = center_text(str(rand), 3)
    rand_str_e = center_text(str(rand_e), 3)
    if is_deff:
        l1 = center_text("Player Deffes", 28)
        l2 = center_text("Enemy Attack", 28)
    else:
        l1 = center_text("Player Attack", 28)
        l2 = center_text("Enemy Deffes", 28)
    print(f"""{center_text(f"{l1}|{l2}", 59)}
{center_text("-------", 29)}|{center_text("-------", 29)}
{center_text("|       |", 29)}|{center_text("|       |", 29)}
{center_text(f"|  {rand_str}  |", 29)}|{center_text(f"|  {rand_str_e}  |", 29)}
{center_text("|       |", 29)}|{center_text("|       |", 29)}
{center_text("-------", 29)}|{center_text("-------", 29)}
{center_text("|", 59)}
===========================================================
""")
    return rand, rand_e


def print_room(
    player: tuple[int, int], room, enemys, traps, cheasts, merchents
) -> None:
    print(room.type)

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
        print(line)


def shop_start_page():
    clear()
    print_titelbar("Merchent", 16)
    print("[1] Buy Items")
    print("[2] Sell Items")
    print("[3] Leave")


def shop_hader(page, max_page, gold):
    print_titelbar(f"Shop Page {page + 1} / {max_page + 1}", 78)
    print(center_text(f"Gold {gold}", 78))
    print(center_text("", 78, "-"))
    print(f""" Q = Close | N = Next | P = Previous | H = Help
 E = Buy |  PAGE = Go to Page | Number = Select Item""")
    print(center_text("", 78, "="))


def shop_buy_page(
    page: int,
    per_page: int,
    max_page: int,
    is_item_selected: bool,
    item_fillter,
    selected_item,
    gold,
):
    clear()
    shop_hader(page, max_page, gold)
    if is_item_selected:
        render_item_details(selected_item)

    start = page * per_page
    end = start + per_page
    items = item_fillter[start:end]
    offset = page * per_page
    item_render = build_item_render(items)
    render_item_boxes(item_render, offset)
