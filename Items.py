import random
import time
from ast import Return
from multiprocessing import Value

import Game_text_data as GTD


class GameItem:
    UNIQUE_ITEMS = GTD.UNIQUE_ITEMS

    GRADE_INFO = {
        "common": {"max_level": 20, "stat_scale": (1, 2)},
        "uncommon": {"max_level": 30, "stat_scale": (2, 4)},
        "rare": {"max_level": 40, "stat_scale": (3, 6)},
        "epic": {"max_level": 50, "stat_scale": (5, 9)},
        "legendary": {"max_level": 75, "stat_scale": (8, 14)},
        "unique": {"max_level": 100, "stat_scale": (0, 0)},
    }

    def __init__(self, grade: str, item_type: str, level: int, name=None):
        self.grade: str = grade.lower()
        self.main_type = "wapon" if item_type in GTD.wappon_sub_typse else "wareable"
        self.sub_type: str = item_type.lower()
        self.level: int = level
        self.max_level: int = self.GRADE_INFO[grade]["max_level"]
        self.prefix: str = ""
        self.suffix: str = ""
        self.name: str = ""
        self.max_hp: int = 0
        self.max_mp: int = 0
        self.atk: int = 0
        self.sp_atk: int = 0
        self.def_: int = 0
        self.sp_def: int = 0
        self.crit_chance: int = 0
        self.crit_bonus: int = 0
        self.price: int = 0
        self.is_equiped: bool = False
        self.is_fav: bool = False
        if random.randint(0,10)< 11:
            self.ele = random.choice(GTD.ele_list)
        else:
            self.ele = None
        if self.grade == "unique":
            self.load_unique(name)
        else:
            self.name = self.generate_name()
            self.generate_stats()
            self.flavor = self.generate_flavor_text()

        self.value = self.get_price()

    def get_price(self) -> int:
        base_prices = {
            "common": 20,
            "uncommon": 30,
            "rare": 45,
            "epic": 65,
            "legendary": 100,
            "unique": 200,
        }
        value: int = base_prices[self.grade]
        value += self.max_hp * GTD.stat_value["max_hp"]
        value += self.max_mp * GTD.stat_value["max_mp"]
        value += self.atk * GTD.stat_value["atk"]
        value += self.sp_atk * GTD.stat_value["sp_atk"]
        value += self.def_ * GTD.stat_value["def"]
        value += self.sp_def * GTD.stat_value["sp_def"]
        value += self.crit_bonus * GTD.stat_value["crit_bonus"]
        value += self.crit_chance * GTD.stat_value["crit_chance"]
        value = int(value)
        # print(value)
        temp = [value, self.price]
        for _ in range(2):
            rand = random.randint(min(temp), max(temp))
            temp.append(rand)
            temp.append(random.randint(min((rand, value)), max((rand, value))))

        dev_by = len(temp)
        avr = sum(temp) // dev_by
        return avr

    def load_unique(self, name=None):
        if name is None:
            self.name, data = random.choice(list(self.UNIQUE_ITEMS.items()))
        else:
            self.name = name
            data = self.UNIQUE_ITEMS[name]
        self.flavor = data["flavor"]
        stats = data["stats"]
        self.sub_type = data["type"]
        self.main_type = "wapon" if self.sub_type in GTD.wappon_sub_typse else "wareable"
        for k, v in stats.items():
            setattr(self, k, int(v * (1 + self.level / 3)))

    # ---- NAME GENERATION ----
    def generate_name(self):
        prefixes = {
            "sword": {
                "common": ["Rusty", "Dull", "Old", "Cracked", "Chipped"],
                "uncommon": [
                    "Iron",
                    "Balanced",
                    "Polished",
                    "Sharpened",
                    "Steel",
                    "Tempered",
                ],
                "rare": [
                    "Runed",
                    "Arcane",
                    "Enchanted",
                    "Swift",
                    "Blessed",
                    "Keen",
                    "Shadowed",
                ],
                "epic": [
                    "Cursed",
                    "Celestial",
                    "Heroic",
                    "Infernal",
                    "Mythic",
                    "Bloodforged",
                    "Nightfang",
                ],
                "legendary": [
                    "Godforged",
                    "Worldbreaker",
                    "Eternal",
                    "Divine",
                    "Doombringer",
                    "Voidcleaver",
                    "Heavenrend",
                    "Soulforge",
                ],
            },
            "knife": {
                "common": ["Small", "Old", "Blunt", "Weak"],
                "uncommon": ["Sharp", "Iron", "Fine", "Steel", "Light"],
                "rare": ["Assassin's", "Poisoned", "Runed", "Silent", "Deadly"],
                "epic": [
                    "Shadowfang",
                    "Cursed",
                    "Phantom",
                    "Wicked",
                    "Blooded",
                    "Night's",
                    "Spectral",
                ],
                "legendary": [
                    "Soulpiercer",
                    "Eternal",
                    "Dagger of Doom",
                    "Voidkiss",
                    "Godfang",
                    "Abyssal",
                ],
            },
            "bow": {
                "common": ["Weak", "Frayed", "Old", "Simple"],
                "uncommon": ["Long", "Ironwood", "Steady", "Fine", "Hardened"],
                "rare": [
                    "Eagle's",
                    "Arcane",
                    "Runed",
                    "Swift",
                    "Blessed",
                    "Windstrung",
                ],
                "epic": [
                    "Storm",
                    "Spectral",
                    "Silent",
                    "Celestial",
                    "Hawkeye",
                    "Nightwind",
                ],
                "legendary": [
                    "Heavenpiercer",
                    "Worldstring",
                    "Godbow",
                    "Oblivion",
                    "Skysunder",
                    "Starcaller",
                ],
            },
            "stafe": {
                "common": ["Wooden", "Old", "Simple", "Cracked"],
                "uncommon": ["Runed", "Crystal", "Polished", "Enchanter's", "Fine"],
                "rare": ["Arcane", "Blessed", "Sage's", "Magus", "Focused", "Aetheric"],
                "epic": [
                    "Celestial",
                    "Infernal",
                    "Cursed",
                    "Druidic",
                    "Stormweaver",
                    "Soulbound",
                ],
                "legendary": [
                    "Godspark",
                    "Eternal",
                    "Worldbinder",
                    "Archmage's",
                    "Heartsong",
                    "Starforged",
                ],
            },
            "spear": {
                "common": ["Bent", "Wooden", "Old", "Rough"],
                "uncommon": ["Steel", "Iron", "Tempered", "Balanced"],
                "rare": ["Hunter's", "Blessed", "Runed", "Sharpened", "Swift"],
                "epic": [
                    "Storm",
                    "Celestial",
                    "Infernal",
                    "Demonic",
                    "Voidlance",
                    "Titan's",
                ],
                "legendary": [
                    "Worldpiercer",
                    "Divine",
                    "Eternal",
                    "Godspear",
                    "Starbreaker",
                    "Sunpiercer",
                ],
            },
            "chestplate": {
                "common": ["Worn", "Rusty", "Cracked", "Leather"],
                "uncommon": ["Iron", "Steel", "Tempered", "Fine"],
                "rare": ["Runed", "Blessed", "Guardian's", "Knight's", "Arcane"],
                "epic": [
                    "Titan",
                    "Celestial",
                    "Infernal",
                    "Dragonbone",
                    "Eternal",
                    "Shadowguard",
                ],
                "legendary": [
                    "Godforged",
                    "Worldplate",
                    "Mythic",
                    "Voidplate",
                    "Divine",
                    "Heavenbound",
                ],
            },
            "helmet": {
                "common": ["Dented", "Old", "Cracked"],
                "uncommon": ["Iron", "Steel", "Reinforced", "Bronze"],
                "rare": ["Runed", "Blessed", "Arcane", "Guardian's", "Knight's"],
                "epic": [
                    "Celestial",
                    "Royal",
                    "Demonic",
                    "Ancient",
                    "Eternal",
                    "Stormforged",
                ],
                "legendary": [
                    "Crown of the Gods",
                    "Voidforged",
                    "Heaven's",
                    "Worldmind",
                    "Godhelm",
                ],
            },
            "boots": {
                "common": ["Worn", "Dusty", "Old", "Leather"],
                "uncommon": ["Steel-Toed", "Traveler's", "Light", "Firm"],
                "rare": ["Swift", "Runed", "Blessed", "Hunter's", "Arcane"],
                "epic": [
                    "Stormwalker",
                    "Celestial",
                    "Shadowstep",
                    "Infernal",
                    "Dragonhide",
                    "Eternal",
                ],
                "legendary": [
                    "Worldrunner",
                    "Voidstep",
                    "Heavenstep",
                    "Divine",
                    "Skywalker",
                ],
            },
            "pants": {
                "common": ["Torn", "Faded", "Patched", "Dusty", "Threadbare"],
                "uncommon": ["Sturdy", "Woolen", "Traveler's", "Linen", "Reinforced"],
                "rare": [
                    "Guardian's",
                    "Rune-stitched",
                    "Shadow",
                    "Explorer's",
                    "Silent",
                ],
                "epic": [
                    "Titanleg",
                    "Celestial",
                    "Infernal",
                    "Dragonhide",
                    "Eternal",
                    "Void-woven",
                ],
                "legendary": [
                    "God-King's",
                    "Worldwalker",
                    "Divine",
                    "Abyssle",
                    "Fate's Weave",
                ],
            },
            "pan": {
                "common": ["Greasy", "Old", "Burnt", "Cracked"],
                "uncommon": ["Iron", "Balanced", "Polished", "Steel"],
                "rare": ["Chef's", "Blessed", "Arcane", "Refined", "Cook's"],
                "epic": [
                    "Cursed",
                    "Enchanted",
                    "Flameforged",
                    "Hell's Kitchen",
                    "Infernal",
                ],
                "legendary": [
                    "Pan of Doom",
                    "Worldcooker",
                    "Celestial Skillet",
                    "Divine Cookware",
                    "God's Fryer",
                ],
            },
            "consumable": {
                "common": ["Weak", "Basic", "Thin", "Watery"],
                "uncommon": ["Refined", "Potent", "Pure", "Distilled"],
                "rare": ["Blessed", "Runed", "Arcane", "Strong", "Elven"],
                "epic": ["Radiant", "Forbidden", "Celestial", "Cursed", "Divine"],
                "legendary": [
                    "Elixir of Eternity",
                    "Blood of Gods",
                    "Essence of Infinity",
                    "Soulbrew",
                    "Phantom Nectar",
                ],
            },
            "gloves": {
                "common": ["Worn", "Thin", "Old", "Frayed"],
                "uncommon": ["Padded", "Iron", "Fine", "Steel"],
                "rare": ["Assassin's", "Blessed", "Runed", "Arcane", "Hunter's"],
                "epic": [
                    "Celestial",
                    "Shadow",
                    "Infernal",
                    "Stormgrip",
                    "Voidtouched",
                    "Eternal",
                ],
                "legendary": [
                    "Hand of God",
                    "Worldgrip",
                    "Heavenreach",
                    "Divine",
                    "Godclaw",
                ],
            },
            "sheald": {
                "common": ["Cracked", "Wooden", "Rusty", "Old"],
                "uncommon": ["Iron", "Steel", "Tempered", "Bronze"],
                "rare": ["Guardian's", "Runed", "Blessed", "Arcane", "Knight's"],
                "epic": [
                    "Titan",
                    "Celestial",
                    "Infernal",
                    "Stormguard",
                    "Eternal",
                    "Dragon",
                ],
                "legendary": [
                    "Worldguard",
                    "Godforged",
                    "Divine",
                    "Heaven's Bulwark",
                    "Voidshield",
                ],
            },
        }

        bases = {
            "sword": ["Blade", "Edge", "Saber", "Katana"],
            "knife": ["Dagger", "Knife", "Shiv", "Stiletto"],
            "bow": ["Bow", "Longbow", "Crossbow"],
            "stafe": ["Staff", "Rod", "Wand"],
            "spear": ["Spear", "Lance", "Pike"],
            "chestplate": ["Armor", "Cuirass", "Mail"],
            "helmet": ["Helm", "Crown", "Mask"],
            "boots": ["Boots", "Greaves", "Treads"],
            "pants": ["Pants", "Trousers", "Leggings"],
            "pan": ["Pan", "Skillet", "Frying Pan"],
            "consumable": ["Potion", "Elixir", "Brew"],
            "gloves": ["Gloves", "Gauntlets", "Hands"],
            "sheald": ["Shield", "Guard", "Aegis"],
        }

        suffixes = {
            "common": ["", "of the Apprentice", "", ""],
            "uncommon": ["", "of Focus", "", "of Fortitude"],
            "rare": ["of Power", "of Shadows", "of Frost", "of Fury"],
            "epic": ["of Souls", "of Chaos", "of Destiny", "of Eternity"],
            "legendary": [
                "of the Gods",
                "of Infinity",
                "of Oblivion",
                "of the End",
                "of Divinity",
            ],
        }

        prefix_list = prefixes.get(self.sub_type, {}).get(self.grade, ["Mysterious"])
        self.base = random.choice(bases.get(self.sub_type, ["Item"]))
        suffix_list = suffixes.get(self.grade, [""])

        self.prefix = random.choice(prefix_list)
        self.suffix = random.choice(suffix_list)

        # Low-grade items: sometimes skip prefix/suffix entirely
        if self.grade in ["common", "uncommon"]:
            if random.random() < 0.4:
                self.prefix = ""
            if random.random() < 0.6:
                self.suffix = ""

        name = f"{self.prefix} {self.base} {self.suffix}".strip()
        return " ".join(name.split())

    # ---- STATS ----
    def generate_stats(self):
        base_stat = {
            "sword": {"atk": (5, 10), "crit_chance": (1, 5), "crit_bonus": (10, 25)},
            "knife": {"atk": (3, 8), "crit_chance": (3, 8), "crit_bonus": (15, 30)},
            "bow": {"atk": (4, 9), "sp_atk": (2, 5), "crit_chance": (2, 6)},
            "stafe": {"sp_atk": (6, 12), "max_mp": (10, 25)},
            "spear": {"atk": (5, 10), "crit_chance": (1, 4)},
            "chestplate": {"def_": (6, 12), "max_hp": (10, 25)},
            "helmet": {"def_": (4, 8), "sp_def": (2, 5)},
            "boots": {"max_hp": (5, 10), "def_": (2, 5)},
            "pants": {"def_": (3, 7), "max_hp": (8, 15)},
            "pan": {"atk": (1, 5), "crit_chance": (10, 15), "crit_bonus": (50, 100)},
            "consumable": {"max_mp": (20, 40)},
            "gloves": {"atk": (2, 5), "sp_atk": (2, 5)},
            "sheald": {"def_": (8, 16), "sp_def": (6, 12)},
        }

        stat_ranges = base_stat.get(self.sub_type, {"mystery": (0, 1)})
        grade_multiplier = {
            "common": 1.0,
            "uncommon": 1.5,
            "rare": 2.0,
            "epic": 2.5,
            "legendary": 3.5,
        }.get(self.grade, 1.0)

        stat_ranges["price"] = (10, 20)

        stats = {}
        for stat, (low, high) in stat_ranges.items():
            value = random.uniform(low, high) * grade_multiplier * (1 + self.level / 5)
            stats[stat] = round(value, 2)

        # Apply the generated stats to the object
        for stat, value in stats.items():
            setattr(self, stat, int(value))

        return stats

    # ---- FLAVOR ----
    def generate_flavor_text(self):
        name = self.name.lower()

        # Item type specific narrative templates by grade
        item_type_narratives = {
            "common": {
                "sword": [
                    "This {blade_description} was {creation_story}. It {combat_behavior} and {special_quality}.",
                    "A simple weapon that {physical_description}. It serves well for {usage_scenario}.",
                    "This blade {historical_significance}. The steel {metal_quality}, making it {practical_quality}.",
                ],
                "knife": [
                    "This dagger {stealth_quality} and {assassin_history}. The edge {sharpness_description}, good for {usage_scenario}.",
                    "A basic blade that {physical_trait}. It {movement_quality} and has {concealment_feature}.",
                    "Made for {creation_purpose}, this knife {balance_description}. It {stealth_feature} and feels {wield_feeling}.",
                ],
                "bow": [
                    "The bow {draw_characteristic} and {aiming_quality}. Each arrow {arrow_behavior}, making it {hunting_style}.",
                    "Carved from {material_source}, this bow {performance_trait}. The string {string_quality}, and shots {shot_effect}.",
                    "A hunter's tool that {reliability_description}. It {weather_resistance} and {accuracy_feature} for {ideal_usage}.",
                ],
                "stafe": [
                    "The staff channels {magical_energy} through its {physical_feature}. It {spellcasting_enhancement}.",
                    "Simple power flows through this staff, {energy_manifestation}. The {focus_component} {component_behavior}.",
                    "A mage's aid that {attunement_quality}. The wood {material_memory} while the crystal {crystal_power}.",
                ],
                "spear": [
                    "This spear {reach_advantage} with {thrust_quality}. The tip {tip_material} and {penetration_capability}.",
                    "Balanced for {throwing_capability}, the spear {flight_characteristic}. In melee, it {melee_performance}.",
                    "A practical tool that {versatility_description}. The shaft {flex_characteristic} while the head {head_quality}.",
                ],
                "chestplate": [
                    "The armor {protection_level} with {comfort_feature}. Made with {forging_method}, it {practical_history}.",
                    "This chestplate {fit_description} and {movement_capability}. It provides {defense_quality} against {threat_type}.",
                    "Standard issue armor that {battle_history}. The construction {craftsmanship_quality} ensures {protection_assurance}.",
                ],
                "helmet": [
                    "The helmet {vision_clarity} while offering {head_protection}. Its design {design_advantage}.",
                    "Made to {design_purpose}, this helm {comfort_aspect}. The metal {metal_treatment}.",
                    "A protective piece that {intimidation_factor}. It {weight_distribution} and provides {situational_advantage}.",
                ],
                "boots": [
                    "These boots {travel_endurance} and {terrain_adaptation}. The soles {traction_quality} while the leather {material_durability}.",
                    "Made for {travel_purpose}, they {comfort_feature} on journeys. They offer {weather_protection} and {stealth_capability}.",
                    "Practical boots that {agility_description}. They {movement_enhancement} and are {maintenance_quality}.",
                ],
                "pants": [
                    "These pants {durability_description} and {comfort_feature}. They serve well for {usage_scenario}.",
                    "A simple pair that {physical_description}. They offer {practical_benefit} for everyday wear.",
                    "Standard trousers that {historical_significance}. They {practical_quality} and {mobility_feature}.",
                ],
                "pan": [
                    "This pan {cooking_performance} with {heat_distribution}. The handle {grip_comfort}.",
                    "A kitchen tool that {food_quality}. The surface {nonstick_feature} while the weight {balance_characteristic}.",
                    "Made in {creation_kitchen}, it {versatile_cooking}. The metal {heat_retention} and it bears {kitchen_reputation}.",
                ],
                "consumable": [
                    "The liquid {visual_appearance} with {scent_description}. When consumed, it {immediate_effect}.",
                    "Brewed using {ingredient_source}, this potion {potency_indication}. It provides {effect_description}.",
                    "A simple concoction that {appearance_characteristic}. It {texture_quality} and offers {practical_effect}.",
                ],
                "gloves": [
                    "These gloves {dexterity_level} with {protection_value}. The material {flexibility} allows for {precision_capability}.",
                    "Made for {intended_use}, they {grip_enhancement}. The fingertips {tactile_sensitivity}.",
                    "Basic handwear that {comfort_feeling}. The gloves {temperature_regulation} and provide {specialized_protection}.",
                ],
                "sheald": [
                    "The shield {defensive_capability} with {weight_characteristic}. The face {surface_description}.",
                    "A basic bulwark that {protection_history}. The boss {impact_resistance}.",
                    "Made to withstand {threat_level}, this shield {durability_testament}. It {combat_utility}.",
                ],
            },
            "uncommon": {
                "sword": [
                    "This {blade_description} was {creation_story}. In combat, it {combat_behavior}, and {special_quality}.",
                    "Forged {forging_circumstances}, the blade {physical_description}. Those who wield it find that {wielder_experience}.",
                    "A reliable weapon that {historical_significance}. The steel {metal_quality}, and it {magical_property}.",
                ],
                "knife": [
                    "This dagger {stealth_quality} and {assassin_history}. The edge {sharpness_description}, perfect for {usage_scenario}.",
                    "Well-made and {physical_trait}, this blade {movement_quality}. It has {concealment_feature} and {deadly_characteristic}.",
                    "Crafted for {creation_purpose}, the knife {balance_description}. It {stealth_feature} and feels {wield_feeling}.",
                ],
                "bow": [
                    "The bow {draw_characteristic} and {aiming_quality}. Each arrow {arrow_behavior}, making it {hunting_style}.",
                    "Carved from {material_source}, this bow {performance_trait}. The string {string_quality}, and shots {shot_effect}.",
                    "A hunter's companion that {reliability_description}. It {weather_resistance} and {accuracy_feature} for {ideal_usage}.",
                ],
                "stafe": [
                    "The staff channels {magical_energy} through its {physical_feature}. It {spellcasting_enhancement} and {arcane_history}.",
                    "Stable power flows through this staff, {energy_manifestation}. The {focus_component} {component_behavior}, allowing {magical_capability}.",
                    "A mage's focus that {attunement_quality}. The wood {material_memory} while the crystal {crystal_power} for {spell_enhancement}.",
                ],
                "spear": [
                    "This spear {reach_advantage} with {thrust_quality}. The tip {tip_material} and {penetration_capability}, good for {combat_style}.",
                    "Balanced for {throwing_capability}, the spear {flight_characteristic}. In melee, it {melee_performance} and has {durability_feature}.",
                    "A warrior's tool that {versatility_description}. The shaft {flex_characteristic} while the head {head_quality} for {tactical_advantage}.",
                ],
                "chestplate": [
                    "The armor {protection_level} with {comfort_feature}. Forged {forging_method}, it has {historical_provenance}.",
                    "This chestplate {fit_description} and {movement_capability}. The plates {material_construction} provide {defense_quality}.",
                    "Well-made armor that {battle_history}. The craftsmanship {craftsmanship_quality} ensures {protection_assurance}.",
                ],
                "helmet": [
                    "The helmet {vision_clarity} while offering {head_protection}. Its design {design_advantage} and it has {special_feature}.",
                    "Crafted to {design_purpose}, this helm {comfort_aspect}. The metal {metal_treatment} and it {environmental_protection}.",
                    "A protective piece that {intimidation_factor}. It {weight_distribution} and provides {situational_advantage} in combat.",
                ],
                "boots": [
                    "These boots {travel_endurance} and {terrain_adaptation}. The soles {traction_quality} while the leather {material_durability}.",
                    "Made for {travel_purpose}, they {comfort_feature} on long journeys. The craftsmanship ensures {weather_protection} and {stealth_capability}.",
                    "Reliable boots that {agility_description}. They {movement_enhancement} and have {special_mobility}.",
                ],
                "pants": [
                    "These pants {physical_description}. They {special_quality} and serve well for {usage_scenario}.",
                    "A reliable pair that {historical_significance}. They offer {practical_benefit} and {comfort_feature}.",
                    "Well-made trousers that {mobility_feature}. They {special_quality} and {durability_description}.",
                ],
                "pan": [
                    "This pan {cooking_performance} with {heat_distribution}. The handle {grip_comfort} and it has {culinary_history}.",
                    "A quality kitchen tool that {food_quality}. The surface {nonstick_feature} while the weight {balance_characteristic} for {cooking_style}.",
                    "Forged in {creation_kitchen}, it {versatile_cooking}. The metal {heat_retention} and it bears {kitchen_reputation}.",
                ],
                "consumable": [
                    "The liquid {visual_appearance} with {scent_description}. When consumed, it {immediate_effect} and leaves {aftertaste_sensation}.",
                    "Brewed using {ingredient_source}, this potion {potency_indication}. The aroma {scent_quality} promises {effect_description}.",
                    "A well-made concoction that {appearance_characteristic}. The viscosity {texture_quality} and it emanates {energy_signature}.",
                ],
                "gloves": [
                    "These gloves {dexterity_level} with {protection_value}. The material {flexibility} allows for {precision_capability}.",
                    "Crafted for {intended_use}, they {grip_enhancement}. The fingertips {tactile_sensitivity} and the palms {palm_protection}.",
                    "Quality handwear that {comfort_feeling}. The gloves {temperature_regulation} and provide {specialized_protection}.",
                ],
                "sheald": [
                    "The shield {defensive_capability} with {weight_characteristic}. The face {surface_description} and it has {deflection_quality}.",
                    "A reliable bulwark that {protection_history}. The boss {impact_resistance} while the rim {edge_advantage}.",
                    "Forged to withstand {threat_level}, this shield {durability_testament}. It {combat_utility} and offers {tactical_defense}.",
                ],
            },
            "rare": {
                "sword": [
                    "This {blade_description} was {creation_story}. In combat, it {combat_behavior}, and {special_quality}.",
                    "Forged {forging_circumstances}, the blade {physical_description}. Those who wield it find that {wielder_experience}.",
                    "An exceptional weapon that {historical_significance}. The steel {metal_quality}, and it {magical_property}.",
                ],
                "knife": [
                    "This exceptional dagger {stealth_quality} and {assassin_history}. The edge {sharpness_description}, perfect for {usage_scenario}.",
                    "Precision-made and {physical_trait}, this blade {movement_quality}. It has {concealment_feature} and {deadly_characteristic}.",
                    "Master-crafted for {creation_purpose}, the knife {balance_description}. It {stealth_feature} and feels {wield_feeling}.",
                ],
                "bow": [
                    "The exceptional bow {draw_characteristic} and {aiming_quality}. Each arrow {arrow_behavior}, making it {hunting_style}.",
                    "Expertly carved from {material_source}, this bow {performance_trait}. The string {string_quality}, and shots {shot_effect}.",
                    "A hunter's prized companion that {reliability_description}. It {weather_resistance} and {accuracy_feature} for {ideal_usage}.",
                ],
                "stafe": [
                    "The staff channels {magical_energy} through its {physical_feature}. It {spellcasting_enhancement} and {arcane_history}.",
                    "Ancient power flows through this staff, {energy_manifestation}. The {focus_component} {component_behavior}, allowing {magical_capability}.",
                    "A mage's prized focus that {attunement_quality}. The wood {material_memory} while the crystal {crystal_power} for {spell_enhancement}.",
                ],
                "spear": [
                    "This exceptional spear {reach_advantage} with {thrust_quality}. The tip {tip_material} and {penetration_capability}, ideal for {combat_style}.",
                    "Perfectly balanced for {throwing_capability}, the spear {flight_characteristic}. In melee, it {melee_performance} and has {durability_feature}.",
                    "A warrior's prized tool that {versatility_description}. The shaft {flex_characteristic} while the head {head_quality} for {tactical_advantage}.",
                ],
                "chestplate": [
                    "The armor {protection_level} with {comfort_feature}. Forged {forging_method}, it has {historical_provenance} and {battle_reputation}.",
                    "This exceptional chestplate {fit_description} and {movement_capability}. The plates {material_construction} provide {defense_quality} against {threat_type}.",
                    "Superior armor worn by {previous_owner}. The craftsmanship {craftsmanship_quality} ensures {protection_assurance}.",
                ],
                "helmet": [
                    "The helmet {vision_clarity} while offering {head_protection}. Its design {design_advantage} and it has {special_feature}.",
                    "Expertly crafted to {design_purpose}, this helm {comfort_aspect}. The metal {metal_treatment} and it {environmental_protection}.",
                    "A superior protective piece that {intimidation_factor}. It {weight_distribution} and provides {situational_advantage} in combat.",
                ],
                "boots": [
                    "These exceptional boots {travel_endurance} and {terrain_adaptation}. The soles {traction_quality} while the leather {material_durability}.",
                    "Expertly made for {travel_purpose}, they {comfort_feature} on long journeys. The craftsmanship ensures {weather_protection} and {stealth_capability}.",
                    "Superior boots that {agility_description}. They {movement_enhancement} and have {special_mobility}.",
                ],
                "pants": [
                    "These pants {physical_description}. They {special_quality} and {magical_property}.",
                    "An exceptional pair that {historical_significance}. They {mobility_feature} and {special_quality}.",
                    "Superior trousers that {wielder_experience}. They {magical_property} and {comfort_feature}.",
                ],
                "pan": [
                    "This master-crafted pan {cooking_performance} with {heat_distribution}. The handle {grip_comfort} and it has {culinary_history}.",
                    "A chef's prized tool that {food_quality}. The surface {nonstick_feature} while the weight {balance_characteristic} for {cooking_style}.",
                    "Expertly forged in {creation_kitchen}, it {versatile_cooking}. The metal {heat_retention} and it bears {kitchen_reputation}.",
                ],
                "consumable": [
                    "The exceptional liquid {visual_appearance} with {scent_description}. When consumed, it {immediate_effect} and leaves {aftertaste_sensation}.",
                    "Expertly brewed using {ingredient_source}, this potion {potency_indication}. The aroma {scent_quality} promises {effect_description}.",
                    "A masterful concoction that {appearance_characteristic}. The viscosity {texture_quality} and it emanates {energy_signature}.",
                ],
                "gloves": [
                    "These superior gloves {dexterity_level} with {protection_value}. The material {flexibility} allows for {precision_capability}.",
                    "Expertly crafted for {intended_use}, they {grip_enhancement}. The fingertips {tactile_sensitivity} and the palms {palm_protection}.",
                    "Masterwork handwear that {comfort_feeling}. The gloves {temperature_regulation} and provide {specialized_protection}.",
                ],
                "sheald": [
                    "The superior shield {defensive_capability} with {weight_characteristic}. The face {surface_description} and it has {deflection_quality}.",
                    "An exceptional bulwark that {protection_history}. The boss {impact_resistance} while the rim {edge_advantage} in combat.",
                    "Expertly forged to withstand {threat_level}, this shield {durability_testament}. It {combat_utility} and offers {tactical_defense}.",
                ],
            },
            "epic": {
                "sword": [
                    "This {blade_description} was {creation_story}. In combat, it {combat_behavior}, and {special_quality}.",
                    "Forged {forging_circumstances}, the blade {physical_description}. Those who wield it find that {wielder_experience}.",
                    "A legendary weapon that {historical_significance}. The steel {metal_quality}, and it {magical_property}.",
                ],
                "knife": [
                    "This legendary dagger {stealth_quality} and {assassin_history}. The edge {sharpness_description}, perfect for {usage_scenario}.",
                    "Whisper-thin and {physical_trait}, this blade {movement_quality}. It has {concealment_feature} and {deadly_characteristic}.",
                    "Master-crafted for {creation_purpose}, the knife {balance_description}. It {stealth_feature} and feels {wield_feeling}.",
                ],
                "bow": [
                    "The legendary bow {draw_characteristic} and {aiming_quality}. Each arrow {arrow_behavior}, making it {hunting_style}.",
                    "Exquisitely carved from {material_source}, this bow {performance_trait}. The string {string_quality}, and shots {shot_effect}.",
                    "A hunter's legendary companion that {reliability_description}. It {weather_resistance} and {accuracy_feature} for {ideal_usage}.",
                ],
                "stafe": [
                    "The staff channels {magical_energy} through its {physical_feature}. It {spellcasting_enhancement} and {arcane_history}.",
                    "Ancient power flows through this staff, {energy_manifestation}. The {focus_component} {component_behavior}, allowing {magical_capability}.",
                    "A mage's legendary focus that {attunement_quality}. The wood {material_memory} while the crystal {crystal_power} for {spell_enhancement}.",
                ],
                "spear": [
                    "This legendary spear {reach_advantage} with {thrust_quality}. The tip {tip_material} and {penetration_capability}, ideal for {combat_style}.",
                    "Perfectly balanced for {throwing_capability}, the spear {flight_characteristic}. In melee, it {melee_performance} and has {durability_feature}.",
                    "A warrior's legendary tool that {versatility_description}. The shaft {flex_characteristic} while the head {head_quality} for {tactical_advantage}.",
                ],
                "chestplate": [
                    "The armor {protection_level} with {comfort_feature}. Forged {forging_method}, it has {historical_provenance} and {battle_reputation}.",
                    "This legendary chestplate {fit_description} and {movement_capability}. The plates {material_construction} provide {defense_quality} against {threat_type}.",
                    "Worn by {previous_owner}, the armor {battle_history}. The craftsmanship {craftsmanship_quality} ensures {protection_assurance}.",
                ],
                "helmet": [
                    "The helmet {vision_clarity} while offering {head_protection}. Its design {design_advantage} and it has {special_feature}.",
                    "Legendarily crafted to {design_purpose}, this helm {comfort_aspect}. The metal {metal_treatment} and it {environmental_protection}.",
                    "A legendary protective piece that {intimidation_factor}. It {weight_distribution} and provides {situational_advantage} in combat.",
                ],
                "boots": [
                    "These legendary boots {travel_endurance} and {terrain_adaptation}. The soles {traction_quality} while the leather {material_durability}.",
                    "Legendarily made for {travel_purpose}, they {comfort_feature} on long journeys. The craftsmanship ensures {weather_protection} and {stealth_capability}.",
                    "Legendary boots that {agility_description}. They {movement_enhancement} and have {special_mobility}.",
                ],
                "pants": [
                    "These pants {physical_description}. They {special_quality} and {magical_property}.",
                    "A legendary pair that {historical_significance}. They {mobility_feature} and {special_quality}.",
                    "Mythic trousers that {wielder_experience}. They {magical_property} and {defensive_feature}.",
                ],
                "pan": [
                    "This legendary pan {cooking_performance} with {heat_distribution}. The handle {grip_comfort} and it has {culinary_history}.",
                    "A legendary kitchen weapon that {food_quality}. The surface {nonstick_feature} while the weight {balance_characteristic} for {cooking_style}.",
                    "Legendarily forged in {creation_kitchen}, it {versatile_cooking}. The metal {heat_retention} and it bears {kitchen_reputation}.",
                ],
                "consumable": [
                    "The legendary liquid {visual_appearance} with {scent_description}. When consumed, it {immediate_effect} and leaves {aftertaste_sensation}.",
                    "Legendarily brewed using {ingredient_source}, this potion {potency_indication}. The aroma {scent_quality} promises {effect_description}.",
                    "A legendary concoction that {appearance_characteristic}. The viscosity {texture_quality} and it emanates {energy_signature}.",
                ],
                "gloves": [
                    "These legendary gloves {dexterity_level} with {protection_value}. The material {flexibility} allows for {precision_capability}.",
                    "Legendarily crafted for {intended_use}, they {grip_enhancement}. The fingertips {tactile_sensitivity} and the palms {palm_protection}.",
                    "Legendary handwear that {comfort_feeling}. The gloves {temperature_regulation} and provide {specialized_protection}.",
                ],
                "sheald": [
                    "The legendary shield {defensive_capability} with {weight_characteristic}. The face {surface_description} and it has {deflection_quality}.",
                    "A legendary bulwark that {protection_history}. The boss {impact_resistance} while the rim {edge_advantage} in combat.",
                    "Legendarily forged to withstand {threat_level}, this shield {durability_testament}. It {combat_utility} and offers {tactical_defense}.",
                ],
            },
            "legendary": {
                "sword": [
                    "This {blade_description} was {creation_story}. In combat, it {combat_behavior}, and {special_quality}.",
                    "Forged {forging_circumstances}, the blade {physical_description}. Those who wield it find that {wielder_experience}.",
                    "A weapon of myth that {historical_significance}. The steel {metal_quality}, and it {magical_property}.",
                ],
                "knife": [
                    "This mythical dagger {stealth_quality} and {assassin_history}. The edge {sharpness_description}, perfect for {usage_scenario}.",
                    "Reality-thin and {physical_trait}, this blade {movement_quality}. It has {concealment_feature} and {deadly_characteristic}.",
                    "Divinely crafted for {creation_purpose}, the knife {balance_description}. It {stealth_feature} and feels {wield_feeling}.",
                ],
                "bow": [
                    "The mythical bow {draw_characteristic} and {aiming_quality}. Each arrow {arrow_behavior}, making it {hunting_style}.",
                    "Divinely carved from {material_source}, this bow {performance_trait}. The string {string_quality}, and shots {shot_effect}.",
                    "A hunter's mythical companion that {reliability_description}. It {weather_resistance} and {accuracy_feature} for {ideal_usage}.",
                ],
                "stafe": [
                    "The staff channels {magical_energy} through its {physical_feature}. It {spellcasting_enhancement} and {arcane_history}.",
                    "Primordial power flows through this staff, {energy_manifestation}. The {focus_component} {component_behavior}, allowing {magical_capability}.",
                    "A mage's mythical focus that {attunement_quality}. The wood {material_memory} while the crystal {crystal_power} for {spell_enhancement}.",
                ],
                "spear": [
                    "This mythical spear {reach_advantage} with {thrust_quality}. The tip {tip_material} and {penetration_capability}, ideal for {combat_style}.",
                    "Divinely balanced for {throwing_capability}, the spear {flight_characteristic}. In melee, it {melee_performance} and has {durability_feature}.",
                    "A warrior's mythical tool that {versatility_description}. The shaft {flex_characteristic} while the head {head_quality} for {tactical_advantage}.",
                ],
                "chestplate": [
                    "The armor {protection_level} with {comfort_feature}. Forged {forging_method}, it has {historical_provenance} and {battle_reputation}.",
                    "This mythical chestplate {fit_description} and {movement_capability}. The plates {material_construction} provide {defense_quality} against {threat_type}.",
                    "Worn by {previous_owner}, the armor {battle_history}. The craftsmanship {craftsmanship_quality} ensures {protection_assurance}.",
                ],
                "helmet": [
                    "The helmet {vision_clarity} while offering {head_protection}. Its design {design_advantage} and it has {special_feature}.",
                    "Mythically crafted to {design_purpose}, this helm {comfort_aspect}. The metal {metal_treatment} and it {environmental_protection}.",
                    "A mythical protective piece that {intimidation_factor}. It {weight_distribution} and provides {situational_advantage} in combat.",
                ],
                "boots": [
                    "These mythical boots {travel_endurance} and {terrain_adaptation}. The soles {traction_quality} while the leather {material_durability}.",
                    "Mythically made for {travel_purpose}, they {comfort_feature} on long journeys. The craftsmanship ensures {weather_protection} and {stealth_capability}.",
                    "Mythical boots that {agility_description}. They {movement_enhancement} and have {special_mobility}.",
                ],
                "pants": [
                    "These pants {physical_description}. They {special_quality} and {magical_property}.",
                    "An artifact pair that {historical_significance}. They {mobility_feature} and {special_quality}.",
                    "Divine trousers that {wielder_experience}. They {magical_property} and {reality_feature}.",
                ],
                "pan": [
                    "This mythical pan {cooking_performance} with {heat_distribution}. The handle {grip_comfort} and it has {culinary_history}.",
                    "A mythical kitchen weapon that {food_quality}. The surface {nonstick_feature} while the weight {balance_characteristic} for {cooking_style}.",
                    "Mythically forged in {creation_kitchen}, it {versatile_cooking}. The metal {heat_retention} and it bears {kitchen_reputation}.",
                ],
                "consumable": [
                    "The mythical liquid {visual_appearance} with {scent_description}. When consumed, it {immediate_effect} and leaves {aftertaste_sensation}.",
                    "Mythically brewed using {ingredient_source}, this potion {potency_indication}. The aroma {scent_quality} promises {effect_description}.",
                    "A mythical concoction that {appearance_characteristic}. The viscosity {texture_quality} and it emanates {energy_signature}.",
                ],
                "gloves": [
                    "These mythical gloves {dexterity_level} with {protection_value}. The material {flexibility} allows for {precision_capability}.",
                    "Mythically crafted for {intended_use}, they {grip_enhancement}. The fingertips {tactile_sensitivity} and the palms {palm_protection}.",
                    "Mythical handwear that {comfort_feeling}. The gloves {temperature_regulation} and provide {specialized_protection}.",
                ],
                "sheald": [
                    "The mythical shield {defensive_capability} with {weight_characteristic}. The face {surface_description} and it has {deflection_quality}.",
                    "A mythical bulwark that {protection_history}. The boss {impact_resistance} while the rim {edge_advantage} in combat.",
                    "Mythically forged to withstand {threat_level}, this shield {durability_testament}. It {combat_utility} and offers {tactical_defense}.",
                ],
            },
        }

        # Default templates for any missing item types
        default_templates = {
            "common": [
                "This {item_type} {practical_description}. It serves well for {usage_scenario}.",
                "A simple {item_type} that {physical_description}. It offers {practical_benefit}.",
                "Standard {item_type} that {historical_significance}. It {practical_quality}.",
            ],
            "uncommon": [
                "This {item_type} {physical_description}. It {special_quality} and serves well for {usage_scenario}.",
                "A reliable {item_type} that {historical_significance}. It offers {practical_benefit}.",
                "Well-made {item_type} that {combat_behavior}. It {special_quality}.",
            ],
            "rare": [
                "This {item_type} {physical_description}. It {special_quality} and {magical_property}.",
                "An exceptional {item_type} that {historical_significance}. It {combat_behavior} and {special_quality}.",
                "Superior {item_type} that {wielder_experience}. It {magical_property}.",
            ],
            "epic": [
                "This {item_type} {physical_description}. It {special_quality} and {magical_property}.",
                "A legendary {item_type} that {historical_significance}. It {combat_behavior} and {special_quality}.",
                "Mythic {item_type} that {wielder_experience}. It {magical_property}.",
            ],
            "legendary": [
                "This {item_type} {physical_description}. It {special_quality} and {magical_property}.",
                "An artifact {item_type} that {historical_significance}. It {combat_behavior} and {special_quality}.",
                "Divine {item_type} that {wielder_experience}. It {magical_property}.",
            ],
        }

        # Complete phrase banks by grade
        phrase_banks = {
            "common": {
                # Sword phrases
                "blade_description": [
                    "has a serviceable edge",
                    "shows basic craftsmanship",
                    "is functional and reliable",
                ],
                "creation_story": [
                    "made by the local blacksmith",
                    "produced in a military forge",
                    "crafted for militia use",
                ],
                "combat_behavior": [
                    "swings with decent balance",
                    "holds an edge through several fights",
                    "performs reliably in skirmishes",
                ],
                "special_quality": [
                    "requires little maintenance",
                    "is easy to sharpen",
                    "won't break under normal use",
                ],
                "physical_description": [
                    "has a plain but functional design",
                    "shows signs of regular use",
                    "bears the marks of practical craftsmanship",
                ],
                "usage_scenario": [
                    "hunting and basic defense",
                    "guarding caravans",
                    "patrolling city streets",
                ],
                "historical_significance": [
                    "has seen typical service",
                    "was standard issue in local garrisons",
                    "has been used by many travelers",
                ],
                "metal_quality": [
                    "is made of reliable steel",
                    "holds up well to regular use",
                    "won't rust easily",
                ],
                "practical_quality": [
                    "a dependable everyday tool",
                    "good value for the coin",
                    "reliable when needed",
                ],
                "forging_circumstances": [
                    "with standard techniques",
                    "in a basic forge",
                    "using common methods",
                ],
                "wielder_experience": [
                    "it feels comfortable in hand",
                    "the grip is secure",
                    "it responds well to basic techniques",
                ],
                "magical_property": [
                    "resists rust well",
                    "holds an edge decently",
                    "feels balanced when swung",
                ],
                # Knife phrases
                "stealth_quality": [
                    "moves quietly through the air",
                    "makes little sound when drawn",
                    "is easily concealed",
                ],
                "assassin_history": [
                    "has seen discreet use",
                    "was carried by messengers",
                    "has been used for utility tasks",
                ],
                "sharpness_description": [
                    "is serviceably sharp",
                    "cuts cleanly",
                    "holds an edge well",
                ],
                "physical_trait": [
                    "well-balanced",
                    "moderately weighted",
                    "comfortably sized",
                ],
                "movement_quality": [
                    "moves smoothly",
                    "handles easily",
                    "responds well to the wrist",
                ],
                "concealment_feature": [
                    "a simple sheath",
                    "compact dimensions",
                    "discreet appearance",
                ],
                "creation_purpose": [
                    "everyday utility",
                    "hunting and crafting",
                    "general purpose use",
                ],
                "balance_description": [
                    "feels natural in hand",
                    "is well-proportioned",
                    "has comfortable weight distribution",
                ],
                "stealth_feature": [
                    "doesn't catch light easily",
                    "moves silently",
                    "is easily hidden",
                ],
                "wield_feeling": [
                    "secure and reliable",
                    "comfortable and familiar",
                    "balanced and ready",
                ],
                "deadly_characteristic": [
                    "delivers precise cuts",
                    "penetrates effectively",
                    "strikes true",
                ],
                # Bow phrases
                "draw_characteristic": [
                    "requires moderate strength",
                    "has a smooth pull",
                    "draws consistently",
                ],
                "aiming_quality": [
                    "holds steady when drawn",
                    "allows decent accuracy",
                    "provides reliable sighting",
                ],
                "arrow_behavior": [
                    "flies straight and true",
                    "maintains good trajectory",
                    "hits with consistent force",
                ],
                "hunting_style": [
                    "effective for small game",
                    "suitable for practice",
                    "reliable for basic hunting",
                ],
                "material_source": [
                    "seasoned wood",
                    "local timber",
                    "reliable hardwood",
                ],
                "performance_trait": [
                    "shoots consistently",
                    "performs reliably",
                    "maintains its shape",
                ],
                "string_quality": [
                    "is durable and strong",
                    "holds tension well",
                    "resists fraying",
                ],
                "shot_effect": [
                    "hit with satisfying impact",
                    "fly with good speed",
                    "maintain accuracy",
                ],
                "reliability_description": [
                    "rarely fails its user",
                    "performs consistently",
                    "stands up to regular use",
                ],
                "weather_resistance": [
                    "handles normal conditions",
                    "works in typical weather",
                    "resists minor moisture",
                ],
                "accuracy_feature": [
                    "consistent arrow flight",
                    "reliable aiming",
                    "steady hold",
                ],
                "ideal_usage": [
                    "target practice and hunting",
                    "basic archery needs",
                    "recreational shooting",
                ],
                # Staff phrases
                "magical_energy": [
                    "subtle arcane forces",
                    "basic mystical power",
                    "elemental essence",
                ],
                "physical_feature": [
                    "carved surface",
                    "natural grain pattern",
                    "simple crystal setting",
                ],
                "spellcasting_enhancement": [
                    "aids focus for beginners",
                    "helps channel basic spells",
                    "supports elementary magic",
                ],
                "energy_manifestation": [
                    "glowing faintly when used",
                    "warming to the touch during casting",
                    "emitting soft light spells",
                ],
                "focus_component": ["crystal", "carving", "metal caps"],
                "component_behavior": [
                    "glows during spellcasting",
                    "warms with use",
                    "resonates with magic",
                ],
                "attunement_quality": [
                    "responds to basic commands",
                    "accepts simple enchantments",
                    "works with novice mages",
                ],
                "material_memory": [
                    "retains traces of spells cast",
                    "remembers its magical history",
                    "stores residual energy",
                ],
                "crystal_power": [
                    "amplifies spell effects slightly",
                    "focuses magical energy",
                    "stabilizes casting",
                ],
                "arcane_history": [
                    "has seen modest magical use",
                    "was used by apprentice mages",
                    "has basic enchantments",
                ],
                "magical_capability": [
                    "enhanced spell focus",
                    "improved energy channeling",
                    "better magical control",
                ],
                "spell_enhancement": [
                    "more precise spellwork",
                    "enhanced magical effects",
                    "improved casting efficiency",
                ],
                # Spear phrases
                "reach_advantage": [
                    "keeps enemies at distance",
                    "provides good range",
                    "allows striking from safety",
                ],
                "thrust_quality": [
                    "penetrates effectively",
                    "moves quickly forward",
                    "strikes with force",
                ],
                "tip_material": ["hardened steel", "tempered iron", "sharpened metal"],
                "penetration_capability": [
                    "pierces light armor",
                    "penetrates deeply",
                    "cuts through defenses",
                ],
                "throwing_capability": [
                    "flies straight when thrown",
                    "maintains balance in air",
                    "hits with good force",
                ],
                "flight_characteristic": [
                    "spins steadily",
                    "flies true",
                    "maintains trajectory",
                ],
                "melee_performance": [
                    "blocks and parries well",
                    "strikes quickly",
                    "defends effectively",
                ],
                "versatility_description": [
                    "serves multiple combat roles",
                    "adapts to different situations",
                    "works in various scenarios",
                ],
                "flex_characteristic": [
                    "bends without breaking",
                    "absorbs impact well",
                    "returns to true",
                ],
                "head_quality": [
                    "holds sharpness well",
                    "resists damage",
                    "maintains its point",
                ],
                "combat_style": [
                    "defensive formations",
                    "hunting large game",
                    "single combat",
                ],
                "durability_feature": [
                    "withstands heavy use",
                    "resists breaking",
                    "maintains integrity",
                ],
                "tactical_advantage": [
                    "controlling engagement distance",
                    "maintaining defensive positions",
                    "pressuring opponents",
                ],
                # Chestplate phrases
                "protection_level": [
                    "offers basic protection",
                    "stops common weapons",
                    "provides adequate defense",
                ],
                "comfort_feature": [
                    "is reasonably comfortable",
                    "allows decent movement",
                    "doesn't chafe too much",
                ],
                "forging_method": [
                    "standard smithing techniques",
                    "common armor-making methods",
                    "traditional forging processes",
                ],
                "practical_history": [
                    "has served several owners well",
                    "shows honest wear from use",
                    "has protected many in minor skirmishes",
                ],
                "fit_description": [
                    "fits most body types",
                    "adjusts reasonably well",
                    "is comfortable enough for extended wear",
                ],
                "movement_capability": [
                    "allows for basic combat maneuvers",
                    "doesn't restrict movement too much",
                    "is flexible enough for most situations",
                ],
                "defense_quality": [
                    "reliable protection",
                    "adequate defense value",
                    "solid coverage",
                ],
                "threat_type": [
                    "common bandits and wildlife",
                    "typical combat threats",
                    "everyday dangers",
                ],
                "battle_history": [
                    "has seen minor skirmishes",
                    "bears scratches from typical use",
                    "has protected its wearer adequately",
                ],
                "craftsmanship_quality": [
                    "is competently made",
                    "shows decent workmanship",
                    "will last with proper care",
                ],
                "protection_assurance": [
                    "the wearer can face common threats with confidence",
                    "it provides reliable protection for its class",
                    "most attacks will be turned aside",
                ],
                "historical_provenance": [
                    "has seen typical military service",
                    "was used in local conflicts",
                    "has protected town guards",
                ],
                "material_construction": [
                    "standard steel plates",
                    "basic metal construction",
                    "common protective materials",
                ],
                # Helmet phrases
                "vision_clarity": [
                    "allows good visibility",
                    "provides clear sight lines",
                    "offers unobstructed view",
                ],
                "head_protection": [
                    "solid impact resistance",
                    "reliable cranial coverage",
                    "good defensive coverage",
                ],
                "design_advantage": [
                    "doesn't obstruct hearing",
                    "allows good ventilation",
                    "provides comfortable wear",
                ],
                "design_purpose": [
                    "protect in combat",
                    "offer reliable defense",
                    "provide secure coverage",
                ],
                "comfort_aspect": [
                    "fits well without pinching",
                    "distributes weight evenly",
                    "allows full head movement",
                ],
                "metal_treatment": [
                    "is properly tempered",
                    "shows quality finishing",
                    "resists rust effectively",
                ],
                "intimidation_factor": [
                    "looks professionally menacing",
                    "appears battle-ready",
                    "suggests experienced wearer",
                ],
                "weight_distribution": [
                    "feels balanced on the head",
                    "sits comfortably",
                    "doesn't strain the neck",
                ],
                "situational_advantage": [
                    "protection in formation fighting",
                    "defense against ranged attacks",
                    "security in chaotic battles",
                ],
                "special_feature": [
                    "removable visor",
                    "adjustable padding",
                    "reinforced brow",
                ],
                "environmental_protection": [
                    "shields from weather",
                    "protects from debris",
                    "guards against environmental hazards",
                ],
                # Boots phrases
                "travel_endurance": [
                    "hold up well on long walks",
                    "provide decent support for travel",
                    "are comfortable enough for daily use",
                ],
                "terrain_adaptation": [
                    "work on most common surfaces",
                    "provide adequate grip on normal terrain",
                    "handle typical walking conditions well",
                ],
                "traction_quality": [
                    "prevent slipping on wet ground",
                    "grip reasonably well on dirt paths",
                    "provide sure footing in normal conditions",
                ],
                "material_durability": [
                    "will last with proper care",
                    "shows good craftsmanship for the price",
                    "holds up to regular use",
                ],
                "travel_purpose": [
                    "daily commuting and light travel",
                    "walking between villages",
                    "carrying out daily chores",
                ],
                "weather_protection": [
                    "keep feet dry in light rain",
                    "provide basic warmth in cool weather",
                    "offer reasonable comfort in typical conditions",
                ],
                "stealth_capability": [
                    "are reasonably quiet when walking",
                    "don't make excessive noise",
                    "allow for discreet movement when needed",
                ],
                "agility_description": [
                    "comfortable and practical",
                    "light enough for everyday use",
                    "offer basic mobility",
                ],
                "movement_enhancement": [
                    "make walking more comfortable",
                    "reduce fatigue on long treks",
                    "provide decent support",
                ],
                "maintenance_quality": [
                    "are easy to clean and maintain",
                    "require basic care to stay in good condition",
                    "will last with occasional attention",
                ],
                "special_mobility": [
                    "sure footing on uneven ground",
                    "enhanced movement in combat",
                    "better traction when running",
                ],
                # Pants phrases
                "durability_description": [
                    "hold up to regular wear",
                    "show basic stitching",
                    "are serviceable for their purpose",
                ],
                "comfort_feature": [
                    "are reasonably comfortable",
                    "allow decent movement",
                    "don't chafe too much",
                ],
                "usage_scenario": [
                    "daily chores and travel",
                    "working in town",
                    "basic adventuring",
                ],
                "physical_description": [
                    "have a simple, functional cut",
                    "show signs of regular use",
                    "are made of common fabrics",
                ],
                "practical_benefit": [
                    "keep the elements at bay",
                    "provide basic protection",
                    "are easy to move in",
                ],
                "historical_significance": [
                    "have seen typical service",
                    "were made for common folk",
                    "have been worn by many travelers",
                ],
                "practical_quality": [
                    "are easy to mend",
                    "dry quickly when wet",
                    "don't show dirt too badly",
                ],
                "mobility_feature": [
                    "allow free leg movement",
                    "don't restrict walking",
                    "are flexible at the knees",
                ],
                # Pan phrases
                "cooking_performance": [
                    "heats evenly",
                    "cooks food consistently",
                    "performs reliably",
                ],
                "heat_distribution": [
                    "spreads warmth uniformly",
                    "maintains consistent temperature",
                    "avoids hot spots",
                ],
                "grip_comfort": [
                    "stays cool during use",
                    "fits well in hand",
                    "provides secure hold",
                ],
                "food_quality": [
                    "browns meats perfectly",
                    "cooks vegetables evenly",
                    "sears beautifully",
                ],
                "nonstick_feature": [
                    "releases food easily",
                    "cleans with little effort",
                    "resists sticking",
                ],
                "balance_characteristic": [
                    "sits steadily on heat",
                    "handles well when full",
                    "feels balanced in use",
                ],
                "creation_kitchen": [
                    "a reputable workshop",
                    "a skilled artisan's forge",
                    "a quality metalworks",
                ],
                "versatile_cooking": [
                    "handles various cooking methods",
                    "works with different foods",
                    "adapts to multiple recipes",
                ],
                "heat_retention": [
                    "holds temperature well",
                    "stays hot after removal from heat",
                    "maintains cooking warmth",
                ],
                "kitchen_reputation": [
                    "trusted by home cooks",
                    "valued by practical users",
                    "appreciated for reliability",
                ],
                "culinary_history": [
                    "has prepared many meals",
                    "seen regular kitchen use",
                    "cooked for family gatherings",
                ],
                "cooking_style": [
                    "everyday family cooking",
                    "basic culinary tasks",
                    "routine meal preparation",
                ],
                # Consumable phrases
                "visual_appearance": [
                    "looks like typical potion",
                    "has a standard color for its type",
                    "appears as expected",
                ],
                "scent_description": [
                    "smells as it should",
                    "has the characteristic aroma",
                    "carries the expected scent",
                ],
                "immediate_effect": [
                    "provides the promised benefit",
                    "works as advertised",
                    "delivers standard results",
                ],
                "ingredient_source": [
                    "common herbs and minerals",
                    "readily available components",
                    "standard alchemical ingredients",
                ],
                "potency_indication": [
                    "shows typical potency",
                    "appears to be properly brewed",
                    "meets standard quality",
                ],
                "effect_description": [
                    "basic enhancement as expected",
                    "reliable but modest improvement",
                    "consistent with its type",
                ],
                "appearance_characteristic": [
                    "looks properly prepared",
                    "shows standard brewing quality",
                    "appears to be correctly made",
                ],
                "texture_quality": [
                    "has the expected consistency",
                    "feels right when consumed",
                    "is typical for its kind",
                ],
                "practical_effect": [
                    "modest but useful benefits",
                    "reliable assistance when needed",
                    "consistent performance",
                ],
                "aftertaste_sensation": [
                    "leaves a pleasant finish",
                    "has a clean aftertaste",
                    "ends with satisfying notes",
                ],
                "scent_quality": [
                    "hints at its effects",
                    "suggests its potency",
                    "indicates its nature",
                ],
                "energy_signature": [
                    "radiates subtle power",
                    "emits faint magical aura",
                    "pulses with contained energy",
                ],
                # Gloves phrases
                "dexterity_level": [
                    "allow good finger movement",
                    "provide decent manual control",
                    "enable precise handling",
                ],
                "protection_value": [
                    "adequate hand protection",
                    "reliable coverage",
                    "good impact resistance",
                ],
                "flexibility": [
                    "moves with the hand",
                    "bends easily at joints",
                    "allows natural motion",
                ],
                "precision_capability": [
                    "detailed manual tasks",
                    "fine manipulation",
                    "intricate work",
                ],
                "intended_use": [
                    "crafting and combat",
                    "general utility",
                    "protective work",
                ],
                "grip_enhancement": [
                    "improve hold on weapons",
                    "provide better tool control",
                    "enhance grasping ability",
                ],
                "tactile_sensitivity": [
                    "allow feeling through material",
                    "provide good touch feedback",
                    "enable texture discernment",
                ],
                "comfort_feeling": [
                    "soft against the skin",
                    "breathable during use",
                    "comfortable for extended wear",
                ],
                "temperature_regulation": [
                    "keep hands warm in cool weather",
                    "prevent overheating",
                    "maintain comfortable temperature",
                ],
                "specialized_protection": [
                    "against blisters and abrasions",
                    "from minor impacts",
                    "during rough work",
                ],
                "palm_protection": [
                    "reinforced against wear",
                    "padded for comfort",
                    "durable for gripping",
                ],
                # Shield phrases
                "defensive_capability": [
                    "blocks attacks reliably",
                    "provides solid cover",
                    "deflects blows effectively",
                ],
                "weight_characteristic": [
                    "manageable for most users",
                    "balanced for defense",
                    "comfortable to carry",
                ],
                "surface_description": [
                    "shows honest wear",
                    "bears minor scratches",
                    "displays basic craftsmanship",
                ],
                "protection_history": [
                    "has turned aside many blows",
                    "shows signs of regular use",
                    "has protected its wielder well",
                ],
                "impact_resistance": [
                    "absorbs shock effectively",
                    "withstands heavy strikes",
                    "distributes force well",
                ],
                "threat_level": [
                    "common battlefield dangers",
                    "typical combat threats",
                    "standard military engagements",
                ],
                "durability_testament": [
                    "has survived many encounters",
                    "shows longevity in service",
                    "proves reliable over time",
                ],
                "combat_utility": [
                    "serves well in formation",
                    "protects effectively in duels",
                    "works for defense and offense",
                ],
                "deflection_quality": [
                    "turns blades aside",
                    "redirects attack force",
                    "angles blows away",
                ],
                "edge_advantage": [
                    "can catch opposing weapons",
                    "provides striking surface",
                    "offers tactical options",
                ],
                "tactical_defense": [
                    "covering advancing troops",
                    "protecting against projectiles",
                    "forming defensive lines",
                ],
            },
            "uncommon": {
                # Sword phrases
                "blade_description": [
                    "gleams with careful polishing",
                    "shows above-average craftsmanship",
                    "has a well-honed edge",
                ],
                "creation_story": [
                    "made by a skilled town blacksmith",
                    "crafted with extra care and attention",
                    "forged using superior techniques",
                ],
                "combat_behavior": [
                    "moves with good balance and speed",
                    "responds well to skilled handling",
                    "performs reliably in serious combat",
                ],
                "special_quality": [
                    "holds an edge longer than usual",
                    "requires minimal maintenance",
                    "feels perfectly balanced in hand",
                ],
                "physical_description": [
                    "shows careful attention to detail",
                    "bears the marks of skilled craftsmanship",
                    "has a refined appearance",
                ],
                "usage_scenario": [
                    "serious combat and advanced training",
                    "guarding important locations",
                    "serving in professional forces",
                ],
                "historical_significance": [
                    "has seen respectable service",
                    "was carried by experienced warriors",
                    "has been tested in real battles",
                ],
                "metal_quality": [
                    "is made of quality steel",
                    "shows superior metallurgy",
                    "maintains its edge through heavy use",
                ],
                "practical_quality": [
                    "a cut above standard issue",
                    "worth the extra investment",
                    "reliable in demanding situations",
                ],
                "forging_circumstances": [
                    "with imported steel and careful tempering",
                    "by a blacksmith known for quality work",
                    "using techniques beyond the ordinary",
                ],
                "wielder_experience": [
                    "their skills are enhanced by the quality",
                    "they can fight with greater confidence",
                    "the weapon becomes an extension of their will",
                ],
                "magical_property": [
                    "seems to resist rust and corrosion",
                    "maintains its sharpness unusually well",
                    "feels perfectly balanced for its owner",
                ],
                # Knife phrases
                "stealth_quality": [
                    "moves like a shadow",
                    "makes no sound when drawn",
                    "seems to absorb light",
                ],
                "assassin_history": [
                    "has seen professional use",
                    "was carried by skilled agents",
                    "has been used in covert operations",
                ],
                "sharpness_description": [
                    "cuts with surgical precision",
                    "holds a razor edge",
                    "slices through material effortlessly",
                ],
                "physical_trait": [
                    "perfectly weighted",
                    "expertly balanced",
                    "crafted for precision",
                ],
                "movement_quality": [
                    "flows through the air",
                    "responds to subtle motions",
                    "moves with deadly grace",
                ],
                "concealment_feature": [
                    "hidden compartments",
                    "specialized sheaths",
                    "designed for quick access",
                ],
                "creation_purpose": [
                    "professional applications",
                    "specialized tasks",
                    "expert-level use",
                ],
                "balance_description": [
                    "feels like an extension of the arm",
                    "perfectly weighted for throwing",
                    "expertly balanced for combat",
                ],
                "stealth_feature": [
                    "non-reflective surface",
                    "silent deployment mechanism",
                    "minimal profile",
                ],
                "wield_feeling": [
                    "natural and instinctive",
                    "deadly and precise",
                    "confident and controlled",
                ],
                "deadly_characteristic": [
                    "delivers lethal strikes",
                    "penetrates armor weak points",
                    "strikes with surgical accuracy",
                ],
                # Bow phrases
                "draw_characteristic": [
                    "has a smooth, consistent pull",
                    "requires skilled handling",
                    "draws with satisfying tension",
                ],
                "aiming_quality": [
                    "holds rock-steady when drawn",
                    "allows precise targeting",
                    "provides excellent sight picture",
                ],
                "arrow_behavior": [
                    "flies with exceptional accuracy",
                    "maintains perfect trajectory",
                    "hits with impressive force",
                ],
                "hunting_style": [
                    "effective for large game",
                    "suitable for competition",
                    "reliable for professional hunting",
                ],
                "material_source": [
                    "carefully selected wood",
                    "quality materials",
                    "professional-grade components",
                ],
                "performance_trait": [
                    "shoots with consistency",
                    "performs under pressure",
                    "maintains accuracy over distance",
                ],
                "string_quality": [
                    "is high-quality and durable",
                    "maintains perfect tension",
                    "resists weather and wear",
                ],
                "shot_effect": [
                    "strike with authority",
                    "fly with deadly speed",
                    "maintain power at range",
                ],
                "reliability_description": [
                    "never fails when needed",
                    "performs flawlessly",
                    "stands up to heavy use",
                ],
                "weather_resistance": [
                    "handles harsh conditions",
                    "works in adverse weather",
                    "resists moisture and heat",
                ],
                "accuracy_feature": [
                    "exceptional arrow flight",
                    "precise aiming",
                    "steady hold under tension",
                ],
                "ideal_usage": [
                    "professional hunting",
                    "competitive archery",
                    "serious combat situations",
                ],
                # Staff phrases
                "magical_energy": [
                    "controlled arcane power",
                    "refined mystical energy",
                    "focused elemental forces",
                ],
                "physical_feature": [
                    "intricate carvings",
                    "polished surface",
                    "quality crystal setting",
                ],
                "spellcasting_enhancement": [
                    "improves spell accuracy",
                    "enhances magical control",
                    "supports complex casting",
                ],
                "energy_manifestation": [
                    "pulsing with contained power",
                    "glowing with steady light",
                    "humming with magical energy",
                ],
                "focus_component": [
                    "quality crystal",
                    "intricate carvings",
                    "enchanted metal",
                ],
                "component_behavior": [
                    "glows with power",
                    "resonates with spells",
                    "amplifies magical effects",
                ],
                "attunement_quality": [
                    "responds to experienced casters",
                    "accepts complex enchantments",
                    "works with skilled mages",
                ],
                "material_memory": [
                    "stores spell patterns",
                    "remembers complex enchantments",
                    "retains magical signatures",
                ],
                "crystal_power": [
                    "amplifies spells significantly",
                    "focuses energy efficiently",
                    "stabilizes powerful magic",
                ],
                "arcane_history": [
                    "has seen serious magical use",
                    "was used by practicing mages",
                    "has advanced enchantments",
                ],
                "magical_capability": [
                    "enhanced spell power",
                    "improved magical efficiency",
                    "better energy control",
                ],
                "spell_enhancement": [
                    "more powerful spell effects",
                    "enhanced magical precision",
                    "improved casting speed",
                ],
                # Spear phrases
                "reach_advantage": [
                    "dominates combat distance",
                    "provides excellent range",
                    "controls engagement space",
                ],
                "thrust_quality": [
                    "penetrates with authority",
                    "moves with lightning speed",
                    "strikes with devastating force",
                ],
                "tip_material": [
                    "quality hardened steel",
                    "tempered iron alloy",
                    "sharpened specialty metal",
                ],
                "penetration_capability": [
                    "pierces medium armor",
                    "penetrates deeply",
                    "cuts through strong defenses",
                ],
                "throwing_capability": [
                    "flies with perfect balance",
                    "maintains stability in air",
                    "hits with impressive impact",
                ],
                "flight_characteristic": [
                    "spins with precision",
                    "flies true to target",
                    "maintains deadly trajectory",
                ],
                "melee_performance": [
                    "parries and counters effectively",
                    "strikes with speed and power",
                    "defends with expert control",
                ],
                "versatility_description": [
                    "excels in multiple combat roles",
                    "adapts to various situations",
                    "performs well in different scenarios",
                ],
                "flex_characteristic": [
                    "flexes without losing strength",
                    "absorbs heavy impact",
                    "returns to perfect straightness",
                ],
                "head_quality": [
                    "holds exceptional sharpness",
                    "resists damage effectively",
                    "maintains perfect point",
                ],
                "combat_style": [
                    "advanced combat techniques",
                    "professional military use",
                    "experienced warrior tactics",
                ],
                "durability_feature": [
                    "withstands extreme use",
                    "resists heavy impacts",
                    "maintains structural integrity",
                ],
                "tactical_advantage": [
                    "controlling battlefield space",
                    "maintaining offensive pressure",
                    "dominating combat engagements",
                ],
                # Chestplate phrases
                "protection_level": [
                    "stops most weapons effectively",
                    "provides solid protection",
                    "offers reliable defense",
                ],
                "comfort_feature": [
                    "is quite comfortable for armor",
                    "allows good freedom of movement",
                    "breathes well during exertion",
                ],
                "forging_method": [
                    "superior armor-making techniques",
                    "careful fitting and adjustment",
                    "quality materials and workmanship",
                ],
                "historical_provenance": [
                    "has served in notable conflicts",
                    "was worn by respected fighters",
                    "has a history of reliable service",
                ],
                "fit_description": [
                    "fits well and moves comfortably",
                    "hugs the body without restricting",
                    "feels custom-made for movement",
                ],
                "movement_capability": [
                    "allows for advanced combat techniques",
                    "moves naturally with the wearer",
                    "supports athletic maneuvers",
                ],
                "material_construction": [
                    "of quality steel plates",
                    "with careful articulation",
                    "using durable and flexible materials",
                ],
                "defense_quality": [
                    "solid protection",
                    "reliable defense",
                    "quality coverage",
                ],
                "threat_type": [
                    "skilled warriors and dangerous beasts",
                    "serious combat situations",
                    "professional military threats",
                ],
                "battle_reputation": [
                    "has turned aside many attacks",
                    "shows scars from meaningful combat",
                    "has proven its worth repeatedly",
                ],
                "previous_owner": [
                    "a respected guards captain",
                    "an experienced mercenary",
                    "a veteran of several campaigns",
                ],
                "craftsmanship_quality": [
                    "shows skilled workmanship",
                    "is well above average quality",
                    "demonstrates professional crafting",
                ],
                "protection_assurance": [
                    "the wearer can face serious threats",
                    "it provides solid protection in combat",
                    "most weapons will find it difficult to penetrate",
                ],
                "battle_history": [
                    "has seen significant combat",
                    "bears marks from serious battles",
                    "has protected in dangerous situations",
                ],
                # Helmet phrases
                "vision_clarity": [
                    "provides excellent visibility",
                    "offers clear sight lines",
                    "allows full peripheral vision",
                ],
                "head_protection": [
                    "excellent impact resistance",
                    "superior cranial coverage",
                    "outstanding defensive coverage",
                ],
                "design_advantage": [
                    "optimized for combat awareness",
                    "allows excellent hearing",
                    "provides superior ventilation",
                ],
                "design_purpose": [
                    "excel in combat situations",
                    "provide superior defense",
                    "offer advanced protection",
                ],
                "comfort_aspect": [
                    "fits perfectly without pressure points",
                    "distributes weight optimally",
                    "allows complete head mobility",
                ],
                "metal_treatment": [
                    "is expertly tempered",
                    "shows superior finishing",
                    "resists corrosion completely",
                ],
                "intimidation_factor": [
                    "commands respect on battlefield",
                    "appears professionally menacing",
                    "suggests veteran warrior",
                ],
                "weight_distribution": [
                    "feels perfectly balanced",
                    "sits comfortably for hours",
                    "causes no neck strain",
                ],
                "situational_advantage": [
                    "superior protection in melee",
                    "excellent defense against missiles",
                    "optimal security in battle",
                ],
                "special_feature": [
                    "advanced vision slits",
                    "superior padding system",
                    "reinforced construction",
                ],
                "environmental_protection": [
                    "excellent weather protection",
                    "superior debris defense",
                    "optimal environmental security",
                ],
                # Boots phrases
                "travel_endurance": [
                    "excel on extended journeys",
                    "provide excellent support for travel",
                    "remain comfortable for days",
                ],
                "terrain_adaptation": [
                    "work well on difficult surfaces",
                    "provide excellent grip on varied terrain",
                    "handle challenging conditions well",
                ],
                "traction_quality": [
                    "prevent slipping on slippery surfaces",
                    "grip excellently on rough ground",
                    "provide sure footing in difficult conditions",
                ],
                "material_durability": [
                    "will last through heavy use",
                    "shows excellent craftsmanship",
                    "holds up to demanding conditions",
                ],
                "travel_purpose": [
                    "extended wilderness travel",
                    "professional messenger work",
                    "military campaigning",
                ],
                "weather_protection": [
                    "keep feet dry in heavy rain",
                    "provide excellent warmth in cold",
                    "offer superior comfort in harsh conditions",
                ],
                "stealth_capability": [
                    "are very quiet when moving",
                    "make minimal noise",
                    "allow for silent movement",
                ],
                "agility_description": [
                    "comfortable and responsive",
                    "light and agile",
                    "offer excellent mobility",
                ],
                "movement_enhancement": [
                    "make movement more efficient",
                    "reduce fatigue on extended treks",
                    "provide excellent support",
                ],
                "maintenance_quality": [
                    "are easy to maintain",
                    "require minimal care",
                    "will last with basic attention",
                ],
                "special_mobility": [
                    "excellent footing on difficult terrain",
                    "enhanced movement in combat",
                    "superior traction when running",
                ],
                # Pants phrases
                "durability_description": [
                    "withstand rough treatment",
                    "show reinforced stitching",
                    "are made of quality materials",
                ],
                "comfort_feature": [
                    "are quite comfortable for long wear",
                    "move naturally with the body",
                    "breathe well during exertion",
                ],
                "usage_scenario": [
                    "extended travel and exploration",
                    "skilled labor and combat",
                    "professional adventuring",
                ],
                "physical_description": [
                    "show careful tailoring",
                    "bear the marks of skilled craftsmanship",
                    "have a refined appearance",
                ],
                "practical_benefit": [
                    "offer good weather protection",
                    "provide reliable defense",
                    "enhance mobility",
                ],
                "historical_significance": [
                    "have seen respectable service",
                    "were worn by experienced adventurers",
                    "have been tested in real situations",
                ],
                "practical_quality": [
                    "require little maintenance",
                    "hold up well to washing",
                    "maintain their color",
                ],
                "mobility_feature": [
                    "enable advanced maneuvers",
                    "support athletic movements",
                    "flex without restriction",
                ],
                "special_quality": [
                    "offer better protection than most",
                    "are surprisingly durable",
                    "maintain their shape well",
                ],
                "wielder_experience": [
                    "they feel more capable when wearing them",
                    "their steps feel more confident",
                    "they can move with greater assurance",
                ],
                # Pan phrases
                "cooking_performance": [
                    "heats perfectly evenly",
                    "cooks food excellently",
                    "performs flawlessly",
                ],
                "heat_distribution": [
                    "spreads heat perfectly",
                    "maintains ideal temperature",
                    "eliminates hot spots",
                ],
                "grip_comfort": [
                    "remains cool during extended use",
                    "fits perfectly in hand",
                    "provides secure comfortable hold",
                ],
                "food_quality": [
                    "creates perfect sear on meats",
                    "cooks vegetables to perfection",
                    "produces excellent results",
                ],
                "nonstick_feature": [
                    "releases food perfectly",
                    "cleans with minimal effort",
                    "resists sticking completely",
                ],
                "balance_characteristic": [
                    "sits perfectly on heat",
                    "handles beautifully when full",
                    "feels perfectly balanced",
                ],
                "creation_kitchen": [
                    "a master artisan's workshop",
                    "a renowned metalworks",
                    "a specialty forge",
                ],
                "versatile_cooking": [
                    "excels at various cooking methods",
                    "works perfectly with different foods",
                    "adapts beautifully to multiple recipes",
                ],
                "heat_retention": [
                    "holds temperature perfectly",
                    "stays hot long after removal",
                    "maintains ideal cooking warmth",
                ],
                "kitchen_reputation": [
                    "trusted by professional cooks",
                    "valued by serious home chefs",
                    "appreciated for superior quality",
                ],
                "culinary_history": [
                    "has prepared many excellent meals",
                    "seen professional kitchen use",
                    "cooked for important gatherings",
                ],
                "cooking_style": [
                    "serious home cooking",
                    "professional culinary tasks",
                    "quality meal preparation",
                ],
                # Consumable phrases
                "visual_appearance": [
                    "looks like quality potion",
                    "has a rich color for its type",
                    "appears well-made",
                ],
                "scent_description": [
                    "smells potent and effective",
                    "has a rich characteristic aroma",
                    "carries a promising scent",
                ],
                "immediate_effect": [
                    "provides excellent benefits",
                    "works very effectively",
                    "delivers strong results",
                ],
                "ingredient_source": [
                    "quality herbs and minerals",
                    "carefully selected components",
                    "superior alchemical ingredients",
                ],
                "potency_indication": [
                    "shows good potency",
                    "appears to be expertly brewed",
                    "meets high quality standards",
                ],
                "effect_description": [
                    "solid enhancement as expected",
                    "reliable and good improvement",
                    "consistent quality with its type",
                ],
                "appearance_characteristic": [
                    "looks expertly prepared",
                    "shows quality brewing",
                    "appears to be well-made",
                ],
                "texture_quality": [
                    "has a pleasant consistency",
                    "feels smooth when consumed",
                    "is high quality for its kind",
                ],
                "practical_effect": [
                    "good and useful benefits",
                    "reliable assistance when needed",
                    "consistent quality performance",
                ],
                "aftertaste_sensation": [
                    "leaves an excellent finish",
                    "has a clean pleasant aftertaste",
                    "ends with satisfying refined notes",
                ],
                "scent_quality": [
                    "clearly indicates its effects",
                    "confidently suggests its potency",
                    "strongly indicates its nature",
                ],
                "energy_signature": [
                    "radiates noticeable power",
                    "emits clear magical aura",
                    "pulses with contained energy",
                ],
                # Gloves phrases
                "dexterity_level": [
                    "allow excellent finger movement",
                    "provide great manual control",
                    "enable very precise handling",
                ],
                "protection_value": [
                    "good hand protection",
                    "reliable quality coverage",
                    "solid impact resistance",
                ],
                "flexibility": [
                    "moves naturally with the hand",
                    "bends easily at all joints",
                    "allows complete natural motion",
                ],
                "precision_capability": [
                    "excellent detailed manual tasks",
                    "very fine manipulation",
                    "intricate precision work",
                ],
                "intended_use": [
                    "professional crafting and combat",
                    "serious utility work",
                    "quality protective work",
                ],
                "grip_enhancement": [
                    "significantly improve weapon hold",
                    "provide excellent tool control",
                    "greatly enhance grasping ability",
                ],
                "tactile_sensitivity": [
                    "allow good feeling through material",
                    "provide excellent touch feedback",
                    "enable good texture discernment",
                ],
                "comfort_feeling": [
                    "very soft against the skin",
                    "highly breathable during use",
                    "very comfortable for extended wear",
                ],
                "temperature_regulation": [
                    "keep hands warm in cold weather",
                    "effectively prevent overheating",
                    "maintain ideal temperature",
                ],
                "specialized_protection": [
                    "excellent against blisters",
                    "good protection from impacts",
                    "reliable during heavy work",
                ],
                "palm_protection": [
                    "well-reinforced against wear",
                    "comfortably padded",
                    "durable for heavy gripping",
                ],
                # Shield phrases
                "defensive_capability": [
                    "blocks attacks very effectively",
                    "provides excellent cover",
                    "deflects blows with authority",
                ],
                "weight_characteristic": [
                    "well-balanced for defense",
                    "comfortable for extended use",
                    "maneuverable in combat",
                ],
                "surface_description": [
                    "shows quality craftsmanship",
                    "bears marks of serious use",
                    "displays skilled workmanship",
                ],
                "protection_history": [
                    "has turned aside serious blows",
                    "shows signs of combat use",
                    "has protected well in battle",
                ],
                "impact_resistance": [
                    "absorbs heavy shock effectively",
                    "withstands powerful strikes",
                    "distributes force very well",
                ],
                "threat_level": [
                    "serious battlefield dangers",
                    "skilled combat threats",
                    "professional military engagements",
                ],
                "durability_testament": [
                    "has survived serious encounters",
                    "shows durability in service",
                    "proves reliable in combat",
                ],
                "combat_utility": [
                    "serves excellently in formation",
                    "protects very effectively in duels",
                    "works well for defense and offense",
                ],
                "deflection_quality": [
                    "expertly turns blades aside",
                    "effectively redirects attack force",
                    "skillfully angles blows away",
                ],
                "edge_advantage": [
                    "effectively catches weapons",
                    "provides good striking surface",
                    "offers useful tactical options",
                ],
                "tactical_defense": [
                    "excellent cover for advancing",
                    "good protection against projectiles",
                    "effective defensive formations",
                ],
            },
            "rare": {
                # Sword phrases
                "blade_description": [
                    "gleams with a cold light",
                    "shows master-level craftsmanship",
                    "hums with subtle energy",
                ],
                "creation_story": [
                    "folded many times by a master smith",
                    "quenched in special oils under specific stars",
                    "forged using rare and expensive materials",
                ],
                "combat_behavior": [
                    "seems to anticipate the wielder's moves",
                    "moves with unnatural grace",
                    "cuts through the air with minimal resistance",
                ],
                "special_quality": [
                    "never seems to dull",
                    "feels warm to the touch of its owner",
                    "leaves faint trails of light when swung",
                ],
                "physical_description": [
                    "catches the light in unusual ways",
                    "shows patterns in the steel like flowing water",
                    "bears subtle runes along the fuller",
                ],
                "historical_significance": [
                    "was present at famous battles",
                    "has been passed down through warrior families",
                    "was thought to be lost until recently",
                ],
                "metal_quality": [
                    "seems to drink surrounding light",
                    "shows a faint glow in darkness",
                    "remains cool even in hot conditions",
                ],
                "magical_property": [
                    "can cut through minor magical barriers",
                    "stores the memory of combat techniques",
                    "adapts slightly to its wielder's style",
                ],
                "forging_circumstances": [
                    "during a rare celestial alignment",
                    "by a smith who learned ancient techniques",
                    "using metal from a fallen star",
                ],
                "wielder_experience": [
                    "their combat instincts are heightened",
                    "they can sense approaching danger",
                    "the weapon feels like part of their body",
                ],
                "usage_scenario": [
                    "facing supernatural threats",
                    "battling legendary creatures",
                    "fighting in epic conflicts",
                ],
                # Knife phrases
                "stealth_quality": [
                    "moves between realities",
                    "makes no sound even to magical senses",
                    "exists partially in shadow",
                ],
                "assassin_history": [
                    "has ended famous lives",
                    "was carried by legendary assassins",
                    "has been used in historical murders",
                ],
                "sharpness_description": [
                    "cuts between molecules",
                    "holds an edge forever",
                    "slices through space itself",
                ],
                "physical_trait": [
                    "impossibly thin yet strong",
                    "perfect in every dimension",
                    "crafted beyond mortal skill",
                ],
                "movement_quality": [
                    "defies normal physics",
                    "moves faster than thought",
                    "teleports between strikes",
                ],
                "concealment_feature": [
                    "magical hiding enchantments",
                    "dimensional storage",
                    "reality-bending concealment",
                ],
                "creation_purpose": [
                    "legendary assassinations",
                    "reality-altering tasks",
                    "cosmic-level operations",
                ],
                "balance_description": [
                    "perfect in all planes of existence",
                    "balanced across multiple dimensions",
                    "feels right in any reality",
                ],
                "stealth_feature": [
                    "bends light around it",
                    "exists outside normal perception",
                    "hides from magical detection",
                ],
                "wield_feeling": [
                    "like holding destiny itself",
                    "natural as breathing",
                    "instinctive as thought",
                ],
                "deadly_characteristic": [
                    "delivers inevitable death",
                    "penetrates any defense",
                    "strikes with absolute precision",
                ],
                # Bow phrases
                "draw_characteristic": [
                    "requires almost no effort",
                    "draws with perfect smoothness",
                    "adjusts to the archer's strength",
                ],
                "aiming_quality": [
                    "locks onto targets magically",
                    "provides perfect sight picture",
                    "guides arrows instinctively",
                ],
                "arrow_behavior": [
                    "flies with impossible accuracy",
                    "bends around obstacles",
                    "hits with supernatural force",
                ],
                "hunting_style": [
                    "effective for mythical creatures",
                    "suitable for divine hunting",
                    "reliable for epic quests",
                ],
                "material_source": [
                    "wood from legendary trees",
                    "materials from other planes",
                    "components of cosmic origin",
                ],
                "performance_trait": [
                    "shoots with perfect consistency",
                    "performs impossibly well",
                    "maintains flawless accuracy",
                ],
                "string_quality": [
                    "is unbreakable and eternal",
                    "maintains perfect tension forever",
                    "resists all damage",
                ],
                "shot_effect": [
                    "strike with cosmic power",
                    "fly with impossible speed",
                    "maintain infinite power",
                ],
                "reliability_description": [
                    "cannot fail by any means",
                    "performs perfectly always",
                    "stands up to any use",
                ],
                "weather_resistance": [
                    "ignores all conditions",
                    "works in any environment",
                    "resists all elements",
                ],
                "accuracy_feature": [
                    "perfect arrow flight",
                    "absolute aiming precision",
                    "steady beyond physics",
                ],
                "ideal_usage": [
                    "mythical creature hunting",
                    "divine archery",
                    "cosmic combat situations",
                ],
                # Staff phrases
                "magical_energy": [
                    "raw cosmic power",
                    "primordial mystical energy",
                    "reality-shaping forces",
                ],
                "physical_feature": [
                    "living wood carvings",
                    "shifting crystal patterns",
                    "dimensional material",
                ],
                "spellcasting_enhancement": [
                    "magnifies spell power enormously",
                    "perfects magical control",
                    "enables god-like casting",
                ],
                "energy_manifestation": [
                    "warping reality around it",
                    "glowing with cosmic light",
                    "humming with primordial power",
                ],
                "focus_component": [
                    "living crystal",
                    "reality-shaping carvings",
                    "cosmic metal",
                ],
                "component_behavior": [
                    "shapes reality",
                    "controls cosmic forces",
                    "rewrites magical laws",
                ],
                "attunement_quality": [
                    "responds to god-like casters",
                    "accepts reality-altering enchantments",
                    "works with cosmic mages",
                ],
                "material_memory": [
                    "stores cosmic knowledge",
                    "remembers reality shifts",
                    "retains divine signatures",
                ],
                "crystal_power": [
                    "amplifies spells cosmically",
                    "focuses energy perfectly",
                    "stabilizes god-like magic",
                ],
                "arcane_history": [
                    "has seen reality-altering use",
                    "was used by archmages",
                    "has cosmic enchantments",
                ],
                "magical_capability": [
                    "cosmic spell power",
                    "perfect magical efficiency",
                    "absolute energy control",
                ],
                "spell_enhancement": [
                    "reality-altering spell effects",
                    "cosmic magical precision",
                    "instant casting speed",
                ],
                # Spear phrases
                "reach_advantage": [
                    "controls entire battlefields",
                    "provides infinite range",
                    "dominates all engagement space",
                ],
                "thrust_quality": [
                    "penetrates reality itself",
                    "moves outside time",
                    "strikes with cosmic force",
                ],
                "tip_material": [
                    "solidified light",
                    "hardened void",
                    "sharpened destiny",
                ],
                "penetration_capability": [
                    "pierces any armor",
                    "penetrates all defenses",
                    "cuts through dimensions",
                ],
                "throwing_capability": [
                    "flies across dimensions",
                    "maintains perfect reality alignment",
                    "hits with cosmic impact",
                ],
                "flight_characteristic": [
                    "defies physics completely",
                    "flies true across realities",
                    "maintains impossible trajectory",
                ],
                "melee_performance": [
                    "parries all attacks simultaneously",
                    "strikes with absolute speed and power",
                    "defends with cosmic control",
                ],
                "versatility_description": [
                    "transcends all combat roles",
                    "adapts to any situation",
                    "performs perfectly in all scenarios",
                ],
                "flex_characteristic": [
                    "flexes across dimensions",
                    "absorbs cosmic impact",
                    "returns to perfect alignment",
                ],
                "head_quality": [
                    "holds infinite sharpness",
                    "resists all damage",
                    "maintains perfect point eternally",
                ],
                "combat_style": [
                    "cosmic combat techniques",
                    "reality-altering warfare",
                    "divine warrior tactics",
                ],
                "durability_feature": [
                    "withstands cosmic forces",
                    "resists reality warping",
                    "maintains existence itself",
                ],
                "tactical_advantage": [
                    "controlling reality itself",
                    "maintaining cosmic pressure",
                    "dominating all combat everywhere",
                ],
                # Chestplate phrases
                "protection_level": [
                    "deflects arrows and spells with equal ease",
                    "makes the wearer feel invulnerable",
                    "stops any blade that touches it",
                ],
                "comfort_feature": [
                    "remains comfortable during days of continuous wear",
                    "breathes perfectly while offering complete protection",
                    "feels lighter than linen yet protects like mountains of steel",
                ],
                "forging_method": [
                    "over three years by a master armorer and her apprentices",
                    "using techniques taught by celestial beings",
                    "in a single continuous 40-day forging session",
                ],
                "historical_provenance": [
                    "has saved kings and peasants alike from certain death",
                    "was present at every major battle for three centuries",
                    "has more legends about it than some kingdoms",
                ],
                "fit_description": [
                    "hugs the torso like it was born there",
                    "moves with the wearer as if part of their body",
                    "feels custom-fitted regardless of who wears it",
                ],
                "movement_capability": [
                    "allows for acrobatics that seem impossible in armor",
                    "never binds or restricts even the most complex motions",
                    "becomes more comfortable the more vigorously one moves",
                ],
                "material_construction": [
                    "of interlocking scales that shift with each movement",
                    "from a single piece of mystical metal that shouldn't exist",
                    "using lost techniques that make steel behave like cloth",
                ],
                "defense_quality": [
                    "absolute protection",
                    "unbreakable defense",
                    "impervious resistance",
                ],
                "threat_type": [
                    "dragonfire and dark magic alike",
                    "the crushing blows of giants and the precise strikes of assassins",
                    "both physical and spiritual attacks",
                ],
                "battle_reputation": [
                    "enemies break upon its wearer like waves on rock",
                    "allies fight with greater courage when they see it",
                    "turns certain defeat into glorious victory",
                ],
                "previous_owner": [
                    "a general who never lost a battle",
                    "a hero who saved the world three times over",
                    "a warrior so skilled they retired out of boredom",
                ],
                "battle_history": [
                    "has never been penetrated by any weapon",
                    "shows no scratches despite centuries of use",
                    "gleams as if new despite witnessing countless battles",
                ],
                "craftsmanship_quality": [
                    "so perfect that modern smiths cannot replicate it",
                    "represents the pinnacle of defensive enchantment",
                    "combines physical and magical protection seamlessly",
                ],
                "protection_assurance": [
                    "the wearer need fear no mortal weapon",
                    "any attack is turned aside before it can land properly",
                    "danger becomes an abstract concept rather than a threat",
                ],
                # Helmet phrases
                "vision_clarity": [
                    "provides vision beyond normal sight",
                    "allows seeing through illusions",
                    "grants perception of magical energies",
                ],
                "head_protection": [
                    "absolute impact immunity",
                    "cosmic cranial protection",
                    "reality-level defensive coverage",
                ],
                "design_advantage": [
                    "enhances all senses magically",
                    "allows supernatural awareness",
                    "provides cosmic-level perception",
                ],
                "design_purpose": [
                    "transcend normal combat",
                    "provide cosmic defense",
                    "offer reality-level protection",
                ],
                "comfort_aspect": [
                    "feels better than wearing nothing",
                    "becomes part of the wearer's essence",
                    "adapts to be perfect comfort",
                ],
                "metal_treatment": [
                    "is cosmically tempered",
                    "shows reality-level finishing",
                    "resists all corrosion eternally",
                ],
                "intimidation_factor": [
                    "terrifies reality itself",
                    "appears cosmically menacing",
                    "suggests god-like warrior",
                ],
                "weight_distribution": [
                    "feels weightless yet substantial",
                    "sits perfectly for eternity",
                    "causes no physical strain",
                ],
                "situational_advantage": [
                    "cosmic protection in all situations",
                    "absolute defense against all threats",
                    "optimal security in any reality",
                ],
                "special_feature": [
                    "reality-shifting vision",
                    "cosmic padding system",
                    "dimensional construction",
                ],
                "environmental_protection": [
                    "absolute weather immunity",
                    "cosmic debris defense",
                    "reality-level environmental security",
                ],
                # Boots phrases
                "travel_endurance": [
                    "function perfectly for eternal journeys",
                    "provide cosmic support for travel",
                    "remain absolutely comfortable forever",
                ],
                "terrain_adaptation": [
                    "work perfectly on any surface",
                    "provide absolute grip on all terrain",
                    "handle any conditions perfectly",
                ],
                "traction_quality": [
                    "prevent slipping on any surface",
                    "grip perfectly on all ground",
                    "provide sure footing in all conditions",
                ],
                "material_durability": [
                    "will last through eternity",
                    "shows cosmic craftsmanship",
                    "holds up to any conditions",
                ],
                "travel_purpose": [
                    "interdimensional travel",
                    "cosmic messenger work",
                    "reality-spanning campaigning",
                ],
                "weather_protection": [
                    "keep feet perfect in any weather",
                    "provide absolute warmth in any cold",
                    "offer cosmic comfort in all conditions",
                ],
                "stealth_capability": [
                    "are completely silent when moving",
                    "make no sound at all",
                    "allow for absolutely silent movement",
                ],
                "agility_description": [
                    "cosmically comfortable and responsive",
                    "weightless and infinitely agile",
                    "offer perfect mobility",
                ],
                "movement_enhancement": [
                    "make movement perfectly efficient",
                    "eliminate fatigue completely",
                    "provide cosmic support",
                ],
                "maintenance_quality": [
                    "require no maintenance",
                    "are self-repairing",
                    "will last eternally without attention",
                ],
                "special_mobility": [
                    "perfect footing on any terrain",
                    "cosmic movement in combat",
                    "absolute traction always",
                ],
                # Pants phrases
                "durability_description": [
                    "seem to resist normal wear",
                    "show no signs of aging",
                    "are made of exceptional materials",
                ],
                "comfort_feature": [
                    "feel perfectly comfortable in any condition",
                    "adapt to the wearer's body temperature",
                    "never bind or restrict",
                ],
                "usage_scenario": [
                    "dangerous expeditions and battles",
                    "facing supernatural threats",
                    "elite military operations",
                ],
                "physical_description": [
                    "gleam with subtle enchantment",
                    "show intricate patterns in the fabric",
                    "seem to shift with movement",
                ],
                "practical_benefit": [
                    "provide significant protection",
                    "enhance the wearer's abilities",
                    "offer magical advantages",
                ],
                "historical_significance": [
                    "have seen heroic service",
                    "were worn by famous adventurers",
                    "have been present at important events",
                ],
                "practical_quality": [
                    "clean themselves of minor dirt",
                    "repair small tears automatically",
                    "resist magical degradation",
                ],
                "mobility_feature": [
                    "enable superhuman agility",
                    "enhance running and jumping",
                    "allow impossible maneuvers",
                ],
                "special_quality": [
                    "grant increased speed and agility",
                    "protect against magical attacks",
                    "enhance stealth and silence",
                ],
                "wielder_experience": [
                    "their movements feel preternaturally smooth",
                    "they can sense approaching danger",
                    "the pants feel like part of their body",
                ],
                "magical_property": [
                    "seem to resist stains and tears",
                    "maintain perfect comfort in any weather",
                    "adjust slightly to the wearer's movements",
                ],
                "defensive_feature": [
                    "turn aside minor blows",
                    "resist elemental damage",
                    "protect against environmental hazards",
                ],
                # Pan phrases
                "cooking_performance": [
                    "heats with cosmic perfection",
                    "cooks food divinely",
                    "performs beyond perfection",
                ],
                "heat_distribution": [
                    "spreads heat cosmically evenly",
                    "maintains perfect temperature eternally",
                    "creates ideal cooking reality",
                ],
                "grip_comfort": [
                    "feels perfect in any hand",
                    "becomes one with the user",
                    "provides cosmic comfortable hold",
                ],
                "food_quality": [
                    "creates meals of divine quality",
                    "cooks ingredients to cosmic perfection",
                    "produces god-like results",
                ],
                "nonstick_feature": [
                    "rejects food perfectly",
                    "cleans with thought alone",
                    "exists beyond sticking physics",
                ],
                "balance_characteristic": [
                    "sits perfectly in any reality",
                    "handles cosmically when full",
                    "feels balanced across dimensions",
                ],
                "creation_kitchen": [
                    "a divine artisan's workshop",
                    "a cosmic metalworks",
                    "a reality-forging facility",
                ],
                "versatile_cooking": [
                    "transcends all cooking methods",
                    "works perfectly with any foods",
                    "adapts to all recipes simultaneously",
                ],
                "heat_retention": [
                    "holds temperature eternally",
                    "stays perfectly hot forever",
                    "maintains ideal cooking reality",
                ],
                "kitchen_reputation": [
                    "used by divine cooks",
                    "valued by cosmic chefs",
                    "appreciated for reality-level quality",
                ],
                "culinary_history": [
                    "has prepared cosmic meals",
                    "seen divine kitchen use",
                    "cooked for reality-altering gatherings",
                ],
                "cooking_style": [
                    "cosmic cooking",
                    "reality-altering culinary tasks",
                    "divine meal preparation",
                ],
                # Consumable phrases
                "visual_appearance": [
                    "looks like liquid light",
                    "has a cosmic color beyond description",
                    "appears divinely made",
                ],
                "scent_description": [
                    "smells like creation itself",
                    "has a reality-altering aroma",
                    "carries a cosmic scent",
                ],
                "immediate_effect": [
                    "provides cosmic benefits",
                    "works with divine effectiveness",
                    "delivers reality-altering results",
                ],
                "ingredient_source": [
                    "cosmic herbs and minerals",
                    "reality-shaping components",
                    "divine alchemical ingredients",
                ],
                "potency_indication": [
                    "shows cosmic potency",
                    "appears to be divinely brewed",
                    "meets reality-level quality standards",
                ],
                "effect_description": [
                    "cosmic enhancement",
                    "reality-altering improvement",
                    "divine quality with its type",
                ],
                "appearance_characteristic": [
                    "looks divinely prepared",
                    "shows cosmic brewing",
                    "appears to be reality-made",
                ],
                "texture_quality": [
                    "has a cosmic consistency",
                    "feels divine when consumed",
                    "is reality-level quality for its kind",
                ],
                "practical_effect": [
                    "cosmic and useful benefits",
                    "reality-altering assistance when needed",
                    "cosmic quality performance",
                ],
                "aftertaste_sensation": [
                    "leaves a cosmic finish",
                    "has a divine aftertaste",
                    "ends with reality-altering notes",
                ],
                "scent_quality": [
                    "cosmically indicates its effects",
                    "divinely suggests its potency",
                    "reality-level indicates its nature",
                ],
                "energy_signature": [
                    "radiates cosmic power",
                    "emits divine magical aura",
                    "pulses with reality-shaping energy",
                ],
                # Gloves phrases
                "dexterity_level": [
                    "allow cosmic finger movement",
                    "provide divine manual control",
                    "enable absolute precise handling",
                ],
                "protection_value": [
                    "cosmic hand protection",
                    "reality-level coverage",
                    "absolute impact resistance",
                ],
                "flexibility": [
                    "moves with cosmic naturalness",
                    "bends across dimensions",
                    "allows reality-level natural motion",
                ],
                "precision_capability": [
                    "cosmic detailed manual tasks",
                    "absolute fine manipulation",
                    "reality-level intricate work",
                ],
                "intended_use": [
                    "cosmic crafting and combat",
                    "reality-altering utility work",
                    "divine protective work",
                ],
                "grip_enhancement": [
                    "cosmically improve weapon hold",
                    "provide divine tool control",
                    "absolutely enhance grasping ability",
                ],
                "tactile_sensitivity": [
                    "allow cosmic feeling through material",
                    "provide divine touch feedback",
                    "enable reality-level texture discernment",
                ],
                "comfort_feeling": [
                    "cosmically soft against the skin",
                    "divinely breathable during use",
                    "absolutely comfortable for eternal wear",
                ],
                "temperature_regulation": [
                    "keep hands perfect in any temperature",
                    "cosmically prevent overheating",
                    "maintain divine temperature",
                ],
                "specialized_protection": [
                    "cosmic protection against all harm",
                    "divine protection from impacts",
                    "reality-level during heavy work",
                ],
                "palm_protection": [
                    "cosmically reinforced against wear",
                    "divinely padded",
                    "eternally durable for heavy gripping",
                ],
                # Shield phrases
                "defensive_capability": [
                    "blocks all attacks perfectly",
                    "provides cosmic cover",
                    "deflects reality-level blows",
                ],
                "weight_characteristic": [
                    "cosmically balanced for defense",
                    "divinely comfortable for eternal use",
                    "reality-level maneuverable in combat",
                ],
                "surface_description": [
                    "shows cosmic craftsmanship",
                    "bears marks of reality-altering use",
                    "displays divine workmanship",
                ],
                "protection_history": [
                    "has turned aside cosmic blows",
                    "shows signs of reality-level use",
                    "has protected in divine battles",
                ],
                "impact_resistance": [
                    "absorbs cosmic shock perfectly",
                    "withstands reality-level strikes",
                    "distributes force cosmically well",
                ],
                "threat_level": [
                    "cosmic battlefield dangers",
                    "reality-altering combat threats",
                    "divine military engagements",
                ],
                "durability_testament": [
                    "has survived cosmic encounters",
                    "shows eternal durability in service",
                    "proves reliable in reality-level combat",
                ],
                "combat_utility": [
                    "serves cosmically in formation",
                    "protects divinely in duels",
                    "works perfectly for defense and offense",
                ],
                "deflection_quality": [
                    "cosmically turns attacks aside",
                    "divinely redirects attack force",
                    "reality-level angles blows away",
                ],
                "edge_advantage": [
                    "cosmically catches weapons",
                    "provides divine striking surface",
                    "offers reality-level tactical options",
                ],
                "tactical_defense": [
                    "cosmic cover for advancing",
                    "divine protection against projectiles",
                    "reality-level defensive formations",
                ],
            },
            "epic": {
                # Sword phrases
                "blade_description": [
                    "gleams with a cold, steady light",
                    "hums with restrained energy",
                    "shows the careful marks of a master smith",
                ],
                "creation_story": [
                    "quenched in dragon's blood under a full moon",
                    "folded a thousand times by dwarf artisans",
                    "forged from a meteorite that fell during a solar eclipse",
                ],
                "combat_behavior": [
                    "moves with the grace of a flowing river",
                    "seems to anticipate the enemy's movements",
                    "sings a deadly song as it cuts through the air",
                ],
                "special_quality": [
                    "its edge never dulls, no matter what it strikes",
                    "it leaves trails of shimmering light in its wake",
                    "the steel warms to the touch of a worthy wielder",
                ],
                "forging_circumstances": [
                    "during the great war of the northern kingdoms",
                    "by a reclusive smith who worked only by starlight",
                    "using techniques lost to modern craftsmen",
                ],
                "physical_description": [
                    "catches the light in a way that seems almost alive",
                    "bears the subtle curve of a leaf in autumn",
                    "shows a wood-grain pattern in the folded steel",
                ],
                "wielder_experience": [
                    "their reflexes become unnaturally quick in battle",
                    "enemy attacks seem to slow when the blade is drawn",
                    "they can sense approaching danger before it manifests",
                ],
                "historical_significance": [
                    "was present at the founding of the first empire",
                    "has been passed down through generations of heroes",
                    "was thought lost in the great cataclysm",
                ],
                "metal_quality": [
                    "seems to drink the light from torches and campfires",
                    "shows a faint blue glow when danger is near",
                    "remains cool to the touch even in blazing heat",
                ],
                "magical_property": [
                    "can cut through magical barriers as if they were cloth",
                    "stores the memory of every technique it has witnessed",
                    "adapts its weight and balance to match its wielder's style",
                ],
                "usage_scenario": [
                    "battling ancient evils",
                    "fighting in wars that shape nations",
                    "facing opponents of legendary skill",
                ],
                # Knife phrases
                "stealth_quality": [
                    "exists between heartbeats",
                    "moves through shadows as if they were doors",
                    "makes silence seem loud by comparison",
                ],
                "assassin_history": [
                    "has ended dynasties",
                    "was carried by assassins who became legends",
                    "has been used in killings that changed history",
                ],
                "sharpness_description": [
                    "cuts the bonds of fate",
                    "holds an edge that divides reality",
                    "slices through time itself",
                ],
                "physical_trait": [
                    "crafted from solidified shadow",
                    "perfect beyond mortal comprehension",
                    "exists in multiple dimensions simultaneously",
                ],
                "movement_quality": [
                    "teleports between strikes",
                    "moves outside the flow of time",
                    "strikes from impossible angles",
                ],
                "concealment_feature": [
                    "hides in plain sight through reality warping",
                    "exists in pocket dimensions when not needed",
                    "cannot be perceived until it strikes",
                ],
                "creation_purpose": [
                    "ending gods and kings",
                    "altering the course of history",
                    "performing impossible assassinations",
                ],
                "balance_description": [
                    "perfect across all known realities",
                    "balanced by cosmic forces",
                    "feels right in any possible universe",
                ],
                "stealth_feature": [
                    "erases itself from memory when sheathed",
                    "exists as a concept until drawn",
                    "cannot be detected by any means",
                ],
                "wield_feeling": [
                    "like holding absolute power",
                    "natural as destiny",
                    "instinctive as cosmic law",
                ],
                "deadly_characteristic": [
                    "delivers absolute death",
                    "penetrates all possible defenses",
                    "strikes with cosmic precision",
                ],
                # Bow phrases
                "draw_characteristic": [
                    "draws itself for the worthy",
                    "requires no physical effort",
                    "adjusts to cosmic archery laws",
                ],
                "aiming_quality": [
                    "sees targets across time and space",
                    "provides absolute sight picture",
                    "guides arrows with cosmic intelligence",
                ],
                "arrow_behavior": [
                    "flies across dimensions",
                    "strikes from impossible trajectories",
                    "hits with reality-altering force",
                ],
                "hunting_style": [
                    "effective for divine beings",
                    "suitable for cosmic hunting",
                    "reliable for reality-spanning quests",
                ],
                "material_source": [
                    "wood from the world tree",
                    "materials from before creation",
                    "components of absolute origin",
                ],
                "performance_trait": [
                    "shoots with cosmic consistency",
                    "performs beyond physical laws",
                    "maintains absolute accuracy",
                ],
                "string_quality": [
                    "is the fabric of reality woven",
                    "maintains perfect tension across dimensions",
                    "resists all possible damage",
                ],
                "shot_effect": [
                    "strike with absolute power",
                    "fly with cosmic speed",
                    "maintain infinite power across realities",
                ],
                "reliability_description": [
                    "cannot fail by any physical or magical means",
                    "performs perfectly across all realities",
                    "stands up to cosmic use",
                ],
                "weather_resistance": [
                    "creates its own perfect environment",
                    "works in any possible condition",
                    "resists all elemental forces",
                ],
                "accuracy_feature": [
                    "absolute arrow flight",
                    "cosmic aiming precision",
                    "steady beyond physical laws",
                ],
                "ideal_usage": [
                    "divine being hunting",
                    "cosmic archery",
                    "reality-altering combat situations",
                ],
                # Staff phrases
                "magical_energy": [
                    "raw creation energy",
                    "primordial cosmic power",
                    "reality-defining forces",
                ],
                "physical_feature": [
                    "living reality carvings",
                    "shifting dimensional patterns",
                    "cosmic material manifestation",
                ],
                "spellcasting_enhancement": [
                    "enables creation-level magic",
                    "perfects cosmic spell control",
                    "allows reality rewriting casting",
                ],
                "energy_manifestation": [
                    "bending reality around it constantly",
                    "glowing with creation light",
                    "humming with primordial cosmic power",
                ],
                "focus_component": [
                    "living reality crystal",
                    "cosmic-shaping carvings",
                    "absolute metal",
                ],
                "component_behavior": [
                    "defines reality",
                    "controls cosmic creation forces",
                    "rewrites magical laws of existence",
                ],
                "attunement_quality": [
                    "responds to cosmic-level casters",
                    "accepts creation-altering enchantments",
                    "works with reality-defining mages",
                ],
                "material_memory": [
                    "stores cosmic creation knowledge",
                    "remembers reality beginnings",
                    "retains divine cosmic signatures",
                ],
                "crystal_power": [
                    "amplifies spells to creation level",
                    "focuses energy absolutely",
                    "stabilizes cosmic-level magic",
                ],
                "arcane_history": [
                    "has seen creation-altering use",
                    "was used by cosmic archmages",
                    "has reality-defining enchantments",
                ],
                "magical_capability": [
                    "creation-level spell power",
                    "absolute magical efficiency",
                    "cosmic energy control",
                ],
                "spell_enhancement": [
                    "reality-defining spell effects",
                    "cosmic creation magical precision",
                    "instantaneous casting across realities",
                ],
                # Spear phrases
                "reach_advantage": [
                    "controls all battlefields everywhere",
                    "provides cosmic range",
                    "dominates infinite engagement space",
                ],
                "thrust_quality": [
                    "penetrates creation itself",
                    "moves outside existence",
                    "strikes with absolute force",
                ],
                "tip_material": [
                    "solidified creation",
                    "hardened nothingness",
                    "sharpened cosmic destiny",
                ],
                "penetration_capability": [
                    "pierces all possible armor",
                    "penetrates every defense",
                    "cuts through realities",
                ],
                "throwing_capability": [
                    "flies across all dimensions simultaneously",
                    "maintains perfect cosmic alignment",
                    "hits with absolute impact",
                ],
                "flight_characteristic": [
                    "defies all physics completely",
                    "flies true across all realities",
                    "maintains impossible cosmic trajectory",
                ],
                "melee_performance": [
                    "parries all possible attacks everywhere",
                    "strikes with absolute speed and power",
                    "defends with cosmic control across realities",
                ],
                "versatility_description": [
                    "transcends all possible combat roles",
                    "adapts to any situation across realities",
                    "performs perfectly in all possible scenarios",
                ],
                "flex_characteristic": [
                    "flexes across all dimensions",
                    "absorbs absolute impact",
                    "returns to perfect cosmic alignment",
                ],
                "head_quality": [
                    "holds absolute sharpness",
                    "resists all possible damage",
                    "maintains perfect point across realities",
                ],
                "combat_style": [
                    "cosmic creation combat techniques",
                    "reality-defining warfare",
                    "absolute warrior tactics",
                ],
                "durability_feature": [
                    "withstands absolute forces",
                    "resists reality definition",
                    "maintains cosmic existence itself",
                ],
                "tactical_advantage": [
                    "controlling creation itself",
                    "maintaining absolute pressure",
                    "dominating all combat across all realities",
                ],
                # Chestplate phrases
                "protection_level": [
                    "makes the wearer a fundamental force of reality",
                    "defines the concept of protection wherever it exists",
                    "transcends the very idea of harm",
                ],
                "comfort_feature": [
                    "feels like wearing destiny itself",
                    "becomes more comfortable than not wearing armor",
                    "adapts to be whatever the wearer finds most comfortable",
                ],
                "forging_method": [
                    "crafted from the raw stuff of creation",
                    "forged in the heart of a black hole",
                    "woven from the fabric of spacetime itself",
                ],
                "historical_provenance": [
                    "has witnessed the birth and death of universes",
                    "was worn by beings that shaped existence",
                    "contains the history of all protective magic",
                ],
                "fit_description": [
                    "becomes the wearer's true form",
                    "transcends physical dimensions to fit perfectly",
                    "is simultaneously too large and too small yet always perfect",
                ],
                "movement_capability": [
                    "allows movement through time and space",
                    "never restricts because restriction cannot touch it",
                    "enhances mobility beyond physical limits",
                ],
                "material_construction": [
                    "of solidified concepts and mathematical truths",
                    "from the distilled essence of protection",
                    "using principles that govern reality itself",
                ],
                "defense_quality": [
                    "transcendent protection",
                    "conceptual defense",
                    "absolute inviolability",
                ],
                "threat_type": [
                    "conceptual attacks and existential threats",
                    "the unraveling of reality itself",
                    "anything that could ever possibly exist",
                ],
                "battle_reputation": [
                    "enemies surrender at the mere sight of it",
                    "allies become invincible through proximity",
                    "has never known defeat because defeat cannot comprehend it",
                ],
                "previous_owner": [
                    "a being that predates existence",
                    "the concept of protection given form",
                    "a warrior who defeated entropy itself",
                ],
                "battle_history": [
                    "has never been touched because nothing can reach it",
                    "exists in a state of perpetual victory",
                    "defines what protection means across all realities",
                ],
                "craftsmanship_quality": [
                    "so perfect it improves other items by proximity",
                    "represents the absolute ideal of its type",
                    "cannot be comprehended by mortal minds",
                ],
                "protection_assurance": [
                    "the wearer becomes immune to the concept of harm",
                    "danger ceases to exist in their presence",
                    "they become an axiom of safety in an uncertain universe",
                ],
                # Helmet phrases
                "vision_clarity": [
                    "provides vision across all realities",
                    "allows seeing through all illusions",
                    "grants perception of cosmic energies",
                ],
                "head_protection": [
                    "absolute conceptual immunity",
                    "cosmic cranial inviolability",
                    "reality-level absolute coverage",
                ],
                "design_advantage": [
                    "enhances all senses cosmically",
                    "allows absolute awareness",
                    "provides cosmic-level perception across realities",
                ],
                "design_purpose": [
                    "transcend all combat",
                    "provide absolute defense",
                    "offer cosmic-level protection everywhere",
                ],
                "comfort_aspect": [
                    "feels like perfect existence",
                    "becomes the wearer's cosmic essence",
                    "adapts to be absolute comfort",
                ],
                "metal_treatment": [
                    "is absolutely tempered",
                    "shows cosmic-level finishing",
                    "resists all corrosion across realities",
                ],
                "intimidation_factor": [
                    "terrifies cosmic reality itself",
                    "appears absolutely menacing",
                    "suggests cosmic-level warrior",
                ],
                "weight_distribution": [
                    "feels cosmically weightless",
                    "sits perfectly for eternity across realities",
                    "causes no strain in any dimension",
                ],
                "situational_advantage": [
                    "cosmic protection in all situations everywhere",
                    "absolute defense against all threats across realities",
                    "optimal security in any possible existence",
                ],
                "special_feature": [
                    "cosmic-shifting vision",
                    "absolute padding system",
                    "reality-defining construction",
                ],
                "environmental_protection": [
                    "absolute weather immunity across realities",
                    "cosmic debris defense everywhere",
                    "reality-level environmental security in all existences",
                ],
                # Boots phrases
                "travel_endurance": [
                    "function perfectly for cosmic journeys",
                    "provide absolute support for travel across realities",
                    "remain cosmically comfortable forever",
                ],
                "terrain_adaptation": [
                    "work perfectly on any surface in any reality",
                    "provide absolute grip on all terrain everywhere",
                    "handle any conditions perfectly across existences",
                ],
                "traction_quality": [
                    "prevent slipping on any surface in any dimension",
                    "grip perfectly on all ground across realities",
                    "provide sure footing in all conditions everywhere",
                ],
                "material_durability": [
                    "will last through cosmic eternity",
                    "shows absolute craftsmanship",
                    "holds up to any conditions across realities",
                ],
                "travel_purpose": [
                    "cosmic interdimensional travel",
                    "reality-spanning messenger work",
                    "existence-crossing campaigning",
                ],
                "weather_protection": [
                    "keep feet perfect in any weather across realities",
                    "provide absolute warmth in any cold everywhere",
                    "offer cosmic comfort in all conditions in any existence",
                ],
                "stealth_capability": [
                    "are cosmically silent when moving",
                    "make no sound across any reality",
                    "allow for absolutely silent movement everywhere",
                ],
                "agility_description": [
                    "cosmically comfortable and responsive across realities",
                    "weightless and infinitely agile everywhere",
                    "offer absolute mobility in any existence",
                ],
                "movement_enhancement": [
                    "make movement absolutely efficient",
                    "eliminate fatigue cosmically",
                    "provide absolute support across realities",
                ],
                "maintenance_quality": [
                    "require no maintenance across any reality",
                    "are self-repairing cosmically",
                    "will last eternally without attention everywhere",
                ],
                "special_mobility": [
                    "absolute footing on any terrain across realities",
                    "cosmic movement in combat everywhere",
                    "absolute traction in any existence",
                ],
                # Pants phrases
                "durability_description": [
                    "are virtually indestructible",
                    "show no wear despite centuries of use",
                    "are woven from magical materials",
                ],
                "comfort_feature": [
                    "feel better than wearing nothing at all",
                    "become more comfortable the longer they're worn",
                    "adapt perfectly to any activity",
                ],
                "usage_scenario": [
                    "battling ancient evils and dragons",
                    "exploring other planes of existence",
                    "facing world-ending threats",
                ],
                "physical_description": [
                    "gleam with powerful enchantments",
                    "seem to be woven from light and shadow",
                    "change appearance based on the wearer's needs",
                ],
                "practical_benefit": [
                    "make the wearer nearly invulnerable",
                    "grant extraordinary mobility",
                    "provide complete environmental protection",
                ],
                "historical_significance": [
                    "have saved civilizations from destruction",
                    "were worn by legendary heroes",
                    "have been sought by kings and gods",
                ],
                "practical_quality": [
                    "are completely self-cleaning and repairing",
                    "adapt to any climate instantly",
                    "cannot be damaged by normal means",
                ],
                "mobility_feature": [
                    "enable movement at impossible speeds",
                    "allow brief flight and teleportation",
                    "grant perfect balance and footing",
                ],
                "special_quality": [
                    "grant legendary speed and agility",
                    "make the wearer untouchable in combat",
                    "enhance all physical capabilities",
                ],
                "wielder_experience": [
                    "they feel connected to the flow of battle itself",
                    "their body moves with instinctive perfection",
                    "the pants whisper secrets of movement and evasion",
                ],
                "magical_property": [
                    "can phase through solid objects",
                    "allow running on any surface",
                    "grant temporary invisibility",
                ],
                "defensive_feature": [
                    "deflect spells and arrows automatically",
                    "make the wearer immune to environmental hazards",
                    "absorb and redirect kinetic energy",
                ],
                "reality_feature": [
                    "allow movement through obstacles",
                    "defy normal physical restrictions",
                    "enhance the wearer's presence",
                ],
                # Pan phrases
                "cooking_performance": [
                    "heats with absolute perfection",
                    "cooks food with cosmic quality",
                    "performs beyond all possible perfection",
                ],
                "heat_distribution": [
                    "spreads heat absolutely evenly",
                    "maintains perfect temperature across realities",
                    "creates ideal cooking existence",
                ],
                "grip_comfort": [
                    "feels perfect in any hand across any reality",
                    "becomes one with the user cosmically",
                    "provides absolute comfortable hold everywhere",
                ],
                "food_quality": [
                    "creates meals of cosmic quality",
                    "cooks ingredients to absolute perfection",
                    "produces reality-level results",
                ],
                "nonstick_feature": [
                    "rejects food absolutely",
                    "cleans with cosmic thought alone",
                    "exists beyond all sticking physics across realities",
                ],
                "balance_characteristic": [
                    "sits perfectly in any reality across all dimensions",
                    "handles absolutely when full everywhere",
                    "feels balanced across all existences",
                ],
                "creation_kitchen": [
                    "a cosmic artisan's workshop",
                    "a reality-forging metalworks",
                    "an existence-creating facility",
                ],
                "versatile_cooking": [
                    "transcends all possible cooking methods",
                    "works perfectly with any foods across realities",
                    "adapts to all recipes simultaneously everywhere",
                ],
                "heat_retention": [
                    "holds temperature across eternity",
                    "stays perfectly hot forever across realities",
                    "maintains ideal cooking existence",
                ],
                "kitchen_reputation": [
                    "used by cosmic cooks",
                    "valued by reality-level chefs",
                    "appreciated for absolute quality across existences",
                ],
                "culinary_history": [
                    "has prepared absolute meals",
                    "seen cosmic kitchen use",
                    "cooked for reality-defining gatherings",
                ],
                "cooking_style": [
                    "absolute cooking",
                    "cosmic culinary tasks",
                    "reality-level meal preparation",
                ],
                # Consumable phrases
                "visual_appearance": [
                    "looks like liquid reality",
                    "has an absolute color beyond comprehension",
                    "appears cosmically made",
                ],
                "scent_description": [
                    "smells like cosmic creation",
                    "has a reality-defining aroma",
                    "carries an absolute scent",
                ],
                "immediate_effect": [
                    "provides absolute benefits",
                    "works with cosmic effectiveness",
                    "delivers reality-defining results",
                ],
                "ingredient_source": [
                    "cosmic reality herbs and minerals",
                    "existence-shaping components",
                    "absolute alchemical ingredients",
                ],
                "potency_indication": [
                    "shows absolute potency",
                    "appears to be cosmically brewed",
                    "meets reality-level quality standards across existences",
                ],
                "effect_description": [
                    "absolute enhancement",
                    "reality-defining improvement",
                    "cosmic quality with its type",
                ],
                "appearance_characteristic": [
                    "looks cosmically prepared",
                    "shows absolute brewing",
                    "appears to be reality-made across dimensions",
                ],
                "texture_quality": [
                    "has an absolute consistency",
                    "feels cosmic when consumed",
                    "is reality-level quality for its kind across existences",
                ],
                "practical_effect": [
                    "absolute and useful benefits",
                    "reality-defining assistance when needed",
                    "cosmic quality performance everywhere",
                ],
                "aftertaste_sensation": [
                    "leaves an absolute finish",
                    "has a cosmic aftertaste",
                    "ends with reality-defining notes",
                ],
                "scent_quality": [
                    "absolutely indicates its effects",
                    "cosmically suggests its potency",
                    "reality-level indicates its nature across dimensions",
                ],
                "energy_signature": [
                    "radiates absolute power",
                    "emits cosmic magical aura",
                    "pulses with reality-defining energy",
                ],
                # Gloves phrases
                "dexterity_level": [
                    "allow absolute finger movement",
                    "provide cosmic manual control",
                    "enable reality-level precise handling",
                ],
                "protection_value": [
                    "absolute hand protection",
                    "reality-level coverage across existences",
                    "cosmic impact resistance",
                ],
                "flexibility": [
                    "moves with absolute naturalness",
                    "bends across all dimensions",
                    "allows cosmic-level natural motion",
                ],
                "precision_capability": [
                    "absolute detailed manual tasks",
                    "cosmic fine manipulation",
                    "reality-level intricate work across existences",
                ],
                "intended_use": [
                    "cosmic crafting and combat across realities",
                    "reality-defining utility work",
                    "absolute protective work",
                ],
                "grip_enhancement": [
                    "absolutely improve weapon hold",
                    "provide cosmic tool control",
                    "reality-level enhance grasping ability",
                ],
                "tactile_sensitivity": [
                    "allow absolute feeling through material",
                    "provide cosmic touch feedback",
                    "enable reality-level texture discernment across dimensions",
                ],
                "comfort_feeling": [
                    "absolutely soft against the skin",
                    "cosmically breathable during use",
                    "reality-level comfortable for eternal wear",
                ],
                "temperature_regulation": [
                    "keep hands perfect in any temperature across realities",
                    "absolutely prevent overheating",
                    "maintain cosmic temperature everywhere",
                ],
                "specialized_protection": [
                    "absolute protection against all harm across existences",
                    "cosmic protection from impacts",
                    "reality-level during heavy work everywhere",
                ],
                "palm_protection": [
                    "absolutely reinforced against wear",
                    "cosmically padded",
                    "eternally durable for heavy gripping across realities",
                ],
                # Shield phrases
                "defensive_capability": [
                    "blocks all possible attacks absolutely",
                    "provides absolute cover",
                    "deflects reality-level blows across existences",
                ],
                "weight_characteristic": [
                    "absolutely balanced for defense",
                    "cosmically comfortable for eternal use everywhere",
                    "reality-level maneuverable in combat across dimensions",
                ],
                "surface_description": [
                    "shows absolute craftsmanship",
                    "bears marks of reality-defining use",
                    "displays cosmic workmanship across realities",
                ],
                "protection_history": [
                    "has turned aside absolute blows",
                    "shows signs of reality-level use across existences",
                    "has protected in cosmic battles",
                ],
                "impact_resistance": [
                    "absorbs absolute shock perfectly",
                    "withstands reality-level strikes everywhere",
                    "distributes force absolutely well across dimensions",
                ],
                "threat_level": [
                    "absolute battlefield dangers",
                    "reality-defining combat threats",
                    "cosmic military engagements across existences",
                ],
                "durability_testament": [
                    "has survived absolute encounters",
                    "shows eternal durability in service across realities",
                    "proves reliable in reality-level combat everywhere",
                ],
                "combat_utility": [
                    "serves absolutely in formation across realities",
                    "protects cosmically in duels everywhere",
                    "works perfectly for defense and offense in any existence",
                ],
                "deflection_quality": [
                    "absolutely turns attacks aside",
                    "cosmically redirects attack force",
                    "reality-level angles blows away across dimensions",
                ],
                "edge_advantage": [
                    "absolutely catches weapons",
                    "provides cosmic striking surface",
                    "offers reality-level tactical options across existences",
                ],
                "tactical_defense": [
                    "absolute cover for advancing",
                    "cosmic protection against projectiles",
                    "reality-level defensive formations across realities",
                ],
            },
            "legendary": {
                # Sword phrases
                "blade_description": [
                    "gleams with the light of a thousand battles",
                    "hums with power that shakes reality",
                    "shows craftsmanship that defies mortal understanding",
                ],
                "creation_story": [
                    "forged by gods at the dawn of time",
                    "crafted from the heart of a dying star",
                    "born from the dreams of ancient dragons",
                ],
                "combat_behavior": [
                    "moves with the inevitability of fate",
                    "rewrites the laws of physics with each swing",
                    "exists simultaneously in multiple realities when drawn",
                ],
                "special_quality": [
                    "can cut concepts as well as matter",
                    "stores the souls of those it defeats",
                    "adapts to any threat instantly and perfectly",
                ],
                "forging_circumstances": [
                    "before time itself had meaning",
                    "in the fires of creation at universe's birth",
                    "by hands that shaped reality itself",
                ],
                "physical_description": [
                    "appears different to each who behold it",
                    "contains entire worlds within its steel",
                    "shifts form to match its wielder's deepest nature",
                ],
                "wielder_experience": [
                    "they understand the true nature of combat",
                    "their consciousness expands to encompass battle itself",
                    "they become one with the weapon and all it represents",
                ],
                "historical_significance": [
                    "was present when reality was formed",
                    "has ended and begun ages of the world",
                    "contains the memory of all that ever was",
                ],
                "metal_quality": [
                    "is made of solidified possibility",
                    "contains the essence of victory itself",
                    "transcends normal physical properties",
                ],
                "magical_property": [
                    "can rewrite reality within its sphere of influence",
                    "contains power that could unmake worlds",
                    "adapts to any magical system or none at all",
                ],
                "usage_scenario": [
                    "battling concepts of destruction",
                    "fighting in wars that define existence",
                    "facing opponents that challenge reality itself",
                ],
                # Knife phrases
                "stealth_quality": [
                    "exists before and after time",
                    "moves through the gaps in reality",
                    "makes nonexistence seem present by comparison",
                ],
                "assassin_history": [
                    "has ended cosmic beings",
                    "was carried by assassins who became myths",
                    "has been used in killings that altered reality",
                ],
                "sharpness_description": [
                    "cuts the threads of destiny",
                    "holds an edge that divides existence from nonexistence",
                    "slices through the fabric of reality",
                ],
                "physical_trait": [
                    "crafted from crystallized nothingness",
                    "perfect beyond all comprehension",
                    "exists in all dimensions simultaneously",
                ],
                "movement_quality": [
                    "strikes from before the beginning of time",
                    "moves outside all known realities",
                    "attacks from impossible cosmic angles",
                ],
                "concealment_feature": [
                    "hides in the spaces between thoughts",
                    "exists as potential until actualized",
                    "cannot be comprehended until it acts",
                ],
                "creation_purpose": [
                    "ending cosmic entities",
                    "altering the fabric of reality",
                    "performing conceptually impossible assassinations",
                ],
                "balance_description": [
                    "perfect across all possible realities",
                    "balanced by the laws of existence itself",
                    "feels right in any conceivable universe",
                ],
                "stealth_feature": [
                    "erases the concept of its existence when sheathed",
                    "exists as pure potential until drawn",
                    "cannot be detected by any means across all realities",
                ],
                "wield_feeling": [
                    "like holding cosmic destiny",
                    "natural as existence itself",
                    "instinctive as the laws of physics",
                ],
                "deadly_characteristic": [
                    "delivers conceptual death",
                    "penetrates all possible defenses across realities",
                    "strikes with absolute cosmic precision",
                ],
                # Bow phrases
                "draw_characteristic": [
                    "draws itself across all realities",
                    "requires no effort in any dimension",
                    "adjusts to absolute archery laws",
                ],
                "aiming_quality": [
                    "sees targets across all time and space simultaneously",
                    "provides absolute sight picture across realities",
                    "guides arrows with cosmic intelligence everywhere",
                ],
                "arrow_behavior": [
                    "flies across all dimensions at once",
                    "strikes from all possible trajectories",
                    "hits with reality-defining force",
                ],
                "hunting_style": [
                    "effective for cosmic entities",
                    "suitable for absolute hunting",
                    "reliable for existence-spanning quests",
                ],
                "material_source": [
                    "wood from the tree of reality",
                    "materials from before existence",
                    "components of cosmic origin",
                ],
                "performance_trait": [
                    "shoots with absolute consistency",
                    "performs beyond all physical and magical laws",
                    "maintains cosmic accuracy across realities",
                ],
                "string_quality": [
                    "is the fabric of existence woven",
                    "maintains perfect tension across all dimensions",
                    "resists all possible damage everywhere",
                ],
                "shot_effect": [
                    "strike with cosmic power across realities",
                    "fly with absolute speed",
                    "maintain infinite power across all existences",
                ],
                "reliability_description": [
                    "cannot fail by any means across any reality",
                    "performs perfectly in all possible existences",
                    "stands up to absolute use",
                ],
                "weather_resistance": [
                    "creates absolute perfect environment",
                    "works in any possible condition across realities",
                    "resists all elemental forces everywhere",
                ],
                "accuracy_feature": [
                    "cosmic arrow flight across realities",
                    "absolute aiming precision",
                    "steady beyond all physical laws everywhere",
                ],
                "ideal_usage": [
                    "cosmic entity hunting",
                    "absolute archery",
                    "reality-defining combat situations",
                ],
                # Staff phrases
                "magical_energy": [
                    "raw existence energy",
                    "primordial cosmic power",
                    "reality-creating forces",
                ],
                "physical_feature": [
                    "living cosmic carvings",
                    "shifting reality patterns",
                    "existence material manifestation",
                ],
                "spellcasting_enhancement": [
                    "enables existence-level magic",
                    "perfects cosmic spell control across realities",
                    "allows reality creation casting",
                ],
                "energy_manifestation": [
                    "defining reality around it constantly",
                    "glowing with existence light",
                    "humming with primordial cosmic power everywhere",
                ],
                "focus_component": [
                    "living existence crystal",
                    "cosmic-creating carvings",
                    "absolute metal across realities",
                ],
                "component_behavior": [
                    "creates reality",
                    "controls cosmic creation forces everywhere",
                    "defines magical laws of existence",
                ],
                "attunement_quality": [
                    "responds to existence-level casters",
                    "accepts reality-creating enchantments",
                    "works with cosmic-defining mages across realities",
                ],
                "material_memory": [
                    "stores cosmic existence knowledge",
                    "remembers reality creation",
                    "retains divine cosmic signatures everywhere",
                ],
                "crystal_power": [
                    "amplifies spells to existence level",
                    "focuses energy absolutely across realities",
                    "stabilizes cosmic-level magic everywhere",
                ],
                "arcane_history": [
                    "has seen reality-creating use",
                    "was used by cosmic mages across existences",
                    "has reality-defining enchantments everywhere",
                ],
                "magical_capability": [
                    "existence-level spell power",
                    "absolute magical efficiency across realities",
                    "cosmic energy control everywhere",
                ],
                "spell_enhancement": [
                    "reality-creating spell effects",
                    "cosmic existence magical precision",
                    "instantaneous casting across all realities",
                ],
                # Spear phrases
                "reach_advantage": [
                    "controls all possible battlefields everywhere",
                    "provides absolute range",
                    "dominates infinite engagement space across realities",
                ],
                "thrust_quality": [
                    "penetrates existence itself",
                    "moves outside all known realities",
                    "strikes with cosmic force everywhere",
                ],
                "tip_material": [
                    "solidified existence",
                    "hardened cosmic nothingness",
                    "sharpened absolute destiny",
                ],
                "penetration_capability": [
                    "pierces all possible armor across realities",
                    "penetrates every defense everywhere",
                    "cuts through all existences",
                ],
                "throwing_capability": [
                    "flies across all dimensions simultaneously everywhere",
                    "maintains perfect cosmic alignment across realities",
                    "hits with absolute impact in any existence",
                ],
                "flight_characteristic": [
                    "defies all possible physics completely",
                    "flies true across all realities simultaneously",
                    "maintains impossible cosmic trajectory everywhere",
                ],
                "melee_performance": [
                    "parries all possible attacks everywhere across realities",
                    "strikes with absolute speed and power in any existence",
                    "defends with cosmic control across all dimensions",
                ],
                "versatility_description": [
                    "transcends all possible combat roles across realities",
                    "adapts to any situation in any existence",
                    "performs perfectly in all possible scenarios everywhere",
                ],
                "flex_characteristic": [
                    "flexes across all dimensions simultaneously",
                    "absorbs absolute impact across realities",
                    "returns to perfect cosmic alignment in any existence",
                ],
                "head_quality": [
                    "holds cosmic sharpness",
                    "resists all possible damage across realities",
                    "maintains perfect point in all existences",
                ],
                "combat_style": [
                    "cosmic existence combat techniques",
                    "reality-creating warfare",
                    "absolute warrior tactics across dimensions",
                ],
                "durability_feature": [
                    "withstands cosmic forces across realities",
                    "resists reality creation",
                    "maintains absolute existence itself",
                ],
                "tactical_advantage": [
                    "controlling existence itself",
                    "maintaining cosmic pressure across realities",
                    "dominating all combat in all possible existences",
                ],
                # Chestplate phrases - using the original legendary phrases
                "protection_level": [
                    "makes the wearer a fundamental force of reality",
                    "defines the concept of protection wherever it exists",
                    "transcends the very idea of harm",
                ],
                "comfort_feature": [
                    "feels like wearing destiny itself",
                    "becomes more comfortable than not wearing armor",
                    "adapts to be whatever the wearer finds most comfortable",
                ],
                "forging_method": [
                    "crafted from the raw stuff of creation",
                    "forged in the heart of a black hole",
                    "woven from the fabric of spacetime itself",
                ],
                "historical_provenance": [
                    "has witnessed the birth and death of universes",
                    "was worn by beings that shaped existence",
                    "contains the history of all protective magic",
                ],
                "fit_description": [
                    "becomes the wearer's true form",
                    "transcends physical dimensions to fit perfectly",
                    "is simultaneously too large and too small yet always perfect",
                ],
                "movement_capability": [
                    "allows movement through time and space",
                    "never restricts because restriction cannot touch it",
                    "enhances mobility beyond physical limits",
                ],
                "material_construction": [
                    "of solidified concepts and mathematical truths",
                    "from the distilled essence of protection",
                    "using principles that govern reality itself",
                ],
                "defense_quality": [
                    "transcendent protection",
                    "conceptual defense",
                    "absolute inviolability",
                ],
                "threat_type": [
                    "conceptual attacks and existential threats",
                    "the unraveling of reality itself",
                    "anything that could ever possibly exist",
                ],
                "battle_reputation": [
                    "enemies surrender at the mere sight of it",
                    "allies become invincible through proximity",
                    "has never known defeat because defeat cannot comprehend it",
                ],
                "previous_owner": [
                    "a being that predates existence",
                    "the concept of protection given form",
                    "a warrior who defeated entropy itself",
                ],
                "battle_history": [
                    "has never been touched because nothing can reach it",
                    "exists in a state of perpetual victory",
                    "defines what protection means across all realities",
                ],
                "craftsmanship_quality": [
                    "so perfect it improves other items by proximity",
                    "represents the absolute ideal of its type",
                    "cannot be comprehended by mortal minds",
                ],
                "protection_assurance": [
                    "the wearer becomes immune to the concept of harm",
                    "danger ceases to exist in their presence",
                    "they become an axiom of safety in an uncertain universe",
                ],
                # Helmet phrases
                "vision_clarity": [
                    "provides vision across all possible realities",
                    "allows seeing through all possible illusions",
                    "grants perception of cosmic energies everywhere",
                ],
                "head_protection": [
                    "absolute conceptual immunity across realities",
                    "cosmic cranial inviolability everywhere",
                    "reality-level absolute coverage in any existence",
                ],
                "design_advantage": [
                    "enhances all senses absolutely",
                    "allows cosmic awareness across realities",
                    "provides absolute-level perception everywhere",
                ],
                "design_purpose": [
                    "transcend all possible combat",
                    "provide cosmic defense across realities",
                    "offer absolute-level protection in any existence",
                ],
                "comfort_aspect": [
                    "feels like perfect existence itself",
                    "becomes the wearer's absolute essence",
                    "adapts to be cosmic comfort everywhere",
                ],
                "metal_treatment": [
                    "is cosmically tempered across realities",
                    "shows absolute-level finishing",
                    "resists all corrosion in any existence",
                ],
                "intimidation_factor": [
                    "terrifies absolute reality itself",
                    "appears cosmically menacing across dimensions",
                    "suggests absolute-level warrior",
                ],
                "weight_distribution": [
                    "feels absolutely weightless",
                    "sits perfectly for eternity across all realities",
                    "causes no strain in any possible dimension",
                ],
                "situational_advantage": [
                    "cosmic protection in all situations across realities",
                    "absolute defense against all threats in any existence",
                    "optimal security in all possible existences",
                ],
                "special_feature": [
                    "absolute-shifting vision",
                    "cosmic padding system across realities",
                    "reality-creating construction",
                ],
                "environmental_protection": [
                    "absolute weather immunity across all realities",
                    "cosmic debris defense everywhere",
                    "reality-level environmental security in any existence",
                ],
                # Boots phrases
                "travel_endurance": [
                    "function perfectly for absolute journeys",
                    "provide cosmic support for travel across all realities",
                    "remain absolutely comfortable forever everywhere",
                ],
                "terrain_adaptation": [
                    "work perfectly on any surface in any reality across dimensions",
                    "provide cosmic grip on all terrain everywhere",
                    "handle any conditions perfectly across all existences",
                ],
                "traction_quality": [
                    "prevent slipping on any surface in any dimension across realities",
                    "grip cosmically on all ground across existences",
                    "provide sure footing in all conditions everywhere",
                ],
                "material_durability": [
                    "will last through absolute eternity",
                    "shows cosmic craftsmanship across realities",
                    "holds up to any conditions in any existence",
                ],
                "travel_purpose": [
                    "absolute interdimensional travel",
                    "cosmic reality-spanning messenger work",
                    "existence-crossing campaigning everywhere",
                ],
                "weather_protection": [
                    "keep feet perfect in any weather across all realities",
                    "provide cosmic warmth in any cold everywhere",
                    "offer absolute comfort in all conditions in any existence",
                ],
                "stealth_capability": [
                    "are absolutely silent when moving across realities",
                    "make no sound in any possible dimension",
                    "allow for cosmically silent movement everywhere",
                ],
                "agility_description": [
                    "absolutely comfortable and responsive across all realities",
                    "weightless and infinitely agile everywhere",
                    "offer cosmic mobility in any existence",
                ],
                "movement_enhancement": [
                    "make movement cosmically efficient",
                    "eliminate fatigue absolutely",
                    "provide cosmic support across all realities",
                ],
                "maintenance_quality": [
                    "require no maintenance across any possible reality",
                    "are self-repairing absolutely",
                    "will last eternally without attention everywhere",
                ],
                "special_mobility": [
                    "cosmic footing on any terrain across realities",
                    "absolute movement in combat everywhere",
                    "cosmic traction in any existence",
                ],
                # Pants phrases
                "durability_description": [
                    "are woven from the fabric of reality itself",
                    "exist in a state of perfect preservation",
                    "cannot be comprehended by mortal means",
                ],
                "comfort_feature": [
                    "transcend the very concept of comfort",
                    "become one with the wearer's essence",
                    "are simultaneously too large and too small yet always perfect",
                ],
                "usage_scenario": [
                    "challenging cosmic entities",
                    "participating in wars that shape reality",
                    "moving between dimensions and timelines",
                ],
                "physical_description": [
                    "appear different to each observer",
                    "contain entire worlds within their threads",
                    "shift between multiple forms simultaneously",
                ],
                "practical_benefit": [
                    "make the wearer a fundamental force of mobility",
                    "define the concept of movement wherever they exist",
                    "transcend the very idea of restriction",
                ],
                "historical_significance": [
                    "have witnessed the birth and death of universes",
                    "were worn by beings that shaped existence",
                    "contain the history of all movement and travel",
                ],
                "practical_quality": [
                    "are maintained by cosmic forces",
                    "adapt to all possible conditions across realities",
                    "cannot be damaged by any means",
                ],
                "mobility_feature": [
                    "enable movement through time and space",
                    "allow the wearer to be everywhere at once",
                    "grant absolute freedom of motion",
                ],
                "special_quality": [
                    "grant absolute speed and agility",
                    "make the wearer untouchable across all realities",
                    "enhance existence itself",
                ],
                "wielder_experience": [
                    "they understand the true nature of movement",
                    "their consciousness expands to encompass motion itself",
                    "they become one with the concept of travel",
                ],
                "magical_property": [
                    "can rewrite the laws of physics around the wearer",
                    "contain power that could unmake worlds",
                    "adapt to any magical system or none at all",
                ],
                "defensive_feature": [
                    "make the wearer immune to the concept of harm",
                    "danger ceases to exist in their presence",
                    "they become an axiom of safety",
                ],
                "reality_feature": [
                    "allow movement before and after time",
                    "defy all known physical laws",
                    "enable the wearer to walk between realities",
                ],
                # Pan phrases
                "cooking_performance": [
                    "heats with cosmic perfection",
                    "cooks food with absolute quality",
                    "performs beyond all possible perfection across realities",
                ],
                "heat_distribution": [
                    "spreads heat cosmically evenly",
                    "maintains perfect temperature across all realities",
                    "creates ideal cooking existence everywhere",
                ],
                "grip_comfort": [
                    "feels perfect in any hand across any possible reality",
                    "becomes one with the user absolutely",
                    "provides cosmic comfortable hold everywhere",
                ],
                "food_quality": [
                    "creates meals of absolute quality",
                    "cooks ingredients to cosmic perfection",
                    "produces reality-level results across dimensions",
                ],
                "nonstick_feature": [
                    "rejects food cosmically",
                    "cleans with absolute thought alone",
                    "exists beyond all sticking physics across all realities",
                ],
                "balance_characteristic": [
                    "sits perfectly in any reality across all possible dimensions",
                    "handles cosmically when full everywhere",
                    "feels balanced across all existences",
                ],
                "creation_kitchen": [
                    "an absolute artisan's workshop",
                    "a cosmic-forging metalworks",
                    "an existence-creating facility across realities",
                ],
                "versatile_cooking": [
                    "transcends all possible cooking methods across realities",
                    "works perfectly with any foods in any existence",
                    "adapts to all recipes simultaneously everywhere",
                ],
                "heat_retention": [
                    "holds temperature across cosmic eternity",
                    "stays perfectly hot forever across all realities",
                    "maintains ideal cooking existence everywhere",
                ],
                "kitchen_reputation": [
                    "used by absolute cooks",
                    "valued by cosmic-level chefs across realities",
                    "appreciated for reality-level quality in any existence",
                ],
                "culinary_history": [
                    "has prepared cosmic meals across realities",
                    "seen absolute kitchen use",
                    "cooked for reality-creating gatherings",
                ],
                "cooking_style": [
                    "cosmic cooking across realities",
                    "absolute culinary tasks",
                    "reality-level meal preparation everywhere",
                ],
                # Consumable phrases
                "visual_appearance": [
                    "looks like liquid existence",
                    "has a cosmic color beyond all comprehension",
                    "appears absolutely made across realities",
                ],
                "scent_description": [
                    "smells like absolute creation",
                    "has a reality-creating aroma",
                    "carries a cosmic scent across dimensions",
                ],
                "immediate_effect": [
                    "provides cosmic benefits across realities",
                    "works with absolute effectiveness",
                    "delivers reality-creating results",
                ],
                "ingredient_source": [
                    "cosmic reality herbs and minerals across existences",
                    "existence-creating components",
                    "absolute alchemical ingredients everywhere",
                ],
                "potency_indication": [
                    "shows cosmic potency across realities",
                    "appears to be absolutely brewed",
                    "meets reality-level quality standards in any existence",
                ],
                "effect_description": [
                    "cosmic enhancement across realities",
                    "reality-creating improvement",
                    "absolute quality with its type everywhere",
                ],
                "appearance_characteristic": [
                    "looks absolutely prepared across realities",
                    "shows cosmic brewing",
                    "appears to be reality-made in any existence",
                ],
                "texture_quality": [
                    "has a cosmic consistency across realities",
                    "feels absolute when consumed",
                    "is reality-level quality for its kind in any existence",
                ],
                "practical_effect": [
                    "cosmic and useful benefits across realities",
                    "reality-creating assistance when needed",
                    "absolute quality performance everywhere",
                ],
                "aftertaste_sensation": [
                    "leaves a cosmic finish across realities",
                    "has an absolute aftertaste",
                    "ends with reality-creating notes",
                ],
                "scent_quality": [
                    "cosmically indicates its effects across realities",
                    "absolutely suggests its potency",
                    "reality-level indicates its nature in any existence",
                ],
                "energy_signature": [
                    "radiates cosmic power across realities",
                    "emits absolute magical aura",
                    "pulses with reality-creating energy",
                ],
                # Gloves phrases
                "dexterity_level": [
                    "allow cosmic finger movement across realities",
                    "provide absolute manual control",
                    "enable reality-level precise handling everywhere",
                ],
                "protection_value": [
                    "cosmic hand protection across realities",
                    "reality-level coverage in any existence",
                    "absolute impact resistance",
                ],
                "flexibility": [
                    "moves with cosmic naturalness across dimensions",
                    "bends across all possible realities",
                    "allows absolute-level natural motion",
                ],
                "precision_capability": [
                    "cosmic detailed manual tasks across realities",
                    "absolute fine manipulation",
                    "reality-level intricate work in any existence",
                ],
                "intended_use": [
                    "cosmic crafting and combat across all realities",
                    "reality-creating utility work",
                    "absolute protective work everywhere",
                ],
                "grip_enhancement": [
                    "cosmically improve weapon hold across realities",
                    "provide absolute tool control",
                    "reality-level enhance grasping ability in any existence",
                ],
                "tactile_sensitivity": [
                    "allow cosmic feeling through material across realities",
                    "provide absolute touch feedback",
                    "enable reality-level texture discernment in any dimension",
                ],
                "comfort_feeling": [
                    "cosmically soft against the skin across realities",
                    "absolutely breathable during use",
                    "reality-level comfortable for eternal wear everywhere",
                ],
                "temperature_regulation": [
                    "keep hands perfect in any temperature across all realities",
                    "cosmically prevent overheating",
                    "maintain absolute temperature everywhere",
                ],
                "specialized_protection": [
                    "cosmic protection against all harm across existences",
                    "absolute protection from impacts",
                    "reality-level during heavy work everywhere",
                ],
                "palm_protection": [
                    "cosmically reinforced against wear across realities",
                    "absolutely padded",
                    "eternally durable for heavy gripping in any existence",
                ],
                # Shield phrases
                "defensive_capability": [
                    "blocks all possible attacks cosmically",
                    "provides cosmic cover across realities",
                    "deflects reality-level blows in any existence",
                ],
                "weight_characteristic": [
                    "cosmically balanced for defense across realities",
                    "absolutely comfortable for eternal use everywhere",
                    "reality-level maneuverable in combat in any dimension",
                ],
                "surface_description": [
                    "shows cosmic craftsmanship across realities",
                    "bears marks of reality-creating use",
                    "displays absolute workmanship in any existence",
                ],
                "protection_history": [
                    "has turned aside cosmic blows across realities",
                    "shows signs of reality-level use in any existence",
                    "has protected in absolute battles",
                ],
                "impact_resistance": [
                    "absorbs cosmic shock perfectly across realities",
                    "withstands reality-level strikes everywhere",
                    "distributes force cosmically well in any dimension",
                ],
                "threat_level": [
                    "cosmic battlefield dangers across realities",
                    "reality-creating combat threats",
                    "absolute military engagements in any existence",
                ],
                "durability_testament": [
                    "has survived cosmic encounters across realities",
                    "shows eternal durability in service in any existence",
                    "proves reliable in reality-level combat everywhere",
                ],
                "combat_utility": [
                    "serves cosmically in formation across realities",
                    "protects absolutely in duels everywhere",
                    "works perfectly for defense and offense in any existence",
                ],
                "deflection_quality": [
                    "cosmically turns attacks aside across realities",
                    "absolutely redirects attack force",
                    "reality-level angles blows away in any dimension",
                ],
                "edge_advantage": [
                    "cosmically catches weapons across realities",
                    "provides absolute striking surface",
                    "offers reality-level tactical options in any existence",
                ],
                "tactical_defense": [
                    "cosmic cover for advancing across realities",
                    "absolute protection against projectiles",
                    "reality-level defensive formations in any existence",
                ],
            },
        }

        # Get the appropriate grade templates
        grade_templates = item_type_narratives.get(
            self.grade, item_type_narratives["common"]
        )

        # Get template for this specific item type, or use default
        templates = grade_templates.get(
            self.sub_type,
            default_templates.get(self.grade, default_templates["common"]),
        )
        template = random.choice(templates)

        # Get the appropriate phrase bank for this grade
        current_phrase_bank = phrase_banks.get(self.grade, phrase_banks["common"])

        # Extract all placeholders from the template using string formatting approach
        import string

        formatter = string.Formatter()
        placeholders = [
            field_name
            for _, field_name, _, _ in formatter.parse(template)
            if field_name
        ]

        # Build replacement dictionary
        replacements = {}
        for placeholder in placeholders:
            # Get phrases for this placeholder from the current grade's phrase bank
            available_phrases = current_phrase_bank.get(
                placeholder, [f"performs {placeholder}"]
            )

            # Choose a phrase
            chosen_phrase = random.choice(available_phrases)
            replacements[placeholder] = chosen_phrase

        # Add item_type to replacements for default templates
        replacements["item_type"] = self.sub_type

        # Replace all placeholders in the template
        try:
            result = template.format(**replacements)
        except KeyError as e:
            # Fallback if there's a missing placeholder
            missing = str(e).strip("'")
            result = template.replace(f"{{{missing}}}", f"performs {missing}")

        # Add suffix-based conclusion if applicable (these remain the same)
        suffix_conclusions = {
            "of Power": " Raw energy courses through it.",
            "of Shadows": " It seems most comfortable when the light dies.",
            "of the Gods": " A divine presence watches over those who carry it.",
            "of Eternity": " Time itself seems to flow differently in its presence.",
            "of Doom": " A sense of finality follows wherever it goes.",
            "of Frost": " The air grows cold and still when it is near.",
            "of Flame": " Heat shimmers around it like desert air.",
            "of Souls": " Faint whispers seem to emanate from within.",
            "of Oblivion": " It seems to consume the very light around it.",
            "of the Apprentice": " It shows the careful work of a learning hand.",
            "of Focus": " It helps clear the mind and sharpen intent.",
        }

        if self.suffix in suffix_conclusions:
            result += suffix_conclusions[self.suffix]

        return result

    def get_stats(self):
        stats = {
            "level": self.level,
            "max level": self.max_level,
            "max hp": self.max_hp,
            "max mp": self.max_mp,
            "atk": self.atk,
            "sp atk": self.sp_atk,
            "def": self.def_,
            "sp def": self.sp_def,
            "crit chance": self.crit_chance,
            "crit bonus": self.crit_bonus,
            "price": self.value,
        }
        return stats

    def Name(self):
        return f"<{self.grade.title()} {self.name} (Lvl {self.level})>"

    def __repr__(self):
        stats = {
            "level": self.level,
            "max level": self.max_level,
            "max hp": self.max_hp,
            "max mp": self.max_mp,
            "atk": self.atk,
            "sp atk": self.sp_atk,
            "def": self.def_,
            "sp def": self.sp_def,
            "crit chance": self.crit_chance,
            "crit bonus": self.crit_bonus,
            "price": self.value,
        }
        return (
            f"<{self.grade.title()} {self.name} (Lvl {self.level})>\n  Stats: {stats}\n"
            # f'  Flavor: "{self.flavor}"\n'
        )


if __name__ == "__main__":
    # --- DEMO ---
    for rarity in ["common", "uncommon", "rare", "epic", "legendary", "unique"]:
        for _ in range(2):
            item = GameItem(
                rarity,
                random.choice(
                    [
                        "sword",
                        "knife",
                        "bow",
                        "stafe",
                        "spear",
                        "chestplate",
                        "helmet",
                        "boots",
                        "pants",
                        "pan",
                        "gloves",
                        "sheald",
                    ]
                ),
                random.randint(1, 50),
            )
            print(item)
