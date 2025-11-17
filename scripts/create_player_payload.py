def main(input):
    import uuid

    player = input['player']
    rolled_stats = input['rolled_stats']
    character_name = input['character_name']
    character_class = input['character_class']

    # Defensive fix for typo in rolled stats
    if 'deff' in rolled_stats:
        rolled_stats['def'] = rolled_stats.pop('deff')

    # Generate char_id: <character_name> + last 5 chars of UUID
    char_id = f'{character_name}_{str(uuid.uuid4())[-5:]}'

    new_character = {
        'char_id': char_id,
        'name': character_name,
        'class': character_class,
        'level': 1,
        'xp': 0,
        'gold': 100,
        'hp': rolled_stats.get('hp', 100),
        'max_hp': rolled_stats.get('hp', 100),
        'status': '',
        'stats': {
            'atk': rolled_stats.get('atk', 0),
            'def': rolled_stats.get('def', 0),
            'spd': rolled_stats.get('spd', 0),
            'luck': rolled_stats.get('luck', 0)
        },
        'equipment': [
            {
                'slot': 'helmet',
                'item_id': 'helmet_000001',
                'type': 'equipment',
                'name': 'Common Helmet',
                'rarity': 'common',
                'material': 'Cloth',
                'stats': {'def': 1},
                'effects': [],
                'value': 0
            }
        ],
        'inventory': [
            {'item_id': 'potion', 'name': 'potion', 'qty': 3, 'type': 'consumable', 'effect': 'heal_50'},
            {'item_id': 'antidote', 'name': 'antidote', 'qty': 1, 'type': 'consumable', 'effect': 'cure'},
            {'item_id': 'elixir', 'name': 'elixir', 'qty': 1, 'type': 'consumable', 'effect': 'revive'}
        ],
        'shop_items': input.get('loot', {}),
        'shop_refresh': input.get('timestamp', 0),
        'current_map': {
            'map_type': 'Town',
            'floors': 1,
            'player_position': '0,0',
            'rooms': {},
            'start': '0,0',
            'exit': '5,5'
        }
    }

    player['characters'].append(new_character)

    return {'player': player, 'new_character': new_character}
