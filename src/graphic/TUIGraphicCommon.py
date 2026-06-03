import os
import random
import re
import select
import shutil
import sys
import time

from types import LambdaType

from .TUI_init import *
from .Graphic import FPS
from .TUI_init import input_lol

FPS: int = FPS

ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-9;]*m")
def plen(s: str) -> int:
    clean = ANSI_ESCAPE_RE.sub("", s)
    return len(clean)


def get_size():
    global WIDTH, HEIGHT, FRAME_BUFER
    new_w , new_h = shutil.get_terminal_size(fallback=(80, 30))
    if new_w != WIDTH or new_h != HEIGHT:
        print('\x1b[2J\x1b[H')
    WIDTH, HEIGHT = new_w , new_h
    while WIDTH < 80 or HEIGHT < 30:
        WIDTH, HEIGHT = shutil.get_terminal_size(fallback=(80, 30))
        os.system("cls" if os.name == "nt" else "clear")
        FRAME_BUFER = []
        print("WINDOW TO SMALL")
        color = "red" if HEIGHT < 30 else "green"
        print(f"{get_color_code(color)}min height is 30 curent is {HEIGHT}{get_color_code("none")}")
        color = "red" if WIDTH < 80 else "green"
        print(f"{get_color_code(color)}min width is 80 curent is {WIDTH}{get_color_code("none")}")
        time.sleep(0.1)
        

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
                    #wait(1)
                    # print(keys)
                    break
                #wait(0.005)
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
                #wait(1)
                break
            #wait(0.005)  # ← IMPORTANT
        # printr(keys)
        # printr(str(keys[0].upper().strip()))
        update()
        return key.upper().strip()


def wait(t):
    stt = time.time()
    slt = 1 / (FPS * 2)
    while (time.time() - stt) < t:
        update(False)
        if (time.time() - stt) < t:
            time.sleep(slt)


def clear():
    global PRINT_BUFFER, FRAME_BUFER
    update()
    PRINT_BUFFER = []
    #os.system("cls" if os.name == "nt" else "clear")
    #FRAME_BUFER = []
    get_size()
    #print("\x1b[2J\x1b[H")
    
    


def update(prio = True):
    get_size()
    print_replace(PRINT_BUFFER,prio)


FRAMR_RATE = [time.time()]

def up_frame_rate():
    global FRAMR_RATE
    if len(FRAMR_RATE) > 20:
        _ = FRAMR_RATE.pop(0)
        
    FRAMR_RATE.append(time.time())
    
    if len(FRAMR_RATE) >= 2:
        out = 0
        ft = 0
        for i in range(1,len(FRAMR_RATE)):
            fps = FRAMR_RATE[i] - FRAMR_RATE[i -1]
            if i == len(FRAMR_RATE)-1:
                ft = round(fps * 100000)
            fps = 1 / fps
            out = (out+fps)/2
            #temp.append(fps)
        #out = int(sum(temp)/ len(temp))
        out = round(out)
        exect_t = round(1 / (FRAMR_RATE[-1] - FRAMR_RATE[-2]))
        return out,exect_t, ft
    else:
        return 0 ,0,0

FRAME_BUFER = []
fps = ""

def print_replace(lines,prio = True):
    """
    Prints a list of strings and replaces them in-place
    on subsequent calls.
    """
    global FRAME_BUFER, fps
    if 1 // (time.time() - FRAMR_RATE[-1]) >= FPS and not prio:
        #wait((time.time() - FRAMR_RATE[-1]) * ((1 / (time.time() - FRAMR_RATE[-1])) / (FPS + 10)))
        return

    #print(PRINT_BUFFER)
    fps = str(up_frame_rate())
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

    #print(out_1)
    sys.stdout.write("\033[H\033[2Kfps " + fps + "\033[E")
    for i, line in enumerate(out_1):
        #if i < len(FRAME_BUFER) and FRAME_BUFER[i] == line:
            #sys.stdout.write("\033[E")
            #else:
            # Clear line + write new content
            sys.stdout.write("\033[2K")  # clear line
            sys.stdout.write(line)
            sys.stdout.write("\033[E")
            if i >= len(FRAME_BUFER)-1:
                FRAME_BUFER.append(line)
                FRAME_BUFER[i] = line
            else:
                FRAME_BUFER[i] = line

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
    
    elif color == "black":
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
        r = int(color[1:3],16)
        g = int(color[3:5],16)
        b = int(color[5:7],16)
        if "bg" in bonus:
            out = f"\x1b[48;2;{r};{g};{b}m"
        else:
            out = f"\x1b[38;2;{r};{g};{b}m"
    else:
        printr(f"INVALED COLOR {color} ", "red")
        return ""
    if temp:
        if "bold" in bonus:
            color_c += "1;" 
        if "line" in bonus:
            color_c += "4;"
        
        if "bg" in bonus:
           out = str(int(out)+10)
        
        if "hi" in bonus:
           out = str(int(out)+60)
        out = f"\x1b[{color_c}{out}m"
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



def print_titelbar(text: str, width: int = WIDTH-2):
    if plen(text) > width:
        width = plen(text)
    sep = "═" * (width)
    # text = center_text(text, width)
    printr(f"╔{sep}╗")
    text = f"║{center_text(text,width)}║" 
    printr(text)
    printr(f"╚{sep}╝")
    
def header_options(struc, cursor_temp=[0, 0, 0, 0], width=36, cursor_pos_inver=False):
    cursor = cursor_temp.copy()
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
    
    shape = [len(i) for i in lines]
    #print(shape)
            
    # max_len = max([len(i) for i in lines])
    if cursor_pos_inver:
        cursor[0] = len(lines) + cursor[0]
        if cursor[0] < 0:
            cursor[0] = 0
            cursor_temp[0] = 0 - len(lines)
        
        cursor[2] = len(lines) + cursor[2]
        if cursor[2] < 0:
            cursor[2] = 0
            cursor_temp[2] = 2 - len(lines)

    out = None
    for i in range(len(lines)):
        mark = None
        line = ""
        if cursor[0] == i:
            if cursor[1] < len(lines[i]):
                mark = cursor[1]
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
    return out , shape
    
class BoxPreRender:
    def __init__(self) -> None:
        self.color: str|None = None
        self.num = 0
        self.num_line = ''
        self.texts = []
        self.width = 34
        self.numj = 6
        
    def hight(self) -> int:
        return 1 + len(self.texts)
    
    
def box_menu(pre_render:list[BoxPreRender],cursor:list,size = [2,4]):
        
        shape = []
        #printr(size)
        for i in range(size[1]):
            #printr(f"{(i+1) * size[0]}  {len(pre_render)}  {(i+1) * size[0] > len(pre_render)}")
            if (i+1) * size[0] > len(pre_render):
                shape.append(len(pre_render) - (i) * size[0])
                break
            else: 
                shape.append(size[0])
        
        #printr(shape)
        
        hight = max([i.hight() for i in pre_render])
    
        def make_box(render:BoxPreRender, color):
            box = []
            num1 = f"[{render.num + 1}]".ljust(render.numj)
            box.append(f"┏{center_text('',render.width+2,"━")}┓")
            box.append(f"┃ {num1} {render.num_line} ┃")
            for i in range(hight-1):
                box.append(f"┃ {render.texts[i]} ┃")
            box.append(f"┗{center_text('',render.width+2,"━")}┛")
    
            if color:
                # printr(color)
                for i in range(len(box)):
                    box[i] = f"{color}{box[i]}{get_color_code("none")}"
            return box
    
        def box_to_render(render):
            for i in range(len(shape)):
                out = ""
                for j in range(hight + 2):
                    for k in range(shape[i]):
                        out += str(render[i * shape[0] + k][j])
                        if k+1 < shape[i]:
                            out += "  "
                        else:
                            out += "\n"
                printr(out)
    
        render = []
        if cursor[0] > -1:
            selected = (cursor[0] * size[0] + cursor[1])
            #printr(selected)
        else:
            selected = None
        for i in range(len(pre_render)):
            color = pre_render[i].color
            if color:
                color += get_color_code("green",["bg"]) if selected == i else ""
            else:
                color = get_color_code("green",["bg"]) if selected == i else ""
            render.append(make_box(pre_render[i],color))
    
        box_to_render(render)
        return selected, shape
    
def menu_handler(cursor,box_menu_shape=None,header_menu_shape=None, page=0, max_page=0):
    
    layout = []
    y_off = 0
    
    if header_menu_shape and not box_menu_shape:
        if cursor[0] < 0:
            cursor[0] = 0
        elif cursor[0] >= len(header_menu_shape):
            cursor[0] = len(header_menu_shape) - 1
    elif not header_menu_shape and box_menu_shape:
        if cursor[0] < 0:
            cursor[0] = 0
        elif cursor[0] >= len(box_menu_shape):
            cursor[0] = len(box_menu_shape) - 1
    elif header_menu_shape and box_menu_shape:
        y_off = len(header_menu_shape)
        if cursor[0] < - len(header_menu_shape):
            cursor[0] = 0 - len(header_menu_shape)
        elif cursor[0] >= len(box_menu_shape):
            cursor[0] = len(box_menu_shape) - 1
    
    if cursor[0] >= 0 and box_menu_shape:
        if cursor[1] < 0:
            if page > 0:
                cursor[2] = cursor[0]
                cursor[3] = cursor[1]
                cursor[1] = box_menu_shape[cursor[0]] - 1
                return "P", cursor
            else:
                cursor[1] = 0
        elif cursor[1] > box_menu_shape[cursor[0]] - 1:
            #printr(f"{cursor[1]}  {box_menu_shape[cursor[0]] - 1}")
            if page < max_page:
                cursor[2] = cursor[0]
                cursor[3] = cursor[1]
                cursor[1] = 0
                return "N", cursor
            else:
                cursor[1] = 1
                
    if cursor[0] + y_off < len(layout):
        line_len = layout[cursor[0]+ y_off]
        if cursor[1] >= line_len:
            cursor[1] = line_len - 1
        elif cursor[1] < 0:
            cursor[1] = 0
    elif cursor[2]+ y_off < len(layout):
        line_len = 2
        if cursor[1] >= line_len:
            cursor[1] = line_len - 1
        elif cursor[1] < 0:
            cursor[1] = 0
            
    prev_line = cursor[2]+ y_off
        
        # clamp prev_line too, or it will bite you later
    if cursor[0]+ y_off != cursor[2]+ y_off:
        if prev_line < 0:
            prev_line = 0
            prev_len = layout[prev_line]
        elif prev_line >= len(layout):
            prev_line = cursor[0]+ y_off
            prev_len = 2
        else:
            prev_len = layout[prev_line]
                
        if cursor[0]+ y_off >= len(layout):
            new_len = 2
        else:
            new_len  = layout[cursor[0]+ y_off]
           
        if prev_len > 1:
            ratio = cursor[3] / (prev_len - 1)
        else:
            ratio = 0
           
        cursor[1] = round(ratio * (new_len - 1))
      
    #cursor_temp[1] = cursor[1]
    #cursor_temp[3] = cursor[3]
    
                
    # printr(cursor)
    # printr(header_menu_shape)
    # printr(f"{cursor[0] + y_off},{cursor[1]}")
    return None, cursor

def select_menu_page(
    title: str|None, structure: dict[str, str], special_key: dict[str, str] = {} ,other = None, cursor_pos = 0
):
    elements = [i for i in structure]
    max_el_len = max([plen(structure[i]) for i in structure]) + 6
    el_len = len(elements)
    temp = None
    while True:
        clear()
        if title:
            print_titelbar(title, 35)
        if other:
            printr(other)
        if el_len < HEIGHT - 10:
            for i in range(el_len):
                if i == cursor_pos:
                    printr(
                        f"> {fixed_width(f'[{i + 1}] {structure[elements[i]]}', max_el_len)}",
                        "yellow",
                    )
                else:
                    printr(
                        f"{fixed_width(f'[{i + 1}] {structure[elements[i]]}', max_el_len)}"
                    )
        else:
            if temp:
                if cursor_pos >= temp[1]:
                    if temp[1]+1 <= el_len:
                        temp[0] += 1
                        temp[1] += 1
                    else:
                        temp = [0,HEIGHT - 10]
                elif cursor_pos < temp[0] and temp[0]-1 >= 0:
                    temp[0] -= 1
                    temp[1] -= 1
            else:
                temp = [0,HEIGHT - 10]
            for i in range(*temp):
                if i == cursor_pos:
                    printr(
                        f"> {fixed_width(f'[{i + 1}] {structure[elements[i]]}', max_el_len)}",
                        "yellow",
                    )
                else:
                    printr(
                        f"{fixed_width(f'[{i + 1}] {structure[elements[i]]}', max_el_len)}"
                    )
        update()
        choic = inputT("> ", True if el_len > 9 else False, True)
        if choic == "UP":
            cursor_pos = (cursor_pos - 1) % el_len
        elif choic == "DOWN":
            cursor_pos = (cursor_pos + 1) % el_len
        elif choic == "ENTER":
            return elements[cursor_pos] , cursor_pos
        else:
            if choic in special_key:
                return special_key[choic] , cursor_pos
            else:
                try:
                    choic = int(choic)
                    if choic > 0 and choic <= el_len:
                       return elements[choic - 1], cursor_pos
                    else:
                        printr("nop")
                        update()
                        wait(1)
                except:
                    printr("nop nop")
                    update()
                    wait(1)