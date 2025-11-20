import copy

def main(input):
    '''
    Shop sell handler (updated):
    - Takes in player, character_name, and sale_id (item_id from inventory or equipped gear).
    - Finds the matching item from inventory or equipment.
    - Removes it from the player's inventory/equipment.
    - Adds its gold value to the player's gold.
    - If shop has < 3 items, adds the sold item to shop_items.
    - If shop has 3 or more items, the sold item is destroyed.
    - Returns full updated player object.
    '''

    # === Get inputs ===
    player = copy.deepcopy(input.get('player', {}))
    character_name = input.get('character_name')
    sale_id = input.get('sale_id')

    # === Locate character ===
    character = next((c for c in player.get('characters', []) if c.get('name') == character_name), None)
    if not character:
        return {'error': f"Character '{character_name}' not found."}

    # === Helper to find item in inventory or equipment ===
    def find_item(lists):
        for list_name, lst in lists.items():
            for idx, i in enumerate(lst):
                if i.get('item_id') == sale_id:
                    return list_name, idx, i
        return None, None, None

    lists_to_search = {
        'inventory': character.get('inventory', []),
        'equipment': character.get('equipment', [])
    }

    lst_name, idx, item = find_item(lists_to_search)
    if not item:
        return {'error': f"Item '{sale_id}' not found in inventory or equipment."}

    # === Handle gold transfer ===
    item_value = item.get('value', 0)
    character['gold'] = character.get('gold', 0) + item_value

    # === Remove item from list ===
    if lst_name == 'inventory' and item.get('type') == 'consumable' and item.get('qty', 0) > 1:
        item['qty'] -= 1
    else:
        del character[lst_name][idx]

    # === Manage shop capacity ===
    shop_items = character.get('shop_items', [])
    if len(shop_items) < 3:
        new_item = copy.deepcopy(item)
        if new_item.get('type') == 'consumable':
            new_item['qty'] = 1
        shop_items.append(new_item)
        character['shop_items'] = shop_items
    else:
        # Shop is full – item destroyed
        pass

    # === Update character back into player ===
    for i, c in enumerate(player.get('characters', [])):
        if c.get('name') == character_name:
            player['characters'][i] = character
            break

    return {'player': player}
