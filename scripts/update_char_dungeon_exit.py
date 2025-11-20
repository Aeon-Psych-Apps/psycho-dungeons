def main(input):
    # Extract inputs
    char_id = input.get('char_id', '')
    player_data = input.get('player', {})
    direction = input.get('direction', '').lower().strip()
    loot = input.get('loot', {})
    timestamp = input.get('timestamp', 0)
    refresh = input.get('shop_refresh', False)

    characters = player_data.get('characters', [])
    move_map = {
        'north': (0, -1),
        'south': (0, 1),
        'east': (1, 0),
        'west': (-1, 0)
    }

    for character in characters:
        if character.get('char_id') == char_id:
            current_map = character.get('current_map', {})
            current_position = current_map.get('player_position', '0,0')
            rooms = current_map.get('rooms', {})

            # Parse coordinates
            x, y = map(int, current_position.split(','))

            # Get direction delta
            dx, dy = move_map.get(direction, (0, 0))

            # Compute new position
            new_x, new_y = x + dx, y + dy
            new_position = f'{new_x},{new_y}'

            # Update player position
            current_map['player_position'] = '0,0'

            # Update player map back to Town
            current_map['map_type'] = 'Town'

            # Mark room as visited (if it exists)
            if new_position in rooms:
                rooms[new_position]['visited'] = True
                room_type = rooms[new_position].get('type', 'empty')
            else:
                # If for some reason room doesn’t exist, initialize it
                rooms[new_position] = {
                    'type': 'empty',
                    'visited': True,
                    'resolved': False,
                    'exits': []
                }
                room_type = 'empty'

            # Write back changes
            current_map['rooms'] = {}
            character['current_map'] = current_map

            if refresh:
              character['shop_items'] = loot
              character['shop_refresh'] = timestamp

            # Return both full player data and room type
            return {
                'player': player_data,
                'room_type': room_type
            }

    # Fallback (character not found)
    return {
        'error': f"Character '{char_id}' not found.",
        'player': player_data
    }
