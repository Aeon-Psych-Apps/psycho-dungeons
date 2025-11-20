def main(input):
    # Extract inputs
    char_id = input.get('char_id', '')
    player_data = input.get('player', {})
    new_position = input.get('travel', '0,0')  # e.g., '0,2'

    characters = player_data.get('characters', [])

    for character in characters:
        if character.get('char_id') == char_id:
            current_map = character.get('current_map', {})
            
            # Update player position
            current_map['player_position'] = new_position
            character['current_map'] = current_map

            # Return updated player object
            return {'player': player_data}

    # Fallback (character not found)
    return {
        'error': f"Character '{char_id}' not found.",
        'player': player_data
    }
