import copy

def main(input):
    '''
    Equipment handler (Equip or Unequip):
    - Takes in player (full player object), character_name, equip_id (item_id), and action ('Equip' or 'Unequip').
    - Handles both equipping and unequipping gear.
    - For Equip:
        * Finds the item in inventory and checks its slot.
        * Equips to empty slot or swaps with existing item (two ring slots allowed).
    - For Unequip:
        * Moves item from equipment to inventory.
    - Returns the updated full player object.
    '''

    player = copy.deepcopy(input.get('player', {}))
    character_name = input.get('character_name')
    equip_id = input.get('equip_id')
    action = input.get('action', '').lower()

    # === Find character ===
    character = None
    for char in player.get('characters', []):
        if char.get('name') == character_name:
            character = char
            break
    if not character:
        return {'error': f"Character '{character_name}' not found."}

    inventory = character.get('inventory', [])
    equipment = character.get('equipment', [])

    # ======================================================
    # === EQUIP LOGIC ======================================
    # ======================================================
    if action == 'equip':
        item = next((i for i in inventory if i.get('item_id') == equip_id), None)
        if not item:
            return {'error': f"Item '{equip_id}' not found in inventory."}

        if item.get('type') != 'equipment':
            return {'error': f'Item '{item.get('name')}' is not an equippable item.'}

        slot = item.get('slot')
        if not slot:
            return {'error': f'Item '{item.get('name')}' missing slot type.'}

        # === Handle ring logic (2 slots) ===
        if slot == 'ring':
            equipped_rings = [eq for eq in equipment if eq.get('slot') == 'ring']
            if len(equipped_rings) < 2:
                # Equip directly into empty ring slot
                equipment.append(copy.deepcopy(item))
                inventory = [i for i in inventory if i.get('item_id') != equip_id]
            else:
                # Both ring slots full → swap with first ring
                old_ring = equipped_rings[0]
                equipment = [eq for eq in equipment if eq.get('item_id') != old_ring.get('item_id')]
                equipment.append(copy.deepcopy(item))
                inventory.append(copy.deepcopy(old_ring))
                inventory = [i for i in inventory if i.get('item_id') != equip_id]
        else:
            # === Non-ring equipment ===
            equipped_item = next((eq for eq in equipment if eq.get('slot') == slot), None)
            if equipped_item:
                # Swap old with new
                equipment = [eq for eq in equipment if eq.get('item_id') != equipped_item.get('item_id')]
                equipment.append(copy.deepcopy(item))
                inventory.append(copy.deepcopy(equipped_item))
                inventory = [i for i in inventory if i.get('item_id') != equip_id]
            else:
                # Nothing equipped in that slot, equip directly
                equipment.append(copy.deepcopy(item))
                inventory = [i for i in inventory if i.get('item_id') != equip_id]

    # ======================================================
    # === UNEQUIP LOGIC ====================================
    # ======================================================
    elif action == 'unequip':
        item = next((eq for eq in equipment if eq.get('item_id') == equip_id), None)
        if not item:
            return {'error': f"Item '{equip_id}' not found in equipped gear."}

        # Move to inventory
        inventory.append(copy.deepcopy(item))
        # Remove from equipped list
        equipment = [eq for eq in equipment if eq.get('item_id') != equip_id]

    else:
        return {'error': 'Invalid action. Must be 'Equip' or 'Unequip'.'}

    # === Update character ===
    character['inventory'] = inventory
    character['equipment'] = equipment

    # === Write character back ===
    for i, c in enumerate(player.get('characters', [])):
        if c.get('name') == character_name:
            player['characters'][i] = character
            break

    return {'player': player}
