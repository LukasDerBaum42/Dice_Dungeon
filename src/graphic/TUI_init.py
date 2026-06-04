import os
import sys
import select
import shutil
#from .Graphic import *
#from .TUIGraphic import * 

PLAYER = "P"
TRAP = "T"
CHEAST = "C"
WALL = "#"
BOSS = "B"
ENEMY = "E"
MERCHENT = "M"
WIDTH, HEIGHT = shutil.get_terminal_size(fallback=(80, 30))





class TerminalInputUNIX:
    def __init__(self):
        self.fd = sys.stdin.fileno()
        self.old = termios.tcgetattr(self.fd)
        tty.setcbreak(self.fd)
        self.buf = ""

    def poll(self):
        from . import TUIGraphicCommon as com
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
                
        com.update(False)
        return [e for e in events if e]
        
    def close(self):
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old)


class TerminalInputWIN:
    def __init__(self):
        self.buf = ""

    def poll(self):
        from . import TUIGraphicCommon as com
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

        com.update(False)
        return [e for e in events if e]


if os.name == "nt":
    import msvcrt
    input_lol = TerminalInputWIN()
    print("\x1b[2J\x1b[H")
else:
    import termios
    import tty
    input_lol = TerminalInputUNIX()
    print("\x1b[2J\x1b[H")