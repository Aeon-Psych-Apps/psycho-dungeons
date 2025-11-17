def main(input):
    player = input.get('player', {})
    character_id = input.get('character_id')

    characters = player.get('characters', [])

    # Find the character to remove
    removed_character = next(
        (c for c in characters if str(c.get('char_id')) == str(character_id)),
        None
    )

    if not removed_character:
        return {'error': f'No character found with id '{character_id}'', 'player': player}

    # Remove the character
    player['characters'] = [c for c in characters if str(c.get('char_id')) != str(character_id)]

    return {
        'success': True,
        'player': player,
        'removed_character': removed_character
    }
