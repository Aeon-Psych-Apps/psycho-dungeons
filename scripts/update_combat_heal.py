def main(input):
    action = input.get('action')  # 'heal' or 'antidote'
    player = input.get('player', {})
    char_id = input.get('char_id')

    if not action or not player or not char_id:
        return {'error': 'Missing required input (action, player, char_id)'}

    # Locate active character
    active_char = next((c for c in player.get('characters', []) if c.get('char_id') == char_id), None)
    if not active_char:
        return {'error': f"Character with id '{char_id}' not found"}

    inventory = active_char.get('inventory', [])

    # Helper to find inventory item
    def get_item(item_id):
        return next((i for i in inventory if i.get('item_id') == item_id), None)

    # Process Heal Action
    if action == 'heal':
        potion = get_item('potion')
        if not potion or potion.get('qty', 0) <= 0:
            return player  # no potion available

        heal_amount = int(active_char['max_hp'] * 0.25)
        active_char['hp'] = min(active_char['hp'] + heal_amount, active_char['max_hp'])

        # deduct potion
        potion['qty'] = max(0, potion.get('qty', 0) - 1)

    # Process Antidote Action
    elif action == 'antidote':
        antidote = get_item('antidote')
        if not antidote or antidote.get('qty', 0) <= 0:
            return player  # no antidote available

        # clear status
        active_char['status'] = ''

        # deduct antidote
        antidote['qty'] = max(0, antidote.get('qty', 0) - 1)

    else:
        return {'error': f"Unsupported action '{action}'"}

    return player
