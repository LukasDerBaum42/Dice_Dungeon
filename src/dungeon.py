import random
from random import choice
#from tkinter import TclError

from data import Game_text_data as GTD
from .graphic import Graphic


# from . import afiliation as Mafi
# from . import dungeon as Mdun
# from . import fight as Mfight 
from . import enemy as Mene


from .room_object.cheast import Cheast
from .room_object.trape import Trape
from .room_object.merchent import Merchent

OPPOSITE = {"top": "bottom", "bottom": "top", "left": "right", "right": "left"}
SIDES = ["top", "bottom", "left", "right"]


class EnemySpawner:
    def __init__(self,mob: str,level: int,room,x: int,y: int,min_l,max_l,is_boss: bool = False,) -> None:
        self.room: Room = room
        self.mob: str = mob
        self.is_boss: bool = is_boss
        self.x: int = x
        self.y: int = y
        self.level: int = level
        self.min_l = min_l
        self.max_l = max_l
        self.has_spawned = False
        self.is_spawnd = False
        self.cool_down = 0
        self.enemy = None

    def spawn_enemy(self, player):
        if self.is_boss:
            e_level = self.level
        else:
            e_level = (self.level + player.level) // 2

            if e_level < self.min_l:
                e_level = self.min_l
            if e_level > self.max_l:
                e_level = self.max_l

        self.enemy = Mene.Enemy(self.mob, e_level, self.room, self, self.x, self.y, self.is_boss)
        self.room.enemys.append(self.enemy)
        self.is_spawnd = True
        self.has_spawned = True

    def update(self, player, room = None):
        if self.enemy:
            if self.enemy.is_del:
                self.is_spawnd = False
                self.enemy = None

        # if room == self.room:
        # print(self.is_spawnd)
        # print(f"{self.cool_down}")
        # time.sleep(0.1)

        if not self.is_spawnd and self.cool_down <= 0 and room == self.room:
            if self.is_boss and not self.has_spawned:
                self.spawn_enemy(player)
            else:
                self.spawn_enemy(player)
        elif not self.is_spawnd and self.cool_down > 0:
            self.cool_down -= 1
            # print(f"{self.cool_down}")
            # time.sleep(0.1)


class Dungeon:
    def __init__(self, layer, type):
        room = [
            ["#", "#", "#", "#", "#", "#"],
            ["#", ".", ".", ".", ".", "#"],
            ["#", ".", ".", ".", ".", "#"],
            [".", ".", ".", ".", ".", "."],
            ["#", ".", ".", ".", ".", "#"],
            ["#", ".", ".", ".", ".", "#"],
            ["#", "#", "#", "#", "#", "#"],
        ]
        self.no_child = ["boss", "start"]
        dung_preset = GTD.dungeons_preset[type]["liniar"]["layers"]
        if not isinstance(dung_preset, list):
            raise TypeError("dung_preset should be a list, got {} instead".format(type(dung_preset)))
        
        l_size = len(dung_preset)
        gentype = "liniar" if layer < l_size else "endless"
        print(gentype)
        # self.layer_set = GTD.dungeons_preset[type][gentype]["layers"][layer]
        # self.layer = self.layer_set["layer"]
        if gentype == "liniar":
            self.layer_set = GTD.dungeons_preset[type][gentype]["layers"][layer]
            self.layer = self.layer_set["layer"]
            size_a = int(self.layer_set["Size"][0] * GTD.layers[self.layer]["size"][0])
            size_b = int(self.layer_set["Size"][1] * GTD.layers[self.layer]["size"][1])
            self.level = self.layer_set["level"]
        else:
            e_size = len(GTD.dungeons_preset[type]["endless"]["layers"])
            e_layer = layer - l_size
            self.layer = GTD.dungeons_preset[type][gentype]["layers"][e_layer % e_size]
            size_a = int(
                GTD.dungeons_preset[type][gentype]["Size"][0]
                * GTD.layers[self.layer]["size"][0]
            )
            size_b = int(
                GTD.dungeons_preset[type][gentype]["Size"][1]
                * GTD.layers[self.layer]["size"][1]
            )
            base_level = GTD.dungeons_preset[type][gentype]["start_level"]
            skale = GTD.dungeons_preset[type][gentype]["Skale"]
            self.level = int(base_level * (skale**e_layer))
        rand = random.randint(min(size_a, size_b), max(size_a, size_b))
        print(size_a)
        print(size_b)
        print(rand)
        #time.sleep(10)
        self.room_pos = []
        self.rooms = self.gen_dungeon(num_rooms=rand, layer=self.layer)
        self.rooms[0].show_on_map = True
        self.room = 0
        self.spwaners = []

    def print_room(self, player):
        # clear()
        room: Room = self.rooms[self.room]
        enemys: list[Mene.Enemy] = room.enemys
        traps: list[Trape] = room.traps
        cheasts: list[Cheast] = room.cheasts
        merchents: list[Merchent] = room.shops
        player_pos: tuple[int, int] = (player.x, player.y)
        Graphic.print_room(player_pos, room, enemys, traps, cheasts, merchents)

    def conect_rooms(self, current, rooms):
        pos = current.pos
        side = choice(["top", "bottom", "left", "right"])
        pos_2 = None
        if side == "top":
            pos_2 = (pos[0], pos[1] - 1)
        elif side == "bottom":
            pos_2 = (pos[0], pos[1] + 1)
        elif side == "left":
            pos_2 = (pos[0] - 1, pos[1])
        elif side == "right":
            pos_2 = (pos[0] + 1, pos[1])
        if pos_2 is None:
            return current, rooms
        
        safety_count = 0
        side_options = ["top", "bottom", "left", "right"]
        while side in current.sides_used or pos_2 not in self.room_pos:
            side = choice(side_options)
            side_options.remove(side)
            if side == "top":
                pos_2 = (pos[0], pos[1] - 1)
            elif side == "bottom":
                pos_2 = (pos[0], pos[1] + 1)
            elif side == "left":
                pos_2 = (pos[0] - 1, pos[1])
            elif side == "right":
                pos_2 = (pos[0] + 1, pos[1])
            safety_count += 1
            if safety_count > 3:
                break
        if safety_count > 3:
            return current, rooms
        other_id = self.room_pos.index(pos_2)
        other_room = rooms[other_id]
        if other_room.type == "start" or other_room.type == "boss":
            return current, rooms
        else:
            pos_a = current.add_door(side, self.room_pos, ignor_side=True)
            pos_b = other_room.add_door(
                OPPOSITE[side],
                self.room_pos,
                current.pos,
                mirror=pos_a,
                ignor_side=True,
            )
            if pos_a and pos_b:
                current.doors.append(other_id)
                other_room.doors.append(current.id)
        return current, rooms

    def gen_dungeon(self, num_rooms=8, layer="layer 1"):
        rooms = {0: Room(0, "start", 0, 0, width=5, height=5, layer=layer)}
        todo = [0]
        self.room_pos = [(0, 0)]
        next_id = 1

        SPECIAL_ROOMS: dict = GTD.layers[layer]["rooms"]  # Easy to add more

        while next_id < num_rooms or todo:
            current = rooms[todo.pop(0)]

            # Decide connections (1-3, fewer near end)
            if current.id == 0:
                connections = 1
            elif current.type in self.no_child:
                connections = 0
            else:
                connections = min(
                    min(random.randint(1, 3), num_rooms - next_id),
                    len(current.free_sides),
                )

            for child in range(connections):
                Graphic.clear()
                Graphic.print_titelbar("Generating Dungeon", 16)
                Graphic.printr(todo)
                Graphic.printr(current.id)
                Graphic.printr(next_id)
                #printr(self.room_pos)
                #time.sleep(0.2)
                # if next_id >= num_rooms: break
                # if current.conn <= 0: continue
                # Find available sides and connect
                current.update_free_sides(self.room_pos)
                avail_sides = current.free_sides
                if current.id != 0:
                    if not avail_sides:
                        if random.randint(0, 5) == 0:
                            current, rooms = self.conect_rooms(current, rooms)
                            break
                        else:
                            break
                    if random.randint(0, 5) == 0 and len(todo) > 3:
                        current, rooms = self.conect_rooms(current, rooms)
                        continue

                # Determine room type
                room_type = "boss" if next_id == num_rooms-1 else "normal"
                if room_type != "boss":
                    for (
                        special,
                        chance,
                    ) in SPECIAL_ROOMS.items():  # Willkommen bei der Freiheit
                        if random.random() < chance:
                            room_type = special
                            break

                # Create and connect room

                new_room = Room(next_id, room_type, layer=layer, level=self.level)
                rooms[next_id] = new_room
                
            

                dir_a = random.choice(avail_sides)
                dir_b = OPPOSITE[dir_a]

                pos_a = current.add_door(dir_a, self.room_pos)
                pos_b = new_room.add_door(
                    dir_b, self.room_pos, current.pos, mirror=pos_a
                )

                self.room_pos += [new_room.pos]

                if pos_a and pos_b:
                    current.doors.append(next_id)
                    new_room.doors.append(current.id)
                
                #dist= int(math.sqrt(abs(current.pos[0] ** 2) + abs(current.pos[1] ** 2)))
                
                if next_id < num_rooms:
                    if next_id > num_rooms - 7:
                        todo.insert(0,next_id)
                    elif len(todo) > 4 and next_id % 2 == 0:
                        todo.insert(0,next_id)
                    else:
                        todo.append(next_id)
                    next_id += 1

        for _ in range(len(rooms) // 6):
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
    def __init__(
        self,
        room_id,
        room_type="normal",
        x=0,
        y=0,
        width=None,
        height=None,
        layer="layer 1",
        level=5,
    ):
        self.id = room_id
        self.level = level
        self.type = room_type
        self.pos = (x, y)
        self.layer = layer
        self.doors = []  # [target_room_id, ...]
        self.enemys = []
        self.spawners = []
        self.traps = []
        self.cheasts = []
        self.shops = []
        self.used_pos = []
        self.map = self.generate_room(room_type, width, height)
        self.door_positions = []  # [(x, y), ...]
        self.spawn_positions = []
        self.free_sides = [
            "top",
            "bottom",
            "left",
            "right",
        ]  # which walls already have no doors
        self.sides_used = []
        self.add_asets(layer)
        self.show_on_map = False
        self.conn = None
        

    def place_enemy(self, width, height, layer_name="layer 1"):
        x = random.randint(1, width)
        y = random.randint(1, height)
        while self.map[y][x] != ".":
            x = random.randint(1, width)
            y = random.randint(1, height)
        rarety_temp_1 = 0
        rarety_temp_2 = 0
        rand_num = random.randint(0, 100)
        layer: dict = GTD.layers[layer_name]
        for j in layer["mob"]:
            p = layer["mob"][j]
            # printr(p)
            rarety_temp_1 = rarety_temp_2
            rarety_temp_2 += p
            if (rarety_temp_1 < rand_num) and (rand_num <= rarety_temp_2):
                e_level = self.level + random.randint(-3, 3)
                if e_level <= 0:
                    e_level = 1
                self.spawners.append(
                    EnemySpawner(
                        j, e_level, self, x, y, self.level - layer["min_level"],self.level + layer["max_level"]
                    )
                )
                self.used_pos.append((x, y))

    def place_boss(self, width, height, layer_name="layer 1"):
        x = width
        y = height
        layer: dict = GTD.layers[layer_name]
        e_level = self.level + random.randint(-3, 3)
        if e_level <= 0:
            e_level = 1
        self.spawners.append(
            EnemySpawner(
                layer["boss"],
                e_level,
                self,
                x,
                y,
                self.level - layer["min_level"],
                self.level + layer["max_level"],
                True,
            )
        )
        # self.enemys.append(Enemy(layer["boss"], e_level, self, x, y, True))

    def place_trap(self, width, height, layer_name="layer 1"):
        rarety_temp_1 = 0
        rarety_temp_2 = 0
        rand_num = random.randint(0, 100)
        layer: dict = GTD.layers[layer_name]
        for j in layer["traps"]:
            p = layer["traps"][j]
            # printr(p)
            rarety_temp_1 = rarety_temp_2
            rarety_temp_2 += p
            if (rarety_temp_1 < rand_num) and (rand_num <= rarety_temp_2):
                self.traps.append(Trape(width, height, j, self))

    def place_cheast(self, x, y):
        self.cheasts.append(Cheast(self, x, y))

    def get_enemy_pos(self):
        enemy_pos = []
        for e in self.enemys:
            enemy_pos.append([e.x, e.y])
        return enemy_pos

    def add_asets(self, layer="layer 1"):
        if self.type == "start":
            height = len(self.map) // 2
            width = len(self.map[0]) // 2
            self.map[height][width] = "S"
            Graphic.printr("add assets")

        elif self.type == "boss":
            height = len(self.map) // 2
            width = len(self.map[0]) // 2
            self.place_boss(width, height, layer)
            Graphic.printr("add assets")

        elif self.type == "merchant":
            height = len(self.map) // 2
            width = len(self.map[0]) // 2
            self.shops.append(Merchent(width, height, self))
            Graphic.printr("add assets")

        elif self.type == "normal":
            height = len(self.map) - 2
            width = len(self.map[0]) - 2
            space = height * width
            rand = random.randint((space // 6), (space // 3))
            for i in range(rand):
                if i == 0:
                    self.place_enemy(width, height, layer)
                else:
                    rand_2 = random.randint(0, 3)
                    if rand_2 <= 0:
                        self.place_enemy(width, height, layer)
                    elif rand_2 == 1:
                        x = random.randint(2, width - 1)
                        y = random.randint(2, height - 1)
                        if self.map[y][x] == "." and (x, y) not in self.used_pos:
                            self.used_pos.append((x, y))
                            self.map[y][x] = "#"

                    elif rand_2 == 6:
                        x = random.randint(2, width - 1)
                        y = random.randint(2, height - 1)
                        if self.map[y][x] == "." and (x, y) not in self.used_pos:
                            self.used_pos.append((x, y))
                            self.map[y][x] = "#"
                    elif rand_2 == 5:
                        x = random.randint(2, width - 1)
                        y = random.randint(2, height - 1)
                        if self.map[y][x] == "." and (x, y) not in self.used_pos:
                            self.used_pos.append((x, y))
                            self.map[y][x] = "#"
                    elif rand_2 == 2:
                        x = random.randint(1, width)
                        y = random.randint(1, height)
                        if self.map[y][x] == "." and (x, y) not in self.used_pos:
                            self.used_pos.append((x, y))
                            self.place_cheast(x, y)
                    elif rand_2 == 3:
                        x = random.randint(1, width)
                        y = random.randint(1, height)
                        if self.map[y][x] == "." and (x, y) not in self.used_pos:
                            self.used_pos.append((x, y))
                            self.place_trap(x, y, layer)
                    elif rand_2 == 4:
                        x = random.randint(1, width)
                        y = random.randint(1, height)
                        if self.map[y][x] == "." and (x, y) not in self.used_pos:
                            self.used_pos.append((x, y))
                            self.map[y][x] = " "
                Graphic.printr("add assets")

    def update_free_sides(self, grid):
        f_side = []
        if (self.pos[0], self.pos[1] - 1) not in grid:
            f_side.append('top')
            
        if (self.pos[0], self.pos[1] + 1) not in grid:
            f_side.append('bottom')
        
        if (self.pos[0] - 1, self.pos[1]) not in grid:
            f_side.append('left')
            
        if (self.pos[0] + 1, self.pos[1]) not in grid:
            f_side.append('right')
        
        self.free_sides = f_side
        for i in self.free_sides:
            try:
                if i == "top" and (self.pos[0], self.pos[1] - 1) in grid:
                    self.free_sides.remove("top")
                if i == "bottom" and (self.pos[0], self.pos[1] + 1) in grid:
                    self.free_sides.remove("bottom")
                if i == "left" and (self.pos[0] - 1, self.pos[1]) in grid:
                    self.free_sides.remove("left")
                if i == "right" and (self.pos[0] + 1, self.pos[1]) in grid:
                    self.free_sides.remove("right")
            except:
                pass

    def add_door(self, side, grid, o_pos=None, mirror=None, ignor_side=False):
        if side not in self.free_sides and not ignor_side:
            return None  # already has a door on this side
        height = len(self.map)
        width = len(self.map[0])

        def clamp(val, min_val, max_val):
            return max(min_val, min(val, max_val))


        x, y = None, None
        # compute door coordinates
        if mirror and o_pos:
            mx, my = mirror
            if side == "left":
                x, y = 0, clamp(my, 1, height - 2)
                self.pos = (o_pos[0] + 1, o_pos[1])
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

        if x == None or y == None:
            return (0,0)
        self.map[y][x] = "D"
        self.door_positions.append((x, y))
        try:
            self.free_sides.remove(side)
        except:
            pass
        self.sides_used.append(side)
        self.update_free_sides(grid)
        return (x, y)

    def generate_room(self, room_type, width=None, height=None):
        if not width:
            width = random.randint(6, 10)
        if not height:
            height = random.randint(6, 10)
        self.width, self.height = width , height
        return [
            [
                "#" if x in (0, width - 1) or y in (0, height - 1) else "."
                for x in range(width)
            ]
            for y in range(height)
        ]


