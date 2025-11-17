def main(input):
    # Extract the player name and hp_recovery value
    char_name = input.get('char_id', '')
    hp_recovery = input.get('hp_recovery', 0)
    
    # Get the player data
    player_data = input.get('player', {})
    characters = player_data.get('characters', [])

    print(f'Character:  {characters}')
    
    # Find the character that matches the name
    for character in characters:
        if character.get('char_id') == char_name:
            # Add hp_recovery to the character's hp
            current_hp = character.get('hp', 0)
            max_hp = character.get('max_hp', 0)
            
            # Ensure HP doesn't exceed max_hp
            new_hp = min(current_hp + hp_recovery, max_hp)
            character['hp'] = new_hp
            character['gold'] -= 25
            break
    
    return player_data
