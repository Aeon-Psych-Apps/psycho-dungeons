import random
import copy

def main(input):
    char_id = input.get('char_id')
    player = copy.deepcopy(input.get('player'))
    enemy_base_stats = input.get('enemy_base_stats')
    spawn_type = input.get('type', 'enemy')  # 'enemy' or 'boss'

    # Fetch player character
    char = next((c for c in player['characters'] if c['char_id'] == char_id), None)
    if not char:
        raise ValueError('Character not found.')

    base_key = random.choice(list(enemy_base_stats.keys()))
    base_stats = enemy_base_stats[base_key]

    player_level = char.get('level', 1)
    stats = char.get('stats', {})
    player_max_hp = char.get('max_hp', 100)
    player_atk = stats.get('atk', 10)
    player_spd = stats.get('spd', 5)
    player_luck = stats.get('luck', 1)

    # Calculate player total attack including gear
    player_total_atk = player_atk + sum(
        sum(eq.get('stats', {}).values()) for eq in char.get('equipment', [])
    )

    # Enemy role modifiers
    if spawn_type == 'boss':
        level_variation = random.randint(player_level, player_level + 2)
        hp_multiplier_range = (3, 10)
        dmg_pct_range = (0.02, 0.10)
    else:
        level_variation = random.randint(max(1, player_level - 1), player_level + 1)
        hp_multiplier_range = (1, 3)
        dmg_pct_range = (0.01, 0.05)

    # Expected player damage
    expected_player_dmg = player_total_atk * 1.05

    # Enemy HP
    enemy_hp = max(10, int(expected_player_dmg * random.uniform(*hp_multiplier_range)))

    # Enemy damage
    enemy_damage = int(player_max_hp * random.uniform(*dmg_pct_range))

    # Speed and Luck scaling
    enemy_spd = max(1, int(player_spd * random.uniform(0.9, 1.1)))
    enemy_luck = max(0, int(player_luck * random.uniform(0.8, 1.2)))

    # Build readable tags
    name_prefix = "Boss " if spawn_type == "boss" else ""
    label = "Boss" if spawn_type == "boss" else "Enemy"

    # Build enemy object
    enemy_obj = {
        'name': f"{name_prefix}{base_key}",
        'level': level_variation,
        'max_hp': enemy_hp,
        'current_hp': enemy_hp,
        'damage': enemy_damage,
        'stats': {
            'spd': enemy_spd,
            'luck': enemy_luck
        },
        'status_effects': [],
        'gold': int((base_stats.get('gold', 10) + random.randint(0, player_level * 2)) * (3 if spawn_type == 'boss' else 1)),
        'experience': int(base_stats.get('exp', 10) * (2 if spawn_type == 'boss' else 1)),
    }

    # Attach enemy to active map if present
    if 'current_map' in char:
        char['current_map']['enemy'] = enemy_obj

    # Final message
    message = (
        f"Generated {label} {base_key} "
        f"(Lvl {level_variation}, HP {enemy_hp}, Damage {enemy_damage}, "
        f"SPD {enemy_spd}, Luck {enemy_luck})"
    )

    return {
        'player': player,
        'generated_enemy': enemy_obj,
        'message': message
    }
