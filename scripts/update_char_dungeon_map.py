def main(input):
    # Extract player and new map data
    char_id = input.get('char_id', '')
    new_map = input.get('map', {})  # from map_generator.output
    player_data = input.get('player', {})
    width = input.get('width', 7)
    height = input.get('height', 5)

    characters = player_data.get('characters', [])

    # Find the matching character
    for character in characters:
        if character.get('char_id') == char_id:
            # Create or update current_map safely
            current_map = character.get('current_map', {})

            # Overwrite key parts with new dungeon data
            current_map['map_type'] = 'Dungeon'
            current_map['floors'] = 1  # can be adjusted later if needed
            current_map['width'] = width
            current_map['height'] = height
            current_map['player_position'] = new_map.get('start', '0,0')

            # Directly copy the dungeon_map (using '0,0' style keys)
            current_map['rooms'] = {}
            dungeon_rooms = new_map.get('dungeon_map', {})
            for coord, data in dungeon_rooms.items():
                current_map['rooms'][coord] = {
                    'type': data.get('type', 'empty'),
                    'visited': data.get('visited', False),
                    'resolved': data.get('resolved', False),
                    'exits': data.get('exits', [])
                }

            # Add start and exit coordinates explicitly
            current_map['start'] = new_map.get('start')
            current_map['exit'] = new_map.get('exit')

            # Write the updated map back to the character
            character['current_map'] = current_map
            break

    # Return the full modified player data
    return player_data
