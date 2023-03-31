class Config:
    def __init__(self):
        self.ADVENTURER_CONTRACT = (
            "0x035d755a23ec72df90819f584d9a1849bbc21fa77f96d25e03f1736883895248"
        )
        self.BEAST_CONTRACT = (
            "0x000f4dbfe5d15792aa91025e42ee1d74c22bdeb1eef0b9bc19a37216377290c1"
        )
        self.LOOT_CONTRACT = (
            "0x065669e15c8f1a7f17b7062e4eb1b709b922b931b93c59577f1848a85c30ab1f"
        )
        self.STARTING_BLOCK = 785_000

        self.BEASTS = {
            1: "Pheonix",
            2: "Griffin",
            3: "Minotaur",
            4: "Basilisk",
            5: "Gnome",
            6: "Wraith",
            7: "Ghoul",
            8: "Goblin",
            9: "Skeleton",
            10: "Golem",
            11: "Giant",
            12: "Yeti",
            13: "Orc",
            14: "Beserker",
            15: "Ogre",
            16: "Dragon",
            17: "Vampire",
            18: "Werewolf",
            19: "Spider",
            20: "Rat",
        }

        self.ITEMS = {
            1: "Pendant",
            2: "Necklace",
            3: "Amulet",
            4: "SilverRing",
            5: "BronzeRing",
            6: "PlatinumRing",
            7: "TitaniumRing",
            8: "GoldRing",
            9: "GhostWand",
            10: "GraveWand",
            11: "BoneWand",
            12: "Wand",
            13: "Grimoire",
            14: "Chronicle",
            15: "Tome",
            16: "Book",
            17: "DivineRobe",
            18: "SilkRobe",
            19: "LinenRobe",
            20: "Robe",
            21: "Shirt",
            22: "Crown",
            23: "DivineHood",
            24: "SilkHood",
            25: "LinenHood",
            26: "Hood",
            27: "BrightsilkSash",
            28: "SilkSash",
            29: "WoolSash",
            30: "LinenSash",
            31: "Sash",
            32: "DivineSlippers",
            33: "SilkSlippers",
            34: "WoolShoes",
            35: "LinenShoes",
            36: "Shoes",
            37: "DivineGloves",
            38: "SilkGloves",
            39: "WoolGloves",
            40: "LinenGloves",
            41: "Gloves",
            42: "Katana",
            43: "Falchion",
            44: "Scimitar",
            45: "LongSword",
            46: "ShortSword",
            47: "DemonHusk",
            48: "DragonskinArmor",
            49: "StuddedLeatherArmor",
            50: "HardLeatherArmor",
            51: "LeatherArmor",
            52: "DemonCrown",
            53: "DragonsCrown",
            54: "WarCap",
            55: "LeatherCap",
            56: "Cap",
            57: "DemonhideBelt",
            58: "DragonskinBelt",
            59: "StuddedLeatherBelt",
            60: "HardLeatherBelt",
            61: "LeatherBelt",
            62: "DemonhideBoots",
            63: "DragonskinBoots",
            64: "StuddedLeatherBoots",
            65: "HardLeatherBoots",
            66: "LeatherBoots",
            67: "DemonsHands",
            68: "DragonskinGloves",
            69: "StuddedLeatherGloves",
            70: "HardLeatherGloves",
            71: "LeatherGloves",
            72: "Warhammer",
            73: "Quarterstaff",
            74: "Maul",
            75: "Mace",
            76: "Club",
            77: "HolyChestplate",
            78: "OrnateChestplate",
            79: "PlateMail",
            80: "ChainMail",
            81: "RingMail",
            82: "AncientHelm",
            83: "OrnateHelm",
            84: "GreatHelm",
            85: "FullHelm",
            86: "Helm",
            87: "OrnateBelt",
            88: "WarBelt",
            89: "PlatedBelt",
            90: "MeshBelt",
            91: "HeavyBelt",
            92: "HolyGreaves",
            93: "OrnateGreaves",
            94: "Greaves",
            95: "ChainBoots",
            96: "HeavyBoots",
            97: "HolyGauntlets",
            98: "OrnateGauntlets",
            99: "Gauntlets",
            100: "ChainGloves",
            101: "HeavyGloves",
        }

        self.RACES = {
            1: "Elf",
            2: "Fox",
            3: "Giant",
            4: "Human",
            5: "Orc",
            6: "Demon",
            7: "Goblin",
            8: "Fish",
            9: "Cat",
            10: "Frog",
        }

        self.ORDERS = {
            1: "Power",
            2: "Giants",
            3: "Titans",
            4: "Skill",
            5: "Perfection",
            6: "Brilliance",
            7: "Enlightenment",
            8: "Protection",
            9: "Twins",
            10: "Reflection",
            11: "Detection",
            12: "Fox",
            13: "Vitriol",
            14: "Fury",
            15: "Rage",
            16: "Anger",
        }

        self.STATS = {
            2: "Strength",
            3: "Dexterity",
            4: "Vitality",
            5: "Intelligence",
            6: "Wisdom",
            7: "Charisma",
            8: "Luck",
        }

        self.OBSTACLES = {
            1: "Demonic Alter",
            2: "Curse",
            3: "Hex",
            4: "Magic Lock",
            5: "Dark Mist",
            6: "Collapsing Ceiling",
            7: "Crushing Walls",
            8: "Rockslide",
            9: "Tumbling Boulders",
            10: "Swinging Logs",
            11: "Pendulum Blades",
            12: "Flame Jet",
            13: "Poision Dart",
            14: "Spiked Pit",
            15: "Hidden Arrow",
        }

        self.DISCOVERY_TYPES = {
            0: "Nothing",
            1: "Beast",
            2: "Obstacle",
            3: "Item",
            4: "Adventurer",
        }

        self.ITEM_DISCOVERY_TYPES = {0: "Gold", 1: "Loot", 2: "Health"}

        self.ATTACK_TYPES = {
            0: "Generic",
            100: "Generic Weapon",
            101: "Bludgeon Weapon",
            102: "Blade Weapon",
            103: "Magic Weapon",
            200: "Generic Armor",
            201: "Metal Armor",
            202: "Hide Armor",
            203: "Cloth Armor",
            300: "Ring",
            400: "Necklace",
        }

        self.MATERIALS = {
            0: "Generic",
            1000: "Generic Metal",
            1001: "Ancient Metal",
            1002: "Holy Metal",
            1003: "Ornate Metal",
            1004: "Gold Metal",
            1005: "Silver Metal",
            1006: "Bronze Metal",
            1007: "Platinum Metal",
            1008: "Titanium Metal",
            1009: "Steel Metal",
            2000: "Generic Cloth",
            2001: "Royal Cloth",
            2002: "Divine Cloth",
            2003: "Brightsilk Cloth",
            2004: "Silk Cloth",
            2005: "Wool Cloth",
            2006: "Linen Cloth",
            3000: "Generic Biotic",
            3100: "Demon Generic Biotic",
            3101: "Demon Blood Biotic",
            3102: "Demon Bones Biotic",
            3103: "Demon Brain Biotic",
            3104: "Demon Eyes Biotic",
            3105: "Demon Hide Biotic",
            3106: "Demon Flesh Biotic",
            3107: "Demon Hair Biotic",
            3108: "Demon Heart Biotic",
            3109: "Demon Entrails Biotic",
            3110: "Demon Hands Biotic",
            3111: "Demon Feet Biotic",
            3200: "Dragon Generic Biotic",
            3201: "Dragon Blood Biotic",
            3202: "Dragon Bones Biotic",
            3203: "Dragon Brain Biotic",
            3204: "Dragon Eyes Biotic",
            3205: "Dragon Skin Biotic",
            3206: "Dragon Flesh Biotic",
            3207: "Dragon Hair Biotic",
            3208: "Dragon Heart Biotic",
            3209: "Dragon Entrails Biotic",
            3210: "Dragon Hands Biotic",
            3211: "Dragon Feet Biotic",
            3300: "Animal Generic Biotic",
            3301: "Animal Blood Biotic",
            3302: "Animal Bones Biotic",
            3303: "Animal Brain Biotic",
            3304: "Animal Eyes Biotic",
            3305: "Animal Hide Biotic",
            3306: "Animal Flesh Biotic",
            3307: "Animal Hair Biotic",
            3308: "Animal Heart Biotic",
            3309: "Animal Entrails Biotic",
            3310: "Animal Hands Biotic",
            3311: "Animal Feet Biotic",
            3400: "Human Generic Biotic",
            3401: "Human Blood Biotic",
            3402: "Human Bones Biotic",
            3403: "Human Brain Biotic",
            3404: "Human Eyes Biotic",
            3405: "Human Hide Biotic",
            3406: "Human Flesh Biotic",
            3407: "Human Hair Biotic",
            3408: "Human Heart Biotic",
            3409: "Human Entrails Biotic",
            3410: "Human Hands Biotic",
            3411: "Human Feet Biotic",
            4000: "Generic Paper",
            4001: "Magical Paper",
            5000: "Generic Wood",
            5100: "Generic Hardwood",
            5101: "Walnut Hardwood",
            5102: "Mahogany Hardwood",
            5103: "Maple Hardwood",
            5104: "Oak Hardwood",
            5105: "Rosewood Hardwood",
            5106: "Cherry Hardwood",
            5107: "Balsa Hardwood",
            5108: "Birch Hardwood",
            5109: "Holly Hardwood",
            5200: "Generic Softwood",
            5201: "Cedar Softwood",
            5202: "Pine Softwood",
            5203: "Fir Softwood",
            5204: "Hemlock Softwood",
            5205: "Spruce Softwood",
            5206: "Elder Softwood",
            5207: "Yew Softwood",
        }
