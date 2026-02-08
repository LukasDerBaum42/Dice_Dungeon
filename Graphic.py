import os
import random
import re
import select
import shutil
import sys
import time
from copy import deepcopy
from math import ceil
from types import LambdaType

import Game_text_data as GTD

FPS = 60
os.system("cls" if os.name == "nt" else "clear")
hex_codes = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
]
PLAYER = "P"
TRAP = "T"
CHEAST = "C"
WALL = "#"
BOSS = "B"
ENEMY = "E"
MERCHENT = "M"
WIDTH, HEIGHT = shutil.get_terminal_size(fallback=(80, 30))


def get_size():
    global WIDTH, HEIGHT, FRAME_BUFER
    WIDTH, HEIGHT = shutil.get_terminal_size(fallback=(80, 30))
    while WIDTH < 80 or HEIGHT < 30:#
        WIDTH, HEIGHT = shutil.get_terminal_size(fallback=(80, 30))
        os.system("cls" if os.name == "nt" else "clear")
        FRAME_BUFER = []
        print("WINDOW TO SMALL")
        color = "red" if HEIGHT < 30 else "green"
        print(f"{get_color_code(color)}min height is 30 curent is {HEIGHT}{get_color_code("none")}")
        color = "red" if WIDTH < 80 else "green"
        print(f"{get_color_code(color)}min width is 80 curent is {WIDTH}{get_color_code("none")}")
        time.sleep(0.1)



ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-9;]*m")


def plen(s: str) -> int:
    clean = ANSI_ESCAPE_RE.sub("", s)
    return len(clean)


class TerminalInputUNIX:
    def __init__(self):
        self.fd = sys.stdin.fileno()
        self.old = termios.tcgetattr(self.fd)
        tty.setcbreak(self.fd)
        self.buf = ""

    def poll(self):
        global PRINT_BUFFER
        events = []

        while select.select([sys.stdin], [], [], 0)[0]:
            self.buf += sys.stdin.read(1)
            

        while self.buf:
            while select.select([sys.stdin], [], [], 0)[0]:
                self.buf += sys.stdin.read(1)
            
            
            if self.buf.startswith("\x1b"):
                self.buf += sys.stdin.read(1)
                self.buf += sys.stdin.read(1)
                code = self.buf[2]
                self.buf = self.buf[3:]
                events.append(
                    {"A": "UP", "B": "DOWN", "C": "RIGHT", "D": "LEFT"}.get(code, None)
                )
                continue
            elif self.buf.startswith("\n"):
                self.buf = self.buf[1:]
                events.append("ENTER")
                continue
            elif self.buf.startswith("\x7f"):
                self.buf = self.buf[1:]
                events.append("BACKSPACE")
                continue
            else:
                events.append(self.buf[0])
                self.buf = self.buf[1:]
                
        update(False)
        return [e for e in events if e]
        


class TerminalInputWIN:
    def __init__(self):
        self.buf = ""

    def poll(self):
        events = []

        # drain keyboard buffer (non-blocking)
        while msvcrt.kbhit():
            ch = msvcrt.getwch()

            # special key prefix
            if ch in ("\x00", "\xe0"):
                key = msvcrt.getwch()
                events.append({
                    "H": "UP",
                    "P": "DOWN",
                    "K": "LEFT",
                    "M": "RIGHT",
                }.get(key))
                continue

            if ch == "\r":
                events.append("ENTER")
            elif ch == "\b":
                events.append("BACKSPACE")
            else:
                events.append(ch)

        update(False)
        return [e for e in events if e]


    def close(self):
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old)


if os.name == "nt":
    import msvcrt
    input_lol = TerminalInputWIN()
else:
    import termios
    import tty
    input_lol = TerminalInputUNIX()


def inputT(text="", wait_for_enter: bool = False, num_only: bool = False):
    global PRINT_BUFFER
    printr("")
    if wait_for_enter:
        out = ""
        while True:
            buffer = " " * (len(f"Enter to confirm {text}") - len(out))
            #printr(f"Enter to confirm {text}{out}{buffer}", end="", start="\r")
            PRINT_BUFFER[-1] = []
            PRINT_BUFFER[-1].append("")
            PRINT_BUFFER[-1].append(lambda: f"Enter to confirm {text}{out}{get_color_code(bonus=["bg"]) if int(time.time() * 2) % 2 else ""} {get_color_code("none")}{buffer}")

            
            while True:
                keys = input_lol.poll()
                if keys:
                    #printr(keys)
                    key = keys[-1]
                    #printr(key)
                    update()
                    #time.sleep(1)
                    # print(keys)
                    break
                #time.sleep(0.005)
            # printr(out)
            # printr(key)
            if key == "ENTER" or key == " ":
                # printr("lol")
                if len(out) == 0 and key == "ENTER":
                    return "ENTER"
                elif not num_only:
                    if key == "ENTER":
                        return out
                    else:
                        out += " "
                elif num_only:
                    return out
            elif key == "BACKSPACE":
                out = out[: len(out) - 1]
            else:
                if num_only:
                    try:
                        int(key)
                        out += key.upper().strip()
                    except:
                        return key.upper().strip()
                else:
                    if key.upper().strip() in ["UP", "DOWN", "LEFT", "RIGHT"]:
                        return key.upper().strip()
                    else:
                        out += key.upper().strip()
                        
            update()
    else:
        printr(text)
        while True:
            keys = input_lol.poll()
            if keys:
                #printr(keys)
                key = keys[-1]
                #printr(key)
                update()
                #time.sleep(1)
                break
            #time.sleep(0.005)  # ← IMPORTANT
        # printr(keys)
        # printr(str(keys[0].upper().strip()))
        update()
        return key.upper().strip()


def clear():
    global PRINT_BUFFER, FRAME_BUFER
    update()
    PRINT_BUFFER = []
    #os.system("cls" if os.name == "nt" else "clear")
    #FRAME_BUFER = []
    get_size()
    
    


def update(prio = True):
    get_size()
    print_replace(PRINT_BUFFER,prio)


FRAMR_RATE = [time.time()]

def up_frame_rate():
    global FRAMR_RATE
    if len(FRAMR_RATE) > 10:
        _ = FRAMR_RATE.pop(0)
        
    FRAMR_RATE.append(time.time())
    
    if len(FRAMR_RATE) >= 2:
        temp = []
        for i in range(1,len(FRAMR_RATE)):
            fps = FRAMR_RATE[i] - FRAMR_RATE[i -1]
            if i == len(FRAMR_RATE)-1:
                ft = int(fps * 100000)
            fps = 1 / fps
            temp.append(fps)
        out = int(sum(temp)/ len(temp))
        return out, ft
    else:
        return 0 ,0

FRAME_BUFER = []

def print_replace(lines,prio = True):
    """
    Prints a list of strings and replaces them in-place
    on subsequent calls.
    """
    global FRAME_BUFER
    if 1 // (time.time() - FRAMR_RATE[-1]) > FPS and not prio:
        #time.sleep((time.time() - FRAMR_RATE[-1]) * ((1 / (time.time() - FRAMR_RATE[-1])) / (FPS + 10)))
        return

    #print(PRINT_BUFFER)
    out_1 = []
    for line_s in lines:
        out_2 = []
        if type(line_s) == LambdaType:
            text = line_s()
            if str(text).startswith("\n"):
                text = text[1:]
        
            lines_2 = str(text).split("\n")
            out = []
            
            for line in lines_2:
                out.append(line)
            
            for line in out:
                if type(line) == LambdaType:
                    line = line()
                    #pass
                out_2.append(center_text(str(line), WIDTH))
        
        else:    
            for line in line_s:
                if type(line) == LambdaType:
                    line = line()
                    #pass
                out_2.append(center_text(str(line), WIDTH))

        out_1 += out_2

    # Clear from cursor to end of screen

    fps = str(up_frame_rate())
    #print(out_1)
    sys.stdout.write("\033[Hfps " + fps + "\033[E")
    for i, line in enumerate(out_1):
        if i < len(FRAME_BUFER) and FRAME_BUFER[i] == line:
            sys.stdout.write("\033[E")
        else:
            # Clear line + write new content
            sys.stdout.write("\033[2K")  # clear line
            sys.stdout.write(line)
            sys.stdout.write("\033[E")
            if i >= len(FRAME_BUFER)-1:
                FRAME_BUFER.append(line)
                FRAME_BUFER[i] = line
            else:
                FRAME_BUFER[i] = line
    #sys.stdout.write(str(out_1))
    #sys.stdout.write(str(FRAME_BUFER))
    #FRAME_BUFER.append("")
    if len(FRAME_BUFER) > len(out_1):
        for _ in range(len(FRAME_BUFER) - len(out_1)):
            sys.stdout.write("\033[2K")
            sys.stdout.write("\033[E")
        FRAME_BUFER.pop(-1)

    sys.stdout.flush()

def fixed_width(text: str, width: int) -> str:
    if plen(text) > width:
        return text[:width]
    return text + " " * (width - plen(text))


def center_text(text: str, width: int, fill: str = " ", strip: bool = False) -> str:
    if strip:
        text = text.strip()
    while plen(text) < width:
        if plen(text) == width - 1:
            text = fill + text
        else:
            text = fill + text + fill
    return text


def get_color_code(color: str = "white",bonus:list = []):
    temp = True
    color_c = ""
    if color == "black":
        out = "30"
    elif color == "red":
        out = "31"
    elif color == "green":
        out = "32"
    elif color == "yellow":
        out = "33"
    elif color == "blue":
        out = "34"
    elif color == "purple":
        out = "35"
    elif color == "cyan":
        out = "36"
    elif color == "white":
        out = "37"
    elif color == "none":
        out = "0"
    elif color[0] == "#" and len(color) == 7:
        temp = False
        hex = color
        #print(hex)
        r = hex_codes.index(hex[1]) * 16 + hex_codes.index(hex[2])
        g = hex_codes.index(hex[3]) * 16 + hex_codes.index(hex[4])
        b = hex_codes.index(hex[5]) * 16 + hex_codes.index(hex[6])
        if "bg" in bonus:
            out = f"\033[48;2;{r};{g};{b}m"
        else:
            out = f"\033[38;2;{r};{g};{b}m"
    else:
        printr(f"INVALED COLOR {color} ", "red")
        return None
    if temp:
        if "bold" in bonus:
            color_c += "1;" 
        if "line" in bonus:
            color_c += "4;"
        
        if "bg" in bonus:
           out = str(int(out)+10)
        
        if "hi" in bonus:
           out = str(int(out)+60)
        out = f"\033[{color_c}{out}m"
    return out


PRINT_BUFFER = []

def printr(
    text,
    color: str | None = None,
    strip: bool = False,
    end: str = "\r\n",
    start: str = "",
    pos: int = 0,
):
    global PRINT_BUFFER
    # print(type(text))
    if type(text) == LambdaType:
        PRINT_BUFFER.append(text)
        return
    
    if type(text) == tuple:
        temp = ""
        for i in text:
            temp += str(i) + " "
        text = temp
    if color:
        color_code = get_color_code(color)
        if color_code:
            text = color_code + text + "\033[0m"
        else:
            text = text
    else:
        text = text
    # text = textwrap.dedent(text)

    if str(text).startswith("\n"):
        text = text[1:]

    lines = str(text).split("\n")
    out = []
    
    for line in lines:
        #out.append(center_text(line, WIDTH, strip=strip))
        out.append(line)

    if pos == 0:
        PRINT_BUFFER.append(out)
    else:
        pos -= 1 if pos > 0 else 0
        PRINT_BUFFER[pos] = out
    #fixed_text = start + ("\r\n".join(out)) + end
    #PRINT_BUFFER.append(fixed_text)
    #PRINT_BUFFER += out
    #sys.stdout.write(fixed_text)
    #sys.stdout.flush()


def wrap_text(text: str, width: int = 72, buffer: int = 4):
    out = []
    raw_lines = text.splitlines()
    for line in raw_lines:
        if plen(line) <=width + buffer:
            out.append(line)
        else:
            if not line.strip():
                out.append("")
                continue
            words: list[str] = line.split()
            lines: list[str] = []
            current_line = ""
        
            for word in words:
                if plen(current_line) + plen(word) + 1 > width:
                    lines.append(center_text(current_line.rstrip(), width + buffer))
                    current_line = word + " "
                else:
                    current_line += word + " "
            lines.append(center_text(current_line.rstrip(), width + buffer))
            out += lines
    return "\n".join(out)
    
def put_in_box(text = "", type = "thin", max_width = 80):
    corners = {
        "thin": ["─","│","┌","┐","└","┘"],
        "thick": ["━","┃","┏","┓","┗","┛"],
        "round": ["─","│","╭","╮","╰","╯"],
        "double": ["═","║","╔","╗","╚","╝"]
    }
    lines = text.splitlines()
    lines_len = [plen(i) for i in lines]
    width = max(lines_len)
    if width + 2 >= max_width:
        text = wrap_text(text,max_width-2,1)
        lines = text.splitlines()
        lines_len = [plen(i) for i in lines]
        width = max(lines_len)
    top_line = f"{corners[type][2]}{corners[type][0]*width}{corners[type][3]}"
    bottom_line = f"{corners[type][4]}{corners[type][0]*width}{corners[type][5]}"
    out_lines = []
    out_lines.append(top_line)
    for line in lines:
        out_lines.append(f"{corners[type][1]}{center_text(line,width)}{corners[type][1]}")
    out_lines.append(bottom_line)
    return "\n".join(out_lines)



def print_titelbar(text: str, width: int = WIDTH):
    if plen(text) > width:
        width = plen(text)
    sep = "═" * (width)
    # text = center_text(text, width)
    printr(f"╔{sep}╗")
    text = f"║{center_text(text,width)}║" 
    printr(text)
    printr(f"╚{sep}╝")
    

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
        if len(rand_str) == 1:
            rand_str = " " + rand_str
        if len(rand_str) == 2:
            rand_str = rand_str + " "
        clear()
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
        time.sleep((i + 1) / 50)
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
):
    while True:
        clear()
        out = render_inventory_header(page, max_page, is_shop, gold, curser)
        
        if is_item_selected:
            render_item_details(selected_item)
        start = page * per_page
        end = start + per_page
        items = item_fillter[start:end]
        offset = page * per_page

        item_render = build_item_render(items, is_shop,selected_item)
        
        if curser[0] >= 0:
            if curser[1] < 0:
                if page > 0:
                    curser[2] = curser[0]
                    curser[3] = curser[1]
                    curser[1] = 1
                    return "P", curser
                else:
                    curser[1] = 0
            elif curser[1] > 1:
                if page < max_page:
                    curser[2] = curser[0]
                    curser[3] = curser[1]
                    curser[1] = 0
                    return "N", curser
                else:
                    curser[1] = 1
            elif curser[0] > ceil(len(item_render) / 2) - 1:
                curser[0] = ceil(len(item_render) / 2) - 1

        if curser[0] > -1:
            sel = (curser[0] * 2 + curser[1]) 
        else:
            sel = None
        # printr(ceil(len(item_render) / 2) - 1)
        render_item_boxes(item_render, offset, sel)
        choice = inputT("> ", True)
        if choice not in ["UP", "DOWN", "LEFT", "RIGHT", "ENTER"]:
            return choice, curser
        else:
            if choice == "ENTER":
                if sel != None:
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
            


def render_inventory_header(page, max_page, is_shop, gold, curser) -> str | None:
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
        print_titelbar(f"Shop Page {page + 1} / {max_page + 1}", 78)
        printr(f"Gold {gold}")
        printr(center_text("", 78, "-"))
    else:
        print_titelbar(f"Inventory Page {page + 1} / {max_page + 1}", 78)
    # printr(f""" Q = Close | N = Next | P = Previous | H = Help
    # E = {"Sell" if is_shop else "Equip"} | F = Favorite | SF = Show Favorites
    # PAGE = Go to Page | Number = Select Item | SE = Show Equipped
    # ==============================================================================""")
    out = header_options(ops, curser, 50, True)
    return out


def render_item_boxes(item_render, offset, selected=-1) -> None:
    offset += 1

    def print_render(j: int, line: int) -> str | None:
        # prints a blank if there is no item in that slot
        if j >= len(item_render):
            if line == 3:
                return None
            elif line == 2:
                return fixed_width(" ", 22)
            return fixed_width(" ", 34)
        else:
            return item_render[j][line]

    def make_box(num, color):
        box = []
        num1 = f"[{num + offset}]".ljust(6)
        box.append("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        box.append(f"┃ {num1}      {print_render(num, 2)} ┃")
        box.append(f"┃ {print_render(num, 0)} ┃")
        box.append(f"┃ {print_render(num, 1)} ┃")
        box.append("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

        if color:
            # printr(color)
            for i in range(len(box)):
                box[i] = f"{color}{box[i]}{get_color_code("none")}"
        return box

    def box_to_render(render):
        for i in range(ceil(len(render) / 2)):
            out = ""
            for j in range(4):
                out += str(render[i * 2][j] + "  " + render[i * 2 + 1][j] + "\n")
            out += str(render[i * 2][4] + "  " + render[i * 2 + 1][4])
            printr(out)

    render = []
    for i in range(ceil(len(item_render) / 2)):
        color = print_render(i * 2, 3)
        if color:
            color += get_color_code("green",["bg"]) if selected == i * 2 else ""
        else:
            color = get_color_code("green",["bg"]) if selected == i * 2 else ""
        render.append(make_box(i * 2, color))
        color = print_render(i * 2 + 1, 3)
        if color:
            color += get_color_code("green",["bg"]) if selected == i * 2 + 1 else ""
        else:
            color = get_color_code("green",["bg"]) if selected == i * 2 + 1 else ""
        
        render.append(make_box(i * 2 + 1, color))

    box_to_render(render)


def build_item_render(items, is_shop=False,selected_item = None):
    item_render = []
    for item in items:
        line1 = f"{item.grade} {item.sub_type} (Lvl {item.level})"
        line2 = f"{item.name} {'*' if item.is_equiped else ''}"
        if is_shop:
            line3 = f"{item.value}G"
        else:
            line3 = ""

        # Grafik an Graphics delegieren
        line1 = fixed_width(line1, 34)
        line2 = fixed_width(line2, 34)
        while len(line3) < 22:
            line3 = " " + line3
        color = "red" if item == selected_item else "blue" if item.is_equiped else "yellow" if item.is_fav else None
        if color:
            color = get_color_code(color)

        item_render.append([line1, line2, line3, color])

    return item_render


def render_item_details(selected_item) -> None:
    titel = f"Level {selected_item.level}/{selected_item.max_level} {selected_item.grade} {selected_item.sub_type}: {selected_item.name} {'*' if selected_item.is_equiped else ''}"
    stats = selected_item.get_stats()
    hp = center_text(f"HP {stats['max hp']}", 24)
    mp = center_text(f"MP {stats['max mp']}", 24)
    atk = center_text(f"ATK {stats['atk']}", 24)
    sp_atk = center_text(f"SP ATK {stats['sp atk']}", 24)
    def_ = center_text(f"DEF {stats['def']}", 24)
    sp_def = center_text(f"SP DEF {stats['sp def']}", 24)
    crit_chance = center_text(f"Crit Chance {stats['crit chance']}", 24)
    crit_bounus = center_text(f"Crit Bonus {stats['crit bonus']}", 24)
    item_price = center_text(f"Price {stats['price']}", 24)
    flavor_text = "Flavor text\n\n" + selected_item.flavor
    # flavor_text = wrap_text(selected_item.flavor, 73,1)
    if selected_item.ele:
        ele = f"\nElement: {get_color_code(GTD.elementare[selected_item.ele]["color"])}{selected_item.ele}{get_color_code('none')}"
    else:
        ele = "" #"Element: This item dosen’t have am element"
    #printr(f"┏{"━" * 78}┓")
    line2 = f"{mp} {atk} {sp_atk}"
    line3 = f"{hp} {def_} {sp_def}"
    line4 = f"{crit_chance} {crit_bounus} {item_price}"
    printr(
        put_in_box(f"""{titel}
{line2}
{line3}
{line4}
{ele}
{put_in_box(flavor_text,"round",75)}""","thick",max_width = 78),
        strip=True,
    )


def show_stats(self) -> None:
    clear()
    print_titelbar("Stets", 28)
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
Affiliations:
Elements: {self.ele_afi}
Wapons: {self.wapon_afi}
============================
""")
    _ = inputT("\nPress Enter to return...")


def show_stats_level(self) -> None:
    clear()
    print_titelbar("Level Up", 28)
    printr(f"""Level {self.level} => {self.level + 1}
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


def show_attack(self,curser) -> None:
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
    print(curser)
    printr(f"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ [0] {asfd[0][0]} ┃ ┃ [1] {asfd[1][0]} ┃
┃ {asfd[0][1]} ┃ ┃ {asfd[1][1]} ┃
┃ {asfd[0][2]} ┃ ┃ {asfd[1][2]} ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ [2] {asfd[2][0]} ┃ ┃ [3] {asfd[3][0]} ┃
┃ {asfd[2][1]} ┃ ┃ {asfd[3][1]} ┃
┃ {asfd[2][2]} ┃ ┃ {asfd[3][2]} ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ """)


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
    print_titelbar("FIGHT", 59)
    #printr("Number to select attack")
    #printr("===========================================================")
    print_fight_stats_enemy(enemy)
    fight_art(player, enemy)
    print_bars_player(player)
        


def fight_selact_attack(player, enemy,curser = [0,0,0,0]):
    while True:
        clear()
        print_titelbar("FIGHT", 59)
        printr("Number to select attack")
        printr("===========================================================")
        print_fight_stats_enemy(enemy)
        fight_art(player, enemy)
        print_bars_player(player)
        show_attack(player,curser)
        if curser[0] > -1:
            sel = curser[0] * 2 + curser[1]
        else:
            sel = None
        # printr(ceil(len(item_render) / 2) - 1)
        #render_item_boxes(item_render, offset, sel)
        choice = inputT("> ", True)
        if choice not in ["UP", "DOWN", "LEFT", "RIGHT", "ENTER"]:
            return choice, curser
        else:
            if choice == "ENTER":
                if sel != None:
                    return sel + 1, curser
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
            if curser[0] >= 0:
                if curser[1] < 0:
                    curser[1] = 0
                elif curser[1] > 1:
                    curser[1] = 1
                    #elif curser[0] > ceil(len(item_render) / 2) - 1:
                    #curser[0] = ceil(len(item_render) / 2) - 1

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
    rand_str = center_text(str(rand), 3)
    rand_str_e = center_text(str(rand_e), 3)
    if is_deff:
        l1 = center_text("Player Deffes", 28)
        l2 = center_text("Enemy Attack", 28)
    else:
        l1 = center_text("Player Attack", 28)
        l2 = center_text("Enemy Deffes", 28)
    printr(f"""{center_text(f"{l1}┃{l2}", 59)}
{center_text("╭━━━━━━━╮", 29)}┃{center_text("╭━━━━━━━╮", 29)}
{center_text("┃       ┃", 29)}┃{center_text("┃       ┃", 29)}
{center_text(f"┃  {rand_str}  ┃", 29)}┃{center_text(f"┃  {rand_str_e}  ┃", 29)}
{center_text("┃       ┃", 29)}┃{center_text("┃       ┃", 29)}
{center_text("╰━━━━━━━╯", 29)}┃{center_text("╰━━━━━━━╯", 29)}
{center_text("┃", 59)}
===========================================================
""")
    update()
    return rand, rand_e


def print_room(
    player: tuple[int, int], room, enemys, traps, cheasts, merchents
) -> None:
    printr(room.type)

    room_map: list[list[str]] = deepcopy(room.map)
    for t in traps:
        #if t.show:
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
    print_titelbar(f"Shop Page {page + 1} / {max_page + 1}", 78)
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
    out = header_options(ops, curser, 45, True)
    # printr(f""" Q = Close | N = Next | P = Previous | H = Help
    # E = Buy |  PAGE = Go to Page | Number = Select Item""")
    printr(center_text("", 78, "="))
    return out


def shop_buy_page(
    page: int,
    per_page: int,
    max_page: int,
    is_item_selected: bool,
    item_fillter,
    selected_item,
    gold,
    curser=[0, 0,0,0],
):
    while True:
        clear()
        out = shop_hader(page, max_page, gold, curser)
        if is_item_selected:
            render_item_details(selected_item)

        start = page * per_page
        end = start + per_page
        items = item_fillter[start:end]
        offset = page * per_page
        item_render = build_item_render(items, True)
        if curser[0] > -1:
            sel = curser[0] * 2 + curser[1]
        else:
            sel = None
        render_item_boxes(item_render, offset, sel)
        choice = inputT("> ", True, True)
        if choice not in ["UP", "DOWN", "LEFT", "RIGHT", "ENTER"]:
            return choice, curser
        else:
            if choice == "ENTER":
                if sel != None:
                    return sel + 1, curser
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
            if curser[0] >= 0:
                if curser[1] < 0:
                    if page > 0:
                        curser[1] = 1
                        return "P", curser
                    else:
                        curser[1] = 0
                elif curser[1] > 1:
                    if page < max_page:
                        curser[1] = 0
                        return "N", curser
                    else:
                        curser[1] = 1
                elif curser[0] > ceil(len(item_render) / 2) - 1:
                    curser[0] = ceil(len(item_render) / 2) - 1


def select_menu_page(
    tile: str, structure: dict[str, str], special_key: dict[str, str] = {}
):
    coursr_pos = 0
    elements = [i for i in structure]
    max_el_len = max([len(structure[i]) for i in structure]) + 6
    el_len = len(elements)
    while True:
        clear()
        print_titelbar(tile, 35)
        for i in range(el_len):
            if i == coursr_pos:
                printr(
                    f"> {fixed_width(f'[{i + 1}] {structure[elements[i]]}', max_el_len)}",
                    "yellow",
                )
            else:
                printr(
                    f"{fixed_width(f'[{i + 1}] {structure[elements[i]]}', max_el_len)}"
                )

        choic = inputT("> ", True if el_len > 9 else False, True)
        if choic == "UP":
            coursr_pos = (coursr_pos - 1) % el_len
        elif choic == "DOWN":
            coursr_pos = (coursr_pos + 1) % el_len
        elif choic == "ENTER":
            return elements[coursr_pos]
        else:
            if choic in special_key:
                return special_key[choic]
            else:
                try:
                    choic = int(choic)
                    if choic > 0 and choic <= el_len:
                        return elements[choic - 1]
                    else:
                        printr("nop")
                        time.sleep(1)
                except:
                    printr("nop nop")
                    time.sleep(1)


def header_options(struc, curser_temp=[0, 0, 0, 0], width=36, curser_pos_inver=False):
    curser = curser_temp.copy()
    lines = []
    lines_temp = []
    ops = [i for i in struc]
    line_temp = ""
    line = []
    for i in struc:
        if line_temp == "":
            line_temp += f"{i} = {struc[i]}"
            line.append(i)
        else:
            if len(f"{line_temp} | {i} = {struc[i]}") > width:
                lines.append(line)
                lines_temp.append(line_temp)
                line = []
                line.append(i)
                line_temp = f"{i} = {struc[i]}"
            else:
                line_temp += f" | {i} = {struc[i]}"
                line.append(i)
        if ops.index(i) + 1 >= len(struc):
            lines.append(line)
            
    # max_len = max([len(i) for i in lines])
    if curser_pos_inver:
        curser[0] = len(lines) + curser[0]
        if curser[0] < 0:
            curser[0] = 0
            curser_temp[0] = 0 - len(lines)
        
        curser[2] = len(lines) + curser[2]
        if curser[2] < 0:
            curser[2] = 0
            curser_temp[2] = 2 - len(lines)
    #curser[1] = min(curser[1], len(lines[curser[0]]) - 1)
    
    # clamp Y
    if curser[0] < 0:
        curser[0] = 0
    
    # print(curser_temp)
    # print(curser)
        # clamp X (tile) BASED ON CURRENT LINE
    if curser[0] < len(lines):
        line_len = len(lines[curser[0]])
        if curser[1] >= line_len:
            curser[1] = line_len - 1
        elif curser[1] < 0:
            curser[1] = 0
    elif curser[2] < len(lines):
        line_len = 2
        if curser[1] >= line_len:
            curser[1] = line_len - 1
        elif curser[1] < 0:
            curser[1] = 0
            
    prev_line = curser[2]
        
        # clamp prev_line too, or it will bite you later
    if curser[0] != curser[2]:
        if prev_line < 0:
            prev_line = 0
            prev_len = len(lines[prev_line])
        elif prev_line >= len(lines):
            prev_line = curser[0]
            prev_len = 2
        else:
            prev_len = len(lines[prev_line])
                
        if curser[0] >= len(lines):
            new_len = 2
        else:
            new_len  = len(lines[curser[0]])
           
        if prev_len > 1:
            ratio = curser[3] / (prev_len - 1)
        else:
            ratio = 0
           
        curser[1] = round(ratio * (new_len - 1))
      
    curser_temp[1] = curser[1]
    curser_temp[3] = curser[3]
    
    # print(curser_temp)
    # print(curser)
        
    out = None
    for i in range(len(lines)):
        mark = None
        line = ""
        if curser[0] == i:
            if curser[1] < len(lines[i]):
                mark = curser[1]
            else:
                mark = len(lines[i]) - 1
        for j in range(len(lines[i])):
            if j == mark:
                temp = f"{get_color_code('green')}{lines[i][j]} = {struc[lines[i][j]]}{get_color_code('none')}"
                out = str(lines[i][j])
                line += temp
            else:
                line += f"{lines[i][j]} = {struc[lines[i][j]]}"
            if not j >= len(lines[i]) - 1:
                line += " | "
        printr(line)
    return out


def game_menu(player):
    hp: str = f"HP {player.hp}/{player.max_hp + player.max_hp_items}"
    mp: str = f"MP {player.mp}/{player.max_mp + player.max_mp_items}"
    gold: str = f"Gold {player.gold}"
    xp: str = f"XP {player.xp}/{player.max_xp}"
    level: str = f"Level {player.level}"
    hp = fixed_width(hp, 13)
    mp = fixed_width(mp, 13)
    gold = fixed_width(gold, 13)
    xp = fixed_width(xp, 13)
    level = fixed_width(level, 13)
    clear()
    print_titelbar("Dice Dungeon", 40)
    printr(
        f"""{hp}  {mp}  {gold}
{level}  {xp}
H = Help | I = Invetory | T = Stats
Q = Quit
========================================""",
        strip=True,
    )


def print_dungeon_map(dungeon, spacing=1, room_size=2, CHEATS_ON=False):
    # 1. BFS: relative Positionen bestimmen
    rooms = dungeon.rooms
    printr(rooms)
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
    height = (maxy - miny + 1) * (room_size + spacing) - spacing

    grid = [[" " for _ in range(width)] for _ in range(height)]

    # 3. Räume zeichnen
    room_coords = {}
    for room in dungeon.rooms.values():
        # if room.show_on_map == False:
        # continue
        gx, gy = room.pos
        gx = (gx - minx) * (room_size + (spacing * 2))
        gy = (gy - miny) * (room_size + spacing)

        rid_str = str(room.id)
        if room.show_on_map or CHEATS_ON:
            if room.id == dungeon.room:
                if len(rid_str) < room_size:
                    for i in range(room_size - len(rid_str)):
                        grid[gy][gx + len(rid_str) + i] = "\33[32m#\33[0m"
                grid[gy][gx : gx + len(rid_str)] = [
                    f"\33[32m{i}\33[0m" for i in rid_str
                ]
                for i in range(room_size - 1):
                    for j in range(room_size):
                        grid[gy + 1 + i][gx + j] = "\33[32m#\33[0m"
            elif room.type == "boss":
                if len(rid_str) < room_size:
                    for i in range(room_size - len(rid_str)):
                        grid[gy][gx + len(rid_str) + i] = "\33[31m#\33[0m"
                grid[gy][gx : gx + len(rid_str)] = [
                    f"\33[31m{i}\33[0m" for i in rid_str
                ]
                for i in range(room_size - 1):
                    for j in range(room_size):
                        grid[gy + 1 + i][gx + j] = "\33[31m#\33[0m"
            elif room.type == "merchant":
                if len(rid_str) < room_size:
                    for i in range(room_size - len(rid_str)):
                        grid[gy][gx + len(rid_str) + i] = "\33[34m#\33[0m"
                grid[gy][gx : gx + len(rid_str)] = [
                    f"\33[34m{i}\33[0m" for i in rid_str
                ]
                for i in range(room_size - 1):
                    for j in range(room_size):
                        grid[gy + 1 + i][gx + j] = "\33[34m#\33[0m"
            else:
                if len(rid_str) < room_size:
                    for i in range(room_size - len(rid_str)):
                        grid[gy][gx + len(rid_str) + i] = "#"
                grid[gy][gx : gx + len(rid_str)] = list(rid_str)
                for i in range(room_size - 1):
                    for j in range(room_size):
                        grid[gy + 1 + i][gx + j] = "#"
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
    # clear()
    # printr(dungeon.room_pos)
    printr("=" * (width+6))
    text = "Dungeon Map"
    printr(text)
    for row in grid:
        if any(i != " " for i in row):
            temp = "".join(row)
            # print(temp)
            # printr(plen(temp))
            # printr(len(temp))
            printr(temp, strip=False)
    # for i in rooms:
    # printr('room:',i,'doors',rooms[i].doors)
