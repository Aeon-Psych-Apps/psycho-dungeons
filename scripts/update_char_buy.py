import copy

def main(input):
    '''
    Shop purchase handler:
    - Takes in player (full player object), character_name, and purchase_id.
    - Finds the matching shop item by item_id.
    - Deducts the item's cost from character gold (if affordable).
    - Adds the item to character inventory (stacking consumables if applicable).
    - Removes the purchased item from shop_items.
    - Returns full updated player object.
    '''

    # === Get inputs ===
    player = copy.deepcopy(input.get('player', {}))
    character_name = input.get('character_name')
    purchase_id = input.get('purchase_id')

    # === Locate the character ===
    character = None
    for char in player.get('characters', []):
        if char.get('name') == character_name:
            character = char
            break

    if not character:
        return {'error': f'Character '{character_name}' not found.'}

    # === Locate the item in shop ===
    shop_items = character.get('shop_items', [])
    item = next((i for i in shop_items if i.get('item_id') == purchase_id), None)

    if not item:
        return {'error': f'Item '{purchase_id}' not found in shop.'}

    item_value = item.get('value', 0)
    gold = character.get('gold', 0)

    # === Check affordability ===
    if gold < item_value:
        return {'error': f'Not enough gold. Need {item_value}, have {gold}.'}

    # === Deduct gold ===
    character['gold'] = gold - item_value

    # === Add item to inventory ===
    inventory = character.get('inventory', [])

    # Stackable check (only for consumables with qty)
    if item.get('type') == 'consumable':
        existing = next((i for i in inventory if i.get('item_id') == item.get('item_id')), None)
        if existing:
            existing['qty'] = existing.get('qty', 0) + 1
        else:
            new_item = copy.deepcopy(item)
            new_item['qty'] = 1
            inventory.append(new_item)
    else:
        # Equipment or other unique items
        inventory.append(copy.deepcopy(item))

    # === Remove from shop ===
    character['shop_items'] = [i for i in shop_items if i.get('item_id') != purchase_id]

    # === Update the character back into player ===
    for i, c in enumerate(player.get('characters', [])):
        if c.get('name') == character_name:
            player['characters'][i] = character
            break

    # === Return updated player object ===
    return {'player': player}
