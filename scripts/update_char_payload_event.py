import random
import copy

def main(input):
    '''
    Event handler for non-battle dungeon room interactions.
    Updates the full player object with event outcomes such as:
    - Rest: heals HP and removes debuffs
    - Chest/NPC: grants loot (gear + consumables + gold)
    - Trap: applies damage or disarm chance
    '''

    # Retrieve input
    event_type = input.get('event_type')
    char_id = input.get('char_id')
    loot_gear = input.get('gear', [])
    loot_consume = input.get('consumable_dropped')
    player = input.get('player', {})

    if not event_type or not player or 'characters' not in player or not char_id:
        return {'error': 'Missing required data: event_type, player.characters, or char_id'}

    # Deep copy to prevent side effects
    updated_player = copy.deepcopy(player)
    active_char = next((c for c in updated_player['characters'] if c['char_id'] == char_id), None)
    if not active_char:
        return {'error': f"Character with id '{char_id}' not found."}

    # Ensure basic properties
    active_char.setdefault('inventory', [])
    active_char.setdefault('status', [])
    active_char.setdefault('gold', 0)
    active_char.setdefault('hp', active_char.get('max_hp', 100))
    active_char.setdefault('current_map', {'rooms': {}, 'player_position': None})

    # Inventory limits
    MAX_INVENTORY = 10
    CONSUMABLE_LIMITS = {'potion': 3, 'antidote': 1, 'elixir': 1}

    inventory = active_char['inventory']
    inventory_count = len(inventory)
    loot_texts = []

    result = {
        'event_type': event_type,
        'event_result': {},
        'updated_player': updated_player,
        'room_resolved': False
    }

    # REST EVENT
    if event_type == 'rest':
        heal_percent = random.randint(30, 50) / 100.0
        potential_heal = max(10, int(active_char['max_hp'] * heal_percent))
        actual_heal = min(potential_heal, active_char['max_hp'] - active_char['hp'])
        active_char['hp'] += actual_heal

        negative_statuses = ['poison', 'burn', 'bleed', 'curse', 'fatigue']
        removed_statuses = []
        for status in negative_statuses:
            if status in active_char['status'] and random.random() < 0.6:
                active_char['status'].remove(status)
                removed_statuses.append(status)

        heal_text = f"You rest and recover {actual_heal} HP."
        if removed_statuses:
            heal_text += " You also shake off " + ", ".join(removed_statuses) + "."

        result['event_result'] = {
            'text': heal_text,
            'hp_recovered': actual_heal,
            'status_removed': removed_statuses
        }
        result['room_resolved'] = True

    # CHEST / NPC EVENTS
    elif event_type in ['chest', 'npc']:

        # Handle consumable drop
        if loot_consume:
            existing = next((item for item in inventory if item.get('type') == 'consumable' and item.get('item_id') == loot_consume), None)
            if existing:
                limit = CONSUMABLE_LIMITS.get(loot_consume, 99)
                if existing['qty'] < limit:
                    existing['qty'] = min(limit, existing['qty'] + 1)
                    loot_texts.append(f"You gain 1 {loot_consume}.")
                else:
                    loot_texts.append(f"You found {loot_consume}, but cannot carry more.")
            else:
                if inventory_count < MAX_INVENTORY:
                    effect = (
                        'heal_25' if loot_consume == 'potion' else
                        'cure' if loot_consume == 'antidote' else
                        'revive'
                    )
                    new_item = {
                        'item_id': loot_consume,
                        'name': loot_consume,
                        'qty': 1,
                        'type': 'consumable',
                        'effect': effect
                    }
                    inventory.append(new_item)
                    inventory_count += 1
                    loot_texts.append(f"You gain a new {loot_consume}.")
                else:
                    loot_texts.append(f"You found {loot_consume}, but have no space.")

        # NPC EVENT
        if event_type == 'npc':
            story_flavor = [
                "A weary traveler offers a smile and something shiny in return for your company.",
                "You find a cloaked figure tending to a wounded beast — they hand you a reward for your silence.",
                "A hooded stranger mutters a blessing, and you feel a strange warmth course through your veins.",
                "You stumble upon a merchant who lost their way. They offer a trinket to aid your quest."
            ]
            flavor_text = random.choice(story_flavor)

            if loot_gear and isinstance(loot_gear, list) and len(loot_gear) > 0:
                item = loot_gear[0]
                rarity = item.get('rarity', 'unknown').capitalize()
                name = item.get('name', 'Unknown Item')

                if inventory_count < MAX_INVENTORY:
                    inventory.append(item)
                    loot_texts = [f"{flavor_text} You obtain {name} ({rarity})."]
                else:
                    loot_texts = [f"{flavor_text} You found {name}, but your inventory is full."]
            else:
                if random.random() < 0.5:
                    heal_amount = int(active_char['max_hp'] * 0.25)
                    active_char['hp'] = min(active_char['max_hp'], active_char['hp'] + heal_amount)
                    active_char['status'] = []
                    loot_texts.append(f"{flavor_text} You feel restored and recover 25 percent of your health.")
                else:
                    loot_texts.append(f"{flavor_text} The encounter leaves you pondering their cryptic words.")

        # CHEST EVENT
        elif event_type == 'chest':
            if loot_gear and isinstance(loot_gear, list):
                for item in loot_gear:
                    rarity = item.get('rarity', 'unknown').capitalize()
                    name = item.get('name', 'Unknown Item')
                    if inventory_count < MAX_INVENTORY:
                        inventory.append(item)
                        inventory_count += 1
                        loot_texts.append(f"You obtain {name} ({rarity}).")
                    else:
                        loot_texts.append(f"You found {name}, but inventory is full.")
            else:
                gold_gain = random.randint(10, 50)
                active_char['gold'] += gold_gain
                loot_texts.appen_
