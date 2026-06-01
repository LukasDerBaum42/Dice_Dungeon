import math
import os
import random
import time
from random import Random, choice, randint
#from tkinter import TclError

from data import Game_text_data as GTD
from ..graphic import Graphic
from ..Items import GameItem


from ..common import p_chois

# from src.player import *
# from src.enemy import *
# from src.dungeon import *
# from src.afiliation import *
# from src.fight import *


class Merchent:
    def __init__(self, x, y, room):
        self.x = x
        self.y = y
        self.room = room
        self.layer = GTD.layers[room.layer]
        self.type = p_chois(self.layer["shops"])
        self.gtd_shop = GTD.shops[self.type]
        self.items = self.gen_items()

    def gen_items(self):
        size_temp = self.gtd_shop["size"]
        size = randint(*size_temp)
        items = []
        for _ in range(size):
            item_type = p_chois(self.gtd_shop["item type"])
            item_rarety = p_chois(self.gtd_shop["rarety"])
            level = self.room.level + randint(*self.gtd_shop["level"])
            items.append(GameItem(item_rarety, item_type, level))

        return items

    def shop_buy(self, player):
        size = [2,4]
        def items_per_page(is_selected: bool):
            out = 4 if is_selected else 8
            if out == 4:
                size = [2, 2]
            else:
                temp = Graphic.WIDTH // 40
                temp2 = (Graphic.HEIGHT - 10) // 6
                size = [temp, temp2]
                out = temp * temp2
                # size = [2,4]
            return out, size

        is_item_selected: bool = False
        page: int = 0
        item_fillter = self.items
        selected_item: None | GameItem = None
        selected_num = None
        show_inv = True
        curser = [0, 0, 0, 0]
        while show_inv:
            per_page, size = items_per_page(is_item_selected)
            max_page = max(0, (len(item_fillter) - 1) // per_page)

            choice, curser = Graphic.shop_buy_page(
                page,
                per_page,
                max_page,
                is_item_selected,
                item_fillter,
                selected_item,
                player.gold,
                curser,
                size,
            )
            # choice = inputT("> ", True).upper().strip()
            if choice == "Q":
                show_inv = False
                break
            elif choice == "N":
                page += 1 if page < max_page else 0
            elif choice == "P":
                page -= 1 if page > 0 else 0

            elif choice == "E":
                if is_item_selected and isinstance(selected_item, GameItem):
                    if selected_item.value <= player.gold:
                        choice = (
                            Graphic.inputT(
                                f"Do you want to buy this item?\nthe item costs {selected_item.value} gold\nyou have {player.gold}, after buying you'll have {player.gold - selected_item.value}\n [Y/N] > "
                            )
                            .upper()
                            .strip()
                        )
                        if choice == "Y" or choice == "E":
                            player.add_to_inv(selected_item)
                            player.gold -= selected_item.value
                            self.items.remove(selected_item)
                            selected_item = None
                            is_item_selected = False
                            per_page, size = items_per_page(is_item_selected)
                            if selected_num is not None:
                                page = selected_num // per_page
                            selected_num = None
                    else:
                        Graphic.printr("You don’t have enough gold to buy this item")
                        Graphic.wait(1)
                else:
                    Graphic.printr("No Item Selected")
                    Graphic.wait(1)

            elif choice == "PAGE":
                choice = Graphic.inputT("Selacte page > ", True, True).upper().strip()
                try:
                    if (int(choice) - 1) >= 0 and (int(choice) - 1) <= max_page:
                        page = int(choice) - 1
                except:
                    Graphic.printr("Invalid inputT")
                    Graphic.wait(1)
            elif is_item_selected and (choice == ""):
                selected_item = None
                is_item_selected = False
                per_page, size = items_per_page(is_item_selected)
                if selected_num is not None:
                    page = selected_num // per_page
                selected_num = None

            else:
                try:
                    choice = int(choice)
                    choice -= 1
                    if choice >= 0 and choice <= len(item_fillter):
                        if choice == selected_num:
                            selected_item = None
                            is_item_selected = False
                            selected_num = None
                            per_page, size = items_per_page(is_item_selected)
                            page = choice // per_page
                            curser[2] = curser[0]
                            curser[3] = curser[1]
                            temp = choice % per_page
                            curser[1] = temp % 2
                            curser[0] = temp // 2
                        else:
                            selected_item = item_fillter[choice]
                            is_item_selected = True
                            selected_num = choice
                            per_page, size = items_per_page(is_item_selected)
                            page = choice // per_page
                            curser[2] = curser[0]
                            curser[3] = curser[1]
                            temp = choice % per_page
                            curser[1] = temp % 2
                            curser[0] = temp // 2
                except:
                    Graphic.printr("Invalid inputT")
                    Graphic.wait(1)

    def interact_player(self, player):
        is_in_shop: bool = True
        struc = {"buy": "Buy Items", "sell": "Sell Items", "Q": "Leave"}
        while is_in_shop:
            choice,_ = Graphic.select_menu_page("Merchent", struc, {"Q": "Q"})
            if choice == "Q":
                is_in_shop = False
            elif choice == "sell":
                player.show_inventory(True)
            elif choice == "buy":
                self.shop_buy(player)
