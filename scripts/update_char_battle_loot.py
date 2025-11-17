import random
import copy
import math

def main(input):
    '''
    Battle processor — equipment-aware, scaling-friendly.
    Handles loot_gear and loot_consume drops on victory.
    Normal enemies: 2-5 turns.
    Bosses: 5-10 turns.
    '''

    # --- Inputs ---
    char_id = input.get('char_id')
    player_obj = copy.deepcopy(input.get('player'))
    action = input.get('action', '').lower()
    enemy = copy.deepcopy(input.get('enemy'))
    test_mode = input.get('test_mode', False)
    xp_scaling = input.get('xp_scaling', {'base_xp': 100, 'growth_rate': 1.25})
    stat_scaling = input.get('stat_scaling', {})
    loot_gear = input.get('loot_gear', [])
    loot_consume = input.get('loot_consume')

    # --- Config ---
    BASE_CRIT_CHANCE = 0.05
    CRIT_MULTIPLIER = 1.5
    DAMAGE_SCALE = 1.0
    DEFEND_MULTIPLIER = 0.5
    BASE_BLOCK_CHANCE = 0.1
    BASE_XP_GAIN = 10
    BASE_GOLD_GAIN = 5

    # --- Helper functions ---
    def get_character(player, char_id):
        return next((c for c in player['characters'] if c['char_id'] == char_id), None)

    def get_stat(entity, stat_name):
        base = entity.get('stats', {}).get(stat_name, 0)
        equip_bonus = sum(item.get('stats', {}).get(stat_name, 0) for item in entity.get('equipment', []))
        return base + equip_bonus

    def calc_damage(attacker_atk, defender_def, crit_chance=BASE_CRIT_CHANCE, crit_mult=CRIT_MULTIPLIER):
        attacker_atk = max(0.0, float(attacker_atk))
        defender_def = max(0.0, float(defender_def))
        effective = attacker_atk * (100.0 / (100.0 + defender_def))
        damage = effective * DAMAGE_SCALE * random.uniform(0.95, 1.05)
        is_crit = random.random() < crit_chance
        if is_crit:
            damage *= crit_mult
        return int(max(round(damage), 1)), is_crit

    def xp_required(level):
        base = xp_scaling.get('base_xp', 100)
        growth = xp_scaling.get('growth_rate', 1.25)
        return int(base * (growth ** (level - 1)))

    def find_consumable(inv_list, consumable_id):
        for it in inv_list:
            if it.get('type') == 'consumable':
                if it.get('item_id') == consumable_id or it.get('name') == consumable_id:
                    return it
        return None

    # --- Ensure enemy has all needed stats ---
    enemy.setdefault('stats', {})
    enemy['stats'].setdefault('def', 0)
    enemy['stats'].setdefault('atk', enemy.get('damage', 5))
    enemy['stats'].setdefault('spd', 5)
    enemy['stats'].setdefault('luck', 0)

    # --- Fetch character ---
    character = get_character(player_obj, char_id)
    if not character:
        raise ValueError('Character not found')

    # --- Pre-battle check ---
    if character.get('hp', 0) <= 0:
        battle_result = 'player_lost'
    elif enemy.get('current_hp', 0) <= 0:
        battle_result = 'player_won'
    else:
        battle_result = 'ongoing'

    if battle_result != 'ongoing':
        return {'player': player_obj, 'character': character, 'enemy': enemy, 'battle_result': battle_result, 'turn_log': [{'status': 'pre_battle_end'}]}

    # --- Core stats ---
    player_spd = get_stat(character, 'spd')
    enemy_spd = get_stat(enemy, 'spd')
    player_luck = get_stat(character, 'luck')
    enemy_luck = get_stat(enemy, 'luck')
    ESCAPE_CHANCE = min(max(0.3 + (player_spd - enemy_spd) * 0.05, 0.1), 0.8)

    # --- Initiative ---
    player_initiative = player_spd + random.uniform(-1, 1) * (1 + player_luck / 5)
    enemy_initiative = enemy_spd + random.random() * (1 + enemy_luck / 10)
    turn_order = ['player', 'enemy'] if player_initiative >= enemy_initiative else ['enemy', 'player']

    turn_log = []

    # --- Defend ---
    player_defending = action == 'defend'
    enemy_action = 'attack' if random.random() > 0.15 else 'defend'
    enemy_defending = enemy_action == 'defend'
    enemy['action'] = enemy_action

    player_block_chance = BASE_BLOCK_CHANCE + player_luck / 200
    enemy_block_chance = BASE_BLOCK_CHANCE + enemy_luck / 200

    # --- Turn Resolution ---
    for actor in turn_order:
        if battle_result != 'ongoing':
            break

        actor_obj = character if actor == 'player' else enemy
        target_obj = enemy if actor == 'player' else character
        actor_action = action if actor == 'player' else enemy_action
        target_hp_key = 'current_hp' if actor == 'player' else 'hp'

        log_entry = {'actor': actor_obj.get('name', 'Unknown'), 'action': actor_action, 'damage': 0, 'status': ''}

        if actor_action == 'attack':
            if actor == 'player':
                # Player attack: gear-aware, crits included
                atk = get_stat(actor_obj, 'atk')
                enemy_def = get_stat(target_obj, 'def')  # include enemy def
                damage, crit = calc_damage(atk, enemy_def)
            else:
                # Enemy attack: % of player max HP
                player_max_hp = character.get('max_hp', 100)
                if 'Boss' in enemy.get('name', ''):
                    dmg_pct = random.uniform(0.03, 0.10)
                else:
                    dmg_pct = random.uniform(0.02, 0.07)
                damage = int(player_max_hp * dmg_pct * random.uniform(0.9, 1.1))

                # Crit check
                crit = random.random() < BASE_CRIT_CHANCE
                if crit:
                    damage = int(damage * CRIT_MULTIPLIER)

            # --- Defend / Block ---
            if target_obj == character and player_defending:
                if random.random() < player_block_chance:
                    damage = 0
                    log_entry['status'] = 'player_blocked'
                else:
                    damage = int(damage * DEFEND_MULTIPLIER)
            elif target_obj == enemy and enemy_defending:
                if random.random() < enemy_block_chance:
                    damage = 0
                    log_entry['status'] = 'enemy_blocked'
                else:
                    damage = int(damage * DEFEND_MULTIPLIER)

            # Apply damage
            target_obj[target_hp_key] = max(target_obj.get(target_hp_key, 1) - damage, 0)
            if test_mode and actor != 'player':
                target_obj[target_hp_key] = max(target_obj[target_hp_key], 1)

            log_entry['damage'] = damage
            if crit:
                log_entry['status'] += (' ' if log_entry['status'] else '') + 'crit'

            # Check end of battle
            if target_obj[target_hp_key] <= 0:
                battle_result = 'player_won' if actor == 'player' else 'player_lost'

        elif actor_action == 'defend':
            log_entry['status'] = 'defending'

        elif actor_action == 'escape' and actor == 'player':
            if random.random() < ESCAPE_CHANCE:
                battle_result = 'escaped'
                log_entry['status'] = 'escaped_success'
                break
            else:
                log_entry['status'] = 'escape_failed'

        turn_log.append(log_entry)

    # --- Battle End & Rewards ---
    if battle_result in ['player_won', 'player_lost']:
        if 'current_map' in character:
            pos = character['current_map'].get('player_position')
            if pos and pos in character['current_map'].get('rooms', {}):
                character['current_map']['rooms'][pos]['resolved'] = True

        if battle_result == 'player_won':
            enemy['action'] = 'death'
            gained_xp = enemy.get('experience', BASE_XP_GAIN)
            gained_gold = enemy.get('gold', BASE_GOLD_GAIN)
            character['xp'] = character.get('xp', 0) + gained_xp
            character['gold'] = character.get('gold', 0) + gained_gold
            turn_log.append({'status': f'Gained {gained_xp} XP and {gained_gold} gold!'})

            # --- Level-up logic ---
            char_class = character.get('class', 'warrior').lower()
            scaling = stat_scaling.get(char_class, {})
            current_level = character.get('level', 1)
            current_xp = character.get('xp', 0)
            stats = character.get('stats', {})
            leveled_up = False

            while current_xp >= xp_required(current_level):
                current_xp -= xp_required(current_level)
                current_level += 1
                leveled_up = True
                hp_mult = scaling.get('hp', 1)
                base_max_hp = character.get('max_hp', 100)
                increase_hp = int(base_max_hp * 0.10 * hp_mult)
                character['max_hp'] = base_max_hp + increase_hp
                character['hp'] = character['max_hp']
                for stat, mult in scaling.items():
                    if stat != 'hp':
                        stats[stat] = round(stats.get(stat, 10) * (1 + 0.10 * mult), 2)

            character['xp'] = current_xp
            character['level'] = current_level
            character['stats'] = stats

            if leveled_up:
                turn_log.append({'status': f'Level up! Now level {current_level}.'})

            # --- Loot Handling ---
            if not test_mode:
                if 'inventory' not in character or not isinstance(character['inventory'], list):
                    character['inventory'] = []

                MAX_INVENTORY_SLOTS = 10
                CONSUMABLE_LIMITS = {'potion': 3, 'antidote': 1, 'elixir': 1}

                # Consumable drop
                if loot_consume and isinstance(loot_consume, str):
                    existing = find_consumable(character['inventory'], loot_consume)
                    if existing:
                        max_qty = CONSUMABLE_LIMITS.get(existing.get('item_id', existing.get('name')), 99)
                        if existing.get('qty', 0) < max_qty:
                            existing['qty'] = min(existing.get('qty', 0) + 1, max_qty)
                            turn_log.append({'status': f'Obtained {loot_consume} (+1).'})
                        else:
                            turn_log.append({'status': f'Cannot carry more {loot_consume}s.'})
                    else:
                        if len(character['inventory']) < MAX_INVENTORY_SLOTS:
                            effect = 'heal_25' if loot_consume == 'potion' else 'cure' if loot_consume == 'antidote' else 'revive'
                            character['inventory'].append({
                                'item_id': loot_consume,
                                'name': loot_consume,
                                'qty': 1,
                                'type': 'consumable',
                                'effect': effect
                            })
                            turn_log.append({'status': f'Obtained new {loot_consume}.'})
                        else:
                            turn_log.append({'status': f'Inventory full — {loot_consume} left behind.'})

                # Gear drops
                if loot_gear and isinstance(loot_gear, list):
                    for item in loot_gear:
                        if len(character['inventory']) < MAX_INVENTORY_SLOTS:
                            character['inventory'].append(item)
                            turn_log.append({'status': f'Found gear: {item.get('name', 'Unknown Item')} ({item.get('rarity', 'unknown').capitalize()})'})
                        else:
                            turn_log.append({'status': f'Inventory full — {item.get('name', 'Unknown Item')} left behind.'})

                if (not loot_gear or len(loot_gear) == 0) and not loot_consume:
                    turn_log.append({'status': 'No loot dropped this time.'})

    # --- Persist enemy state ---
    if 'current_map' in character:
        character['current_map']['enemy'] = enemy

    # --- Update player object ---
    for i, char in enumerate(player_obj['characters']):
        if char['char_id'] == char_id:
            player_obj['characters'][i] = character
            break

    return {
        'player': player_obj,
        'character': character,
        'enemy': enemy,
        'battle_result': battle_result,
        'turn_log': turn_log
    }
