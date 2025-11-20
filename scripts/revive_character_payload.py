def main(input):
    player = input.get('player', {})
    character_id = input.get('character_id')

    characters = player.get('characters', [])

    # Find the character to revive
    character = next(
        (c for c in characters if str(c.get('char_id')) == str(character_id)),
        None
    )

    if not character:
        return {'error': f"No character found with id '{character_id}'", 'player': player}

    # Look for an elixir in the inventory
    inventory = character.get('inventory', [])
    elixir_item = next((item for item in inventory if item.get('item_id') == 'elixir'), None)

    # Decrement elixir qty (assumes pre-check qty > 0)
    elixir_item['qty'] -= 1

    # Revive character
    character['hp'] = character.get('max_hp', 50)
    character['inventory'] = inventory

    return {
        'success': True,
        'player': player,
        'revived_character': character
    }
