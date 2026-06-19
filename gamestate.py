class GameState:
    def __init__(self):
        from src import player as Mply
        from src import dungeon as Mdun
        self.loop = "main"
        self.prv_loop:list[str] = []
        self.running = True
        self.cheats_on = False
        self.layers: list[Mdun.Dungeon] = []
        self.curent_Layer = 0
        self.dungeon: Mdun.Dungeon
        self.dungeon_type = ""
        self.player: Mply.Player
        self.cursor = [0,0,0,0]
        self.other: dict | None = None
        self.prv_other : list[dict | None] = []
        
    def new_loop(self,loop:str,other:dict | None = None):
        self.prv_loop.append(self.loop)
        self.loop = loop
        self.prv_other.append(self.other)
        self.other = other
    
    def ret_loop(self):
        prv_l = self.prv_loop.pop(-1)
        self.loop = prv_l
        prv_o = self.prv_other.pop(-1)
        self.other = prv_o
        
        