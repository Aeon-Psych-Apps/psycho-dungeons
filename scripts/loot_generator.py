import random
import uuid

def main(input):
    # Version 1.0.1
    # Updated 10/28/25 22:36 PST
  
    # ---------------------
    # Inputs
    # ---------------------
    source = input.get('source', 'enemy').lower()  # shop, chest, enemy, boss, npc
    count = max(int(input.get('count', 1)), 1)
    player_level = input.get('player_level', 1)

    # ---------------------
    # Drop chance settings
    # ---------------------
    loot_config = {
        'enemy': {'gear_chance': 0.50, 'consumable_chance': 0.25},
        'chest': {'gear_chance': 0.35, 'consumable_chance': 0.40},
        'npc': {'gear_chance': 0.10, 'consumable_chance': 0.50},
        'boss': {'gear_chance': 1.00, 'consumable_chance': 0.50},
        'shop': {'gear_chance': 1.00, 'consumable_chance': 0.00}
    }

    # ---------------------
    # Rarity definitions
    # ---------------------
    rarities = {
        'common':    {'mult': 1.0, 'weights': {'shop': 0.6, 'chest': 0.7, 'enemy': 0.10, 'boss': 0.0}},
        'uncommon':  {'mult': 1.2, 'weights': {'shop': 0.25, 'chest': 0.2, 'enemy': 0.25, 'boss': 0.1}},
        'rare':      {'mult': 1.5, 'weights': {'shop': 0.1, 'chest': 0.08, 'enemy': 0.04, 'boss': 0.4}},
        'epic':      {'mult': 2.0, 'weights': {'shop': 0.04, 'chest': 0.02, 'enemy': 0.01, 'boss': 0.25}},
        'legendary': {'mult': 3.0, 'weights': {'shop': 0.01, 'chest': 0.01, 'enemy': 0.0, 'boss': 0.10}}
    }

    # ---------------------
    # Material quality multipliers
    # ---------------------
    materials = [
        {'name': 'Cloth', 'bonus': 1.0},
        {'name': 'Leather', 'bonus': 1.1},
        {'name': 'Iron', 'bonus': 1.25},
        {'name': 'Steel', 'bonus': 1.4},
        {'name': 'Mithril', 'bonus': 1.6}
    ]

    # ---------------------
    # Base item templates
    # ---------------------
    base_items = {
    'helmet': [
        {'def': (3, 8)},
        {'hp': (10, 25)}
    ],
    'chest': [
        {'def': (6, 12)},
        {'hp': (20, 40)}
    ],
    'legs': [
        {'def': (4, 10)},
        {'hp': (15, 30)},
        {'spd': (1, 3)}
    ],
    'boots': [
        {'def': (2, 6)},
        {'spd': (1, 3)}
    ],
    'main_hand': [
        {'atk': (8, 14)},
        {'spd': (1, 2)}
    ],
    'off_hand': [
        {'atk': (6, 10)},
        {'def': (4, 8)},
        {'spd': (1, 3)},
        {'luck': (1, 4)}
    ],
    'ring': [
        {'atk': (1, 4)},
        {'def': (1, 4)},
        {'spd': (1, 3)},
        {'luck': (1, 4)},
        {'hp': (10, 25)}
    ]
}

    # ---------------------
    # Base item names by slot
    # ---------------------
    item_base_names = {
        'helmet': ['Cap', 'Hood', 'Helm'],
        'chest': ['Tunic', 'Vest', 'Robes', 'Armor', 'Chestplate'],
        'legs': ['Pants', 'Leggings', 'Greaves'],
        'boots': ['Shoes', 'Boots', 'Sabatons', 'Footwear'],
        'main_hand': ['Sword', 'Axe', 'Staff', 'Mace'],
        'off_hand': ['Shield', 'Tome', 'Orb'],
        'ring': ['Ring', 'Band', 'Loop']
    }

    # ---------------------
    # Signature items
    # ---------------------
    signature_items = {
        'helmet': ['Helm of the Phoenix', 'Crown of Valor', 'Celestial Helm'],
        'chest': ['Breastplate of Eternity', 'Robe of the Archmage', 'Armor of Legends'],
        'legs': ['Leggings of Eternity', 'Greaves of the Archmage', 'Legguards of Legends'],
        'boots': ['Boots of Eternity', 'Sabotons of the Archmage', 'Footwear of Legends'],
        'main_hand': ['Excalibur', 'Dragonfang', 'Staff of Eternity'],
        'off_hand': ['Shield of Eternity', 'Tome of Legends'],
        'ring': ['Ring of the Ancients', 'Band of Fortune']
    }

    # ---------------------
    # Consumables
    # ---------------------
    consumables = [
        {'item_id': 'potion', 'effect': 'heal_50'},
        {'item_id': 'antidote', 'effect': 'cure'},
        {'item_id': 'elixir', 'effect': 'revive'}
    ]

    # ---------------------
    # Stat floors for higher-tier items
    # ---------------------
    stat_floors = {
        'rare': 1,
        'epic': 3,
        'legendary': 5,
        'signature': 6
    }

    # ---------------------
    # Generate item helper
    # ---------------------
    def generate_item(src):
        slot = random.choice(list(base_items.keys()))

        # Determine rarity
        weighted_pool = []
        for rarity, data in rarities.items():
            weight = data['weights'].get(src, 0)
            weighted_pool.extend([rarity] * int(weight * 100))
        rarity = random.choice(weighted_pool or ['common'])
        rarity_data = rarities[rarity]

        # Choose material (weighted slightly higher for higher rarity)
        material_index = min(random.randint(0, len(materials)-1) + (['common','uncommon','rare'].index(rarity) if rarity in ['common','uncommon','rare'] else 0), len(materials)-1)
        material = materials[material_index]

        # Adjust base stats for rings/off-hand
        base = {'base_stats': random.choice(base_items[slot])}

        # Determine if signature
        is_signature = False
        if rarity in ['epic', 'legendary'] and random.random() < 0.15:
            is_signature = True
            rarity_tag = 'signature'
        else:
            rarity_tag = rarity

        # Roll stats with floor
        stats = {}
        level_scale = 1 + (player_level - 1) * 0.05  # 5% per player level
        for stat, (minv, maxv) in base['base_stats'].items():
            roll = random.randint(minv, maxv)
            scaled = int(roll * rarity_data['mult'] * material['bonus'] * level_scale)
            floor = stat_floors.get(rarity_tag, 0)
            stats[stat] = max(scaled, floor)

        # Effects for epic/legendary/signature
        effects = []
        if rarity in ['epic', 'legendary'] or is_signature:
            effects.append(random.choice([
                'lifesteal', 'crit_boost', 'resist_fire',
                'inflict_burn', 'inflict_poison', 'resist_poison'
            ]))

        # Name
        if is_signature:
            name = f'{rarity.title()} {random.choice(signature_items[slot])}'
        else:
            name = f'{rarity.title()} {material['name']} {random.choice(item_base_names[slot])}'

        # Value calculation
        base_value = sum(stats.values()) * 5
        effect_bonus = len(effects) * int(20 * rarity_data['mult'])
        fluctuation = random.choice(range(-10, 26, 5))  # smaller range for more predictable progression
        value = base_value + effect_bonus + fluctuation

        return {
            'item_id': f'{slot}_{uuid.uuid4().hex[:6]}',
            'type': 'equipment',
            'name': name,
            'rarity': rarity,
            'slot': slot,
            'material': material['name'],
            'stats': stats,
            'effects': effects,
            'value': max(value, 1)
        }

    # ---------------------
    # Loot roll
    # ---------------------
    config = loot_config.get(source, loot_config['enemy'])
    result = {'source': source, 'gear': [], 'consumable_dropped': None}

    if random.random() < config['gear_chance']:
        result['gear'] = [generate_item(source) for _ in range(count)]

    if random.random() < config['consumable_chance']:
        consumable = random.choices(
            consumables, weights=[0.5, 0.25, 0.25], k=1
        )[0]
        result['consumable_dropped'] = consumable['item_id']

    return result
