def main(input):
    player = input['player']
    character_name = input['character_name']
    character_pos = int(input['character_pos'])

    characters = player.get('characters', [])

    # Find all indices where the character name matches
    matches = [i for i, c in enumerate(characters) if c['name'] == character_name]

    if not matches:
        return {'error': f"No character found with name '{character_name}'", 'player': player}

    # If only one match, remove it directly
    if len(matches) == 1:
        target_index = matches[0]
    else:
        # If multiple matches, use the provided position
        if character_pos < 1 or character_pos > len(matches):
            return {'error': f"Invalid character_pos {character_pos} for name '{character_name}'", 'player': player}
        target_index = matches[character_pos - 1]

    removed_character = characters.pop(target_index)
    player['characters'] = characters

    return {
        'player': player,
        'removed_character': removed_character
    }
