import math
import os
import random
import time
from random import Random, choice, randint
#from tkinter import TclError

import Game_text_data as GTD
import Graphic
from Graphic import clear, inputT, printr, wait
from Items import GameItem

# from src.player import *
# from src.enemy import *
# from src.dungeon import *
# from src.afiliation import *
# from src.fight import *


class Fight:
    def __init__(self,player,enemy,stat):
        self.player = player
        self.enemy = enemy
        self.stat = stat
    
    

def fight_won(player, enemy):
    gold_gain = f"{enemy.gold} Gold"
    while len(gold_gain) < 27:
        gold_gain = gold_gain + " "
        if len(gold_gain) < 27:
            gold_gain = " " + gold_gain
    xp_gain = f"{enemy.xp} XP"
    while len(xp_gain) < 27:
        xp_gain = xp_gain + " "
        if len(xp_gain) < 27:
            xp_gain = " " + xp_gain
    stats_gain = gold_gain + " " + xp_gain

    clear()
    Graphic.print_fight_UI(player, enemy)
    printr(stats_gain)
    printr("                          ITEMS                            ")
    for item in enemy.items:
        printr(item.Name())
        player.inventory.append(item)
    inputT("\nPress Enter to return...")
    player.gold += enemy.gold
    player.Level(enemy.xp)


def you_died():
    clear()
    printr("You died")
    inputT("\nPress Enter to return...")


def fight_selact_attack(player, enemy, curser):
    clear()
    choice, curser = Graphic.fight_selact_attack(player, enemy, curser)
    return choice, curser


def get_attaker_stats(attaker, defender, sel):
    attake = attaker.attacks[sel]
    atk_ele = attake["ele"]
    p_crit = (
        attaker.crit_chance + attaker.crit_chance_items + attake["stats"]["crit_chance"]
    )
    p_crit_bonus = (
        attaker.crit_bonus + attaker.crit_bonus_items + attake["stats"]["crit_bonus"]
    )

    crit = p_chance(p_crit)
    atk = attaker.atk + attaker.atk_items
    atk = int(atk * (attake["stats"]["atk"] / 100))
    sp_atk = attaker.sp_atk + attaker.sp_atk_items
    sp_atk = int(sp_atk * (attake["stats"]["sp_atk"] / 100))
    if atk_ele:
        afi_stat = attaker.ele_afi.fin_afi[atk_ele] / 100
        atk = int(atk * afi_stat)
        sp_atk = int(sp_atk * afi_stat)

        if attaker.wapon_ele == atk_ele:
            atk = int(atk * 1.5)
            sp_atk = int(sp_atk * 1.5)

        if defender.ele_afi.main_afi in GTD.elementare[atk_ele]["atk"]:
            atk = int(atk * 2)
            sp_atk = int(sp_atk * 2)
    atk += int(atk * (p_crit_bonus / 100)) if crit else 0
    sp_atk += int(sp_atk * (p_crit_bonus / 100)) if crit else 0
    attaker.ele_afi_up(atk_ele)
    return atk, sp_atk, crit


def get_deffender_stats(attaker, defender, sel):
    attake = attaker.attacks[sel]
    atk_ele = attake["ele"]

    def_ = defender.def_ + defender.def_items
    sp_def = defender.sp_def + defender.sp_def_items
    if atk_ele:
        afi_stat = defender.ele_afi.fin_afi[atk_ele] / 100
        def_ = int(def_ * afi_stat)
        sp_def = int(sp_def * afi_stat)

        if defender.ele_afi.main_afi in GTD.elementare[atk_ele]["def"]:
            def_ = int(def_ * 2)
            sp_def = int(sp_def * 2)
    return def_, sp_def


def enemy_fight_ai(attacker, deffender):
    rand = random.randint(0, 3)
    return rand


def fight_roll_dice(player, enemy, start, end, sel=0, advan=0, atk=True):
    rand = 0
    advan_e = 0
    if atk:
        attaker = player
        deffender = enemy
    else:
        attaker = enemy
        deffender = player
        sel = enemy_fight_ai(attaker, deffender)
    clear()
    Graphic.print_fight_UI(player, enemy)
    rand, rand_e = Graphic.fight_roll_dice(
        player, enemy, start, end, advan, advan_e, not (atk)
    )

    if atk:
        rand_a = rand
        rand_d = rand_e
    else:
        rand_a = rand_e
        rand_d = rand

    base_atk, base_sp_atk, crit = get_attaker_stats(attaker, deffender, sel)
    base_def, base_sp_def = get_deffender_stats(attaker, deffender, sel)
    # print("base atk:",base_atk)
    # print("base sp atk:",base_sp_atk)
    base_atk *= rand_a
    base_sp_atk *= rand_a
    # print("base def:",base_def)
    # print("base sp def:",base_sp_def)
    base_def *= rand_d
    base_sp_def *= rand_d
    # print("base atk:",base_atk)
    # print("base sp atk:",base_sp_atk)
    # print("base def:",base_def)
    # print("base sp def:",base_sp_def)
    strangth = base_atk - base_def
    sp_strangth = base_sp_atk - base_sp_def
    strangth = 0 if strangth < 0 else strangth
    sp_strangth = 0 if sp_strangth < 0 else sp_strangth
    # print("strangth:", strangth)
    # print("sp strangth:", sp_strangth)
    damage = strangth + sp_strangth
    # print("damage:",damage)
    deffender.hp -= damage
    sel_atk = list(attaker.attacks_used)[sel]
    Graphic.print_atk_damage(
        sel_atk, base_atk, base_sp_atk, base_def, base_sp_def, crit, damage, atk
    )
    inputT("\nPress Enter to return...")

    return player, enemy


def fight_loop(player, enemy, player_start=True):
    global loop_fight, loop_room
    loop_fight = True
    curser = [0, 0, 0, 0]
    turn = 1 if player_start else 0
    first_turn = True
    while loop_fight:
        if enemy.hp <= 0:
            fight_won(player, enemy)
            loop_fight = False
            loop_room = True
            return player, True
        elif player.hp <= 0:
            you_died()
            loop_fight = False
            loop_room = False
            return player, False
        # printr(turn)
        if turn == 0:
            clear()
            Graphic.print_fight_UI(player, enemy)
            choice = inputT("\nPress Enter to continue...").upper().strip()
            if choice == "Q" and CHEATS_ON:
                loop_fight = False
                return player, True
            elif choice == "S":
                printr(enemy)
                inputT("\nPress Enter to return...")
            else:
                player, enemy = fight_roll_dice(
                    player, enemy, 1, 6, advan=-1 if first_turn else 0, atk=False
                )
                turn = 1
                first_turn = False
        elif turn == 1:
            choice, curser = fight_selact_attack(player, enemy, curser)
            # choice = inputT(">").upper().strip()
            
            try:
                if choice == "Q":
                    loop_fight = False
                    return player, True
                elif choice == "S":
                    printr(enemy)
                    inputT("\nPress Enter to return...")
                elif (0 <= int(choice) - 1) and (int(choice) - 1 <= 3):
                    attack_num = int(choice) - 1
                    attack_used = list(player.attacks_used)[attack_num]
                    attack_max_used = player.attacks[attack_num]["stats"]["max_use"]
                    wappon = player.equipt_slots["wappon"]
                    needed_wappon = player.attacks[attack_num]["wapon"]
                    if needed_wappon == []:
                        pass
                    else:
                        if wappon[1] == None:
                            printr("You dont have a wapon")
                            # print(needed_wappon)
                            # print(wappon[1])
                            wait(2)
                            continue
                        elif not wappon[1].sub_type in needed_wappon:
                            printr(
                                f"You dont have the requred wapon, you need a {needed_wappon}"
                            )
                            # print(needed_wappon)
                            # print(wappon[1].sub_type)
                            wait(2)
                            continue
                    if player.attacks_used[attack_used] >= attack_max_used:
                        printr("No more uses of selected attack left")
                        wait(1)
                    elif player.attacks[attack_num]["stats"]["mp"] > player.mp:
                        printr("Not enough mp for this attack")
                        wait(1)
                    else:
                        player.attacks_used[attack_used] += 1
                        player.mp -= player.attacks[attack_num]["stats"]["mp"]
                        player, enemy = fight_roll_dice(
                            player, enemy, 1, 6, attack_num, 1 if first_turn else 0
                        )
                        turn = 0
                        first_turn = False
            except:
                printr("Invalid inputT lol")
                wait(1)