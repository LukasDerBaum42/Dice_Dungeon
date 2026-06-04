
from data import Game_text_data as GTD
from .graphic import Graphic
from .Items import GameItem
from gamestate import GameState



class Inventory:
    def __init__(self) -> None:
        self.inventory: list[GameItem] = []
        self.equiped_items: list[GameItem] = []
        self.favorit: list[GameItem] = []
        self.equipt_slots: dict[str,list] = {
            "wappon": [False, None],
            "helmet": [False, None],
            "chestplate": [False, None],
            "pants": [False, None],
            "boots": [False, None],
            "sheald": [False, None],
        }
        
        
    def add(self, item: GameItem):
        self.inventory.append(item)
        
    def equip_item(self, item: GameItem):
        if item.sub_type in self.equipt_slots:
            slot: str = item.sub_type
        elif item.sub_type == "consumable":
            slot = item.sub_type
        else:
            slot = "wappon"
        if item in self.equiped_items:
            self.equiped_items.remove(item)
            item.is_equiped = False
            self.equipt_slots[slot][0] = False
            self.equipt_slots[slot][1] = None
        else:
            if self.equipt_slots[slot][0]:
                # Graphic.printr("\033[u")

                Graphic.printr(f"You have laredy a {slot} equipped", pos=-1)
                choice = Graphic.inputT("Do you want to swape? [y/n]>")
                if choice == "Y" or choice == "E":
                    self.equiped_items.remove(self.equipt_slots[slot][1])
                    self.equipt_slots[slot][1].is_equiped = False
                    self.equiped_items.append(item)
                    item.is_equiped = True
                    self.equipt_slots[slot][0] = True
                    self.equipt_slots[slot][1] = item
            else:
                self.equiped_items.append(item)
                item.is_equiped = True
                self.equipt_slots[slot][0] = True
                self.equipt_slots[slot][1] = item

    def remove_item(self, item):
        if item in self.equiped_items:
            self.equip_item(item)
        if item in self.favorit:
            self.favorit.remove(item)
        self.inventory.remove(item)

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

def show_inventory(GS: GameState):
    if GS.other is None:
        raise LookupError("GameState has other no other set: show_inventory needs other to have element 'is_shop'")
    is_shop = GS.other["is_shop"]
    player = GS.player
    size = [2, 4]
    is_item_selected: bool = False
    page: int = 0
    is_fav: bool = False
    is_equ: bool = False
    # item_fillter = self.inventory
    selected_item: None | GameItem = None
    selected_num = None
    show_inv = True
    cursor = [0, 0, 0, 0]
    while show_inv:
        # clear()
        per_page, size = items_per_page(is_item_selected)
        max_page = max(0, (len(item_fillter) - 1) // per_page)
        choice, cursor = Graphic.show_inventory(
            page,
            per_page,
            max_page,
            is_item_selected,
            item_fillter,
            selected_item,
            is_shop,
            GS.player.gold,
            cursor,
            size,
        )
        # Graphic.printr(choice)
        # choice = inputT("> ", True).upper().strip()
        if choice == "Q":
            GS.ret_loop()
            return
        elif choice == "N":
            page += 1 if page < max_page else 0
        elif choice == "P":
            page -= 1 if page > 0 else 0
        elif choice == "E":
            if is_item_selected and selected_item != None:
                if is_shop:
                    choice = (
                        Graphic.inputT(
                            f"You sure you want to sell this item?\nYou will get {selected_item.value} Gold\n [y/n] >"
                        )
                        .upper()
                        .strip()
                    )
                    if choice == "Y" or choice == "E":
                        self.remove_item(selected_item)
                        self.gold += selected_item.value
                        selected_item = None
                        is_item_selected = False
                        per_page, size = items_per_page(is_item_selected)
                        if selected_num != None:
                            page = selected_num // per_page
                            selected_num = None
                else:
                    self.equip_item(selected_item)
            else:
                Graphic.printr("No item select")
                Graphic.wait(1)
        elif choice == "SE":
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
        elif choice == "F":
            if is_item_selected and selected_item != None:
                if selected_item in self.favorit:
                    self.favorit.remove(selected_item)
                    selected_item.is_fav = False
                else:
                    self.favorit.append(selected_item)
                    selected_item.is_fav = True
        elif choice == "SF":
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
            if selected_num != None:
                page = selected_num // per_page
                selected_num = None
            else:
                page = 0

        else:
            try:
                if choice == None:
                    return
                choice = int(choice)
                choice -= 1
                if choice >= 0 and choice <= len(item_fillter):
                    if choice == selected_num:
                        selected_item = None
                        is_item_selected = False
                        selected_num = None
                        per_page, size = items_per_page(is_item_selected)
                        page = choice // per_page
                        cursor[2] = cursor[0]
                        cursor[3] = cursor[1]
                        temp = choice % per_page
                        cursor[1] = temp % 2
                        cursor[0] = temp // 2
                    else:
                        selected_item = item_fillter[choice]
                        is_item_selected = True
                        selected_num = choice
                        per_page, size = items_per_page(is_item_selected)
                        page = choice // per_page
                        cursor[2] = cursor[0]
                        cursor[3] = cursor[1]
                        temp = choice % per_page
                        cursor[1] = temp % 2
                        cursor[0] = temp // 2
            except:
                Graphic.printr("Invalid inputT\n Item can’t be selected")
                Graphic.printr(f"{choice}")
                Graphic.update()
                Graphic.wait(1)
                Graphic.printr("done")
                Graphic.update()