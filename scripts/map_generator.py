import random

def main(input):
    # === CONFIGURABLE PARAMETERS ===
    GRID_WIDTH = input.get('grid_width', random.randint(6, 10))
    GRID_HEIGHT = input.get('grid_height', random.randint(4, 7))
    MIN_PATH_LEN = input.get('min_path_len', 8)
    MAX_PATH_PERCENT = input.get('max_path_percent', 0.4)
    MAX_PATH_LEN = int(GRID_WIDTH * GRID_HEIGHT * MAX_PATH_PERCENT)
    BRANCH_CHANCE = input.get('branch_chance', 0.6)
    MAX_BRANCH_LEN = input.get('max_branch_len', 4)
    MAX_TOTAL_ROOMS = int(GRID_WIDTH * GRID_HEIGHT * 0.45)

    # Dynamic rest logic based on dungeon size
    is_small_map = GRID_WIDTH * GRID_HEIGHT <= 35
    EVENT_SCALING = {
        'chest': {'min': 0, 'max_percent': 0.05, 'max_count': 3},
        'npc': {'min': 0, 'max_percent': 0.03, 'max_count': 2},
        'enemy': {'min': 2, 'max_percent': 0.18, 'max_count': 6},
        'trap': {'min': 0, 'max_percent': 0.05, 'max_count': 3},
        'rest': {'min': 0 if not is_small_map else 1, 'max_percent': 0.02, 'max_count': 1},
    }

    # === HELPERS ===
    def get_neighbors(x, y):
        dirs = [(0,1),(1,0),(0,-1),(-1,0)]
        return [(x+dx, y+dy) for dx,dy in dirs if 0 <= x+dx < GRID_WIDTH and 0 <= y+dy < GRID_HEIGHT]

    def direction(a, b):
        ax, ay = a
        bx, by = b
        if ax == bx and by == ay-1: return 'north'
        if ax == bx and by == ay+1: return 'south'
        if ay == by and bx == ax-1: return 'west'
        if ay == by and bx == ax+1: return 'east'
        return None

    # === PATH GENERATION ===
    def generate_solvable_path():
        start = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
        path = [start]
        visited = {start}
        stack = [start]

        while stack and len(path) < MAX_PATH_LEN:
            current = stack[-1]
            neighbors = [n for n in get_neighbors(*current) if n not in visited]
            if neighbors:
                def score(n):
                    x, y = n
                    edge_dist = min(x, GRID_WIDTH-1-x, y, GRID_HEIGHT-1-y)
                    adj_to_path = sum((nx,ny) in visited for nx,ny in get_neighbors(x,y))
                    return edge_dist - adj_to_path + random.random()*0.5
                neighbors.sort(key=score, reverse=True)
                next_room = neighbors[0]
                path.append(next_room)
                visited.add(next_room)
                stack.append(next_room)
            else:
                stack.pop()

        # Ensure minimum path length
        while len(path) < MIN_PATH_LEN:
            current = random.choice(path)
            candidates = [n for n in get_neighbors(*current) if n not in visited]
            if not candidates: break
            candidates.sort(key=lambda n: -sum((nx,ny) in visited for nx,ny in get_neighbors(*n)) + random.random()*0.5)
            next_room = candidates[0]
            path.append(next_room)
            visited.add(next_room)

        # Exit chosen among farthest rooms
        possible_exits = sorted(path, key=lambda r: abs(r[0]-start[0]) + abs(r[1]-start[1]), reverse=True)
        exit_room = random.choice(possible_exits[:max(1,len(possible_exits)//4)])
        return start, exit_room, path

    # === GRID BUILDING ===
    def build_grid(path):
        grid = {}
        for coord in path:
            key = f'{coord[0]},{coord[1]}'
            grid[key] = {'type':'empty', 'visited':False, 'resolved':False, 'exits':[]}
        for i in range(len(path)-1):
            a, b = path[i], path[i+1]
            dir_ab = direction(a,b)
            dir_ba = direction(b,a)
            a_key = f'{a[0]},{a[1]}'
            b_key = f'{b[0]},{b[1]}'
            if dir_ab and dir_ab not in grid[a_key]['exits']: grid[a_key]['exits'].append(dir_ab)
            if dir_ba and dir_ba not in grid[b_key]['exits']: grid[b_key]['exits'].append(dir_ba)
        return grid

    # === BRANCHING ===
    def add_branches(grid):
        used = set(tuple(map(int,k.split(','))) for k in grid.keys())
        reachable = list(used)
        while len(used) < MAX_TOTAL_ROOMS:
            base_room = random.choice(reachable)
            if random.random() > BRANCH_CHANCE: continue
            branch_length = random.randint(1, MAX_BRANCH_LEN)
            current = base_room
            for _ in range(branch_length):
                candidates = [n for n in get_neighbors(*current) if n not in used]
                if not candidates: break
                # prefer central tiles and avoid hugging existing path
                candidates.sort(key=lambda n: min(n[0], GRID_WIDTH-1-n[0], n[1], GRID_HEIGHT-1-n[1])
                                - sum((nx,ny) in used for nx,ny in get_neighbors(*n)) + random.random()*0.5,
                                reverse=True)
                next_room = candidates[0]
                a_key = f'{current[0]},{current[1]}'
                b_key = f'{next_room[0]},{next_room[1]}'
                if b_key not in grid:
                    grid[b_key] = {'type':'empty','visited':False,'resolved':False,'exits':[]}
                dir_ab = direction(current, next_room)
                dir_ba = direction(next_room, current)
                if dir_ab and dir_ab not in grid[a_key]['exits']: grid[a_key]['exits'].append(dir_ab)
                if dir_ba and dir_ba not in grid[b_key]['exits']: grid[b_key]['exits'].append(dir_ba)
                used.add(next_room)
                reachable.append(next_room)
                current = next_room
                if len(used) >= MAX_TOTAL_ROOMS: break
        return grid

    # === ROOM TYPES WITH GUARANTEED DIVERSITY ===
    def assign_room_types(grid, start, exit_room):
        empty_keys = [k for k,v in grid.items() if v['type']=='empty' and k not in (f'{start[0]},{start[1]}', f'{exit_room[0]},{exit_room[1]}')]
        random.shuffle(empty_keys)
        total = len(empty_keys)
        def calc_count(event):
            params = EVENT_SCALING[event]
            base = int(total * params['max_percent'])
            return max(params['min'], min(base, params['max_count']))
        event_counts = {k: calc_count(k) for k in EVENT_SCALING.keys()}
        def assign_type(type_name, count):
            nonlocal empty_keys
            for _ in range(count):
                if not empty_keys: return
                key = empty_keys.pop()
                grid[key]['type'] = type_name
        for event, count in event_counts.items():
            assign_type(event, count)

        # --- Diversity pass: ensure at least a couple non-enemy types exist ---
        non_enemy_keys = [k for k,v in grid.items() if v['type'] not in ('enemy','empty','start','exit')]
        if len(non_enemy_keys) < 2:
            needed = 2 - len(non_enemy_keys)
            potential_keys = [k for k,v in grid.items() if v['type']=='empty' and k not in (f'{start[0]},{start[1]}', f'{exit_room[0]},{exit_room[1]}')]
            random.shuffle(potential_keys)
            for i in range(min(needed, len(potential_keys))):
                grid[potential_keys[i]]['type'] = random.choice(['trap','chest','npc','rest'])
        return grid

    # === ASCII RENDER ===
    def render_ascii(grid):
        display = [[' . ' for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        for key, val in grid.items():
            x, y = map(int,key.split(','))
            cell = val['type']
            char = 'S' if cell=='start' else 'E' if cell=='exit' else \
                   'C' if cell=='chest' else 'M' if cell=='enemy' else \
                   'T' if cell=='trap' else 'R' if cell=='rest' else 'N' if cell=='npc' else '.' 
            display[y][x] = f' {char} '
        # Add simple connections
        for key, val in grid.items():
            x, y = map(int,key.split(','))
            for exit_dir in val['exits']:
                if exit_dir=='south' and y+1<GRID_HEIGHT: display[y+1][x] = '|'
                if exit_dir=='north' and y-1>=0: display[y-1][x] = '|'
                if exit_dir=='east' and x+1<GRID_WIDTH: display[y][x+1] = '-'
                if exit_dir=='west' and x-1>=0: display[y][x-1] = '-'
        # Print grid
        print('\nASCII Dungeon Map:')
        for row in display:
            print(''.join(row))

    # === EXECUTION ===
    start, exit_room, path = generate_solvable_path()
    grid = build_grid(path)
    grid = add_branches(grid)
    grid[f'{start[0]},{start[1]}'].update({'type':'start','visited':True,'resolved':True})
    grid[f'{exit_room[0]},{exit_room[1]}']['type'] = 'exit'
    grid = assign_room_types(grid, start, exit_room)

    render_ascii(grid)  # print the ASCII map

    return {
        'dungeon_map': grid,
        'path': [f'{x},{y}' for x,y in path],
        'start': f'{start[0]},{start[1]}',
        'exit': f'{exit_room[0]},{exit_room[1]}',
        'width': GRID_WIDTH,
        'height': GRID_HEIGHT,
        'total_rooms': len(grid)
    }
