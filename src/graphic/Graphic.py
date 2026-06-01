#import os
#import random
#import re
#import select
#import shutil
#import sys
#import time
#from copy import deepcopy
#from math import ceil
#from types import LambdaType

#from ...data import Game_text_data as GTD
from ...data.settings_handler import settings

# group 1

FPS = 120
#os.system("cls" if os.name == "nt" else "clear")
GAPHICMODE = settings["general"]["graphic_mode"]
if GAPHICMODE == "TUI":
    from .TUI_init import *
    from .TUIGraphic import *
    from .TUIGraphicCommon import *
else:
    from .TUI_init import *
    from .TUIGraphic import *
    from .TUIGraphicCommon import * 


